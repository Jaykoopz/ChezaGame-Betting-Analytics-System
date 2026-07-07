import pandas as pd


class BettingIntelligence:

    def __init__(self, bets_df, selections_df):
        self.bets = bets_df.copy()
        self.selections = selections_df.copy()

    # ==========================================
    # MAIN AI REPORT
    # ==========================================
    def run(self):

        report = []

        report.extend(self.detect_chasing())
        report.extend(self.detect_high_odds())
        report.extend(self.detect_bankroll())
        report.extend(self.detect_best_strategy())

        if len(report) == 0:
            report.append("No significant betting patterns detected.")

        return report

    # ==========================================
    # Detect Chasing Behaviour
    # ==========================================
    def detect_chasing(self):

        report = []

        stakes = self.bets["stake"].tolist()
        results = self.bets["result"].tolist()

        for i in range(1, len(stakes)):

            if (
                results[i - 1] == "Lost"
                and stakes[i] > stakes[i - 1] * 1.5
            ):

                report.append(
                    f"Possible chasing behaviour: stake increased from "
                    f"{stakes[i-1]:,.0f} to {stakes[i]:,.0f} after a loss."
                )

        return report

    # ==========================================
    # Detect High Odds Betting
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
    # Detect Poor Bankroll Management
    # ==========================================
    def detect_bankroll(self):

        report = []

        average = self.bets["stake"].mean()
        highest = self.bets["stake"].max()

        if highest > average * 4:

            report.append(
                f"Highest stake ({highest:,.0f}) is much larger than your average stake "
                f"({average:,.0f}). This suggests poor bankroll management."
            )

        return report

    # ==========================================
    # Detect Best Winning Odds Range
    # ==========================================
    def detect_best_strategy(self):

        report = []

        if "profit" not in self.bets.columns:
            return report

        winners = self.bets[self.bets["profit"] > 0]

        if winners.empty:
            return report

        avg_odds = winners["total_odds"].mean()

        report.append(
            f"Your winning bets average odds of {avg_odds:.2f}. "
            f"Consider concentrating around this odds range."
        )

        return report