# state.py

from typing import TypedDict, Optional

class InteractionState(TypedDict):
    hcp_name: Optional[str]
    date: Optional[str]
    sentiment: Optional[str]
    brochures_shared: Optional[bool]
    notes: Optional[str]
    summary: Optional[str] 