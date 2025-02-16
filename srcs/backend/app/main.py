from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import users, items
from app.routers.video_analysis import extract_squat_data, new_extract_squat_data
from app.routers.message import llm
import cv2
import asyncio
import base64
import numpy as np
import mediapipe as mp
import json
import tempfile
import math

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
# app.include_router(video_analysis.router)

@app.get("/api/")
def root():
	return {"message": "Bienvenue sur FastAPI avec PostgreSQL !"}

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

@app.websocket("/ws/video")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)
    
    squats_list = []  # Liste de tous les squats détectés
    current_squat = []  # Liste temporaire pour stocker un squat en cours
    temp_squat = []
    mouv_complet = []

    # Détection de l'orientation
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    squatTrigger = 150 if height > width else 170
    tolerance = 5  # Tolérance de 5 degrés
    trigger_start = squatTrigger - tolerance

    print(f"Sélection du trigger à {squatTrigger}° avec une tolérance de {tolerance}°")

    in_squat = False  # Indicateur si un squat est en cours
    squat_validated = False  # Vérifie qu'on a atteint la position basse
    prev_landmark = None
    gt = {}
    try:    
        while True:
            try:
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
                data = json.loads(message)
                if data.get("action") == "close":
                    break
            except asyncio.TimeoutError:
                pass
            except json.JSONDecodeError:
                pass
            ret, frame = cap.read()
            if not ret:
                break

            ret, frame = cap.read()
        
            # Convertir l'image en RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Détection des points clés
            results = pose.process(frame_rgb)
            data, prev_landmark = new_extract_squat_data(results, prev_landmark, 0.05) 
            if "left_knee" in data and "right_knee" in data:
                left_knee_angle = data["left_knee"]
                right_knee_angle = data["right_knee"]
                back_angle = data["back_angle"]
                # Détection du début du squat (zone de tolérance)
                if not in_squat and (left_knee_angle + right_knee_angle)/2 < trigger_start and back_angle < trigger_start:
                    in_squat = True
                    squat_validated = False  # On attend encore de confirmer le squat
                    current_squat = []  # Nouvelle liste pour stocker le squat en cours
                    print("Détection en approche du squat")
                # Validation du squat (descente sous squatTrigger)
                if in_squat and not squat_validated and (left_knee_angle + right_knee_angle)/2 < squatTrigger and back_angle < squatTrigger:
                    squat_validated = True
                    print("Squat validé, enregistrement des frames")
                # Ajout des frames au squat en cours si validé
                if squat_validated:
                    current_squat.append(data)
                    mouv_complet.append(data)
                # Détection de la fin d’un squat (remontée au-dessus du trigger)
                if in_squat and squat_validated and (left_knee_angle + right_knee_angle)/2 >= squatTrigger and back_angle >=squatTrigger:
                    in_squat = False
                    squat_validated = False
                    if len(current_squat) > 0:
                        await llm(current_squat, gt, websocket=websocket)
                        squats_list.append(current_squat)
                        print(f"Squat terminé, {len(current_squat)} frames enregistrées")
         

            # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # results = pose.process(rgb_frame)
            # squat_data = extract_squat_data(results)
            # frames_data.append(squat_data)
            # await llm(squat_data, websocket=websocket)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Détection des points clés de la frame en cours
            cur_landmark = results

            if cur_landmark.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, cur_landmark.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )

            if len(data)>0:
                cv2.putText(frame, f"Gauche: {data.get('left_knee', 0):.2f}", 
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Droite: {data.get('right_knee', 0):.2f}", 
                                (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Dos: {data.get('back_angle', 0):.2f}", 
                                (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

            _, buffer = cv2.imencode(".jpg", frame)
            img_base64 = base64.b64encode(buffer).decode()

            await websocket.send_text(json.dumps({"image": img_base64}))
            await asyncio.sleep(0.03)
    except WebSocketDisconnect:
        print("❌ WebSocket déconnecté par le client.")

    finally:
        cap.release()
        print("\n===== Fin du streaming WebSocket =====")
        print(f"Nombre total de frames collectées : {len(current_squat)}")
        print("Aperçu des données collectées :")
        for i, dataSquat in enumerate(current_squat[:5]):
            print(f"Frame {i+1} : {dataSquat}")

        json_filename = "dataMouv.json"
        with open(json_filename, "w") as f:
            json.dump(current_squat, f, indent=4)

        await websocket.close()
        print("✅ WebSocket fermé proprement.\n")
    # return {"message": "Analyse terminée", "data": frames_data}
