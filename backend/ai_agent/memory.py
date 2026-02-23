# backend/ai_agent/memory.py
from database import SessionLocal
import models

def get_memory(hcp_name: str):
    db = SessionLocal()
    try:
        # Database se is doctor ki purani interactions nikalna
        interactions = db.query(models.Interaction).filter(
            models.Interaction.hcp_name == hcp_name
        ).order_by(models.Interaction.created_at.desc()).limit(5).all()
        
        # Data ko readable format mein convert karna
        history = []
        for i in reversed(interactions):
            history.append({"user": i.user_message, "ai": i.summary})
        return history
    finally:
        db.close()