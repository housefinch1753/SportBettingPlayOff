from dataclasses import dataclass
from typing import Optional


@dataclass
class ValueIndicator:
    """Model for value indicators on player props"""
    prop_type: str  # points, rebounds, assists
    line: float
    over_under_bet: str  # "over" or "under"
    stats_baseline: float
    # Threshold for indicating strong value (percentage or fixed)
    threshold: float
    # Lower threshold for indicating positive value (default 3%)
    lower_threshold: float = 0.03

    @property
    def value_direction(self) -> Optional[str]:
        """
        Determine if the bet has positive or negative value compared to historical stats

        OVER BET VISUALIZATION (Baseline = B):

        Strong Positive  |     Positive    |    Neutral     |     Negative
        <----------------|-----------------|----------------|------------------>
                      0.90B             0.97B               B               1.03B
              baseline*(1-threshold)  baseline*(1-lower_threshold)    baseline*(1+lower_threshold)

        Line positions and resulting classifications:
             L1                  L2                  L3                     L4
             |                   |                   |                      |
        <----|-------------------|-------------------|----------------------|----->
         Strong Positive       Positive            Neutral              Negative
             (🔥)                (👍)                (🔮)                 (❌)


        UNDER BET VISUALIZATION (Baseline = B):

        Negative         |     Neutral     |    Positive   |  Strong Positive
        <----------------|-----------------|---------------|------------------>
                      0.97B                B              1.03B             1.10B
             baseline*(1-lower_threshold)           baseline*(1+lower_threshold)  baseline*(1+threshold)

        Line positions and resulting classifications:
            L1                                                   L4
             |                    L2      L3                     |
             |                    |         |                    |
        <----|--------------------|---------|--------------------|--------->
          Negative              Neutral  Positive         Strong Positive
           (❌)                  (🔮)      (👍)               (🔥)

        Returns:
            "strong positive", "positive", "neutral", or "negative"
        """
        if self.over_under_bet == "over":
            if self.line < self.stats_baseline * (1 - self.threshold):
                return "strong positive"  # Line significantly below baseline
            elif self.line < self.stats_baseline * (1 - self.lower_threshold):
                return "positive"  # Line moderately below baseline
            elif self.line <= self.stats_baseline * (1 + self.lower_threshold):
                return "neutral"  # Line close to baseline
            else:
                return "negative"  # Line above baseline + lower threshold

        elif self.over_under_bet == "under":
            if self.line > self.stats_baseline * (1 + self.threshold):
                return "strong positive"  # Line significantly above baseline
            elif self.line > self.stats_baseline * (1 + self.lower_threshold):
                return "positive"  # Line moderately above baseline
            elif self.line >= self.stats_baseline * (1 - self.lower_threshold):
                return "neutral"  # Line close to baseline
            else:
                return "negative"  # Line below baseline - lower threshold

        return "neutral"

    @property
    def emoji_indicator(self) -> str:
        """
        Returns an emoji indicating value direction

        Returns:
            Emoji string
        """
        direction = self.value_direction
        if direction == "strong positive":
            return "🔥"  # Fire for strong positive value
        elif direction == "positive":
            return "👍"  # Thumbs up for positive value
        elif direction == "negative":
            return "❌"  # Red cross for negative value
        return "🔮"  # Crystal ball for neutral/uncertain value
