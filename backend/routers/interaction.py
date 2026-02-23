from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models
import schemas
import json
from datetime import datetime

# Correct Imports
from ai_agent.scoring import calculate_hcp_score 
from ai_agent.priority import get_priority_level
from sqlalchemy import func

router = APIRouter(prefix="/interactions", tags=["Interactions"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_agent_output(agent_output):
    try:
        messages = agent_output.get("messages", [])

        # 🔥 reverse me search karo latest ToolMessage
        for msg in reversed(messages):
            if msg.__class__.__name__ == "ToolMessage":
                content = msg.content.strip()

                # markdown cleanup
                content = content.replace("```json", "").replace("```", "").strip()

                return json.loads(content)

        return {}

    except Exception as e:
        print("Parse error:", e)
        return {}

@router.post("/", response_model=schemas.InteractionResponse)
def create_interaction(data: schemas.InteractionCreate, db: Session = Depends(get_db)):
    # ✅ Local import yahan karo function ke andar
    from ai_agent.agent import agent_executor 
    
    # ✅ PEHLE extracted_data ko initialize karo
    extracted_data = {}
    
    try:
        agent_output = agent_executor.invoke({"messages": [("user", data.user_message)]})
        print("AGENT OUTPUT:", agent_output)
        
        # ✅ Agent output ko parse karo
        extracted_data = parse_agent_output(agent_output)
        print("EXTRACTED DATA:", extracted_data)
        
        action = extracted_data.get("action")
        print("ACTION:", action)
        
    except Exception as e:
        print(f"Agent Error: {e}")
        extracted_data = {}

    # 2. Scoring aur Data preparation
    hcp_score = calculate_hcp_score(data.interaction_type, data.user_message)
    
    # 3. Action ke base pe summary text decide karo
    action = extracted_data.get("action", "log")
    
    if action == "summarized":
        summary_text = extracted_data.get("summary", "Interaction summarized.")
    elif action == "scored":
        summary_text = f"Interaction quality score: {extracted_data.get('score', 0)}"
    elif action == "clear_form":
        summary_text = "Form cleared successfully."
    else:
        summary_text = (
            "Interaction logged successfully! The details (HCP Name, Date, Sentiment, and Materials) "
            "have been automatically populated based on your summary. "
            "Would you like me to suggest a specific follow-up action, such as scheduling a meeting?"
        )

    # 4. Final HCP name fix - prioritize extracted data
    final_hcp = extracted_data.get("hcp_name") or data.hcp_name or "Unknown HCP"
    
    # 5. Set current date/time if not provided
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M")

    # 6. Database model creation with ALL fields
    new_interaction = models.Interaction(
        hcp_name=final_hcp,
        interaction_type=data.interaction_type,
        user_message=data.user_message,
        notes=extracted_data.get("notes") or data.notes or "",
        summary=summary_text,
        score=extracted_data.get("score") or hcp_score,
        date=extracted_data.get("date") or data.date or current_date,
        time=extracted_data.get("time") or data.time or current_time,
        attendees=extracted_data.get("attendees") or data.attendees or "",
        topics_discussed=extracted_data.get("topics_discussed") or data.topics_discussed or "",
        materials=extracted_data.get("materials") or data.materials or "",
        sentiment=extracted_data.get("sentiment") or data.sentiment or "Positive 😊",
        ai_followups=extracted_data.get("ai_followups") or data.ai_followups or "",
    )

    db.add(new_interaction)
    db.commit()
    db.refresh(new_interaction)
 
    # 7. Response taiyar karna
    response_data = schemas.InteractionResponse.model_validate(
        new_interaction
    ).model_dump()
    
    # Extra 'extracted_fields' add karna
    return {
        **response_data,
        "extracted_fields": extracted_data 
    }

# Leaderboard aur Followup logic
@router.get("/hcp-leaderboard")
def get_hcp_leaderboard(db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction.hcp_name, 
        func.sum(models.Interaction.score).label("total_score")
    ).group_by(models.Interaction.hcp_name).order_by(
        func.sum(models.Interaction.score).desc()
    ).all()
    return [{"hcp_name": name, "total_score": total} for name, total in results]

@router.get("/followup-alerts")
def get_followup_alerts(db: Session = Depends(get_db)):
    results = db.query(
        models.Interaction.hcp_name, 
        func.sum(models.Interaction.score).label("total_score")
    ).group_by(models.Interaction.hcp_name).all()
    alerts = [
        {"hcp_name": name, "total_score": total, "priority": get_priority_level(total)} 
        for name, total in results
    ]
    alerts.sort(key=lambda x: x["total_score"], reverse=True)
    return alerts