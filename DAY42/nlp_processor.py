def process_choice(user_input: str) -> str:
    user_input = user_input.lower().strip()
    if "left" in user_input:
        return "left"
    elif "right" in user_input:
        return "right"
    else:
        return "unknown"