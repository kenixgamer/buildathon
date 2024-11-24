import streamlit as st
from sqlalchemy import select
from llama_index.core import SQLDatabase
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.query_engine import NLSQLTableQueryEngine
from database import create_engine_and_metadata, create_movie_database, populate_movie_database, upload_movie_data, update_movie_data
from datetime import datetime
from vapi_component import vapi_widget

GROQ_API_KEY = "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"

# Enhanced page configuration
st.set_page_config(
    page_title="CineManager",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern UI styling with enhanced visual elements
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    
    /* Card Styles */
    .stCard {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .stCard:hover {
        transform: translateY(-5px);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(33, 147, 176, 0.3);
    }
    
    /* Input Field Styles */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2193b0;
        box-shadow: 0 0 0 2px rgba(33, 147, 176, 0.2);
    }
    
    /* Movie Card Styles */
    .movie-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
    }
    
    /* Header Styles */
    .main-header {
        background: linear-gradient(45deg, #1e3d59, #2193b0);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: white;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
    }
    
    /* Role Selection Styles */
    .role-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        padding: 2rem;
    }
    
    .role-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        width: 300px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .role-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Search Container Styles */
    .search-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Rating Badge Styles */
    .rating-badge {
        background: #ffd700;
        color: #1e3d59;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Form Styles */
    .form-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Alert Styles */
    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Dashboard Stats */
    .stat-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 600;
        color: #2193b0;
    }
    
    .stat-label {
        color: #666;
        margin-top: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 0;
        padding-bottom: 0;
    }m
    
    .recommendation-form {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'role_selection'
    if 'role' not in st.session_state:
        st.session_state.role = None
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

def role_selection_page():
    st.markdown("""
        <div class='main-header' style='text-align: center;'>
            <h1>🎬 CineManager Pro</h1>
            <p>Your complete movie management solution</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(""" 
            <div class='role-container'>
                <div class='role-card text-center mb-4'>
                    <h3 style='color: #1e3d59; margin-bottom: 1rem;'>👤 Visitor</h3>
                    <p style='color: #666; margin-bottom: 1.5rem;'>Browse movies, check showtimes, and get recommendations</p>
                </div>
                <div class='role-card text-center mb-4'>
                    <h3 style='color: #1e3d59; margin-bottom: 1rem;'>🎭 Theater Owner</h3>
                    <p style='color: #666; margin-bottom: 1.5rem;'>Manage your theater, movies, and showtimes</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Add button functionality
    if st.button("Enter as Visitor"):
        st.session_state.role = "Visitor"
        st.session_state.page = "visitor_page"
        st.rerun()
    
    if st.button("Login as Owner"):
        st.session_state.role = "Theater Owner"
        st.session_state.page = "owner_login"
        st.rerun()

def show_role_header():
    if st.session_state.role:
        st.markdown(f"""
            <div style='text-align: right; padding: 1rem;'>
                <span style='color: #666;'>Current Role:</span> 
                <span style='color: #2193b0; font-weight: 500;'>{st.session_state.role}</span>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Change Role", key="change_role"):
            st.session_state.page = "role_selection"
            st.session_state.role = None
            st.session_state.logged_in = False
            st.rerun()

def visitor_page(query_engine, engine, movie_showtimes_table, llm):
    show_role_header()
    st.markdown("""
        <div class='main-header'>
            <h1>Movie Explorer</h1>
            <p>Discover the latest movies and showtimes</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Add CSS to remove white line between tabs
    st.markdown("""
        <style>
        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0;
            padding-bottom: 0;
        }
        
        .recommendation-form {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔍 Search & Browse", "🎯 Movie Recommendations"])
    
    with tab1:
        st.markdown("<div class='search-container'>", unsafe_allow_html=True)
        user_question = st.text_input("Search movies, theaters, or ask questions:", 
                                    placeholder="Enter movie name, location, or any question...",
                                    key="search_input")
        
        if st.button("🔍 Search", key="search_btn"):
            if user_question:
                with st.spinner("Searching..."):
                    stmt = select(movie_showtimes_table).where(
                        movie_showtimes_table.c.movie_name.ilike(f"%{user_question}%") |
                        movie_showtimes_table.c.theater_location.ilike(f"%{user_question}%")
                    )
                    with engine.connect() as connection:
                        result = connection.execute(stmt).fetchall()
                    
                    if result:
                        for movie in result:
                            st.markdown(f"""
                                <div class='movie-card'>
                                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                                        <h3 style='color: #1e3d59; margin-bottom: 1rem;'>{movie.movie_name}</h3>
                                        <span class='rating-badge'>⭐ {movie.imdb_rating}</span>
                                    </div>
                                    <div style='color: #666; margin-bottom: 1rem;'>
                                        <p><strong>Theater:</strong> {movie.theater_name}</p>
                                        <p><strong>Location:</strong> {movie.theater_location}</p>
                                        <p><strong>Language:</strong> {movie.language}</p>
                                    </div>
                                    <div style='padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
                                        <h4 style='color: #1e3d59; margin-bottom: 0.5rem;'>Showtimes</h4>
                                        <p>🌅 Morning: {movie.morning_showtime.strftime("%I:%M %p")} - {movie.morning_available_seats} seats</p>
                                        <p>🌆 Evening: {movie.evening_showtime.strftime("%I:%M %p")} - {movie.evening_available_seats} seats</p>
                                        <p>🌃 Night: {movie.night_showtime.strftime("%I:%M %p")} - {movie.night_available_seats} seats</p>
                                    </div>
                                    <h4 style='color: #1e3d59; margin-bottom: 0.5rem;'>Trailer</h4>
                                    <iframe width="100%" height="315" src='https://www.youtube.com/embed/O9CaB4J4VEI' frameborder="0" allowfullscreen></iframe>
                                    <a href='{movie.booking_link}' target='_blank' class='stButton'>
                                        <button>🎟 Book Now</button>
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
                    else:
                        response = query_engine.query(user_question)
                        st.info(f"💡 {response}")
            else:
                st.warning("Please enter a search term or question")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='recommendation-form'>", unsafe_allow_html=True)
        
        # Movie Preferences Section
        st.subheader(" Your Movie Preferences")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            genre = st.selectbox("Genre", 
                               ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Fantasy", "Thriller"])
            mood = st.selectbox("Mood", 
                              ["Happy", "Relaxed", "Excited", "Thoughtful", "Adventurous"])
            
        with col2:
            language = st.selectbox("Language", 
                                  ["English", "Hindi", "Spanish", "Korean", "Japanese"])
            occasion = st.selectbox("Occasion", 
                                  ["Solo Watch", "Date Night", "Family Time", "Friend Gathering"])
            
        with col3:
            favorite_actor = st.text_input("Favorite Actor/Actress", 
                                         placeholder="e.g., Tom Hanks, Emma Stone")
            release_year = st.slider("Release Year", 1990, 2024, 2020)
            
        # Additional Preferences
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            rating_min = st.slider("Minimum IMDb Rating", 1.0, 10.0, 7.0, 0.1)
            duration_preference = st.select_slider(
                "Movie Duration",
                options=["Short (<90min)", "Medium (90-120min)", "Long (>120min)"],
                value="Medium (90-120min)"
            )
            
        with col2:
            custom_preferences = st.text_area(
                "Additional Preferences",
                placeholder="e.g., movies with plot twists, based on true stories, award-winning films...",
                height=100
            )
        
        # Get Recommendations
        if st.button("Get Personalized Recommendations", key="rec_btn", use_container_width=True):
            with st.spinner("Finding your perfect movie matches..."):
                # Collect all preferences
                preferences = {
                    "genre": genre,
                    "mood": mood,
                    "language": language,
                    "occasion": occasion,
                    "favorite_actor": favorite_actor,
                    "release_year": release_year,
                    "rating_min": rating_min,
                    "duration": duration_preference,
                    "custom_preferences": custom_preferences
                }
                
                # Get recommendations using Groq
                recommendations = get_movie_recommendations(llm, preferences)
                
                # Display recommendations with updated CSS
                st.markdown(f"""
                    <div style='background: transparent; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;'>
                        <h4 style='color: #1e3d59; margin-bottom: 1rem;'>🎬 Your Personalized Recommendations</h4>
                        <p style='white-space: pre-line; color: #1e3d59;'>{recommendations}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        st.markdown("</div>", unsafe_allow_html=True)

def owner_login():
    show_role_header()
    
    st.markdown(""" 
        <div class='main-header'>
            <h1>Theater Owner Login</h1>
            <p>Access your management dashboard</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        with st.form("login_form"):
            id = st.text_input("Owner ID", placeholder="Enter your ID")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if id == "1234" and password == "1234":
                    st.session_state.logged_in = True
                    st.session_state.page = "owner_dashboard"
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Add VAPI widget below the login form
        st.components.v1.html(""" 
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>VAPI Voice Assistant</title>
            </head>
            <body>
                <!-- VAPI Widget Script -->
                <script>
                    var vapiInstance = null;

                    // Replace these with your actual Assistant ID and API Key
                    const assistant = "669a5299-6ab1-4bde-a183-f3ca75b59875"; // Ensure this is correct
                    const apiKey = "5680e105-a9ff-4ed2-a55e-31075962331d"; // Ensure this is correct

                    // Button configuration
                    const buttonConfig = {
                        position: "bottom-right", // Button position
                        offset: "40px", // Distance from the edge
                        width: "50px", // Width of the button
                        height: "50px", // Height of the button
                        idle: { // Button style when idle
                            color: `rgb(93, 254, 202)`, 
                            type: "pill", // "pill" or "round"
                            title: "Need help? Talk to our assistant", 
                            subtitle: "Click to get started",
                            icon: `https://unpkg.com/lucide-static@0.321.0/icons/phone.svg`,
                        },
                        loading: { // Button style when loading
                            color: `rgb(93, 124, 202)`,
                            type: "pill", 
                            title: "Connecting...", 
                            subtitle: "Please wait",
                            icon: `https://unpkg.com/lucide-static@0.321.0/icons/loader-2.svg`,
                        },
                        active: { // Button style when active
                            color: `rgb(255, 0, 0)`,
                            type: "pill",
                            title: "Call in progress",
                            subtitle: "Click to end the call",
                            icon: `https://unpkg.com/lucide-static@0.321.0/icons/phone-off.svg`,
                        },
                    };

                    // Script to load and run the VAPI widget
                    (function (d, t) {
                        var g = document.createElement(t),
                            s = d.getElementsByTagName(t)[0];
                        g.src =
                            "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
                        g.defer = true;
                        g.async = true;
                        s.parentNode.insertBefore(g, s);
                        g.onload = function () {
                            vapiInstance = window.vapiSDK.run({
                                apiKey: apiKey, // mandatory
                                assistant: assistant, // mandatory
                                config: buttonConfig, // optional
                            });
                        };
                    })(document, "script");
                </script>
            </body>
            </html>
        """, height=600)  # Adjust height as needed

def owner_dashboard(engine, movie_showtimes_table):
    show_role_header()
    
    st.markdown("""
        <div class='main-header'>
            <h1>Theater Management Dashboard</h1>
            <p>Manage your movies and showtimes efficiently</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Dashboard Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>24</div>
                <div class='stat-label'>Active Movies</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>1,250</div>
                <div class='stat-label'>Available Seats</div>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>89%</div>
                <div class='stat-label'>Occupancy Rate</div>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>₹52K</div>
                <div class='stat-label'>Today's Revenue</div>
            </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["➕ Add New Movie", "✏️ Edit Movies"])
    
    with tab1:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        with st.form("new_movie_form"):
            st.subheader("Add New Movie Details")
            
            col1, col2 = st.columns(2)
            with col1:
                movie_id = st.number_input("Movie ID", min_value=1, help="Unique identifier for the movie")
                movie_name = st.text_input("Movie Name", placeholder="Enter movie title")
                theater_name = st.text_input("Theater Name", placeholder="Enter theater name")
                language = st.selectbox("Language", ["English", "Hindi", "Spanish", "Korean", "Japanese"])
                
            with col2:
                theater_location = st.text_input("Theater Location", placeholder="Enter theater address")
                booking_link = st.text_input("Booking Link", placeholder="Enter booking URL")
                imdb_rating = st.number_input("IMDb Rating", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
                trailer_link = st.text_input("Trailer Link", placeholder="Enter YouTube trailer URL")
            
            st.subheader("Showtimes")
            col1, col2, col3 = st.columns(3)
            with col1:
                morning_showtime = st.time_input("Morning Show")
                morning_price = st.number_input("Morning Price", min_value=0)
                morning_seats = st.number_input("Morning Available Seats", min_value=0)
            with col2:
                evening_showtime = st.time_input("Evening Show")
                evening_price = st.number_input("Evening Price", min_value=0)
                evening_seats = st.number_input("Evening Available Seats", min_value=0)
            with col3:
                night_showtime = st.time_input("Night Show")
                night_price = st.number_input("Night Price", min_value=0)
                night_seats = st.number_input("Night Available Seats", min_value=0)
            
            st.subheader("Movie Details")
            cast = st.text_area("Cast", placeholder="Enter cast members (comma separated)")
            storyline = st.text_area("Storyline", placeholder="Enter movie plot summary")
            
            if st.form_submit_button("Add Movie", use_container_width=True):
                with st.spinner("Adding movie..."):
                    movie_data = {
                        "movie_id": movie_id,
                        "movie_name": movie_name,
                        "theater_name": theater_name,
                        "morning_showtime": datetime.combine(datetime.today(), morning_showtime),
                        "evening_showtime": datetime.combine(datetime.today(), evening_showtime),
                        "night_showtime": datetime.combine(datetime.today(), night_showtime),
                        "language": language,
                        "theater_location": theater_location,
                        "booking_link": booking_link,
                        "imdb_rating": imdb_rating,
                        "cast": cast,
                        "storyline": storyline,
                        "trailer_link": trailer_link,
                        "morning_ticket_price": morning_price,
                        "evening_ticket_price": evening_price,
                        "night_ticket_price": night_price,
                        "morning_available_seats": morning_seats,
                        "evening_available_seats": evening_seats,
                        "night_available_seats": night_seats
                    }
                    upload_movie_data(engine, movie_showtimes_table, movie_data)
                    st.success("Movie added successfully! 🎉")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        movie_id_to_edit = st.number_input("Enter Movie ID to Edit:", min_value=1)
        
        if movie_id_to_edit:
            with st.spinner("Loading movie details..."):
                stmt = select(movie_showtimes_table).where(movie_showtimes_table.c.movie_id == movie_id_to_edit)
                with engine.connect() as connection:
                    result = connection.execute(stmt).fetchone()
                
                if result:
                    with st.form("edit_movie_form"):
                        # Similar form fields as Add New Movie, but pre-filled
                        col1, col2 = st.columns(2)
                        with col1:
                            movie_name = st.text_input("Movie Name", value=result.movie_name)
                            theater_name = st.text_input("Theater Name", value=result.theater_name)
                            language = st.text_input("Language", value=result.language)
                        with col2:
                            theater_location = st.text_input("Theater Location", value=result.theater_location)
                            booking_link = st.text_input("Booking Link", value=result.booking_link)
                            imdb_rating = st.number_input("IMDb Rating", value=result.imdb_rating, min_value=0.0, max_value=10.0)
                        
                        st.subheader("Show Times")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            morning_showtime = st.time_input("Morning Show", value=result.morning_showtime.time())
                        with col2:
                            evening_showtime = st.time_input("Evening Show", value=result.evening_showtime.time())
                        with col3:
                            night_showtime = st.time_input("Night Show", value=result.night_showtime.time())
                        
                        cast = st.text_area("Cast", value=result.cast)
                        storyline = st.text_area("Storyline", value=result.storyline)
                        
                        if st.form_submit_button("Update Movie", use_container_width=True):
                            with st.spinner("Updating movie..."):
                                movie_data = {
                                    "movie_id": movie_id_to_edit,
                                    "movie_name": movie_name,
                                    "theater_name": theater_name,
                                    "morning_showtime": datetime.combine(datetime.today(), morning_showtime),
                                    "evening_showtime": datetime.combine(datetime.today(), evening_showtime),
                                    "night_showtime": datetime.combine(datetime.today(), night_showtime),
                                    "language": language,
                                    "theater_location": theater_location,
                                    "booking_link": booking_link,
                                    "imdb_rating": imdb_rating,
                                    "cast": cast,
                                    "storyline": storyline
                                }
                                update_movie_data(engine, movie_showtimes_table, movie_data)
                                st.success("Movie updated successfully! 🎉")
                else:
                    st.error("Movie not found. Please check the Movie ID.")
        st.markdown("</div>", unsafe_allow_html=True)

def get_movie_recommendations(llm, preferences):
    """
    Get movie recommendations using Groq LLM based on user preferences.
    
    Args:
        llm: Groq LLM instance
        preferences (dict): Dictionary containing user preferences
    """
    # Construct a detailed prompt for the LLM
    prompt = f"""You are a knowledgeable movie expert. Based on the following preferences, recommend 5 movies that would be perfect for the viewer. For each movie, explain why it matches their preferences.

User Preferences:
- Genre: {preferences['genre']}
- Mood: {preferences['mood']}
- Language: {preferences['language']}
- Occasion: {preferences['occasion']}
- Favorite Actor/Actress: {preferences.get('favorite_actor', 'Not specified')}
- Preferred Release Year: {preferences.get('release_year', 'Any')}
- Minimum Rating: {preferences.get('rating_min', 'Any')}
- Duration Preference: {preferences.get('duration', 'Any')}
{f"- Additional Preferences: {preferences['custom_preferences']}" if preferences.get('custom_preferences') else ""}

Please provide recommendations in this format:
1. [Movie Title] (Year) - Rating
   - Brief description
   - Why it matches: [Explanation]

2. [Next Movie]...
"""
    
    # Get recommendations from Groq
    try:
        response = llm.complete(prompt).text
        return response
    except Exception as e:
        return f"Error getting recommendations: {str(e)}"

def recommendation_page(llm):
    st.markdown("<div class='recommendation-form'>", unsafe_allow_html=True)
    
    # Movie Preferences Section
    st.subheader("🎬 Your Movie Preferences")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        genre = st.selectbox("Genre", 
                           ["Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Fantasy", "Thriller"])
        mood = st.selectbox("Mood", 
                          ["Happy", "Relaxed", "Excited", "Thoughtful", "Adventurous"])
        
    with col2:
        language = st.selectbox("Language", 
                              ["English", "Hindi", "Spanish", "Korean", "Japanese"])
        occasion = st.selectbox("Occasion", 
                              ["Solo Watch", "Date Night", "Family Time", "Friend Gathering"])
        
    with col3:
        favorite_actor = st.text_input("Favorite Actor/Actress", 
                                     placeholder="e.g., Tom Hanks, Emma Stone")
        release_year = st.slider("Release Year", 1990, 2024, 2020)
        
    # Additional Preferences
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        rating_min = st.slider("Minimum IMDb Rating", 1.0, 10.0, 7.0, 0.1)
        duration_preference = st.select_slider(
            "Movie Duration",
            options=["Short (<90min)", "Medium (90-120min)", "Long (>120min)"],
            value="Medium (90-120min)"
        )
        
    with col2:
        custom_preferences = st.text_area(
            "Additional Preferences",
            placeholder="e.g., movies with plot twists, based on true stories, award-winning films...",
            height=100
        )
    
    # Get Recommendations
    if st.button("Get Personalized Recommendations", key="rec_btn", use_container_width=True):
        with st.spinner("Finding your perfect movie matches..."):
            # Collect all preferences
            preferences = {
                "genre": genre,
                "mood": mood,
                "language": language,
                "occasion": occasion,
                "favorite_actor": favorite_actor,
                "release_year": release_year,
                "rating_min": rating_min,
                "duration": duration_preference,
                "custom_preferences": custom_preferences
            }
            
            # Get recommendations using Groq
            recommendations = get_movie_recommendations(llm, preferences)
            
            # Display recommendations with updated CSS
            st.markdown(f"""
                <div style='background: transparent; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;'>
                    <h4 style='color: #1e3d59; margin-bottom: 1rem;'>🎬 Your Personalized Recommendations</h4>
                    <p style='white-space: pre-line; color: #1e3d59;'>{recommendations}</p>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    initialize_session_state()
    
    # Initialize database and query engine
    engine, metadata_obj = create_engine_and_metadata()
    movie_showtimes_table = create_movie_database(engine, metadata_obj)
    populate_movie_database(engine, movie_showtimes_table)
    
    sql_database = SQLDatabase(engine, include_tables=["movie_showtimes"])
    
    # Initialize Groq LLM
    llm = Groq(
        model="llama3-70b-8192",
        api_key=GROQ_API_KEY
    )
    
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database,
        tables=["movie_showtimes"],
        llm=llm,
        embed_model=embed_model
    )
    
    # Add the Vapi Widget HTML and JavaScript
    st.components.v1.html("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Vapi Voice Assistant</title>
        </head>
        <body>
            <!-- Vapi Widget Script -->
            <script>
                var vapiInstance = null;

                // Replace these with your actual Assistant ID and API Key
                const assistant = "<assistant_id>"; // Example: "abc123"
                const apiKey = "<your_public_api_key>"; // Example: "xyz456"

                // Button configuration
                const buttonConfig = {
                    position: "bottom-right", // Button position
                    offset: "40px", // Distance from the edge
                    width: "50px", // Width of the button
                    height: "50px", // Height of the button
                    idle: { // Button style when idle
                        color: `rgb(93, 254, 202)`, 
                        type: "pill", // "pill" or "round"
                        title: "want recommandation or book tickets?", 
                        subtitle: "Talk with Booky AI",
                        icon: `https://unpkg.com/lucide-static@0.321.0/icons/phone.svg`,
                    },
                    loading: { // Button style when loading
                        color: `rgb(93, 124, 202)`,
                        type: "pill", 
                        title: "Connecting...", 
                        subtitle: "Please wait",
                        icon: `https://unpkg.com/lucide-static@0.321.0/icons/loader-2.svg`,
                    },
                    active: { // Button style when active
                        color: `rgb(255, 0, 0)`,
                        type: "pill",
                        title: "Call is in progress...",
                        subtitle: "End the call.",
                        icon: `https://unpkg.com/lucide-static@0.321.0/icons/phone-off.svg`,
                    },
                };

                // Script to load and run the Vapi widget
                (function (d, t) {
                    var g = document.createElement(t),
                        s = d.getElementsByTagName(t)[0];
                    g.src =
                        "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
                    g.defer = true;
                    g.async = true;
                    s.parentNode.insertBefore(g, s);
                    g.onload = function () {
                        vapiInstance = window.vapiSDK.run({
                            apiKey: apiKey, // mandatory
                            assistant: assistant, // mandatory
                            config: buttonConfig, // optional
                        });
                    };
                })(document, "script");
            </script>
        </body>
        </html>
    """, height=600)  # Adjust height as needed
    
    # Page routing
    if st.session_state.page == "role_selection":
        role_selection_page()
    elif st.session_state.page == "visitor_page":
        visitor_page(query_engine, engine, movie_showtimes_table, llm)
    elif st.session_state.page == "owner_login":
        owner_login()
    elif st.session_state.page == "owner_dashboard" and st.session_state.logged_in:
        owner_dashboard(engine, movie_showtimes_table)
    elif st.session_state.page == "recommendation_page":
        recommendation_page(llm)
    else:
        role_selection_page()

if __name__ == "__main__":
    main()