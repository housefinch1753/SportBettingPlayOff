import logging

import pandas as pd

from betting_odds.models.orm_models import GameStatsORM, PlayerORM

logger = logging.getLogger(__name__)


class StatsRepository:
    def __init__(self, database):
        self.database = database

    def query_team_for_all_players(self) -> dict[str, str]:
        """
        Query the team for all players in the database
        """
        session = self.database.get_session()
        try:
            player = session.query(PlayerORM).all()
            team_by_player_name = {}
            for player in player:
                team_by_player_name[player.name] = player.team
            return team_by_player_name

        except Exception as e:
            logger.error(f"Error querying team for all players: {str(e)}")
            raise

        finally:
            session.close()

    def query_player_stats(self, player_name: str, season: str, season_type: str) -> pd.DataFrame:
        """
        Query player stats from the database with various filters

        Returns:
        - DataFrame with query results
        """
        session = self.database.get_session()
        try:
            query = session.query(GameStatsORM).join(
                PlayerORM).filter(PlayerORM.name == player_name)

            query = query.filter(GameStatsORM.season == season)

            query = query.filter(GameStatsORM.season_type == season_type)

            # Execute query and get results
            results = query.all()

            # Convert to dictionary and then to DataFrame
            data = []
            for game in results:
                game_dict = {
                    'player_name': player_name,
                    'player_id': game.player_id,
                    'game_id': game.game_id,
                    'game_date': game.game_date,
                    'matchup': game.matchup,
                    'season': game.season,
                    'season_type': game.season_type,
                    'points': game.points,
                    'assists': game.assists,
                    'rebounds': game.rebounds,
                    'three_pointers_made': game.three_pointers_made,
                    'minutes': game.minutes,
                }
                data.append(game_dict)

            return pd.DataFrame(data)

        finally:
            session.close()
