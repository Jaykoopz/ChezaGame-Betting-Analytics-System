import streamlit as st


def show_cheza_ai(
    win_rate,
    roi,
    total_profit,
    average_odds,
):
    st.subheader("🤖 ChezaAI Decision Engine")

    messages = []

    # -------------------------
    # Decision Score
    # -------------------------

    score = 50

    # -------------------------
    # Win Rate
    # -------------------------

    if win_rate >= 60:
        score += 20
        messages.append(
            "✅ Excellent win rate. Your strategy is performing consistently."
        )

    elif win_rate >= 50:
        score += 10
        messages.append(
            "🟡 Win rate is stable, but there is room for improvement."
        )

    else:
        score -= 10
        messages.append(
            "🔴 Win rate is low. Review your betting selections."
        )

    # -------------------------
    # ROI
    # -------------------------

    if roi > 15:
        score += 20
        messages.append(
            "📈 Strong ROI. Continue following disciplined bankroll management."
        )

    elif roi > 0:
        score += 10
        messages.append(
            "📊 Positive ROI, but growth opportunities exist."
        )

    else:
        score -= 20
        messages.append(
            "⚠️ Negative ROI detected. Reduce risk until performance improves."
        )

    # -------------------------
    # Average Odds
    # -------------------------

    if average_odds > 7:
        messages.append(
            "🎯 High average odds suggest an aggressive betting strategy."
        )
    else:
        messages.append(
            "⚽ Odds selection appears balanced."
        )

    # -------------------------
    # Profit
    # -------------------------

    if total_profit > 0:
        messages.append(
            f"💰 Overall profit: KES {total_profit:,.2f}"
        )
    else:
        messages.append(
            f"📉 Current loss: KES {abs(total_profit):,.2f}"
        )

    # -------------------------
    # Keep score between 0 and 100
    # -------------------------

    score = max(0, min(score, 100))

    # -------------------------
    # Display Decision Score
    # -------------------------

    st.metric(
        "🧠 Decision Score",
        f"{score}/100"
    )

    # -------------------------
    # Display AI Analysis
    # -------------------------

    st.info("\n\n".join(messages))