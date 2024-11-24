# database.py

import warnings
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, DateTime, Float, insert
from datetime import datetime, timedelta
import random

warnings.filterwarnings('ignore')

def create_movie_database(engine, metadata_obj):
    # Create movie showtimes table with additional columns for different showtimes
    movie_showtimes_table = Table(
        "movie_showtimes",
        metadata_obj,
        Column("movie_id", Integer, primary_key=True),
        Column("movie_name", String(100), nullable=False),
        Column("theater_name", String(100), nullable=False),
        Column("morning_showtime", DateTime, nullable=False),  # New column for morning showtime
        Column("evening_showtime", DateTime, nullable=False),  # New column for evening showtime
        Column("night_showtime", DateTime, nullable=False),  # New column for night showtime
        Column("showtime", DateTime, nullable=False),
        Column("theater_location", String(100), nullable=False),
        Column("booking_link", String(255), nullable=True),  # New column for booking link
        Column("imdb_rating", Float, nullable=True),          # New column for IMDb rating
        Column("cast", String(255), nullable=True),           # New column for cast
        Column("storyline", String(500), nullable=True),      # New column for storyline
        Column("language", String(50), nullable=True),        # New column for language
        Column("trailer_link", String(255), nullable=True),    # New column for YouTube trailer link
        Column("morning_available_seats", Integer, nullable=True),  # New column for morning available seats
        Column("morning_ticket_price", Float, nullable=True),       # New column for morning ticket price
        Column("evening_available_seats", Integer, nullable=True),  # New column for evening available seats
        Column("evening_ticket_price", Float, nullable=True),       # New column for evening ticket price
        Column("night_available_seats", Integer, nullable=True),    # New column for night available seats
        Column("night_ticket_price", Float, nullable=True)           # New column for night ticket price
    )
    metadata_obj.create_all(engine)
    return movie_showtimes_table

def populate_movie_database(engine, movie_showtimes_table):
    # Sample movie showtime data with additional fields for different showtimes
    showtimes = [
        {
            "movie_id": 1,
            "movie_name": "Avengers: Endgame",
            "theater_name": "IMAX Downtown",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "morning_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "morning_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "evening_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "evening_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "night_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "night_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "showtime": datetime.now() + timedelta(hours=2),
            "theater_location": "Downtown City Center",
            "booking_link": "https://bookmyshow.com/avengers-endgame-downtown",
            "imdb_rating": 8.4,
            "cast": "Robert Downey Jr., Chris Evans, Scarlett Johansson",
            "storyline": "The Avengers assemble to reverse the damage caused by Thanos.",
            "language": "English",
            "trailer_link": "https://www.youtube.com/watch?v=TcMBFSGVi1c"
        },
        # ... other existing movie entries ...
        {
            "movie_id": 14,
            "movie_name": "Bhool Bhulaiyaa 2",
            "theater_name": "INOX Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "morning_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "morning_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "evening_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "evening_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "night_available_seats": random.randint(20, 100),  # Random available seats between 20 and 100
            "night_ticket_price": round(random.uniform(150, 500), 2),  # Random price between 150 and 500
            "showtime": datetime.now() + timedelta(hours=3),
            "theater_location": "Phoenix Mall",
            "booking_link": "https://youtu.be/6YMY62tMLUA?si=TDr1Ch7uNQP4xVev",
            "imdb_rating": 8.1,
            "cast": "Kartik Aaryan, Triptii Dimri, Vidya Balan",
            "storyline": "The third installment in the popular Bhool Bhulaiyaa franchise follows a new supernatural mystery in a haunted haveli.",
            "language": "Hindi",
            "trailer_link": "https://youtu.be/6YMY62tMLUA?si=TDr1Ch7uNQP4xVev"
        },
        {
            "movie_id": 15,
            "movie_name": "Venom: The Last Dance",
            "theater_name": "Cinepolis IMAX",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "morning_available_seats": random.randint(20, 100),
            "morning_ticket_price": round(random.uniform(150, 500), 2),
            "evening_showtime": datetime.now() + timedelta(hours=2),
            "evening_available_seats": random.randint(20, 100),
            "evening_ticket_price": round(random.uniform(150, 500), 2),
            "night_showtime": datetime.now() + timedelta(hours=3),
            "night_available_seats": random.randint(20, 100),
            "night_ticket_price": round(random.uniform(150, 500), 2),
            "showtime": datetime.now() + timedelta(hours=4),
            "theater_location": "Downtown Plaza",
            "booking_link": "https://bookmyshow.com/venom3-cinepolis",
            "imdb_rating": 7.5,
            "cast": "Tom Hardy, Juno Temple, Chiwetel Ejiofor",
            "storyline": "Eddie Brock attempts to navigate his final adventure with the alien symbiote Venom in this concluding chapter.",
            "language": "English",
            "trailer_link": "https://youtu.be/VWB8RM9qHPg?si=EG6iQqmwEZlyB61T"
        },
        {
            "movie_id": 16,
            "movie_name": "The Sabarmati Report",
            "theater_name": "PVR Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=5),
            "theater_location": "City Centre Mall",
            "booking_link": "https://bookmyshow.com/sabarmati-report-pvr",
            "imdb_rating": 6.6,
            "cast": "Vikrant Massey, Raashii Khanna, Ridhi Dogra",
            "storyline": "An investigative thriller that uncovers the truth behind a significant historical event at Sabarmati.",
            "language": "Hindi",
            "trailer_link": "https://youtu.be/Mjtv0KkgCqM?si=z1RkkXv1z3v7LWFQ"
        },
        {
            "movie_id": 17,
            "movie_name": "Kanguva",
            "theater_name": "AGS Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=6),
            "theater_location": "Marina Mall",
            "booking_link": "https://bookmyshow.com/kanguva-ags",
            "imdb_rating": 7.7,
            "cast": "Suriya, Bobby Deol, Disha Patani",
            "storyline": "A period action drama set in a different era, following the journey of a warrior who must protect his kingdom.",
            "language": "Tamil",
            "trailer_link": "https://youtu.be/ajnCMSC4VPo?si=A_OQT7FUFb2M7oa-"
        },
        {
            "movie_id": 18,
            "movie_name": "Vicky Vidya Ka Woh Wala Video",
            "theater_name": "PVR Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=7),
            "theater_location": "Citywalk Mall",
            "booking_link": "https://bookmyshow.com/vickyvideo-pvr",
            "imdb_rating": 7.1,
            "cast": "Rajkummar Rao, Triptii Dimri, Vijay Raaz, Mallika Sherawat",
            "storyline": "A newly married couple's relationship and reputation are put at risk when their private video CD is stolen.",
            "language": "Hindi",
            "trailer_link": "https://youtu.be/0xXa9a2rHoQ?si=dNm9pwM9lO7VSowB"
        },
        {
            "movie_id": 19,
            "movie_name": "I Want to Talk",
            "theater_name": "INOX Movies",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=8),
            "theater_location": "Central Square",
            "booking_link": "https://bookmyshow.com/iwanttotalk-inox",
            "imdb_rating": 5.5,
            "cast": "To be announced",
            "storyline": "An intimate drama exploring human connections and the importance of communication in modern relationships.",
            "language": "Hindi",
            "trailer_link": "https://youtu.be/kZXlMsupVz8?si=VqdEx40O7prYwy6v"
        },
        {
            "movie_id": 20,
            "movie_name": "Gladiator II",
            "theater_name": "Cinepolis",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=9),
            "theater_location": "Grand Mall",
            "booking_link": "https://bookmyshow.com/gladiator2-cinepolis",
            "imdb_rating": 5.5,
            "cast": "Russell Crowe, Joaquin Phoenix, Denzel Washington",
            "storyline": "The sequel to the epic Gladiator, following the rise of a new Roman Empire after the death of Maximus.",
            "language": "English and Hindi",
            "trailer_link": "https://youtu.be/4rgYUipGJNo?si=D7QkM0Mamx_YEkRI"
        },
        {
            "movie_id": 21,
            "movie_name": "Wicked",
            "theater_name": "PVR Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=10),
            "theater_location": "Mall of India",
            "booking_link": "https://bookmyshow.com/wicked-pvr",
            "imdb_rating": 6.6,
            "cast": "Ariana Grande, Cynthia Erivo, Jeff Goldblum",
            "storyline": "A musical based on the life of Elphaba and Glinda, exploring the origins of the witches from The Wizard of Oz.",
            "language": "English and Hindi",
            "trailer_link": "https://youtu.be/6COmYeLsz4c?si=uv6INq8xuXculBxS"
        },
        {
            "movie_id": 22,
            "movie_name": "Tumbad",
            "theater_name": "INOX",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=11),
            "theater_location": "City Center Mall",
            "booking_link": "https://in.bookmyshow.com/movies/tumbbad/ET00079092",
            "imdb_rating": 8.2,
            "cast": "Sohum Shah, Jyoti Malshe, Anita Date",
            "storyline": "A dark fantasy about a man's quest to uncover a hidden treasure in the village of Tumbad, surrounded by ancient evil.",
            "language": "Hindi",
            "trailer_link": "https://youtu.be/O9CaB4J4VEI?si=YxZVtvbLl6m8Rjgy"
        },
        {
            "movie_id": 23,
            "movie_name": "Despicable Me 4",
            "theater_name": "Carnival Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=12),
            "theater_location": "Star Mall",
            "booking_link": "https://bookmyshow.com/despicableme4-carnival",
            "imdb_rating": 6.5,
            "cast": "Steve Carell, Kristen Wiig, Miranda Cosgrove",
            "storyline": "Gru and the Minions face new challenges and embark on an adventure full of humor, chaos, and heart.",
            "language": "English",
            "trailer_link": "https://youtube.com/despicableme4-trailer"
        },
        {
            "movie_id": 24,
            "movie_name": "Kung Fu Panda 4",
            "theater_name": "Wave Cinemas",
            "morning_showtime": datetime.now() + timedelta(hours=1),  # Morning showtime
            "evening_showtime": datetime.now() + timedelta(hours=2),  # Evening showtime
            "night_showtime": datetime.now() + timedelta(hours=3),  # Night showtime
            "showtime": datetime.now() + timedelta(hours=13),
            "theater_location": "Cineplex Mall",
            "booking_link": "https://bookmyshow.com/kungfupanda4-wave",
            "imdb_rating": 5.6,
            "cast": "Jack Black, Angelina Jolie, Dustin Hoffman",
            "storyline": "Po continues his journey to be the Dragon Warrior while facing a new, powerful adversary.",
            "language": "English and Hindi",
            "trailer_link": "https://youtube.com/kungfupanda4-trailer"
        }
    ]

    # Insert showtimes
    for showtime in showtimes:
        stmt = insert(movie_showtimes_table).values(**showtime)
        with engine.begin() as connection:
            connection.execute(stmt)

def upload_movie_data(engine, movie_showtimes_table, movie_data):
    stmt = insert(movie_showtimes_table).values(**movie_data)
    with engine.begin() as connection:
        connection.execute(stmt)

def create_engine_and_metadata():
    # Create SQLite in-memory database
    engine = create_engine("sqlite:///:memory:")
    metadata_obj = MetaData()
    return engine, metadata_obj

def update_movie_data(engine, movie_showtimes_table, movie_data):
    # Update the movie details in the database
    stmt = (
        movie_showtimes_table.update()
        .where(movie_showtimes_table.c.movie_id == movie_data["movie_id"])
        .values(
            movie_name=movie_data["movie_name"],
            theater_name=movie_data["theater_name"],
            showtime=movie_data["showtime"],
            theater_location=movie_data["theater_location"],
            booking_link=movie_data["booking_link"],
            imdb_rating=movie_data["imdb_rating"],
            cast=movie_data["cast"],
            storyline=movie_data["storyline"],
            language=movie_data["language"],
            trailer_link=movie_data["trailer_link"]
        )
    )
    with engine.begin() as connection:
        connection.execute(stmt)