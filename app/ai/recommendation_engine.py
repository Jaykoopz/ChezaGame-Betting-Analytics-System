def generate_ai_summary(
    win_rate,
    roi,
    average_odds,
    total_profit,
):

    score = 50

    # Score
    if win_rate >= 60:
        score += 20
    elif win_rate >= 50:
        score += 10
    else:
        score -= 10

    if roi > 15:
        score += 20
    elif roi > 0:
        score += 10
    else:
        score -= 20

    score = max(0, min(score, 100))

    # Risk
    if score >= 80:
        risk = "🟢 LOW"

    elif score >= 60:
        risk = "🟡 MODERATE"

    else:
        risk = "🔴 HIGH"

    # Confidence
    confidence = f"{score}%"

    # Insight
    if roi < 0:
        insight = "Your current strategy is producing negative returns."

    else:
        insight = "Your betting strategy is profitable."

    # Recommendation
    if average_odds > 7:
        recommendation = (
            "Reduce average odds below 5.0."
        )

    else:
        recommendation = (
            "Maintain your current betting discipline."
        )

    return {
        "score": score,
        "risk": risk,
        "confidence": confidence,
        "insight": insight,
        "recommendation": recommendation,
    }