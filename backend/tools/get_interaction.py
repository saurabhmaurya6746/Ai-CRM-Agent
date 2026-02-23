# tools/get_interaction.py

from langchain.tools import tool

@tool
def get_interaction():
    """
    Fetch current interaction details.
    """
    return {"message": "Fetch current form state from frontend"}