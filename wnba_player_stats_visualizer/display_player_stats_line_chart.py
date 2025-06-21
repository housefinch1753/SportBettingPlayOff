import logging
from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy.stats
import streamlit as st
from nba_api.stats.library.parameters import SeasonTypeAllStar

from betting_odds.data_access.stats_repository import StatsRepository
from database.utils import get_database

# Initialize logger
logger = logging.getLogger(__name__)

# Constants
MIN_MINUTES = 10  # Minimum minutes played to include a game
MIN_GAMES = 10  # Minimum number of games required for analysis

# Initialize database and repository
database = get_database('wnba')
stats_repository = StatsRepository(database)

@st.cache_data(ttl=3600)
def get_cached_player_stats_for_line_chart(player_name: str, season_type: str):
    """Get all player data for line chart"""
    return stats_repository.query_all_player_stats(player_name, season_type)


def display_player_stats(player_name: str, selected_stat: str, seasons: list, season_type: str):
    """Display player statistics and visualization for WNBA players across multiple seasons."""
    # Get all player data (cached)
    all_player_data = get_cached_player_stats_for_line_chart(player_name, season_type)

    if all_player_data.empty:
        st.error(f"No data available for {player_name}.")
        return

    # Filter for selected seasons
    player_stats_df = all_player_data[all_player_data['season'].isin(seasons)]

    if player_stats_df.empty:
        st.error(
            f"No data available for {player_name} in the selected seasons: {', '.join(seasons)}")
        return

    # Filter for games with significant minutes
    filtered_stats = player_stats_df[player_stats_df['minutes'] >= MIN_MINUTES]

    # Sort by date to ensure proper ordering
    filtered_stats = filtered_stats.sort_values('game_date')

    # Determine if games are away based on matchup
    filtered_stats['is_away'] = filtered_stats['matchup'].str.contains('@')

    # Create plotly figure
    fig = go.Figure()

    # Ensure game_date is properly formatted for plotting
    filtered_stats['game_date'] = pd.to_datetime(filtered_stats['game_date'])

    # Convert selected_stat to numeric, handling any non-numeric values
    filtered_stats[selected_stat] = pd.to_numeric(
        filtered_stats[selected_stat], errors='coerce')

    # Remove any rows with NaN values in the selected stat
    filtered_stats = filtered_stats.dropna(subset=[selected_stat])

    if filtered_stats.empty:
        st.warning(f"No valid data available for {selected_stat}")
        return

    # Get unique seasons for legend
    unique_seasons = filtered_stats['season'].unique()

    # Create a continuous timeline by assigning sequential game numbers
    # This removes time gaps between seasons
    game_counter = 1
    filtered_stats['game_number'] = 0
    season_boundaries = {}  # Store the game numbers where seasons change

    for season in sorted(unique_seasons):
        season_mask = filtered_stats['season'] == season
        season_count = filtered_stats[season_mask].shape[0]
        filtered_stats.loc[season_mask, 'game_number'] = range(
            game_counter, game_counter + season_count)
        # Store the start of each season
        season_boundaries[season] = game_counter
        game_counter += season_count

    # Create traces for each season
    for season in unique_seasons:
        season_data = filtered_stats[filtered_stats['season'] == season]

        # Add base line for this season using game numbers instead of dates
        fig.add_trace(go.Scatter(
            x=season_data['game_number'],
            y=season_data[selected_stat],
            mode='lines',
            name=f'{selected_stat} Trend',
            line=dict(color='black', width=1.5),
            hovertemplate=None,
            hoverinfo='skip',
            visible=True,
            # Only show legend for first season
            showlegend=True if season == unique_seasons[0] else False
        ))

        # Add home games scatter for this season
        home_games = season_data[~season_data['is_away']]
        if not home_games.empty:
            fig.add_trace(go.Scatter(
                x=home_games['game_number'],
                y=home_games[selected_stat],
                mode='markers',
                name='Home Games',
                marker=dict(
                    color='blue',
                    symbol='circle',
                    size=8
                ),
                hovertemplate=f'Season: {season}<br>Game: %{{x}}<br>{selected_stat}: %{{y:.1f}}<br>Date: %{{customdata[0]}}<br>Minutes: %{{customdata[1]}}<br>Matchup: %{{customdata[2]}}<extra></extra>',
                customdata=list(zip(home_games['game_date'].dt.strftime(
                    '%Y-%m-%d'), home_games['minutes'].values, home_games['matchup'].values)),
                visible=True,
                # Only show legend for first season
                showlegend=True if season == unique_seasons[0] else False
            ))

        # Add away games scatter for this season
        away_games = season_data[season_data['is_away']]
        if not away_games.empty:
            fig.add_trace(go.Scatter(
                x=away_games['game_number'],
                y=away_games[selected_stat],
                mode='markers',
                name='Away Games',
                marker=dict(
                    color='red',
                    symbol='triangle-up',
                    size=8
                ),
                hovertemplate=f'Season: {season}<br>Game: %{{x}}<br>{selected_stat}: %{{y:.1f}}<br>Date: %{{customdata[0]}}<br>Minutes: %{{customdata[1]}}<br>Matchup: %{{customdata[2]}}<extra></extra>',
                customdata=list(zip(away_games['game_date'].dt.strftime(
                    '%Y-%m-%d'), away_games['minutes'].values, away_games['matchup'].values)),
                visible=True,
                # Only show legend for first season
                showlegend=True if season == unique_seasons[0] else False
            ))

    # Add vertical lines to separate seasons
    for season in sorted(unique_seasons):
        # Position line between seasons
        boundary_x = season_boundaries[season] - 0.5
        fig.add_vline(
            x=boundary_x,
            line_dash="dash",
            line_color="gray",
            line_width=1,
            opacity=0.7,
            annotation_text=f"{season}",
            annotation_position="top",
            annotation=dict(
                font=dict(size=10),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1
            )
        )

    # Update layout
    fig.update_layout(
        title=f"{player_name}'s Game-by-Game {selected_stat} ({', '.join(seasons)}) - Continuous Timeline",
        xaxis_title="Game Number (Sequential across seasons)",
        yaxis_title=selected_stat.title(),
        hovermode="closest",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=40, b=20),
        height=500
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)

    # Display raw data if desired
    if st.checkbox("Show Raw Data"):
        display_df = filtered_stats.copy()
        display_df['Game Type'] = display_df['is_away'].map(
            {True: 'Away', False: 'Home'})
        display_df = display_df[['season', 'game_date',
                                 'Game Type', 'matchup', selected_stat, 'minutes']]
        st.dataframe(display_df)
