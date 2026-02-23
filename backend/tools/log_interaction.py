# tools/log_interaction.py

from langchain.tools import tool
from datetime import datetime

@tool
def log_interaction(
    hcp_name: str,
    sentiment: str,
    brochures_shared: bool,
    notes: str = "",
):
    """
    Extract interaction details and populate the form.
    """

    return {
        "hcp_name": hcp_name,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "sentiment": sentiment,
        "brochures_shared": brochures_shared,
        "notes": notes,
    }