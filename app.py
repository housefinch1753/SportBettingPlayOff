import logging

import streamlit as st

from ui_component.feedback import render_feedback_sidebar


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Set page configuration
st.set_page_config(
    page_title="NBA Stats & Odds",
    page_icon="🏀",
    layout="wide"
)

# Define pages using st.Page
welcome_page = st.Page("welcome_page.py", title="Welcome", icon="👋")
visualizer_page = st.Page(
    "nba_playoff_stats_visualizer/playoff_visualizer_page.py", title="NBA Playoff Visualizer", icon="📊")
nba_odds_page = st.Page("betting_odds/nba_betting_odds_page.py",
                        title="NBA Betting Odds", icon="⛹️‍♂️")

wnba_odds_page = st.Page("betting_odds/wnba_betting_odds_page.py",
                         title="WNBA Betting Odds", icon="⛹️‍♀️")

wnba_player_stats_page = st.Page("wnba_player_stats_visualizer/wnba_player_stats_page.py",
                                 title="WNBA Player Stats", icon="📊") 


# Set up the navigation
nav = st.navigation([welcome_page, nba_odds_page,
                     wnba_odds_page, visualizer_page, wnba_player_stats_page])

# Render the feedback sidebar on all pages
render_feedback_sidebar()

# Run the selected page
nav.run()
