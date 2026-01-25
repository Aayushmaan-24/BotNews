import os
import httpx
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://newsdata.io/api/1/latest"

async def get_news():

    if not API_KEY:
        return {
            "articles" : [],
            "total" : 0,
            "message" : "API_KEY not found in environment variables"
        }

    params = {
        "api_key" : API_KEY,
        "query" : 'AI OR "artificial intelligence" OR "machine learning" OR "neural network" OR "deep learning" (breakthrough OR advancement OR innovation OR progress)'
        "language" : "en",
        "country" : "us",
        "sortBy" : "pubdate",
        "timeframe" : 48,
        "size" : 10,
        "image" : 1
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])

            articles = []
            for result in results:
                if not result.get("title") or not result.get("link"):
                    continue
                articles.append({
                    "title" : result.get("title","Unknown")
                    "description" : result.get("description","Not available")
                    "image" : result.get("image_url","https://img.freepik.com/free-vector/glitch-error-404-page-background_23-2148090004.jpg?semt=ais_hybrid&w=740&q=80")
                    "url" : result.get("link","")
                    "source": result.get("source_id", "Unknown").replace("-", " ").title(),
                    "publishedAt" : result.get("pubDate", "Recent")
                })
            return {
                "articles" : articles,
                "total" : len(articles),
                "message" : None
            }
        except Exception as e:
            return {
                "articles" : [],
                "total" : 0,
                "message" : str(e)
            }
