def get_priority_level(score: int):
    if score >= 80:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    else:
        return "LOW"