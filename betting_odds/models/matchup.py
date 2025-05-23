from dataclasses import dataclass
from datetime import datetime


@dataclass
class Matchup:
    """Matchup model representing a game between two teams"""
    game_id: str
    commence_time_utc: datetime
    derived_game_name: str
    home_team: str
    away_team: str
