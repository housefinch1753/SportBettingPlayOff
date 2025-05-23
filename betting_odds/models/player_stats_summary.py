from dataclasses import dataclass
from typing import Dict


@dataclass
class PlayerStatsSummary:
    """Player statistics model"""
    player_id: str
    player_name: str
    # e.g., {"points": 25.5, "rebounds": 7.5, "assists": 4.5}
    season_avg_by_stats: Dict[str, float]
    season_median_by_stats: Dict[str, float]
    last_5_avg_by_stats: Dict[str, float]
    last_10_avg_by_stats: Dict[str, float]

    def get_stat_summary(self, stat_type: str, metric_type: str) -> float:
        """
        Get the projection value for a specific stat type

        Args:
            stat_type: The stat type (points, rebounds, assists)
            metric_type: Which metric to use (season_avg, last_5_avg, last_10_avg, season_median)

        Returns:
            The metric value or 0 if not available
        """
        if metric_type == "Season Average":
            return self.season_avg_by_stats.get(stat_type, 0)
        elif metric_type == "Last 5 Games Average":
            return self.last_5_avg_by_stats.get(stat_type, 0)
        elif metric_type == "Last 10 Games Average":
            return self.last_10_avg_by_stats.get(stat_type, 0)
        elif metric_type == "Season Median":
            return self.season_median_by_stats.get(stat_type, 0)
        return 0
