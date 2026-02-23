# tools/suggest_next_action.py

from langchain.tools import tool

@tool
def suggest_next_action(hcp_name: str, sentiment: str):
    """
    Suggest next best action for the HCP.
    """

    if sentiment == "positive":
        action = f"Schedule a follow-up demo for {hcp_name}."
    elif sentiment == "negative":
        action = f"Plan a re-engagement strategy for {hcp_name}."
    else:
        action = f"Monitor future interactions with {hcp_name}."

    return {"next_action": action}