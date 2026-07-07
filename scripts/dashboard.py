import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="🔥 THIS IS THE NEW DASHBOARD 🔥",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM STYLING
# ==========================================

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
    border:1px solid #d9d9d9;
    padding:18px;
    border-radius:12px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================

st.title("📊 ChezaGame Betting Analytics System")

st.caption(
    "AI-Powered Betting Analytics & Intelligence Dashboard"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Navigation")

uploaded = st.sidebar.file_uploader(
    "Upload CBAS_Database.xlsx",
    type=["xlsx"]
)

if uploaded:

    # ======================================
    # LOAD DATABASE
    # ======================================

    bets = pd.read_excel(
        uploaded,
        sheet_name="Bets"
    )

    selections = pd.read_excel(
        uploaded,
        sheet_name="Selections"
    )

    # ======================================
    # KPI CALCULATIONS
    # ======================================

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

    roi = 0

    if total_stake > 0:
        roi = (total_profit / total_stake) * 100

    win_rate = 0

    if total_bets > 0:
        win_rate = (winning_bets / total_bets) * 100

    average_stake = bets["stake"].mean()

    average_odds = bets["total_odds"].mean()

    # ======================================
    # SUCCESS MESSAGE
    # ======================================

    st.success("✅ Database Loaded Successfully")

    # ======================================
    # EXECUTIVE OVERVIEW
    # ======================================

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
    st.warning("✅ Reached Part 2")
    # ======================================
    # BETTING PERFORMANCE
    # ======================================

    st.header("📊 Betting Performance Overview")

    # -------------------------
    # Row 1
    # -------------------------
    st.write("Creating Win/Loss chart...")
    left, right = st.columns(2)

    with left:

        results = bets["result"].value_counts().reset_index()
        results.columns = ["Result", "Count"]

        fig = px.pie(
            results,
            names="Result",
            values="Count",
            hole=0.45,
            title="Win / Loss Distribution"
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

    # -------------------------
    # Row 2
    # -------------------------

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
            title="Profit / Loss Distribution"
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

    # ======================================
    # QUICK INSIGHTS
    # ======================================

    st.header("📌 Quick Insights")

    c1, c2 = st.columns(2)

    with c1:

        st.info(
            f"""
            **Average Stake**

            KES {average_stake:,.2f}
            """
        )

        st.info(
            f"""
            **Average Odds**

            {average_odds:.2f}
            """
        )

    with c2:

        highest_profit = bets["profit"].max()

        largest_loss = bets["profit"].min()

        st.success(
            f"""
            **Highest Profit**

            KES {highest_profit:,.2f}
            """
        )

        st.error(
            f"""
            **Largest Loss**

            KES {largest_loss:,.2f}
            """
        )

    st.divider()
