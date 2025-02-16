from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@postgres:5432/mydb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def add_video(db: Session, video_name: str, video_data: bytes):
#     db = SessionLocal()
#     print("LA1A")
#     print(video_name)
#     print(video_data)
#     print("LA1A")

#     video = Video(
#         id=1,
#         name=video_name,
#         video_data=video_data
#     )
#     print("LA2A")
#     db.add(video)
#     db.commit()
#     print("LA3A")
#     db.refresh(video)

# @router.post("/upload/")
# async def upload_video(
#     print("LA4")
#     video: UploadFile = File(...),
#     exercise_name: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     try:
#         # Save the video file temporarily or read it directly
#         video_content = await video.read()

#         # Add the video to the database (you can also add extra metadata, like exercise_name)
#         new_video = add_video(db, video_name=exercise_name, video_data=video_content)

#         # You can return the video ID or URL for download
#         return JSONResponse(content={"video_id": new_video.id, "message": "Video uploaded successfully."}, status_code=200)

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Error uploading video: {str(e)}")
