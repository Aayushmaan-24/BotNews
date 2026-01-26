from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_client import get_news  # ← make sure this import works

app = FastAPI(title="BotNews API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to ["http://localhost:3000"] in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news")
def news():
    return get_news()