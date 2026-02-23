def calculate_hcp_score(interaction_type: str, user_message: str):
    score = 0

    # interaction weight
    if interaction_type.lower() == "call":
        score += 30
    elif interaction_type.lower() == "meeting":
        score += 40
    elif interaction_type.lower() == "email":
        score += 10

    # interest keywords
    keywords = [
        "interested",
        "prescribe",
        "trial",
        "buy",
        "start",
        "patient"
    ]

    msg_lower = user_message.lower()

    for word in keywords:
        if word in msg_lower:
            score += 20

    return min(score, 100)