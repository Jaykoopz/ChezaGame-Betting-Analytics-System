class BettingIntelligence:

    def __init__(self, bets_df, selections_df):
        self.bets = bets_df
        self.selections = selections_df

    # ==========================================
    # MAIN AI ENGINE
    # ==========================================
    def run(self):

        report = []

        report.extend(self.detect_chasing())
        report.extend(self.detect_high_odds())
        report.extend(self.detect_bankroll())
        report.extend(self.detect_best_strategy())

        return report

    # ==========================================
    # CHASING LOSSES
    # ==========================================
    def detect_chasing(self):

        report = []

        stakes = self.bets["stake"].tolist()

        for i in range(1, len(stakes)):

            if stakes[i] > stakes[i - 1] * 1.5:

                report.append(
                    f"Possible chasing behaviour detected: stake increased from "
                    f"{stakes[i-1]:,.0f} to {stakes[i]:,.0f}."
                )

        return report

    # ==========================================
    # HIGH ODDS
    # ==========================================
    def detect_high_odds(self):

        report = []

        avg = self.bets["total_odds"].mean()

        if avg > 10:

            report.append(
                f"Average odds are {avg:.2f}. High-odds betting usually reduces long-term profitability."
            )

        return report

    # ==========================================
    # BANKROLL MANAGEMENT
    # ==========================================
    def detect_bankroll(self):

        report = []

        average = self.bets["stake"].mean()

        highest = self.bets["stake"].max()

        if highest > average * 4:

            report.append(
                f"Highest stake ({highest:,.0f}) is much larger than your average "
                f"stake ({average:,.0f}). This suggests poor bankroll management."
            )

        return report

    # ==========================================
    # BEST STRATEGY
    # ==========================================
    def detect_best_strategy(self):

        report = []

        if "profit" not in self.bets.columns:
            return report

        winners = self.bets[self.bets["profit"] > 0]

        if len(winners) == 0:
            return report

        avg_odds = winners["total_odds"].mean()

        report.append(
            f"Winning bets average odds: {avg_odds:.2f}. "
            f"Consider focusing around this odds range."
        )

        return report