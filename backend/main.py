from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api_client import get_news

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/news"):
async def news():
    return await get_news()