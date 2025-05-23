import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import func

from betting_odds.models.matchup import Matchup
from betting_odds.models.orm_models import PlayerPropORM

logger = logging.getLogger(__name__)


class OddsRepository:
    """SQLAlchemy ORM implementation of the odds repository."""

    def __init__(self, database):
        self.database = database

    def get_latest_props_for_game(self, game: Matchup) -> list[PlayerPropORM]:
        """
        Args:
            game: a game to get latest props for

        Returns:
            List of the latest props for all players in the game
        """
        session = self.database.get_session()

        try:
            results: list[PlayerPropORM] = (
                session.query(PlayerPropORM)
                .filter(
                    PlayerPropORM.game_id == game.game_id,
                    PlayerPropORM.job_start_time_utc == session.query(
                        func.max(PlayerPropORM.job_start_time_utc))
                    .filter(PlayerPropORM.game_id == game.game_id)
                    .scalar_subquery()
                )
                .all())

            return results

        except Exception as e:
            logger.error(
                f"Error getting latest props update time for {game.derived_game_name}: {e}")
            raise

        finally:
            session.close()

    def get_latest_odds_update_time(self, game: Matchup) -> Optional[datetime]:
        """
        Get the latest job_start_time_utc for a given game to show when odds were last retrieved
        
        Args:
            game: a game to get the latest update time for
            
        Returns:
            The latest job_start_time_utc or None if no props exist for the game
        """
        session = self.database.get_session()
        
        try:
            latest_time = (
                session.query(func.max(PlayerPropORM.job_start_time_utc))
                .filter(PlayerPropORM.game_id == game.game_id)
                .scalar()
            )
            
            return latest_time
            
        except Exception as e:
            logger.error(
                f"Error getting latest odds update time for {game.derived_game_name}: {e}")
            return None
            
        finally:
            session.close()
