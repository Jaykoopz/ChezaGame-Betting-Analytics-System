import streamlit as st
from app.ai.recommendation_engine import generate_ai_summary


def show_cheza_ai(
    win_rate,
    roi,
    total_profit,
    average_odds,
):
    st.subheader("🤖 ChezaAI Decision Engine")

    # Get AI summary
    ai = generate_ai_summary(
        win_rate=win_rate,
        roi=roi,
        average_odds=average_odds,
        total_profit=total_profit,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🧠 Decision Score",
            f"{ai['score']}/100"
        )

    with col2:

        if ai["score"] >= 80:
            st.success("🟢 LOW RISK")

        elif ai["score"] >= 60:
            st.warning("🟡 MODERATE RISK")

        else:
            st.error("🔴 HIGH RISK")

    st.subheader("💡 AI Insight")

    st.info(ai["insight"])

    st.subheader("🎯 Recommendation")

    st.success(ai["recommendation"])