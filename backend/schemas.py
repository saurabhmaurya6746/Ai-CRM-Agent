from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class InteractionCreate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: str = "Meeting"
    user_message: str
    notes: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials: Optional[str] = None
    sentiment: Optional[str] = None
    ai_followups: Optional[str] = None


class InteractionResponse(BaseModel):
    id: int
    hcp_name: Optional[str] = None
    interaction_type: str
    user_message: str
    notes: Optional[str] = None
    summary: Optional[str] = None
    score: Optional[float] = None
    date: Optional[str] = None
    time: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials: Optional[str] = None
    sentiment: Optional[str] = None
    ai_followups: Optional[str] = None
    created_at: datetime
    extracted_fields: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True)