# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from app.database import engine
# from app import models
# from app.routers import users, items
# from app.routers.video_analysis import extract_squat_data, new_extract_squat_data
# from app.routers.message import llm
# import cv2
# import asyncio
# import base64
# import numpy as np
# import mediapipe as mp
# import json
# import tempfile
# import math

# # Création des tables dans la base de données
# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()

# # Ajout du middleware CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(users.router)
# app.include_router(items.router)
# # app.include_router(video_analysis.router)

# @app.get("/api/")
# def root():
# 	return {"message": "Bienvenue sur FastAPI avec PostgreSQL !"}

# mp_pose = mp.solutions.pose
# pose = mp_pose.Pose()

# @app.websocket("/ws/video")
# async def video_feed(websocket: WebSocket):
#     await websocket.accept()
#     cap = cv2.VideoCapture(0)
#     frames_data = []

#     try:
#         while True:
#             try:
#                 message = await asyncio.wait_for(websocket.receive_text(), timeout=0.01)
#                 data = json.loads(message)
#                 if data.get("action") == "close":
#                     break
#             except asyncio.TimeoutError:
#                 pass
#             except json.JSONDecodeError:
#                 pass
#             ret, frame = cap.read()
#             if not ret:
#                 break

#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = pose.process(rgb_frame)
#             squat_data = extract_squat_data(results)
#             frames_data.append(squat_data)
#             await llm(squat_data, websocket=websocket)
#             # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # # Détection des points clés
#             # results = pose.process(frame_rgb)
#             # data["angles"], prev_landmark = new_extract_squat_data(results, prev_landmark)
#             # if len(data["angles"])>0:
#             #     frames_data.append(data["angles"])

#             if results.pose_landmarks:
#                 mp.solutions.drawing_utils.draw_landmarks(
#                     frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
#                 )
#             cv2.putText(frame, f"Gauche: {squat_data.get('left_knee', 0):.2f}", 
#                             (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#             cv2.putText(frame, f"Droite: {squat_data.get('right_knee', 0):.2f}", 
#                             (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#             cv2.putText(frame, f"Dos: {squat_data.get('back_angle', 0):.2f}", 
#                             (50, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

#             _, buffer = cv2.imencode(".jpg", frame)
#             img_base64 = base64.b64encode(buffer).decode()

#             await websocket.send_text(json.dumps({"image": img_base64}))
#             await asyncio.sleep(0.03)
#     except WebSocketDisconnect:
#         print("❌ WebSocket déconnecté par le client.")

#     finally:
#         cap.release()
#         print("\n===== Fin du streaming WebSocket =====")
#         print(f"Nombre total de frames collectées : {len(frames_data)}")
#         print("Aperçu des données collectées :")
#         for i, data in enumerate(frames_data[:5]):
#             print(f"Frame {i+1} : {data}")

#         json_filename = "dataMouv.json"
#         with open(json_filename, "w") as f:
#             json.dump(frames_data, f, indent=4)

#         await websocket.close()
#         print("✅ WebSocket fermé proprement.\n")
#     # return {"message": "Analyse terminée", "data": frames_data}

# @app.get("/")
# async def read_root():
#     return {"message": "Hello World"}

# @app.post("/upload/")
# async def upload_file():
#     # Logique pour gérer le téléchargement de fichiers
#     return {"message": "File uploaded successfully"}

from fastapi import FastAPI, File, UploadFile, WebSocket, WebSocketDisconnect
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
import os
import uuid
from fastapi.responses import FileResponse
from fastapi import File, UploadFile, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import get_db
from app.video_service import add_video
import io
from fastapi.responses import StreamingResponse
from app.database import SessionLocal, init_db
from fastapi.responses import JSONResponse


init_db()
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
    frames_data = []

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

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)
            squat_data = extract_squat_data(results)
            frames_data.append(squat_data)
            await llm(squat_data, websocket=websocket)

            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )
            cv2.putText(frame, f"Gauche: {squat_data.get('left_knee', 0):.2f}",
                            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Droite: {squat_data.get('right_knee', 0):.2f}",
                            (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.putText(frame, f"Dos: {squat_data.get('back_angle', 0):.2f}",
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
        print(f"Nombre total de frames collectées : {len(frames_data)}")
        print("Aperçu des données collectées :")
        for i, data in enumerate(frames_data[:5]):
            print(f"Frame {i+1} : {data}")

        json_filename = "dataMouv.json"
        with open(json_filename, "w") as f:
            json.dump(frames_data, f, indent=4)

        await websocket.close()
        print("✅ WebSocket fermé proprement.\n")

@app.post("/upload/")
async def upload_video(
    video: UploadFile = File(...),
    exercise_name: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        video_content = await video.read()
        print(exercise_name)
        new_video = add_video(
            db=db,
            video_name=exercise_name,
            video_data=video_content
        )
        print("Video uploaded successfully.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return JSONResponse(content={"video_id": new_video.id, "name": new_video.name}, status_code=200)
        

@app.get("/videos/")
async def list_videos(db: Session = Depends(get_db)):
    videos = db.query(Video).all()
    return videos

@app.get("/videos/{video_id}/download")
async def download_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id).first()
    if video:
        return FileResponse(video.video_data, media_type="video/mp4", filename=f"{video.name}.mp4")
    return JSONResponse(content={"detail": "Video not found"}, status_code=404)