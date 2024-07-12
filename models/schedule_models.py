from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from uuid import uuid4


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    day = Column(String, index=True)
    date = Column(DateTime, index=True)
    start_time = Column(DateTime, index=True)
    end_time = Column(DateTime, index=True)
    generated_playlist_id = Column(String,ForeignKey("playlists.id"))
    final_playlist_id = Column(String, ForeignKey("playlists.id"))

    created_at = Column(DateTime, default=datetime.now)
    generated_playlist = relationship("Playlist", back_populates="schedule", foreign_keys=[generated_playlist_id])
    final_playlist = relationship("Playlist", back_populates="schedule", foreign_keys=[final_playlist_id])
