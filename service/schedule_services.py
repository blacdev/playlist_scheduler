from models.schedule_models import Schedule
from models.playlist_models import Playlist
from models.settings_models import Settings
from service.utils import get_settings
from datetime import datetime
import random
from random import choice
from database import get_db
from typing import List, Tuple, Set, Optional
import re
from datetime import timedelta

WEEKDAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def save_schedule_to_db(schedule: list) -> list:
    """
    Save schedule to database:
        This function saves a schedule to the database.
    """
    with get_db() as db:
        db.add_all(schedule)
        db.commit()


def generate_schedule(
    playlists: List[Playlist], start_date: datetime,
) -> List[Schedule]:
    schedule = []
    selected_playlists = set()
    valid_playlists, outdated_playlists, sunday_playlists = filter_outdated_playlists(
        playlists
    )
    end_date = start_date + timedelta(days=7)
    current_date = start_date

    while current_date < end_date:
        day_schedule = generate_day_schedule(
            current_date,
            valid_playlists,
            sunday_playlists,
            outdated_playlists,
            selected_playlists,

        )
        schedule.extend(day_schedule)
        current_date += timedelta(days=1)

    return schedule


def filter_outdated_playlists(
    playlists: List[Playlist],
) -> Tuple[List[Playlist], List[Playlist], List[Playlist]]:
    current_year = datetime.now().year
    cutoff_year = (
        current_year - 3
    )  # Adjusted to allow playlists from current year up to 3 years back
    year_pattern = re.compile(r"\b(\d{4})\b")

    sunday_playlists = [p for p in playlists if "Gospel" in p.name]
    valid_playlists = [
        p
        for p in playlists
        if not "Gospel" in p.name
        and year_pattern.search(p.name)
        and int(year_pattern.search(p.name).group(1)) >= cutoff_year
    ]
    outdated_playlists = [
        p
        for p in playlists
        if not "Gospel" in p.name
        and (
            not year_pattern.search(p.name)
            or int(year_pattern.search(p.name).group(1)) < cutoff_year
        )
    ]
    
    return valid_playlists, outdated_playlists, sunday_playlists


def generate_day_schedule(
    date: datetime,
    valid_playlists: List[Playlist],
    sunday_playlists: List[Playlist],
    outdated_playlists: List[Playlist],
    selected_playlists: Set[Playlist],
) -> List[Schedule]:
    day_schedule = []
    day_name = date.strftime("%A")
    remaining_hours = 24
    last_selected_year = None
    selected_years = []

    # Select the first playlist of the day from outdated_playlists
    if day_name != "Thursday":
        playlist = get_playlist_for_outdated(
            outdated_playlists, selected_playlists, selected_years
        )
        if playlist:
            selected_playlists.add(playlist)
            selected_years.append(int(re.search(r"\b(\d{4})\b", playlist.name).group(1)))

            
            slot_start_time = date.replace(hour=0, minute=0, second=0)
            if playlist.duration <= remaining_hours:
                day_schedule.append(
                    Schedule(
                        day=date.strftime("%Y-%m-%d"),
                        start_time=slot_start_time,
                        end_time=slot_start_time + timedelta(hours=playlist.duration),
                        generated_playlist_id=playlist.id,  # Replace with your playlist_id logic
                    )
                )
                remaining_hours -= playlist.duration
            else:
                day_schedule.append(
                    Schedule(
                        day=date.strftime("%Y-%m-%d"),
                        start_time=slot_start_time,
                        end_time=slot_start_time + timedelta(hours=remaining_hours),
                        generated_playlist_id=playlist.id,  # Replace with your playlist_id logic
                    )
                )
                remaining_hours = 0

    # Continue with the rest of the day's schedule
    while remaining_hours > 0 :
        slot_start_time = date.replace(hour=24 - remaining_hours, minute=0, second=0)
        slot_end_time = slot_start_time + timedelta(hours=1)

        if (
            day_name == "Sunday"
            and slot_start_time.hour >= 6
            and slot_end_time.hour <= 14
        ):
            playlist = get_playlist_for_sunday(sunday_playlists, selected_playlists)
        elif day_name == "Thursday":
            playlist = get_playlist_for_thursday(
                outdated_playlists, selected_playlists, selected_years
            )
        else:
            playlist = get_playlist_for_time_slot(
                valid_playlists, selected_playlists, selected_years, last_selected_year
            )
            if playlist and re.search(r"\b(\d{4})\b", playlist.name):
                last_selected_year = int(
                    re.search(r"\b(\d{4})\b", playlist.name).group(1)
                )

        if playlist:
            selected_playlists.add(playlist)
            year_match = re.search(r"\b(\d{4})\b", playlist.name)

            if year_match:
                selected_years.append(year_match.group(1))

            if playlist.duration <= remaining_hours:
                day_schedule.append(
                    Schedule(
                        day=date.strftime("%Y-%m-%d"),
                        start_time=slot_start_time,
                        end_time=slot_start_time + timedelta(hours=playlist.duration),
                        generated_playlist_id=playlist.id,  # Replace with your playlist_id logic
                    )
                )
                remaining_hours -= playlist.duration
            else:
                day_schedule.append(
                    Schedule(
                        day=date.strftime("%Y-%m-%d"),
                        start_time=slot_start_time,
                        end_time=slot_start_time + timedelta(hours=remaining_hours),
                        generated_playlist_id=playlist.id,  # Replace with your playlist_id logic
                    )
                )
                remaining_hours = 0

    return day_schedule


def get_playlist_for_sunday(
    sunday_playlists: List[Playlist], selected_playlists: Set[Playlist]
) -> Playlist:
    available_playlists = [
        p
        for p in sunday_playlists
        if p not in selected_playlists and "Gospel" in p.name
    ]
    if available_playlists:
        return random.choice(available_playlists)
    return None



def get_playlist_for_thursday(
    outdated_playlists: List[Playlist],
    selected_playlists: Set[Playlist],
    selected_years: List[int],
) -> Optional[Playlist]:
    available_playlists = []
    for playlist in outdated_playlists:
        year_match = re.search(r"\b(\d{4})\b", playlist.name)
        if year_match:
            year = int(year_match.group(1))
            if year <= (datetime.now().year - 6) and playlist not in selected_playlists and year not in selected_years:
                available_playlists.append(playlist)

    if available_playlists:
        return random.choice(available_playlists)
    return None


def get_playlist_for_time_slot(
    valid_playlists: List[Playlist],
    selected_playlists: Set[Playlist],
    selected_years: List[int],
    last_selected_year: int = None,
) -> Playlist:
    available_playlists = [p for p in valid_playlists if p not in selected_playlists]

    if last_selected_year is not None:
        available_playlists = [
            p
            for p in available_playlists
            if int(re.search(r"\b(\d{4})\b", p.name).group(1)) != last_selected_year
        ]

    if selected_years:
        available_playlists = [
            p
            for p in available_playlists
            if not any(str(year) in p.name for year in selected_years)
        ]

    if available_playlists:
        return random.choice(available_playlists)
    return None


def get_playlist_for_outdated(
    outdated_playlists: List[Playlist],
    selected_playlists: Set[Playlist],
    selected_years: List[int],
) -> Playlist:
    available_playlists = [
        p
        for p in outdated_playlists
        if p not in selected_playlists
        and not any(str(year) in p.name for year in selected_years)
    ]
    
    if available_playlists:
        return random.choice(available_playlists)
    return None
