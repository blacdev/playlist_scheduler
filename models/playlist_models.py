from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from uuid import uuid4

class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    name = Column(String, unique=True, index=True)
    duration = Column(Integer, index=True)
    year = Column(Integer, index=True)

    created_at = Column(DateTime, default=datetime.now)
    schedule = relationship("Schedule", back_populates="generated_playlist", foreign_keys="Schedule.generated_playlist_id")
    schedule = relationship("Schedule", back_populates="final_playlist", foreign_keys="Schedule.final_playlist_id")