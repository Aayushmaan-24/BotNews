import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def get_news():  # Removed async for simplicity; add back with httpx if needed
    if not API_KEY:
        return {"articles": [], "total": 0, "error": "API key not found in .env"}

    today = datetime.utcnow()
    two_days_ago = (today - timedelta(days=2)).strftime("%Y-%m-%d")

    params = {
    "apiKey": API_KEY,
    "q": '("artificial intelligence" OR AI OR "machine learning" OR "deep learning" OR "neural network") ("breakthrough" OR advancement OR innovation OR progress OR "new model" OR "research breakthrough" OR discovery)',
    "language": "en",
    "from": two_days_ago,
    "sortBy": "publishedAt",
    "pageSize": 10,
}

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # Raises error for 4xx/5xx

        data = response.json()

        if data.get("status") != "ok":
            return {
                "articles": [],
                "total": 0,
                "error": data.get("message", "API returned non-ok status")
            }

        articles_raw = data.get("articles", [])
        formatted = [
            {
                "title": article["title"] or "Untitled",
                "description": article["description"] or "No description available.",
                "image": article["urlToImage"] or "https://via.placeholder.com/800x400?text=BotNews+AI",
                "url": article["url"],
                "source": article["source"]["name"] if article.get("source") else "Unknown",
                "published": article["publishedAt"][:10] if article.get("publishedAt") else "Recent"
            }
            for article in articles_raw
            if article.get("title") and article.get("url")
        ]

        return {
            "articles": formatted,
            "total": len(formatted),
            "error": None
        }

    except requests.exceptions.HTTPError as http_err:
        error_msg = response.json().get("message", str(http_err)) if response.text else str(http_err)
        return {"articles": [], "total": 0, "error": f"HTTP error: {response.status_code} - {error_msg}"}
    except requests.exceptions.RequestException as err:
        return {"articles": [], "total": 0, "error": f"Request failed: {str(err)}"}
    except Exception as e:
        return {"articles": [], "total": 0, "error": f"Unexpected error: {str(e)}"}