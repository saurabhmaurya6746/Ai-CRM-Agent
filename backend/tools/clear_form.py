# tools/clear_form.py

from langchain.tools import tool

@tool
def clear_form():
    """
    Clear all fields in the interaction form.
    """

    return {
        "hcp_name": None,
        "date": None,
        "sentiment": None,
        "brochures_shared": None,
        "notes": None,
    }