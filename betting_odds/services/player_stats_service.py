import logging
from typing import Dict, Optional

import pandas as pd

from betting_odds.data_access.stats_repository import StatsRepository
from betting_odds.models.player_stats_summary import PlayerStatsSummary

logger = logging.getLogger(__name__)


class PlayerStatsService:
    """Service for querying and summarizing player statistics"""

    def __init__(self, database):
        """
        Initialize the player stats service
        Args:
            database: Database instance for data access
        """
        self.stats_repository = StatsRepository(database)

    def query_all_players_team(self) -> dict[str, str]:
        """
        Query the team for all players in the database
        Returns:
            Dictionary mapping player names to their teams
        """
        logger.info("Querying all player teams")
        try:
            team_by_player_name = self.stats_repository.query_team_for_all_players()
            return team_by_player_name

        except Exception as e:
            logger.error(f"Error querying player teams: {str(e)}")
            return {}


    def query_player_stats(self, player_names: list, season: str,
                           season_type: str, date_from: Optional[str] = None,
                           date_to: Optional[str] = None) -> Dict[str, pd.DataFrame]:
        """
        Query stats for multiple players and return as dictionary of dataframes

        Args:
            player_names: List of player names to query
            season: Season identifier (e.g., "2024-2025")
            season_type: Type of season ("regular", "playoffs")
            date_from: Optional start date for filtering
            date_to: Optional end date for filtering

        Returns:
            Dictionary with player names as keys and their stats dataframes as values
        """
        logger.info(f"Querying all player stats for season: {season} and type: {season_type}")
        player_stats_by_name = {}

        for player_name in player_names:
            try:
                stats_df = self.stats_repository.query_player_stats(
                    player_name=player_name,
                    season=season,
                    season_type=season_type
                )
                player_stats_by_name[player_name] = stats_df
            except Exception as e:
                logger.error(
                    f"Error querying stats for {player_name}: {str(e)}")
                # Empty dataframe if error
                player_stats_by_name[player_name] = pd.DataFrame()

        return player_stats_by_name

    def summarize_player_stats(self, player_stats_by_name: Dict[str, pd.DataFrame]) -> Dict[str, PlayerStatsSummary]:
        """
        Summarize player stats into PlayerStatsSummary objects

        Args:
            player_stats_by_name: Dictionary of player names to stats dataframes

        Returns:
            Dictionary with player names as keys and PlayerStatsSummary objects as values
        """
        player_summaries = {}

        for player_name, stats_df in player_stats_by_name.items():
            if stats_df.empty:
                continue

            # Get basic info
            try:

                player_id = stats_df.iloc[0]['player_id']

                stat_types = ['points', 'rebounds', 'assists', 'three_pointers_made']

                # Calculate season averages
                season_avg_by_stats = {}
                season_median_by_stats = {}

                # Sort by date to get recent games


                stats_df = stats_df.sort_values('game_date', ascending=False)

                for stat in stat_types:
                    season_avg_by_stats[stat] = round(float(stats_df[stat].mean()), 2)
                    season_median_by_stats[stat] = round(float(stats_df[stat].median()), 2)

                # Calculate recent game averages (last 5 and last 10)
                last_5_avg_by_stats = {}
                last_10_avg_by_stats = {}

                for stat in stat_types:
                    # Handle cases where there aren't 5 or 10 games
                    games_count = len(stats_df)

                    if games_count >= 5:
                        last_5_avg_by_stats[stat] = round(float(
                            stats_df.iloc[:5][stat].mean()), 2)
                    else:
                        last_5_avg_by_stats[stat] = season_avg_by_stats[stat]

                    if games_count >= 10:
                        last_10_avg_by_stats[stat] = round(float(
                            stats_df.iloc[:10][stat].mean()),2)
                    else:
                        last_10_avg_by_stats[stat] = season_avg_by_stats[stat]

                # Create the PlayerStatsSummary
                summary = PlayerStatsSummary(
                    player_id=player_id,
                    player_name=player_name,
                    season_avg_by_stats=season_avg_by_stats,
                    season_median_by_stats=season_median_by_stats,
                    last_5_avg_by_stats=last_5_avg_by_stats,
                    last_10_avg_by_stats=last_10_avg_by_stats
                )

                player_summaries[player_name] = summary

            except Exception as e:
                logger.error(
                    f"Error summarizing stats for {player_name}: {str(e)}")

        return player_summaries
