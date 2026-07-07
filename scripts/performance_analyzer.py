class PerformanceAnalyzer:

    def __init__(self, bets_df):
        self.bets = bets_df

    def report(self):

        messages = []

        best = self.bets.loc[
            self.bets["profit"].idxmax()
        ]

        worst = self.bets.loc[
            self.bets["profit"].idxmin()
        ]

        messages.append(
            f"Best bet won {best['profit']:.2f}"
        )

        messages.append(
            f"Worst bet lost {abs(worst['profit']):.2f}"
        )

        return messages