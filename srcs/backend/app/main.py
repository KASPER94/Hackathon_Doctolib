from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import users, items

# Création des tables dans la base de données
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclusion des routes
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
def root():
	return {"message": "Bienvenue sur FastAPI avec PostgreSQL !"}

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

@app.websocket("/ws/video")
async def video_feed(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)
    frames_data = []
    prev_landmark = None 
    with open("gt.json", "r") as f:
        gt = json.load(f)
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

            # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # results = pose.process(rgb_frame)
            # squat_data = extract_squat_data(results)
            # frames_data.append(squat_data)
            # await llm(squat_data, websocket=websocket)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Détection des points clés de la frame en cours
            cur_landmark = pose.process(frame_rgb)

            # Calcul des angles uniquement s'il y a un mouvement détecté
            angles, prev_landmark = new_extract_squat_data(cur_landmark, prev_landmark, 0.1)
            if len(angles)>0: # Vérifier si des angles ont été calculés
                frames_data.append(angles)
            
            # Envoi au LLM toutes les X frames (éviter trop d'appels inutiles)
            if len(frames_data) >= 30:
                text = await llm(frames_data, gt, websocket=websocket)
                # add frames_data to an aggregated list
                aggregated_data = []
                aggregated_data.append(text)
                frames_data.clear()
            
            if cur_landmark.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, cur_landmark.pose_landmarks, mp_pose.POSE_CONNECTIONS
                )

            if len(angles)>0:
                cv2.putText(frame, f"Gauche: {angles.get('left_knee', 0):.2f}", 
                                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Droite: {angles.get('right_knee', 0):.2f}", 
                                (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"Dos: {angles.get('back_angle', 0):.2f}", 
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
        # Call the llm with the aggregated data
        session_report = await llm(frames_data, gt, websocket=websocket, aggregated_data=aggregated_data)
        print(session_report)
        print("✅ WebSocket fermé proprement.\n")
    # return {"message": "Analyse terminée", "data": frames_data}
