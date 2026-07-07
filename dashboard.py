from scripts.betting_intelligence import BettingIntelligence
from scripts.pattern_detector import PatternDetector

import streamlit as st
import pandas as pd
import plotly.express as px

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="ChezaGame Betting Analytics System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.main{
    background:#f7f9fc;
}

h1{
    color:#1565C0;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:12px;
    border:1px solid #d9d9d9;
    padding:18px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# TITLE
# ==================================================

st.title("📊 ChezaGame Betting Analytics System")

st.caption(
    "AI-Powered Betting Analytics & Intelligence Dashboard"
)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("Navigation")

uploaded = st.sidebar.file_uploader(
    "Upload CBAS_Database.xlsx",
    type=["xlsx"]
)

# ==================================================
# LOAD DATA
# ==================================================
# ==================================================
# LOAD DATABASE
# ==================================================

@st.cache_data
def load_database(file):

    bets = pd.read_excel(
        file,
        sheet_name="Bets"
    )

    selections = pd.read_excel(
        file,
        sheet_name="Selections"
    )

    return bets, selections
if uploaded:

    bets, selections = load_database(uploaded)

    # ==============================================
    # SIDEBAR FILTERS
    # ==============================================

    st.sidebar.header("Filters")

    results = sorted(
        bets["result"].dropna().unique()
    )

    selected_results = st.sidebar.multiselect(
        "Bet Result",
        results,
        default=results
    )

    min_stake = float(
        bets["stake"].min()
    )

    max_stake = float(
        bets["stake"].max()
    )

    stake_range = st.sidebar.slider(
        "Stake Range (KES)",
        min_value=min_stake,
        max_value=max_stake,
        value=(min_stake, max_stake)
    )

    min_odds = float(
        bets["total_odds"].min()
    )

    max_odds = float(
        bets["total_odds"].max()
    )

    odds_range = st.sidebar.slider(
        "Odds Range",
        min_value=min_odds,
        max_value=max_odds,
        value=(min_odds, max_odds)
    )

    # ==============================================
    # APPLY FILTERS
    # ==============================================

    bets = bets[
        (bets["result"].isin(selected_results))
        &
        (bets["stake"] >= stake_range[0])
        &
        (bets["stake"] <= stake_range[1])
        &
        (bets["total_odds"] >= odds_range[0])
        &
        (bets["total_odds"] <= odds_range[1])
    ]

    # ==============================================
    # KPI CALCULATIONS
    # ==============================================

    total_bets = len(bets)

    winning_bets = len(
        bets[bets["profit"] > 0]
    )

    losing_bets = len(
        bets[bets["profit"] <= 0]
    )

    total_stake = bets["stake"].sum()

    total_returns = bets["returns"].sum()

    total_profit = bets["profit"].sum()

    average_stake = bets["stake"].mean()

    average_odds = bets["total_odds"].mean()

    roi = 0

    if total_stake > 0:

        roi = (
            total_profit / total_stake
        ) * 100

    win_rate = 0

    if total_bets > 0:

        win_rate = (
            winning_bets / total_bets
        ) * 100
            # ==================================================
    # EXECUTIVE OVERVIEW
    # ==================================================

    st.success("✅ Database Loaded Successfully")

    st.header("📈 Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Bets",
        f"{total_bets:,}"
    )

    c2.metric(
        "Win Rate",
        f"{win_rate:.2f}%"
    )

    c3.metric(
        "ROI",
        f"{roi:.2f}%"
    )

    c4.metric(
        "Net Profit",
        f"KES {total_profit:,.2f}"
    )

    c5, c6, c7, c8 = st.columns(4)

    c5.metric(
        "Winning Bets",
        winning_bets
    )

    c6.metric(
        "Losing Bets",
        losing_bets
    )

    c7.metric(
        "Total Stake",
        f"KES {total_stake:,.2f}"
    )

    c8.metric(
        "Total Returns",
        f"KES {total_returns:,.2f}"
    )

    st.divider()

    # ==================================================
    # BETTING PERFORMANCE OVERVIEW
    # ==================================================

    st.header("📊 Betting Performance Overview")

    left, right = st.columns(2)

    with left:

        results_df = (
            bets["result"]
            .value_counts()
            .reset_index()
        )

        results_df.columns = [
            "Result",
            "Count"
        ]

        fig = px.pie(
            results_df,
            names="Result",
            values="Count",
            hole=0.45,
            title="Win vs Loss Distribution"
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        fig = px.histogram(
            bets,
            x="stake",
            nbins=20,
            title="Stake Distribution"
        )

        fig.update_layout(
            xaxis_title="Stake (KES)",
            yaxis_title="Number of Bets"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ==================================================
    # SECOND ROW OF CHARTS
    # ==================================================

    left, right = st.columns(2)

    with left:

        fig = px.histogram(
            bets,
            x="total_odds",
            nbins=20,
            title="Odds Distribution"
        )

        fig.update_layout(
            xaxis_title="Odds",
            yaxis_title="Number of Bets"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    with right:

        fig = px.histogram(
            bets,
            x="profit",
            nbins=20,
            title="Profit Distribution"
        )

        fig.update_layout(
            xaxis_title="Profit (KES)",
            yaxis_title="Number of Bets"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.divider()

    # ==================================================
    # QUICK INSIGHTS
    # ==================================================

    st.header("📌 Quick Insights")

    left, right = st.columns(2)

    with left:

        st.info(
            f"""
### Average Stake

**KES {average_stake:,.2f}**
"""
        )

        st.info(
            f"""
### Average Odds

**{average_odds:.2f}**
"""
        )

    with right:

        highest_profit = bets["profit"].max()

        largest_loss = bets["profit"].min()

        st.success(
            f"""
### Highest Profit

**KES {highest_profit:,.2f}**
"""
        )

        st.error(
            f"""
### Largest Loss

**KES {largest_loss:,.2f}**
"""
        )

    st.divider()
        # ==================================================
    # AI BETTING INTELLIGENCE
    # ==================================================

    st.header("🧠 AI Betting Intelligence")

    brain = BettingIntelligence(
        bets,
        selections
    )

    report = brain.run()

    if len(report) == 0:

        st.success(
            "No significant betting risks detected."
        )

    else:

        for message in report:

            st.warning(message)

    st.divider()

    # ==================================================
    # PATTERN DETECTOR
    # ==================================================

    st.header("🎯 Betting Patterns")

    patterns = PatternDetector(
        bets,
        selections
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Average Selections",
            patterns.average_selections()
        )

        st.metric(
            "High Odds Bets",
            patterns.high_odds()
        )

    with col2:

        biggest_win = patterns.biggest_win()

        if biggest_win:

            st.success(
                f"""
### Highest Winning Bet

**Bet ID:** {biggest_win['bet_id']}

**Profit:** KES {biggest_win['profit']:,.2f}
"""
            )

        biggest_loss = patterns.biggest_loss()

        st.error(
            f"""
### Largest Loss

**Bet ID:** {biggest_loss['bet_id']}

**Loss:** KES {abs(biggest_loss['loss']):,.2f}
"""
        )

    st.divider()

    # ==================================================
    # STAKE CHASING ALERTS
    # ==================================================

    st.header("⚠ Stake Chasing Detection")

    alerts = patterns.stake_chasing()

    if len(alerts) == 0:

        st.success(
            "No stake chasing behaviour detected."
        )

    else:

        for alert in alerts:

            st.warning(alert)

    st.divider()

    # ==================================================
    # CUMULATIVE PROFIT TREND
    # ==================================================

    st.header("📈 Cumulative Profit Trend")

    bets_chart = bets.copy()

    bets_chart["Bet Number"] = range(
        1,
        len(bets_chart) + 1
    )

    bets_chart["Cumulative Profit"] = (
        bets_chart["profit"].cumsum()
    )

    fig = px.line(
        bets_chart,
        x="Bet Number",
        y="Cumulative Profit",
        markers=True,
        title="Running Profit"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==================================================
    # STAKE VS RETURNS
    # ==================================================

    st.header("💰 Stake vs Returns")

    compare = pd.DataFrame({

        "Metric": [
            "Stake",
            "Returns"
        ],

        "Amount": [
            total_stake,
            total_returns
        ]

    })

    fig = px.bar(
        compare,
        x="Metric",
        y="Amount",
        text="Amount",
        title="Money Invested vs Money Returned"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()

    # ==================================================
    # ODDS VS PROFIT
    # ==================================================

    st.header("🎯 Odds vs Profit")

    fig = px.scatter(
        bets,
        x="total_odds",
        y="profit",
        size="stake",
        color="profit",
        hover_data=["bet_id"],
        title="Relationship Between Odds and Profit"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.divider()
        # ==================================================
    # AI BETTING RISK SCORE
    # ==================================================

    st.header("🧠 AI Betting Risk Score")

    risk = 0

    if roi < 0:
        risk += 30

    if win_rate < 45:
        risk += 25

    if average_odds > 10:
        risk += 20

    if total_profit < 0:
        risk += 25

    risk = min(risk, 100)

    st.progress(risk / 100)

    if risk < 30:

        st.success(
            f"Risk Score: {risk}/100 (Low Risk)"
        )

    elif risk < 70:

        st.warning(
            f"Risk Score: {risk}/100 (Moderate Risk)"
        )

    else:

        st.error(
            f"Risk Score: {risk}/100 (High Risk)"
        )

    st.divider()
        # ==================================================
    # BETTING HEALTH SCORE
    # ==================================================

    st.header("🏅 Betting Health Score")

    score = 100

    if roi < 0:
        score -= 30

    if win_rate < 50:
        score -= 20

    if average_odds > 12:
        score -= 20

    if total_profit < 0:
        score -= 30

    score = max(score, 0)

    if score >= 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B"

    elif score >= 60:
        grade = "C"

    elif score >= 50:
        grade = "D"

    else:
        grade = "F"

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Betting Score",
            f"{score}/100"
        )

    with c2:

        st.metric(
            "Grade",
            grade
        )

    st.divider()
        # ==================================================
    # AI RECOMMENDATIONS
    # ==================================================

    st.header("💡 AI Executive Recommendations")

    recommendations = []

    if roi < 0:

        recommendations.append(
            "Reduce stake sizes until ROI becomes positive."
        )

    if average_odds > 10:

        recommendations.append(
            "Consider focusing on medium odds between 2.0 and 6.0."
        )

    if win_rate < 45:

        recommendations.append(
            "Improve match selection before increasing bankroll."
        )

    if total_profit > 0:

        recommendations.append(
            "Current betting strategy is profitable. Maintain discipline."
        )

    if average_stake > 1000:

        recommendations.append(
            "Average stake is relatively high. Consider stronger bankroll controls."
        )

    if len(recommendations) == 0:

        st.success(
            "Excellent betting behaviour detected."
        )

    else:

        for item in recommendations:

            st.info(item)

    st.divider()
        # ==================================================
    # EXECUTIVE SUMMARY
    # ==================================================

    st.header("📝 Executive Summary")

    summary = f"""
### Betting Performance Summary

- Total Bets: **{total_bets:,}**
- Winning Bets: **{winning_bets:,}**
- Losing Bets: **{losing_bets:,}**
- Win Rate: **{win_rate:.2f}%**
- ROI: **{roi:.2f}%**
- Total Stake: **KES {total_stake:,.2f}**
- Total Returns: **KES {total_returns:,.2f}**
- Net Profit: **KES {total_profit:,.2f}**
- Average Stake: **KES {average_stake:,.2f}**
- Average Odds: **{average_odds:.2f}**

Overall, the dashboard indicates the current betting performance and highlights areas that require improvement based on historical betting behaviour.
"""

    st.markdown(summary)

    st.divider()
        # ==================================================
    # DOWNLOAD FILTERED DATA
    # ==================================================

    st.header("📥 Export Data")

    csv = bets.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Bets (CSV)",
        data=csv,
        file_name="Filtered_Bets.csv",
        mime="text/csv"
    )