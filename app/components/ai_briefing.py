import streamlit as st


def show_ai_briefing(
    score,
    risk,
    confidence,
    insight,
    recommendation,
):
    st.markdown("---")

    st.subheader("🧠 ChezaAI Daily Briefing")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Decision Score",
        f"{score}/100"
    )

    c2.metric(
        "Risk Level",
        risk
    )

    c3.metric(
        "Confidence",
        confidence
    )

    st.info(
        f"**Main Insight:** {insight}"
    )

    st.success(
        f"**Recommendation:** {recommendation}"
    )