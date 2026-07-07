class StrategyAnalyzer:

    def __init__(self, bets_df):
        self.bets = bets_df

    def report(self):

        messages = []

        winners = self.bets[
            self.bets["profit"] > 0
        ]

        losers = self.bets[
            self.bets["profit"] <= 0
        ]

        if len(winners):

            messages.append(
                f"Winning odds average {winners['total_odds'].mean():.2f}"
            )

        if len(losers):

            messages.append(
                f"Losing odds average {losers['total_odds'].mean():.2f}"
            )

        return messages