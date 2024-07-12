"""
A simple application used to generate  schedule for a week for azuracast radio station.

The application will have the following features:
- Generate a schedule for a week
- Allow entry of new playlist to the system
- Allow entry of time duration for when any playlist will be played. All selected playlist will be added to the time duration for the week

 Application Policy:
The application is goverened by the following rules:
- The schedule should be generated for a week
- The playlist selected on any day should be different from the playlist selected on the previous days or the next day in the same week
- The playlist cannot be repeated in the same week
- Playlist scheduled on on any weekday should be selected randomly and must not match what was on the previous weekday
- The playlist for an entire week will be unique.
- The playlist played on Thursdays are selected  is always plalist that is 4 year minus the current year
- Sunday playlist is scheduled by selecting the Gospel playlist in ascending order i.e Gospel 1, Gospel 2 etc
"""

import random
from datetime import datetime
from models.playlist_models import Playlist
from models.schedule_models import Schedule
import os
from service.playlist_services import get_playlists_from_db, save_playlists_to_db, get_playlist_by_id_from_db
from service.schedule_services import generate_schedule

from database import get_db, create_database





def main(path: str):
    # create the database
    create_database()
    
    import csv
    playlists = []
    with open(path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            playlists.append(Playlist(**row))

    save_playlists_to_db(playlists)

    # fetch all playlists from the database
    playlists = get_playlists_from_db()

    # generate schedule for the week
    # 14th of july 2024 to 21st of july 2024

    schedule = generate_schedule(playlists, datetime(2024, 7, 14))

    from prettytable import PrettyTable
    
    # Create a table with headings
    table = PrettyTable(["Playlist Name", "Start Time", "End Time", "Day"])
    
    for s in schedule:
        d = get_playlist_by_id_from_db(s.generated_playlist_id)
        day = datetime.strftime(datetime.strptime(s.day, '%Y-%m-%d').date(), '%A')
        
        # Add each row to the table
        table.add_row([d.name, s.start_time, s.end_time, day])
    
    # Print the table
    print(table)
       

        

if __name__ == "__main__":
    path = input("Enter the path to the csv file: ")
    main(path)
