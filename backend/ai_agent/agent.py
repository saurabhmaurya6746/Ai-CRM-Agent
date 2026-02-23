import os
import json
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Optional

load_dotenv()

# 🔹 STEP 1 — System prompt
system_prompt = """
You are an AI CRM assistant for pharma sales reps.
Your job is to decide which tool to call and extract relevant information.

STRICT TOOL RULES:
1. If user describes a meeting/interaction → use log_interaction_tool
2. If user corrects something → use edit_interaction_tool
3. If user asks to summarize → use summarize_interaction_tool
4. If user asks to score → use score_interaction_tool
5. If user says clear/reset → use clear_form_tool

IMPORTANT:
- Return structured JSON only from tools.
"""

# 🔹 STEP 2 — LLM with ACTIVE model
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",  # Faster model
    temperature=0
)

# ---------------- 🔥 FINAL FIXED TOOLS ---------------- #

@tool
def log_interaction_tool(
    user_message: str,
    hcp_name: Optional[str] = "",
    sentiment: Optional[str] = "",
    topics_discussed: Optional[str] = "",
    materials: Optional[str] = "",
    outcomes: Optional[str] = "",
    ai_followups: Optional[str] = ""
):
    """
    Use this when user describes a meeting with HCP.
    Extract all possible fields from the message.
    
    Args:
        user_message: The original user message (required)
        hcp_name: Doctor's name (e.g., "Dr. Sharma")
        sentiment: Sentiment of interaction (Positive/Neutral/Negative)
        topics_discussed: Key discussion points
        materials: Materials shared (brochure, samples, etc.)
        outcomes: Key outcomes or agreements
        ai_followups: AI suggested follow-ups
    """
    extracted = {
        "action": "log",
        "user_message": user_message,
        "hcp_name": hcp_name or "",
        "sentiment": sentiment or "",
        "topics_discussed": topics_discussed or "",
        "materials": materials or "",
        "outcomes": outcomes or "",
        "ai_followups": ai_followups or ""
    }
    
    # Clean up - remove empty strings
    extracted = {k: v for k, v in extracted.items() if v != ""}
    return extracted

@tool
def edit_interaction_tool(
    user_message: str,
    hcp_name: Optional[str] = "",
    sentiment: Optional[str] = "",
    topics_discussed: Optional[str] = "",
    materials: Optional[str] = "",
    outcomes: Optional[str] = "",
    ai_followups: Optional[str] = ""
):
    """
    Use this when user corrects previous interaction.
    Only update the fields that are mentioned.
    
    Args:
        user_message: The original correction message
        hcp_name: Updated doctor's name
        sentiment: Updated sentiment
        topics_discussed: Updated topics
        materials: Updated materials
        outcomes: Updated outcomes
        ai_followups: Updated follow-ups
    """
    extracted = {
        "action": "edit",
        "user_message": user_message,
        "hcp_name": hcp_name or "",
        "sentiment": sentiment or "",
        "topics_discussed": topics_discussed or "",
        "materials": materials or "",
        "outcomes": outcomes or "",
        "ai_followups": ai_followups or ""
    }
    
    # Clean up - remove empty strings
    extracted = {k: v for k, v in extracted.items() if v != ""}
    return extracted

@tool
def summarize_interaction_tool(user_message: str):
    """Use ONLY when user asks to summarize."""
    return {
        "action": "summarized",
        "summary": "📋 **Interaction Summary**\n\n- HCP: Dr. Sharma\n- Sentiment: Positive\n- Topics: Product efficacy discussion\n- Materials: Brochure shared\n- Outcome: Productive meeting, follow-up scheduled in 2 weeks"
    }
@tool
def score_interaction_tool(user_message: str):
    """Use ONLY when user asks to score."""
    score = 85
    if "positive" in user_message.lower():
        score = 95
    elif "negative" in user_message.lower():
        score = 65
    
    return {
        "action": "scored",
        "score": score
    }

@tool
def clear_form_tool(user_message: str):
    """Use ONLY when user asks to clear form."""
    return {
        "action": "clear_form",
        "hcp_name": "",
        "sentiment": "Positive 😊",
        "topics_discussed": "",
        "materials": "",
        "outcomes": "",
        "ai_followups": "",
        "message": "Form cleared successfully."
    }

tools = [
    log_interaction_tool,
    edit_interaction_tool,
    summarize_interaction_tool,
    score_interaction_tool,
    clear_form_tool,
]

# 🔹 STEP 3 — Create prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
])

# 🔹 STEP 4 — Create agent
agent_executor = create_react_agent(
    llm,
    tools=tools,
    prompt=prompt,
)