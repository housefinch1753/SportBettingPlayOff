from datetime import datetime

import streamlit as st
from nba_api.stats.library.parameters import SeasonTypeAllStar

from betting_odds.data_access.stats_repository import StatsRepository
from database.utils import get_database
from ui_component.style_utils import load_css
from wnba_player_stats_visualizer.display_significant_test import display_significant_test

# Load CSS styles
load_css()

# Initialize database and repository
database = get_database('wnba')
stats_repository = StatsRepository(database)


# Cache the player names to avoid repeated database queries
@st.cache_data(ttl=3600 * 24)  # Cache for 24 hour
def get_player_names():
    """Get list of all player names from the database."""
    team_by_player_name = stats_repository.query_team_for_all_players()
    return sorted(list(team_by_player_name.keys()))


# Set page title and description
st.title("WNBA Player Props Analysis")
st.markdown("""
This page provides analysis and insights for WNBA player props, helping you make more informed betting decisions.
""")

# Main content area
st.header("Player Performance Analysis")

# Add Home/Away Analysis section
st.subheader("Home/Away Performance Analysis")

# Generate season options from 2020 to current year
current_year = datetime.now().year
season_options = [str(year) for year in range(2020, current_year + 1)]
season_options.reverse()  # Show most recent years first
selected_season = st.selectbox("Select season", season_options)

season_type_options = {
    "Regular Season": SeasonTypeAllStar.regular,
    "Playoffs": SeasonTypeAllStar.playoffs
}
selected_season_type = st.selectbox(
    "Select season type", list(season_type_options.keys()))

stat_options = ["points", "rebounds", "assists", "three_pointers_made"]
selected_stat = st.selectbox("Select stat to analyze", stat_options)

# Get list of player names for autocomplete
player_names = get_player_names()
player_name = st.selectbox(
    "Select player",
    options=player_names,
    index=0
)

if player_name and selected_stat:
    display_significant_test(
        player_name=player_name,
        stat_name=selected_stat,
        season=selected_season,
        season_type=season_type_options[selected_season_type]
    )

# Add floating button at the bottom
if st.button("← Back to WNBA Betting Odds"):
    st.switch_page("betting_odds/wnba_betting_odds_page.py")
