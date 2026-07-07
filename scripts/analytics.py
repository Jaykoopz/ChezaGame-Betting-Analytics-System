import pandas as pd


class Analytics:

    def __init__(self, bets_df, selections_df=None):

        self.df = bets_df.copy()

        self.sel = (
            selections_df.copy()
            if selections_df is not None
            else pd.DataFrame()
        )

    # --------------------------------
    # CLEAN DATA
    # --------------------------------
    def clean_data(self):

        numeric_columns = [
            "stake",
            "returns",
            "total_odds",
            "profit"
        ]

        for col in numeric_columns:

            if col in self.df.columns:

                self.df[col] = pd.to_numeric(
                    self.df[col],
                    errors="coerce"
                ).fillna(0)

    # --------------------------------
    # SUMMARY
    # --------------------------------
    def summary(self):

        self.clean_data()
        print("\n===== ANALYTICS DEBUG =====")
        print(self.df.head())
        print(self.df.dtypes)
        print("===========================\n")
        
        total_bets = len(self.df)

        total_stake = self.df["stake"].sum()

        total_return = self.df["returns"].sum()

        wins = len(
            self.df[
                self.df["result"] == "Won"
            ]
        )

        losses = len(
            self.df[
                self.df["result"] == "Lost"
            ]
        )

        avg_stake = self.df["stake"].mean()

        avg_odds = self.df["total_odds"].mean()

        profit = self.df["profit"].sum()

        roi = (
            (profit / total_stake) * 100
            if total_stake > 0
            else 0
        )

        return {

            "Total Bets": total_bets,

            "Winning Bets": wins,

            "Losing Bets": losses,

            "Win Rate (%)": round(
                (wins / total_bets) * 100,
                2
            ) if total_bets else 0,

            "Total Stake": round(
                total_stake,
                2
            ),

            "Total Return": round(
                total_return,
                2
            ),

            "Profit/Loss": round(
                profit,
                2
            ),

            "ROI (%)": round(
                roi,
                2
            ),

            "Average Stake": round(
                avg_stake,
                2
            ),

            "Average Odds": round(
                avg_odds,
                2
            )

        }

    # --------------------------------
    # INSIGHTS
    # --------------------------------
    def insights(self):

        self.clean_data()

        insights = []

        streak = 0
        max_streak = 0

        for result in self.df["result"]:

            if result == "Lost":

                streak += 1

                max_streak = max(
                    max_streak,
                    streak
                )

            else:

                streak = 0

        insights.append({
            "type": "risk",
            "message": f"Longest losing streak: {max_streak}"
        })

        avg_odds = self.df["total_odds"].mean()

        if avg_odds > 6:

            insights.append({
                "type": "risk",
                "message": "You are consistently betting high odds."
            })

        stakes = self.df["stake"].tolist()

        escalation = False

        for i in range(1, len(stakes)):

            if stakes[i] > stakes[i - 1] * 1.5:

                escalation = True

        if escalation:

            insights.append({
                "type": "behavior",
                "message": "Stake escalation detected."
            })

        return insights
    
        # ==========================================
    # AI INTELLIGENCE ENGINE
    # ==========================================
    def intelligence(self):

        self.clean_data()

        report = []

        # -------------------------
        # ROI
        # -------------------------
        total_stake = self.df["stake"].sum()
        total_return = self.df["returns"].sum()

        profit = total_return - total_stake

        roi = 0

        if total_stake > 0:
            roi = (profit / total_stake) * 100

        if roi < 0:

            report.append(
                f"Overall ROI is {roi:.2f}%. "
                "Current betting strategy is unprofitable."
            )

        else:

            report.append(
                f"Overall ROI is {roi:.2f}%. "
                "Current betting strategy is profitable."
            )

                    # -------------------------
        # Average Odds
        # -------------------------
        avg_odds = self.df["total_odds"].mean()

        if avg_odds > 15:

            report.append(
                "Average odds are extremely high. "
                "High-risk accumulator strategy detected."
            )

        elif avg_odds > 6:

            report.append(
                "Average odds are above normal. "
                "Consider reducing accumulator size."
            )

        else:

            report.append(
                "Odds profile is relatively conservative."
            )

                    # -------------------------
        # Average Stake
        # -------------------------
        avg_stake = self.df["stake"].mean()

        largest = self.df["stake"].max()

        if largest > avg_stake * 3:

            report.append(
                "Large stake spikes detected. "
                "Possible emotional betting."
            )

                    # -------------------------
        # Winning Rate
        # -------------------------
        wins = len(self.df[self.df["result"] == "Won"])

        total = len(self.df)

        if total > 0:

            rate = wins / total * 100

            report.append(
                f"Win rate is {rate:.1f}%."
            )

            return report