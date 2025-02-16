# from sqlalchemy.orm import Session
# from app.models import Video
# from datetime import datetime

# def add_video(db: Session, video_name: str, video_data: bytes, user_id: int = None):
#     # Create new Video instance and add it to the database
#     video = Video(
#         name=video_name,
#         video_data=video_data,
#         # created_at=datetime.utcnow(),
#         # owner_id=user_id  # Link to a user if needed
#     )
#     db.add(video)
#     db.commit()
#     db.refresh(video)
#     return video

from sqlalchemy.orm import Session
from app.models import Video

def add_video(db: Session, video_name: str, video_data: bytes):
    print("LA1A")
    print(video_name)
    print(type(video_data), len(video_data))    
    print("LA1A")
    try:
        video = Video(
            name=video_name,
            video_data=video_data
        )
        print("LA2A")
        db.add(video)
        db.commit()
        print("LA3A")
        db.refresh(video)
    except Exception as e:
        db.rollback()
        print(f"Erreur SQLAlchemy: {e}")  # Affiche l'erreur exacte
        raise HTTPException(status_code=500, detail=str(e))
        # return video