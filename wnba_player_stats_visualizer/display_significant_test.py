import numpy as np
import plotly.graph_objects as go
import streamlit as st
from nba_api.stats.library.parameters import SeasonTypeAllStar
from scipy import stats

from betting_odds.data_access.stats_repository import StatsRepository
from database.utils import get_database

# Constants
MIN_MINUTES = 10  # Minimum minutes played to include a game
MIN_GAMES = 10  # Minimum number of games required for analysis

database = get_database('wnba')
stats_repository = StatsRepository(database)


def _analyze_player_home_away(player_name: str, stat_name: str, season: str = "2024", season_type: str = SeasonTypeAllStar.regular) -> dict:
    """
    Analyze home/away performance for a player in a specific stat.

    Args:
        player_id: The player's ID
        stat_name: The stat to analyze (points, assists, rebounds, three_pointers_made)
        season: The season to analyze (default: "2024")
        season_type: The type of season (default: regular season)

    Returns:
        Tuple containing:
        - Dictionary with analysis results
        - Boolean indicating if analysis was successful
    """
    # Get player stats
    player_stats_df = stats_repository.query_player_stats(
        player_name=player_name,
        season=season,
        season_type=season_type
    )

    if player_stats_df.empty:
        return {}

    # Filter games by minutes played
    filtered_stats = player_stats_df[player_stats_df['minutes'] >= MIN_MINUTES]

    if len(filtered_stats) < MIN_GAMES:
        return {}

    filtered_stats['is_away'] = filtered_stats['matchup'].str.contains('@')

    home_stats = filtered_stats[~filtered_stats['is_away']][stat_name].values
    away_stats = filtered_stats[filtered_stats['is_away']][stat_name].values

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(home_stats, away_stats)

    # Calculate basic statistics
    home_mean = home_stats.mean()
    away_mean = away_stats.mean()
    home_std = home_stats.std()
    away_std = away_stats.std()

    result = {
        'home_games': len(home_stats),
        'away_games': len(away_stats),
        'home_mean': home_mean,
        'away_mean': away_mean,
        'home_std': home_std,
        'away_std': away_std,
        't_statistic': t_stat,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'better_at': 'home' if home_mean > away_mean else 'away',
        'difference': abs(home_mean - away_mean)
    }

    return result


def display_significant_test(player_name: str, stat_name: str, season: str, season_type: str):
    """
    Display the significant test results in a user-friendly way using Streamlit.

    Args:
        player_name: The player's name
        stat_name: The stat to analyze
        season: The season to analyze
        season_type: The type of season
    """

    result = _analyze_player_home_away(
        player_name, stat_name, season, season_type)

    if not result:
        st.warning(
            f"Not have enough valid games to analyze {player_name}'s {stat_name} home/away splits.")
        return

    # Create a container for the results
    with st.container():
        st.subheader(f"{player_name}'s {stat_name.title()} Home/Away Analysis")

        # Display significance
        if result['significant']:
            st.success(
                f"Statistically significant difference found! (p-value: {result['p_value']:.4f})")
        else:
            st.info(
                f"No statistically significant difference found (p-value: {result['p_value']:.4f})")

        # Get the raw data for distribution plot
        player_stats_df = stats_repository.query_player_stats(
            player_name=player_name,
            season=season,
            season_type=season_type
        )
        filtered_stats = player_stats_df[player_stats_df['minutes']
                                         >= MIN_MINUTES]
        filtered_stats['is_away'] = filtered_stats['matchup'].str.contains('@')
        home_stats = filtered_stats[~filtered_stats['is_away']
        ][stat_name].values
        away_stats = filtered_stats[filtered_stats['is_away']
        ][stat_name].values

        # Calculate the area under the curve for probability
        def calculate_probability(kde, x_min, x_max):
            # Integrate the KDE over the specified range
            x = np.linspace(x_min, x_max, 1000)
            y = kde(x)
            return np.trapezoid(y, x)

        # Create distribution comparison plot
        fig_dist = go.Figure()

        # Add kernel density estimation plots
        home_kde = stats.gaussian_kde(home_stats)
        away_kde = stats.gaussian_kde(away_stats)
        x_range = np.linspace(
            min(min(home_stats), min(away_stats)),
            max(max(home_stats), max(away_stats)),
            100
        )

        fig_dist.add_trace(go.Scatter(
            x=x_range,
            y=home_kde(x_range),
            name='Home Games',
            fill='tozeroy',
            line=dict(color='blue', width=2)
        ))

        fig_dist.add_trace(go.Scatter(
            x=x_range,
            y=away_kde(x_range),
            name='Away Games',
            fill='tozeroy',
            line=dict(color='red', width=2)
        ))

        # Add vertical lines for means
        fig_dist.add_vline(
            x=result['home_mean'],
            line_dash="dash",
            line_color="blue",
            annotation_text=f"Home Mean: {result['home_mean']:.1f}"
        )
        fig_dist.add_vline(
            x=result['away_mean'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Away Mean: {result['away_mean']:.1f}"
        )

        # Update layout
        fig_dist.update_layout(
            title=f"Distribution of {stat_name}: Home vs Away Games",
            xaxis_title=stat_name,
            yaxis_title="Density",
            showlegend=True,
            height=400
        )

        # Show the distribution plot
        st.plotly_chart(fig_dist, use_container_width=True)

        # Add range selection inputs
        max_value = int(max(max(home_stats), max(away_stats)))
        st.subheader("Select Range for Probability Analysis")

        col1, col2 = st.columns(2)
        with col1:
            under_value = st.text_input(
                "Under (or equal to)", placeholder="Enter value")
        with col2:
            over_value = st.text_input(
                "Over (or equal to)", placeholder="Enter value")

        # Process the inputs and calculate probabilities
        if under_value and over_value:
            st.warning("Please enter only one value (either under or over)")
            range_min, range_max = 0, max_value
        elif under_value:
            try:
                under = float(under_value)
                range_min, range_max = 0, under
            except ValueError:
                st.error("Please enter a valid number")
                range_min, range_max = 0, max_value
        elif over_value:
            try:
                over = float(over_value)
                range_min, range_max = over, max_value
            except ValueError:
                st.error("Please enter a valid number")
                range_min, range_max = 0, max_value
        else:
            range_min, range_max = 100, 100

        # Calculate probabilities for the selected range
        home_prob = calculate_probability(home_kde, range_min, range_max)
        away_prob = calculate_probability(away_kde, range_min, range_max)

        # Calculate overall probability (weighted by number of games)
        total_games = result['home_games'] + result['away_games']
        overall_prob = (
                               home_prob * result['home_games'] + away_prob * result['away_games']) / total_games

        # Display probabilities
        if under_value:
            st.markdown(f"""
            **Probability Analysis for {stat_name} under {under_value}:**
            """)

        elif over_value:
            st.markdown(f"""
            **Probability Analysis for {stat_name} over {over_value}:**
            """)
        a, b, c = st.columns(3)
        a.metric("Home Games", f"{home_prob:.1%}", border=True)
        b.metric("Away Games", f"{away_prob:.1%}", border=True)
        c.metric("Overall", f"{overall_prob:.1%}", border=True)
        # Display statistical metrics in columns
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Home Games Stats", "")
            st.metric("Games", result['home_games'])
            st.metric("Mean", f"{result['home_mean']:.1f}")
            st.metric("Std Dev", f"{result['home_std']:.1f}")

        with col2:
            st.metric("Away Games Stats", "")
            st.metric("Games", result['away_games'])
            st.metric("Mean", f"{result['away_mean']:.1f}")
            st.metric("Std Dev", f"{result['away_std']:.1f}")
