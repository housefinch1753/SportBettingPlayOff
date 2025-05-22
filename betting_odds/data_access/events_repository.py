import logging
from datetime import datetime, timezone

from betting_odds.models.matchup import Matchup
from betting_odds.models.orm_models import EventORM

logger = logging.getLogger(__name__)


class EventsRepository:
    """SQLAlchemy ORM implementation of the events repository."""

    def __init__(self, database):
        self.database = database

    def get_future_events(self) -> dict[str, Matchup]:
        session = self.database.get_session()
        current_time_utc = datetime.now(timezone.utc)
        try:
            logger.info("Fetching future events from the database")
            # Fetch all events that are in the future
            future_events = session.query(EventORM).filter(
                EventORM.commence_time_utc > current_time_utc).all()

            matchup_by_derived_name = {}
            for event in future_events:
                matchup_by_derived_name[event.derived_game_name] = Matchup(game_id=event.id,
                                                                           derived_game_name=event.derived_game_name,
                                                                           commence_time_utc=event.commence_time_utc,
                                                                           home_team=event.home_team,
                                                                           away_team=event.away_team
                                                                           )
            logger.info(f"Fetched {len(future_events)} future events")
            return matchup_by_derived_name

        except Exception as e:
            logger.error(f"Error fetching future events: {e}")
            raise

        finally:
            session.close()
