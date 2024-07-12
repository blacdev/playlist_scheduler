from models.settings_models import Settings
from database import get_db
import re

def get_settings() -> Settings:
    """
    Get settings:
        This function fetches the settings from the database and returns them.
    """
    with get_db() as db:
        settings = db.query(Settings).first()
    return settings

def extract_year(name: str) -> int:
    """
    Extract the year from the playlist name. Return None if no year is found.
    """
    pattern = re.compile(r'\b(\d{4})\b')
    match = pattern.search(name)
    if match:
        return int(match.group(1))
    return None