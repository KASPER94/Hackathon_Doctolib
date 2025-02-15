import mediapipe as mp
import numpy as np
from typing import Dict

def calculate_angle(p1: np.ndarray, p2: np.ndarray, p3: np.ndarray) -> float:
  """Calculate angle between three points"""
  v1 = p1 - p2
  v2 = p3 - p2
  cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
  angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
  return np.degrees(angle)

def calculate_distance(p1: np.ndarray, p2: np.ndarray) -> float:
  """Calculate Euclidean distance between two points"""
  return np.linalg.norm(p1 - p2)

def check_knee_bend(landmarks: np.ndarray, side: str = 'right') -> float:
  """Measure knee bend angle"""
  if side == 'right':
      hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
      knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
  else:
      hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
      knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]

  return calculate_angle(hip, knee, ankle)

def check_knee_ankle_alignment(landmarks: np.ndarray, side: str = 'right') -> float:
  """Measure horizontal distance between knee and ankle"""
  if side == 'right':
      knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
  else:
      knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]

  return knee[0] - ankle[0]  # X-axis difference

def check_back_arch(landmarks: np.ndarray) -> float:
  """Measure back arch by calculating angle between shoulders, mid-back, and hips"""
  shoulders_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value] + 
                   landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]) / 2
  hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] + 
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2
  mid_back = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]  # Approximation point

  return calculate_angle(shoulders_mid, mid_back, hips_mid)

def check_tailbone_tilt(landmarks: np.ndarray) -> float:
  """Measure tailbone tilt relative to vertical"""
  hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] + 
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2
  shoulders_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value] + 
                   landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]) / 2
  vertical = np.array([hips_mid[0], hips_mid[1] - 1, hips_mid[2]])  # Vertical reference

  return calculate_angle(shoulders_mid, hips_mid, vertical)

def check_stance_width(landmarks: np.ndarray) -> float:
  """Measure normalized distance between feet"""
  left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
  right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]

  return calculate_distance(left_ankle, right_ankle)

def calculate_subject_height(landmarks: np.ndarray) -> float:
  """Estimate subject height based on landmarks"""
  # Define key landmarks for height estimation
  top_landmark = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]
  bottom_landmark = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]

  # Calculate the distance between the top and bottom landmarks
  height = np.linalg.norm(top_landmark - bottom_landmark)

  return height


def check_hip_square(landmarks: np.ndarray) -> float:
  """Measure hip alignment (how square/level the hips are)"""
  left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
  right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
  horizontal = np.array([right_hip[0] + 1, right_hip[1], right_hip[2]])

  return calculate_angle(left_hip, right_hip, horizontal)

def check_shoulder_alignment(landmarks: np.ndarray) -> float:
  """Measure shoulder alignment"""
  left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
  right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
  horizontal = np.array([right_shoulder[0] + 1, right_shoulder[1], right_shoulder[2]])

  return calculate_angle(left_shoulder, right_shoulder, horizontal)

def check_weight_distribution(landmarks: np.ndarray) -> float:
  """Estimate weight distribution between feet based on hip position"""
  hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] + 
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2
  left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
  right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]

  ankle_midpoint = (left_ankle + right_ankle) / 2
  shift = (hips_mid[0] - ankle_midpoint[0]) / calculate_distance(left_ankle, right_ankle)
  return 0.5 + shift

def check_spine_vertical_alignment(landmarks: np.ndarray) -> float:
  """Measure spine alignment relative to vertical"""
  nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]
  hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] + 
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2
  vertical = np.array([hips_mid[0], hips_mid[1] - 1, hips_mid[2]])

  return calculate_angle(nose, hips_mid, vertical)

def check_pelvis_tilt(landmarks: np.ndarray) -> float:
  """Measure anterior/posterior pelvic tilt"""
  left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
  right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
  mid_hip = (left_hip + right_hip) / 2

  # Approximate pubic bone position
  pubic_point = np.array([mid_hip[0], mid_hip[1] + 0.1, mid_hip[2]])
  vertical = np.array([mid_hip[0], mid_hip[1] - 1, mid_hip[2]])

  return calculate_angle(pubic_point, mid_hip, vertical)

def check_knee_tracking(landmarks: np.ndarray, side: str = 'right') -> float:
  """Check if knee is tracking over toes"""
  if side == 'right':
      knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
      toe = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
  else:
      knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
      ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
      toe = landmarks[mp.solutions.pose.PoseLandmark.LEFT_FOOT_INDEX.value]

  knee_projection = np.array([knee[0], ankle[1], ankle[2]])
  return calculate_distance(knee_projection, toe)

def check_joint_angle(landmarks: np.ndarray, joint: str) -> float:
  """Calculate joint angles for elbow, shoulder, hip, knee, and ankle"""
  if joint == 'right_elbow':
      shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
      elbow = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value]
      wrist = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]
      return calculate_angle(shoulder, elbow, wrist)
  elif joint == 'left_elbow':
      shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
      elbow = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value]
      wrist = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
      return calculate_angle(shoulder, elbow, wrist)
  # Add similar logic for shoulder, hip, knee, and ankle

def check_alignment(landmarks: np.ndarray, part: str) -> float:
  """Check alignment for head, neck, spine, hip, and shoulder"""
  if part == 'head_neck':
      nose = landmarks[mp.solutions.pose.PoseLandmark.NOSE.value]
      neck = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value] +
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]) / 2
      vertical = np.array([neck[0], neck[1] - 1, neck[2]])
      return calculate_angle(nose, neck, vertical)
  elif part == 'hip_shoulder':
      left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
      right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
      left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
      right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
      return calculate_angle(left_hip, right_hip, left_shoulder) + calculate_angle(right_hip, left_hip, right_shoulder)
  # Add similar logic for spine alignment

def check_body_position(landmarks: np.ndarray) -> Dict[str, float]:
  """Calculate body position metrics"""
  left_hand = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]
  right_hand = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]
  left_foot = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
  right_foot = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
  hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] +
              landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2

  return {
      'hand_foot_distance': calculate_distance(left_hand, left_foot) + calculate_distance(right_hand, right_foot),
      'hip_height': hips_mid[1]
  }

def check_symmetry(landmarks: np.ndarray) -> float:
  """Check symmetry between left and right sides"""
  left_side = np.array([
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value],
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value],
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value],
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
  ])
  right_side = np.array([
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value],
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value],
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value],
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
  ])
  return np.mean(np.abs(left_side - right_side))

def check_engagement(landmarks: np.ndarray) -> Dict[str, float]:
  """Estimate core and leg muscle engagement"""
  core_engagement = calculate_distance(
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value],
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]
  )
  leg_engagement = calculate_distance(
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value],
      landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
  ) + calculate_distance(
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value],
      landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
  )
  return {
      'core_engagement': core_engagement,
      'leg_engagement': leg_engagement
  }
  
def calculate_angle_between_legs(landmarks: np.ndarray) -> float:
    """Calculate the angle between the legs"""
    left_knee = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value]
    right_knee = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value]
    left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate vectors
    left_leg_vector = left_ankle - left_knee
    right_leg_vector = right_ankle - right_knee

    # Calculate the dot product
    dot_product = np.dot(left_leg_vector, right_leg_vector)

    # Calculate the magnitudes
    left_leg_magnitude = np.linalg.norm(left_leg_vector)
    right_leg_magnitude = np.linalg.norm(right_leg_vector)

    # Calculate the cosine of the angle
    cosine_angle = dot_product / (left_leg_magnitude * right_leg_magnitude)

    # Calculate the angle in degrees
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def right_calculate_height_of_hand(landmarks: np.ndarray) -> float:
    """Calculate the height of the hand relative to the shoulder"""
    right_shoulder = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value]
    right_hand = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value]

    right_hand_height = right_hand[1] - right_shoulder[1]

    # Return the average height of both hands
    return  right_hand_height
  
def left_calculate_height_of_hand(landmarks: np.ndarray) -> float:
    """Calculate the height of the hand relative to the shoulder"""
    left_shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value]
    left_hand = landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value]

    # Calculate the height of the left hand
    left_hand_height = left_hand[1] - left_shoulder[1]

    # Return the average height of both hands
    return left_hand_height
  

def calculate_height_of_hips(landmarks: np.ndarray) -> float:
    """Calculate the height of the hips relative to the ankles"""
    left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
    left_hip = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]

    # Calculate the height of the left hip
    left_hip_height = left_hip[1] - left_ankle[1]
    # Calculate the height of the right hip
    right_hip_height = right_hip[1] - right_ankle[1]

    # Return the average height of both hips
    return (left_hip_height + right_hip_height) / 2

def check_center_of_gravity_in_between_ankles(landmarks: np.ndarray) -> float:
    """Check if the center of gravity is in between the ankles"""
    left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]
    hips_mid = (landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value] + landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value]) / 2

    # Calculate the distance between the center of gravity and the midpoint of the ankles
    distance = np.linalg.norm(hips_mid - ((left_ankle + right_ankle) / 2))

    # Return the distance
    return distance

def calculate_distance_between_feet(landmarks: np.ndarray) -> float:
    """Calculate the distance between the feet"""
    left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate the distance between the ankles
    distance = np.linalg.norm(left_ankle - right_ankle)
    return distance

def calculate_height_of_feet_right(landmarks: np.ndarray) -> float:
    """Calculate the height of the feet relative to the ground"""
    
    right_ankle = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value]

    right_foot_height = right_ankle[1]

    # Return the average height of both feet
    return right_foot_height
  
  
def calculate_height_of_feet_left(landmarks: np.ndarray) -> float:
    """Calculate the height of the feet relative to the ground"""
    left_ankle = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value]

    # Assuming the ground plane is at y=0 for simplicity
    # Calculate the height of the left foot
    left_foot_height = left_ankle[1]

    # Return the average height of both feet
    return left_foot_height

def get_all_measurements(landmarks: np.ndarray) -> Dict[str, float]:
  """Get all measurements in one function"""
  measurements = {
      'right_knee_bend': check_knee_bend(landmarks, 'right'),
      'left_knee_bend': check_knee_bend(landmarks, 'left'),
      'right_knee_ankle_alignment': check_knee_ankle_alignment(landmarks, 'right'),
      'left_knee_ankle_alignment': check_knee_ankle_alignment(landmarks, 'left'),
      'back_arch': check_back_arch(landmarks),
      'tailbone_tilt': check_tailbone_tilt(landmarks),
      'stance_width': check_stance_width(landmarks),
      'hip_square': check_hip_square(landmarks),
      'shoulder_alignment': check_shoulder_alignment(landmarks),
      'weight_distribution': check_weight_distribution(landmarks),
      'spine_vertical': check_spine_vertical_alignment(landmarks),
      'pelvis_tilt': check_pelvis_tilt(landmarks),
      'right_knee_over_toes': check_knee_tracking(landmarks, 'right'),
      'left_knee_over_toes': check_knee_tracking(landmarks, 'left'),
      'right_elbow_angle': check_joint_angle(landmarks, 'right_elbow'),
      'left_elbow_angle': check_joint_angle(landmarks, 'left_elbow'),
      'head_neck_alignment': check_alignment(landmarks, 'head_neck'),
      'hip_shoulder_alignment': check_alignment(landmarks, 'hip_shoulder'),
      'hand_foot_distance': check_body_position(landmarks)['hand_foot_distance'],
      'hip_height': check_body_position(landmarks)['hip_height'],
      'symmetry': check_symmetry(landmarks),
      'core_engagement': check_engagement(landmarks)['core_engagement'],
      'leg_engagement': check_engagement(landmarks)['leg_engagement'],
      'height' : calculate_subject_height(landmarks),
      
      'angle_between_legs': calculate_angle_between_legs(landmarks),
      'right_hand_height': right_calculate_height_of_hand(landmarks),
      'left_hand_height': left_calculate_height_of_hand(landmarks),
      'hip_distance_from_ground': calculate_height_of_hips(landmarks),
      'hips_in_between_feet': check_center_of_gravity_in_between_ankles(landmarks),
      'stance_width_distance': check_stance_width(landmarks),
      'right_foot_distance_from_ground': calculate_height_of_feet_right(landmarks),
      'left_foot_distance_from_ground': calculate_height_of_feet_left(landmarks),
      'distance_bestween_feet': calculate_distance_between_feet(landmarks)
  }
  return measurements