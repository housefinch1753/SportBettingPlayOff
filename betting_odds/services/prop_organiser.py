import logging
from dataclasses import dataclass
from typing import List, Dict

from betting_odds.models.orm_models import PlayerPropORM

logger = logging.getLogger(__name__)


@dataclass
class BestBookieOdds:
    """
    Represents the best odds for a specific prop type from different bookmakers

    Attributes:
        prop_type (str): The type of prop (e.g., points, rebounds)
        best_odds (Dict[str, float]): Dictionary mapping bookmaker names to their best odds
    """
    bookie: str
    best_odds: float


def get_best_bookie_odds_for_each_prop_type_for_a_player(selected_props_type: List[PlayerPropORM]) -> tuple[Dict[float, BestBookieOdds], Dict[float, BestBookieOdds]]:
    """
    Get the best odds for each prop type for each player

    Args:
        selected_props_type_by_player_name: Dictionary mapping player names to their props

    Returns:
        Dictionary mapping player names to their best odds
    """
    line_to_over_odds: dict[float, list[PlayerPropORM]] = {}
    line_to_under_odds: dict[float, list[PlayerPropORM]] = {}

    for prop in selected_props_type:
        if prop.over_odds:
            if prop.line not in line_to_over_odds:
                line_to_over_odds[prop.line] = []
            line_to_over_odds[prop.line].append(prop)
        if prop.under_odds:
            if prop.line not in line_to_under_odds:
                line_to_under_odds[prop.line] = []
            line_to_under_odds[prop.line].append(prop)

    best_over_odds_by_line = {}
    for line, props in line_to_over_odds.items():
        # Find the best over odds for each line
        best_over_odds = 0
        best_over_odds_object = None
        for prop in props:
            if prop.over_odds and prop.over_odds > best_over_odds:
                best_over_odds = prop.over_odds
                best_over_odds_object = prop
        if best_over_odds_object:
            best_over_odds_by_line[line] = BestBookieOdds(
                bookie=best_over_odds_object.bookmaker,
                best_odds=best_over_odds
            )

    best_under_odds_by_line = {}
    for line, props in line_to_under_odds.items():
        # Find the best under odds for each line
        best_under_odds = 0
        best_under_odds_object = None
        for prop in props:
            if prop.under_odds and prop.under_odds > best_under_odds:
                best_under_odds = prop.under_odds
                best_under_odds_object = prop
        if best_under_odds_object:
            best_under_odds_by_line[line] = BestBookieOdds(
                bookie=best_under_odds_object.bookmaker,
                best_odds=best_under_odds
            )

    return (best_over_odds_by_line, best_under_odds_by_line)
