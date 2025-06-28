import logging
from typing import Optional, Dict, List, Tuple

import pandas as pd
import streamlit as st
from nba_api.stats.library.parameters import SeasonTypeAllStar

from betting_odds.data_access.events_repository import EventsRepository
from betting_odds.data_access.stats_repository import StatsRepository
from betting_odds.models.matchup import Matchup
from betting_odds.services.value_prop_indicator import ValueIndicator
from betting_odds.models.orm_models import PlayerPropORM
from betting_odds.models.player_stats_summary import PlayerStatsSummary
from betting_odds.services.matchup_service import MatchupService
from betting_odds.services.player_stats_service import PlayerStatsService
from betting_odds.services.prop_organiser import get_best_bookie_odds_for_each_prop_type_for_a_player
from database.utils import get_database
from ui_component.style_utils import load_css

# Configure logging
logger = logging.getLogger(__name__)

# Load CSS styles
load_css()

# Hide the st.markdown anchor icon
st.markdown(
    "<style>[data-testid='stHeaderActionElements'] {display: none;}</style>",
    unsafe_allow_html=True
)

database = get_database('wnba')

# Initialize service
matchup_service = MatchupService(database)
player_stats_service = PlayerStatsService(database)
event_repository = EventsRepository(database)
stats_repository = StatsRepository(database)


def main():
    # Title and description
    st.title("WNBA Player Props Hub - BETA version", anchor=False)

    # New explanation of Value Direction
    with st.expander("ℹ️ **Understanding Value Indicators**", expanded=True):
        st.markdown("""
        <div style="font-size: 18px;">
        <h3 style="font-size: 24px;">📊 How Value Indicators Work</h3>
        
        <p>Value indicators compare the betting line with a player's statistical baseline (average or median) to identify potential value opportunities.</p>
        
        <h4>Value Direction Categories:</h4>
        <ul>
            <li><b>🔥 Strong Positive</b>: Significant edge (10%+ difference)</li>
            <li><b>👍 Positive</b>: Moderate edge (3-10% difference)</li>
            <li><b>🔮 Neutral</b>: Line is close to the player's statistical baseline (±3%)</li>
            <li><b>❌ Negative</b>: Line is unfavorable compared to statistical baseline</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Over Bet Example:")
            stats_baseline = 20
            st.markdown(f"**Player's Baseline**: {stats_baseline} points")

            example_data = [
                {"Line": int(stats_baseline * 0.85), "Direction": "🔥 Strong Positive",
                    "Calculation": f"{stats_baseline} × (1 - 0.1) = {stats_baseline * 0.9} (Line < Threshold)"},
                {"Line": int(stats_baseline * 0.95), "Direction": "👍 Positive",
                    "Calculation": f"{stats_baseline} × (1 - 0.03) = {stats_baseline * 0.97} (Line < Threshold)"},
                {"Line": stats_baseline, "Direction": "🔮 Neutral",
                    "Calculation": f"Line is within ±3% of {stats_baseline}"},
                {"Line": int(stats_baseline * 1.05), "Direction": "❌ Negative",
                    "Calculation": f"{stats_baseline} × (1 + 0.03) = {stats_baseline * 1.03} (Line > Threshold)"}
            ]

            example_df = pd.DataFrame(example_data)
            example_df["Line"] = example_df["Line"].round(1)
            st.table(example_df)

            st.markdown("""
            <div style="font-size: 15px;">
            <p><b>For OVER bets</b>: Lower lines relative to the player's baseline provide better value, 
            as the player has historically performed above that line.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### Under Bet Example:")
            st.markdown(f"**Player's Baseline**: {stats_baseline} points")

            example_data = [
                {"Line": int(stats_baseline * 1.15), "Direction": "🔥 Strong Positive",
                    "Calculation": f"{stats_baseline} × (1 + 0.1) = {stats_baseline * 1.1} (Line > Threshold)"},
                {"Line": int(stats_baseline * 1.05), "Direction": "👍 Positive",
                    "Calculation": f"{stats_baseline} × (1 + 0.03) = {stats_baseline * 1.03} (Line > Threshold)"},
                {"Line": stats_baseline, "Direction": "🔮 Neutral",
                    "Calculation": f"Line is within ±3% of {stats_baseline}"},
                {"Line": int(stats_baseline * 0.95), "Direction": "❌ Negative",
                    "Calculation": f"{stats_baseline} × (1 - 0.03) = {stats_baseline * 0.97} (Line < Threshold)"}
            ]

            example_df = pd.DataFrame(example_data)
            example_df["Line"] = example_df["Line"].round(1)
            st.table(example_df)

            st.markdown("""
            <div style="font-size: 15px;">
            <p><b>For UNDER bets</b>: Higher lines relative to the player's baseline provide better value, 
            as the player has historically performed below that line.</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size: 18px;">
    <h3 style="font-size: 28px;">💰 Matchup-Centric Value Overview</h3>

    <p>Select a matchup to view all participating players with their key prop odds and value indicators. 
    Compare the lines against player averages to identify potential betting opportunities.</p>
    </div>
    """, unsafe_allow_html=True)

    matchup_by_derived_name = get_wnba_future_matchup()

    if not matchup_by_derived_name:
        st.warning("No upcoming matchups available.")
        return

    # Create columns for the selection options
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_matchup_derived_name = st.selectbox(
            "Matchup",
            options=matchup_by_derived_name.keys()
        )
        # Get matchups
        selected_matchup: Matchup = matchup_by_derived_name[selected_matchup_derived_name]

    with col2:
        selected_prop_type = st.selectbox(
            "Prop Type",
            # , "Assists", "Rebounds", "Three Pointers Made"]
            options=["Points", "--- MORE TO COME ---"]
        )

    with col3:
        selected_metric_type = st.selectbox(
            "Metrics Type",
            options=[
                "Last 5 Games Average", "Last 10 Games Average",
                "Season Average", "Season Median"
            ]
        )

    # Main content area - display odds value indicators
    if selected_matchup:
        st.header(
            f"Player Props Overview: {selected_matchup.derived_game_name}")

        # Get game date/time
        game_date_str = selected_matchup.commence_time_utc.strftime(
            "%A, %B %d, %Y, %I:%M %p")
        st.subheader(f"Game Date: {game_date_str} UTC")

        # Get and display odds update information
        latest_odds_time = matchup_service.get_latest_odds_update_time(
            selected_matchup)
        if latest_odds_time:
            odds_time_str = latest_odds_time.strftime(
                "%A, %B %d, %Y, %I:%M %p")
            st.info(
                f"❗ **Odds Last Retrieved:** {odds_time_str} UTC | Odds refresh every 6 hours before the game starts")
        else:
            st.warning("⚠️ No odds data available for this matchup")

        # Fetch player props for the matchup
        player_props_by_name = matchup_service.get_player_props_for_matchup(
            selected_matchup)

        # Get stats for all players for the selected matchup
        list_of_players = list(player_props_by_name.keys())
        stats_summary_by_name = calculate_wnba_summary_stats_for_players(
            list_of_players, '2025', SeasonTypeAllStar.regular)

        # Create tabs for home and away teams
        home_tab, away_tab = st.tabs(
            [f"{selected_matchup.home_team} (Home)", f"{selected_matchup.away_team} (Away)"])

        # Filter players for home team and away team
        # Get team by player name mapping
        team_by_player_name = get_wnba_team_by_player_name()
        home_team_players, away_team_players = filter_player_props_by_team(
            player_props_by_name=player_props_by_name,
            team_by_player_name=team_by_player_name,
            home_team=selected_matchup.home_team,
            away_team=selected_matchup.away_team
        )

        # Home team tab
        with home_tab:
            render_team_props(
                team_name=selected_matchup.home_team,
                team_players=home_team_players,
                selected_prop_type=selected_prop_type,
                selected_metric_type=selected_metric_type,
                stats_summary_by_name=stats_summary_by_name
            )

        # Away team tab
        with away_tab:
            render_team_props(
                team_name=selected_matchup.away_team,
                team_players=away_team_players,
                selected_prop_type=selected_prop_type,
                selected_metric_type=selected_metric_type,
                stats_summary_by_name=stats_summary_by_name
            )

    # Add floating button at the bottom (after all content)
    if st.button("📊 View Player Stats Analysis"):
        st.switch_page(
            "wnba_player_stats_visualizer/wnba_player_stats_page.py")


@st.cache_data(ttl=86400)
def get_wnba_team_by_player_name() -> dict[str, str]:
    """Get team by player name for WNBA."""
    team_by_player_name = player_stats_service.query_all_players_team()
    return team_by_player_name


@st.cache_data(ttl=3600)
def get_wnba_future_matchup() -> Optional[dict[str, Matchup]]:
    """Get list of upcoming WNBA events."""
    matchup_by_derived_name = event_repository.get_future_events()
    return matchup_by_derived_name


@st.cache_resource(ttl=3600)
def calculate_wnba_summary_stats_for_players(list_of_players: list[str], season, season_type) -> dict[str, PlayerStatsSummary]:
    player_stats_by_name = player_stats_service.query_player_stats(
        list_of_players, season, season_type)
    stats_summary_by_name = player_stats_service.summarize_player_stats(
        player_stats_by_name)
    return stats_summary_by_name


def filter_player_props_by_team(
        player_props_by_name: Dict[str, List],
        team_by_player_name: Dict[str, str],
        home_team: str,
        away_team: str
) -> Tuple[Dict[str, List[PlayerPropORM]], Dict[str, List[PlayerPropORM]]]:
    """
    Filter players by team and create separate dictionaries for home and away teams

    Args:
        player_props_by_name: Dictionary mapping player names to their props
        team_by_player_name: Dictionary mapping player names to their team
        home_team: Name of the home team
        away_team: Name of the away team

    Returns:
        Tuple containing (home_team_players, away_team_players) dictionaries
    """
    home_team_players = {}
    away_team_players = {}

    for player_name, props in player_props_by_name.items():
        player_team = team_by_player_name.get(player_name)
        if not player_team:
            st.warning(f"No player team available for {player_name}")
            continue

        if player_team == home_team:
            home_team_players[player_name] = props
        elif player_team == away_team:
            away_team_players[player_name] = props

    return home_team_players, away_team_players


def render_team_props(
        team_name: str,
        team_players: Dict[str, List],
        selected_prop_type: str,
        selected_metric_type: str,
        stats_summary_by_name: Dict[str, PlayerStatsSummary]
) -> None:
    """
    Render player props for a given team

    Args:
        team_name: Name of the team
        team_players: Dictionary mapping player names to their props
        selected_prop_type: Type of prop (points, assists, etc.)
        selected_metric_type: Type of metric (last_5_avg, season_avg, etc.)
        stats_summary_by_name: Dictionary mapping player names to their stats summary
    """
    if not team_players:
        st.info(f"No player props available for {team_name}")
        return

    for player_name, props in team_players.items():
        # Filter props by the selected prop type
        selected_props = [
            prop for prop in props if prop.prop_type.lower() == selected_prop_type.lower()]

        if not selected_props:
            continue

        with st.expander(f"**:blue[{player_name}]**"):
            if player_name not in stats_summary_by_name:
                st.warning(f"No stats available for {player_name}")
                continue

            # Get player stats for the selected prop type
            player_stats = stats_summary_by_name.get(player_name)
            stats_baseline = player_stats.get_stat_summary(
                selected_prop_type.lower(), selected_metric_type)

            st.metric(
                label=f"**{selected_prop_type}, {selected_metric_type}**",
                value=f"{stats_baseline:.1f}"
            )

            # Get best odds for over/under bets
            best_over_odds_by_line, best_under_odds_by_line = get_best_bookie_odds_for_each_prop_type_for_a_player(
                selected_props)

            # Create table data with value indicators
            table_data = []

            # Add over bets with value indicators
            for line, best_odds in best_over_odds_by_line.items():
                value_indicator = ValueIndicator(
                    prop_type=selected_prop_type.lower(),
                    line=line,
                    over_under_bet="over",
                    stats_baseline=stats_baseline,
                    threshold=0.1  # 10% threshold for value indication
                )

                # Get the emoji indicator
                emoji = value_indicator.emoji_indicator
                direction = value_indicator.value_direction
                direction_display = direction.capitalize() if direction else "Neutral"
                value_hint = f"{emoji} {direction_display}"

                # Define value priority for sorting (Strong positive -> Positive -> Neutral -> Negative)
                value_priority = {
                    "strong positive": 1,
                    "positive": 2,
                    "neutral": 3,
                    "negative": 4
                }

                # Add numerical sort value for proper sorting
                sort_value = value_priority.get(
                    direction, 5)  # Default to 5 if not found

                # Add row to table
                table_data.append({
                    "Line": line,
                    "Over/Under": "Over",
                    "Best Bookie": best_odds.bookie,
                    "Best Odds": best_odds.best_odds,
                    "Value Indicator": value_hint,
                    "value_sort": sort_value
                })

            # Add under bets with value indicators
            for line, best_odds in best_under_odds_by_line.items():
                value_indicator = ValueIndicator(
                    prop_type=selected_prop_type.lower(),
                    line=line,
                    over_under_bet="under",
                    stats_baseline=stats_baseline,
                    threshold=0.1  # 10% threshold for value indication
                )

                # Get the emoji indicator
                emoji = value_indicator.emoji_indicator
                direction = value_indicator.value_direction
                direction_display = direction.capitalize() if direction else "Neutral"
                value_hint = f"{emoji} {direction_display}"

                # Add numerical sort value for proper sorting
                sort_value = value_priority.get(
                    direction, 5)  # Default to 5 if not found

                # Add row to table
                table_data.append({
                    "Line": line,
                    "Over/Under": "Under",
                    "Best Bookie": best_odds.bookie,
                    "Best Odds": best_odds.best_odds,
                    "Value Indicator": value_hint,
                    "value_sort": sort_value
                })

            if table_data:
                # Convert data to DataFrame
                df = pd.DataFrame(table_data)

                # Sort the dataframe by value priority (Strong positive first)
                df = df.sort_values(by="value_sort")

                # Drop the value_sort column before displaying
                df = df.drop(columns=["value_sort"])

                # Display information about sorting
                st.info("Click on column headers to sort")

                # Add row IDs for tracking
                df['ID'] = [f"{player_name}_{i}" for i in range(len(df))]

                # Initialize session state for notes if not exists
                if 'bet_notes' not in st.session_state:
                    st.session_state.bet_notes = {}

                # Add Notes column with existing values from session state
                df['Notes'] = df['ID'].apply(
                    lambda x: st.session_state.bet_notes.get(x, ""))

                # Make a copy for display
                display_df = df.copy()

                # Remove ID column from display but keep it in the original dataframe
                display_df = display_df.drop(columns=['ID'])

                # Use st.data_editor for an editable table
                edited_df = st.data_editor(
                    display_df,
                    column_config={
                        "Line": st.column_config.NumberColumn("Line", format="%.1f"),
                        "Over/Under": st.column_config.TextColumn("Over/Under"),
                        "Best Bookie": st.column_config.TextColumn("Best Bookie"),
                        "Best Odds": st.column_config.NumberColumn("Best Odds", format="%.2f"),
                        "Value Indicator": st.column_config.TextColumn("Value Indicator"),
                        "Notes": st.column_config.TextColumn("(Upcoming Feature) Your Notes", width="medium"),
                    },
                    hide_index=True,
                    use_container_width=True,
                    num_rows="fixed",
                    disabled=["Line", "Over/Under",
                              "Best Bookie", "Best Odds", "Value Indicator", "Notes"]
                )

                # Add ID column back to edited dataframe for reference when saving notes
                edited_df['ID'] = df['ID']

                # Save any notes the user entered
                for idx, row in edited_df.iterrows():
                    bet_id = row['ID']
                    note = row['Notes']
                    if note:  # Only save non-empty notes
                        st.session_state.bet_notes[bet_id] = note
                    elif bet_id in st.session_state.bet_notes:
                        # Remove empty notes to save space
                        st.session_state.bet_notes.pop(bet_id)
            else:
                st.info(f"No {selected_prop_type} props available")


# Run the main function
if __name__ == "__main__":
    main()
