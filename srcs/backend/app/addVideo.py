# from app.database import SessionLocal
# from app.models import Video, User
# from sqlalchemy.orm import Session

# # Function to insert a video into the database
# def add_video(db: Session, user_id: int, video_name: str, video_path: str):
#     # Read the video file in binary mode
#     with open(video_path, "rb") as video_file:
#         video_data = video_file.read()

#     # Create a new video instance
#     video = Video(
#         name=video_name,
#         video_data=video_data,
#         owner_id=user_id  # Linking the video to a user (optional)
#     )

#     # Add and commit the new video to the database
#     db.add(video)
#     db.commit()
#     db.refresh(video)  # Optional: refresh to get the updated instance with the ID

#     return video

# # Usage example
# db = SessionLocal()  # Create a database session
# user_id = 1  # The ID of the user who owns the video
# video_name = "example_video.mp4"
# video_path = "path_to_your_video/example_video.mp4"

# # Insert the video into the database
# new_video = add_video(db, user_id, video_name, video_path)

# print(f"Video {new_video.name} added with ID {new_video.id}")

from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Video
from app.services.video_service import add_video  # Import the add_video function
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload/")
async def upload_video(
    print("LA4")
    video: UploadFile = File(...),
    exercise_name: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # Save the video file temporarily or read it directly
        video_content = await video.read()

        # Add the video to the database (you can also add extra metadata, like exercise_name)
        new_video = add_video(db, video_name=exercise_name, video_data=video_content)

        # You can return the video ID or URL for download
        return JSONResponse(content={"video_id": new_video.id, "message": "Video uploaded successfully."}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading video: {str(e)}")
