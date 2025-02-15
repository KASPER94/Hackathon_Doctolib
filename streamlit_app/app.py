import cv2
import streamlit as st
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

def stream_camera():
    """Fonction pour capturer et afficher le flux vidéo avec détection des poses."""
    st.title("📹 Suivi en direct avec OpenCV et Mediapipe")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("❌ Impossible d'ouvrir la caméra. Vérifiez qu'elle est bien branchée.")
        return

    frame_placeholder = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("❌ Impossible de capturer la vidéo.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = pose.process(rgb_frame)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
            )

        frame_placeholder.image(frame, channels="BGR", use_column_width=True)

    cap.release()

if __name__ == "__main__":
    stream_camera()
