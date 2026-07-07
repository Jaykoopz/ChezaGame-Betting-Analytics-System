import pandas as pd


class PatternDetector:

    def __init__(self, bets_df, selections_df):

        self.bets = bets_df.copy()
        self.selections = selections_df.copy()

    # =====================================
    # Detect stake chasing
    # =====================================
    def stake_chasing(self):

        messages = []

        previous_stake = None
        previous_result = None

        for _, row in self.bets.iterrows():

            if previous_stake is not None:

                if (
                    row["stake"] > previous_stake * 1.5
                    and previous_result == "Lost"
                ):

                    messages.append(
                        f"Stake increased from {previous_stake:.2f} "
                        f"to {row['stake']:.2f} after a loss."
                    )

            previous_stake = row["stake"]
            previous_result = row["result"]

        return messages

    # =====================================
    # Count high odds bets
    # =====================================
    def high_odds(self):

        high = self.bets[
            self.bets["total_odds"] >= 20
        ]

        return len(high)

    # =====================================
    # Average selections
    # =====================================
    def average_selections(self):

        return round(
            self.bets["selections"].mean(),
            2
        )

    # =====================================
    # Biggest loss
    # =====================================
    def biggest_loss(self):

        worst = self.bets.loc[
            self.bets["profit"].idxmin()
        ]

        return {
            "bet_id": worst["bet_id"],
            "loss": worst["profit"]
        }

    # =====================================
    # Biggest win
    # =====================================
    def biggest_win(self):

        winners = self.bets[
            self.bets["profit"] > 0
        ]

        if winners.empty:
            return None

        best = winners.loc[
            winners["profit"].idxmax()
        ]

        return {
            "bet_id": best["bet_id"],
            "profit": best["profit"]
        }

    # =====================================
    # Pattern Report
    # =====================================
    def report(self):

        print("\n========== PATTERN REPORT ==========\n")

        print(
            "Average selections:",
            self.average_selections()
        )

        print(
            "High odds bets:",
            self.high_odds()
        )

        print(
            "Largest loss:",
            self.biggest_loss()
        )

        print(
            "Largest win:",
            self.biggest_win()
        )

        print("\nStake Chasing")

        chasing = self.stake_chasing()

        if chasing:
            for msg in chasing:
                print("-", msg)
        else:
            print("None detected.")