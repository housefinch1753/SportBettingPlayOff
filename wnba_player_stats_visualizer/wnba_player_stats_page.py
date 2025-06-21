from datetime import datetime

import streamlit as st
from nba_api.stats.library.parameters import SeasonTypeAllStar

from betting_odds.data_access.stats_repository import StatsRepository
from database.utils import get_database
from ui_component.style_utils import load_css
from wnba_player_stats_visualizer.display_significant_test import display_significant_test
from wnba_player_stats_visualizer.display_player_stats_line_chart import display_player_stats

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

# Add Home/Away Analysis section
st.subheader("Home/Away Performance Analysis")

# Generate season options from 2020 to current year
current_year = datetime.now().year
season_options = [str(year) for year in range(2020, current_year + 1)]
season_options.reverse()  # Show most recent years first

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
    # Initialize session state for selection management
    if 'all_selected' not in st.session_state:
        st.session_state.all_selected = True
    if 'individual_seasons' not in st.session_state:
        # latest 3 seasons
        st.session_state.individual_seasons = season_options[:3]

    # Handle "All" selection with callback
    def toggle_all_selection():
        if st.session_state.all_selected:
            st.session_state.individual_seasons = []
        else:
            # Restore default selection when unchecking "All"
            st.session_state.individual_seasons = season_options[:3]
    # Create the checkbox with callback
    all_selected = st.checkbox(
        "Select All Seasons",
        key="all_selected",
        on_change=toggle_all_selection
    )

    # Handle individual season selection (only enabled when "All" is not selected)
    if not st.session_state.all_selected:
        selected_seasons = st.multiselect(
            "Select individual seasons",
            options=season_options,
            key="individual_seasons"
        )
    else:
        # When "All" is selected, show disabled multiselect
        st.multiselect(
            "Select individual seasons (disabled when 'All' is selected)",
            options=season_options,
            disabled=True,
            key="disabled_seasons"
        )
        selected_seasons = season_options

    # Show Game-by-Game Trends second (using all selected seasons)
    st.subheader("📈 Game-by-Game Performance Trends")
    if selected_seasons:
        display_player_stats(
            player_name=player_name,
            selected_stat=selected_stat,
            seasons=selected_seasons,  # Pass all selected seasons
            season_type=season_type_options[selected_season_type]
        )

    # Single season selection for significant test
    selected_season = st.selectbox(
        "Select season for Home/Away Analysis", season_options)

    # Show Home/Away Analysis first (using single selected season)
    st.subheader("📊 Home/Away Performance Analysis")
    display_significant_test(
        player_name=player_name,
        stat_name=selected_stat,
        season=selected_season,  # Use single selected season for home/away analysis
        season_type=season_type_options[selected_season_type]
    )


# Add floating button at the bottom
if st.button("← Back to WNBA Betting Odds"):
    st.switch_page("betting_odds/wnba_betting_odds_page.py")
