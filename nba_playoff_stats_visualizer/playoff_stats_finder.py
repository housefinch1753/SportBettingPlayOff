import logging
from dataclasses import dataclass
from typing import Dict, List

from nba_api.live.nba.endpoints import BoxScore
from nba_api.stats.endpoints import LeagueGameFinder
from nba_api.stats.library.parameters import SeasonTypeAllStar, SeasonType, SeasonTypePlayoffs

logger = logging.getLogger(__name__)


TEAM_IDS_BY_TEAM_ABBRV = {
    'ATL': '1610612737',
    'BKN': '1610612751',
    'BOS': '1610612738',
    'CHA': '1610612766',
    'CHI': '1610612741',
    'CLE': '1610612739',
    'DAL': '1610612742',
    'DEN': '1610612743',
    'DET': '1610612765',
    'GSW': '1610612744',
    'HOU': '1610612745',
    'IND': '1610612754',
    'LAC': '1610612746',
    'LAL': '1610612747',
    'MEM': '1610612763',
    'MIA': '1610612748',
    'MIL': '1610612749',
    'MIN': '1610612750',
    'NOP': '1610612740',
    'NYK': '1610612752',
    'OKC': '1610612760',
    'ORL': '1610612753',
    'PHI': '1610612755',
    'PHX': '1610612756',
    'POR': '1610612757',
    'SAC': '1610612758',
    'SAS': '1610612759',
    'TOR': '1610612761',
    'UTA': '1610612762',
    'WAS': '1610612764',
}


@dataclass
class PlayerGameStats:
    """
    Represents a player's key statistics for a single game.

    Attributes:
        game_date (str): Date of the game
        matchup (str): Game matchup (e.g., "GSW vs. LAL")
        points (int): Points scored
        rebounds (int): Total rebounds
        assists (int): Total assists
        minutes (str): Minutes played
        threes_made (int): 3-point field goals made
    """
    game_date: str
    matchup: str
    points: int
    rebounds: int
    assists: int
    minutes: str
    threes_made: int


class TeamGameFinder:
    """
    A class to fetch game statistics for all players from a team against a specific opponent.
    Makes direct API calls without caching.
    """

    @staticmethod
    def get_team_games(team_abbreviation: str, season: str) -> Dict[str, List[PlayerGameStats]]:
        """
        Retrieves game statistics for all players from a team against a specific opponent.

        Args:
            team_abbreviation (str): NBA API team ID
            season (str): Season in format "YYYY-YY" (e.g., "2022-23")

        Returns:
            Dict[str, List[PlayerGameStats]]: Dictionary mapping player names to their game stats

        Raises:
            Exception: If there's an error fetching the statistics
        """
        try:

            team_id = TEAM_IDS_BY_TEAM_ABBRV[team_abbreviation]
            # Find games between the two teams
            game_finder = LeagueGameFinder(
                team_id_nullable=team_id,
                season_nullable=season,
                season_type_nullable=SeasonTypePlayoffs.playoffs
            )

            games_dict = game_finder.get_dict()

            if not games_dict.get('resultSets', []):
                logger.info(
                    f"No games found for team {team_abbreviation} in season {season}")
                return {}

            # Get game IDs and dates
            games = {}
            for row in games_dict['resultSets'][0]['rowSet']:
                game_id = row[games_dict['resultSets']
                              [0]['headers'].index('GAME_ID')]
                game_date = row[games_dict['resultSets']
                                [0]['headers'].index('GAME_DATE')]
                matchup = row[games_dict['resultSets']
                              [0]['headers'].index('MATCHUP')]
                games[game_id] = {'date': game_date, 'matchup': matchup}

            # Get player stats for each game
            player_stats: Dict[str, List[PlayerGameStats]] = {}

            for game_id, game_info in games.items():
                box_score = BoxScore(game_id=game_id)
                game_data = box_score.get_dict()

                # Determine which team we're looking for
                home_team_id = game_data['game']['homeTeam']['teamId']
                target_team_data = (game_data['game']['homeTeam']
                                    if str(home_team_id) == team_id
                                    else game_data['game']['awayTeam'])

                # Process each player's stats
                for player in target_team_data['players']:
                    player_name = player['name']
                    stats = player['statistics']

                    game_stat = PlayerGameStats(
                        game_date=game_info['date'],
                        matchup=game_info['matchup'],
                        points=int(
                            stats['points']) if stats['points'] is not None else 0,
                        rebounds=int(
                            stats['reboundsTotal']) if stats['reboundsTotal'] is not None else 0,
                        assists=int(
                            stats['assists']) if stats['assists'] is not None else 0,
                        minutes=str(
                            stats['minutes']) if stats['minutes'] is not None else '0',
                        threes_made=int(
                            stats['threePointersMade']) if stats.get('threePointersMade') is not None else 0
                    )

                    if player_name in player_stats:
                        player_stats[player_name].append(game_stat)
                    else:
                        player_stats[player_name] = [game_stat]

            return player_stats

        except Exception as e:
            logger.error(f"Error fetching team stats: {str(e)}")
            raise


if __name__ == "__main__":
    # Example: Get Denver Nuggets vs Miami Heat playoff games (2022-23 season)
    # Denver Nuggets ID: 1610612743
    # Miami Heat ID: 1610612748
    finder = TeamGameFinder()
    try:
        stats = finder.get_team_games('DEN', "2024-25")
        print(f"Found stats for {len(stats)} players")
    except Exception as e:
        print(f"Error: {str(e)}")
