# tools/edit_interaction.py
from langchain_core.tools import tool
import json

@tool
def edit_interaction(field_name: str, new_value: str):
    """
    Use this tool to update specific fields in the interaction form.
    field_name can be: 'hcp_name', 'sentiment', 'topics_discussed', 'outcomes', etc.
    """
    # Hum ek structured response bhejenge
    response = {
        "action": "update_form",
        "field": field_name,
        "value": new_value,
        "message": f"Updated {field_name} to {new_value}"
    }
    return json.dumps(response)