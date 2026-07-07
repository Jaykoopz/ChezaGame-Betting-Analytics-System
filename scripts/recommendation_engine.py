class RecommendationEngine:

    def __init__(self, bets_df):
        self.bets = bets_df

    def report(self):

        advice = []

        roi = (
            self.bets["profit"].sum()
            / self.bets["stake"].sum()
        ) * 100

        average_odds = self.bets["total_odds"].mean()

        if average_odds > 15:

            advice.append(
                "Reduce average odds. Focus on bets between 2 and 8."
            )

        if roi < 0:

            advice.append(
                "Reduce stake sizes until profitability improves."
            )

        if self.bets["stake"].max() > self.bets["stake"].mean() * 4:

            advice.append(
                "Avoid dramatically increasing stakes after losses."
            )

        advice.append(
            "Track performance every 50 bets instead of every individual bet."
        )

        return advice