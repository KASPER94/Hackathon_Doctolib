# from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime

from sqlalchemy.orm import relationship
from app.database import Base

# Modèle pour les utilisateurs
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)

    items = relationship("Item", back_populates="owner")

# Modèle pour les objets
# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, nullable=True)
#     owner_id = Column(Integer, ForeignKey("users.id"))

#     owner = relationship("User", back_populates="items")

# Nouveau modèle pour les vidéos
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Name of the video
    video_data = Column(LargeBinary, nullable=False)  # Storing the video binary data
    # created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp when the video is created
    # owner_id = Column(Integer, ForeignKey("users.id"))  # Linking video to a user (if needed)

    # owner = relationship("User", back_populates="videos")  # Relationship with User model
