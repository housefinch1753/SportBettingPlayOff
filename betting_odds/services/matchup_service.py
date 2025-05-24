import logging
from typing import List, Dict, Optional
from datetime import datetime

from betting_odds.data_access.odds_repository import OddsRepository
from betting_odds.models.matchup import Matchup
from betting_odds.models.orm_models import PlayerPropORM

logger = logging.getLogger(__name__)


class MatchupService:
    """Service for fetching and processing matchup data"""

    def __init__(self, database):
        """
        Initialize the matchup service

        Args:
            odds_repository: Optional odds repository implementation
        """
        self.odds_repository = OddsRepository(database)

    def get_player_props_for_matchup(self, matchup: Matchup) -> Dict[str, List[PlayerPropORM]]:
        """
        Get all player props for a specific matchup, grouped by player name

        Args:
            matchup: The matchup to get props for

        Returns:
            Dictionary mapping player names to their props
        """
        # Fetch all props for the game
        props = self.odds_repository.get_latest_props_for_game(matchup)

        # Group by player name
        player_props_by_player_name = {}
        for prop in props:
            if prop.player_name not in player_props_by_player_name:
                player_props_by_player_name[prop.player_name] = []
            player_props_by_player_name[prop.player_name].append(prop)

        return player_props_by_player_name

    def get_latest_odds_update_time(self, matchup: Matchup) -> Optional[datetime]:
        """
        Get the latest odds update time for a matchup
        
        Args:
            matchup: The matchup to get the latest update time for
            
        Returns:
            The latest job_start_time_utc or None if no props exist for the matchup
        """
        return self.odds_repository.get_latest_odds_update_time(matchup)

