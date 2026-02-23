# Ai-CRM-Agent

AI-First CRM with LangGraph
An intelligent CRM where an AI assistant controls form inputs using 5 LangGraph tools.

Features
Split-screen UI: Form on left, AI chat on right

5 LangGraph Tools: Log, Edit, Summarize, Score, Clear Form

AI-Powered Form Filling: No manual data entry

MySQL Database: Persistent storage

Tech Stack
Frontend: React, Redux, Axios

Backend: FastAPI, SQLAlchemy, MySQL

AI: LangGraph, LangChain, Groq (Llama 3.1)

Quick Start
Backend
bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Create .env:

text
GROQ_API_KEY=your_key_here
DATABASE_URL=mysql+pymysql://user:pass@localhost/crm_db
Run:

bash
uvicorn main:app --reload
Frontend
bash
cd frontend
npm install
npm start
Visit http://localhost:3000

Usage Examples
Command	Action
"Met Dr. Sharma today, positive meeting, shared brochure"	Logs interaction
"Sorry, name was Dr. Gupta, sentiment negative"	Edits fields
"Summarize this"	Shows summary
"Score this"	Rates interaction
"Clear form"	Resets all fields
API Endpoints
POST /interactions/ - Create interaction

GET /interactions/hcp-leaderboard - HCP scores

GET /interactions/followup-alerts - Priority alerts

Project Structure
text
backend/
├── ai_agent/agent.py      # LangGraph tools
├── routers/interaction.py  # API routes
├── models.py               # Database models
└── main.py                 # FastAPI app

frontend/
├── src/components/
│   └── LogInteraction.js   # Main UI
└── src/redux/              # State management
Requirements
Python 3.11+

Node.js 18+

MySQL 8.0+

Groq API key


GitHub: https://github.com/your-username/ai-first-crm

