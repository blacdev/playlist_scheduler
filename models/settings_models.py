from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from uuid import uuid4


class Settings(Base):
    __tablename__ = "settings"

    id = Column(String, primary_key=True, index=True)
    min_schedule_amount_per_day = Column(Integer, default=2) # This is the number of schedules that can be made in a day
    max_schedule_amount_per_day = Column(Integer, default=4) # This is the number of schedules that can be made in a day

    # min_playlist_amount_per_day = Column(Integer, default=4) # This is the number of playlist that will be played in a day
    # max_playlist_amount_per_day = Column(Integer, default=10) # This is the number of playlist that will be played in a day

    min_schedule_hour_rotation = Column(Integer, default=6) # This is the number of hours before the schedule changes
