class RiskAnalyzer:

    def __init__(self, bets_df):
        self.bets = bets_df

    def report(self):

        messages = []

        roi = (
            self.bets["profit"].sum()
            / self.bets["stake"].sum()
        ) * 100

        if roi < -30:

            messages.append(
                f"ROI is {roi:.2f}%. Current betting strategy is highly unprofitable."
            )

        average_odds = self.bets["total_odds"].mean()

        if average_odds > 15:

            messages.append(
                "Risk Level: VERY HIGH (average odds exceed 15)."
            )

        return messages