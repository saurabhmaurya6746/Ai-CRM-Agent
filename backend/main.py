from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # ✅ Naya import
from database import engine, Base
from routers import interaction

# Database tables create karna
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI First CRM")

# ✅ 1. CORS Middleware setup (Iske bina API Error aayega)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # React app ka URL
    allow_credentials=True,
    allow_methods=["*"], # Saare methods (GET, POST, etc.) allow karein
    allow_headers=["*"], # Saare headers allow karein
)

# Routers include karna
app.include_router(interaction.router)

@app.get("/")
def home():
    return {"message": "AI First CRM Backend Running"}