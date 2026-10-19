
def predict_ticket(text):
    text = text.lower()

    # Category prediction
    if any(word in text for word in [
        "payment", "refund", "billing", "charged", "money"
    ]):
        category = "payment"
    elif any(word in text for word in [
        "login", "password", "account", "username", "sign in"
    ]):
        category = "account"
    elif any(word in text for word in [
        "error", "bug", "crash", "not working", "technical"
    ]):
        category = "technical"
    else:
        category = "other"

    # Priority prediction
    if any(word in text for word in [
        "urgent", "critical", "emergency", "completely down"
    ]):
        priority = "urgent"
    elif any(word in text for word in [
        "failed", "cannot access", "blocked", "not working"
    ]):
        priority = "high"
    elif any(word in text for word in [
        "slow", "problem", "issue", "difficulty"
    ]):
        priority = "medium"
    else:
        priority = "low"

    return {
        "category": category,
        "priority": priority,
    }
