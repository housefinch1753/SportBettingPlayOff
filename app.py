import streamlit as st

from nba_playoff_stats_visualizer.feedback import render_feedback_sidebar

# Set page configuration
st.set_page_config(
    page_title="NBA Stats & Odds",
    page_icon="🏀",
    layout="wide"
)

# Define pages using st.Page
welcome_page = st.Page(
    "nba_playoff_stats_visualizer/welcome.py", title="Welcome", icon="👋")
visualizer_page = st.Page(
    "nba_playoff_stats_visualizer/visualization.py", title="Playoff Visualizer", icon="📊")
odds_page = st.Page("nba_playoff_stats_visualizer/odds.py",
                    title="Betting Odds", icon="💰")

# Set up the navigation
nav = st.navigation([welcome_page, visualizer_page, odds_page])

# Render the feedback sidebar on all pages
render_feedback_sidebar()

# Run the selected page
nav.run()
