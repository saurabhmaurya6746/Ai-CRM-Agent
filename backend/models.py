from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from database import Base
from datetime import datetime

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String, nullable=True)
    interaction_type = Column(String, default="Meeting")
    user_message = Column(Text)
    notes = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    date = Column(String, nullable=True)
    time = Column(String, nullable=True)
    attendees = Column(String, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    materials = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    ai_followups = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)