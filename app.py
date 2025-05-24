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
    "nba_playoff_stats_visualizer/playoff_visualizer_page.py", title="Playoff Visualizer", icon="📊")
odds_page = st.Page("betting_odds/betting_odds_page.py",
                    title="Betting Odds", icon="💰")

# Set up the navigation
nav = st.navigation([welcome_page, visualizer_page, odds_page])

# Render the feedback sidebar on all pages
render_feedback_sidebar()

# Run the selected page
nav.run()
