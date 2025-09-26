
# Standard library imports
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import configparser

# Third-party imports
from langchain_core.tools import tool

# Local imports
from utils.uLogger import logger
from api_import import keys_settings



# Standard library imports
import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import configparser

# Third-party imports
from langchain_core.tools import tool

# Local imports
from utils.uLogger import logger
from api_import import keys_settings

@tool
def search_news(
    query: Optional[str] = None,
    sources: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    top_headlines: bool = False,
) -> Dict[str, Any]:
    """
    Search for news articles with optional filters.  
    Returns structured data with relevant articles.

    ### Usage Rules for LLM:
    - If the **user asks for "top headlines"** → set `top_headlines=True`.  
      - This will fetch the latest top headlines from the USA.  
      - `query`, `from_date`, and `to_date` should be ignored in this case.    

    - For **all other queries** (e.g., "Nvidia", "Apple vs Samsung", "stocks", "Floods",  
      "I need news about iPhone 17", "What is news about Russia") → you **must** provide `query`.  
      - Always map the user’s intent into this field.  
      - If no results are returned, try rephrasing the user query and retry.  
      - Once results are fetched, return only the articles that best match the user’s request.  

    ### Parameters:
    - **query (str, required unless `top_headlines=True`):**  
      The user’s request, expressed either as keywords (e.g., `"Nvidia"`, `"stocks"`)  
      or as a natural-language question (e.g., `"What is news about Russia?"`).  

    - **sources (str, optional):**  
      Comma-separated list of sources (e.g., `"cnn,bbc"`). Leave empty if the user doesn’t specify.  
    - Dates:
      - **from_date (str, optional):** Oldest article date (ISO 8601: `"YYYY-MM-DD"`).  
        - Leave empty if the user doesn’t specify (defaults to 7 days ago).  
        - If only year provided → defaults to `"YYYY-01-01"`.  
        - If year + month provided → defaults to `"YYYY-MM-01"`.  

      - **to_date (str, optional):** Newest article date (ISO 8601: `"YYYY-MM-DD"`).  
        - Leave empty if the user doesn’t specify (defaults to today).  
      
      - **Validation:** `from_date` must always be **less than or equal to** `to_date`.

    - **top_headlines (bool, optional):**  
      - `True` → fetches USA top headlines (with optional category).  
      - `False` → searches for articles based on `query` and other filters.  

    - **category (str, optional, only valid if `top_headlines=True`):**  
      One of: `"business"`, `"entertainment"`, `"general"`, `"health"`,  
      `"science"`, `"sports"`, `"technology"`.  
      - Default: `"general"`.  

    - **sort_by:** Always return the most recent articles first.  
    - **Pagination:** Always fixed → `page=1`, `pageSize=10`.  
    - **language:** Always `"en"` (English).  

    ### Returns:
    dict: {
        "message": str,   # "News fetched successfully" or error message
        "count": int,     # number of articles returned
        "articles": [
            {
                "source": str,
                "author": str,
                "title": str,
                "description": str,
                "url_for_details": str,
                "publishedAt": str,
                "content": str
            }
        ]
    }
    - If no results → `"message": "No results found. Try rephrasing the query."`, with empty `articles`.  
    - If request fails → `"message": "Request failed: <error>"`, with empty `articles`.  
    
    """

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    NEWS_API_KEY = keys_settings.news_api_key
    if not NEWS_API_KEY:
        return {"message": "Error: NEWS_API_KEY not set", "count": 0, "articles": []}

    # --- Handle top headlines separately ---
    if top_headlines:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": NEWS_API_KEY,
            "category": "general",  # default
            "country": "us",
            "pageSize": 10,
            "language": "en",
            "page": 1,
        }
    else:
        if not query:
            return {
                "message": "Error: query is required when top_headlines=False",
                "count": 0,
                "articles": [],
            }

        if not to_date:
            to_date = today
        if not from_date:
            from_date = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")

        url = "https://newsapi.org/v2/everything"
        params = {
            "apiKey": NEWS_API_KEY,
            "q": query,
            "sortBy": "publishedAt",
            "pageSize": 10,
            "page": 1,
            "from": from_date,
            "to": to_date,
            "language": "en",
        }
        if sources:
            params["sources"] = sources

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {
                "message": f"Error: {response.status_code} - {response.text}",
                "count": 0,
                "articles": [],
            }

        raw = response.json()
        if raw.get("status") == "ok" and raw.get("totalResults", 0) == 0:
            return {
                "message": "No results found. Try rephrasing the query.",
                "count": 0,
                "articles": [],
            }

        articles = []
        for art in raw.get("articles", []):
            articles.append({
                "source": art.get("source", {}).get("name", "-"),
                "author": art.get("author", "-"),
                "title": art.get("title", "-"),
                "description": art.get("description", "-"),
                "url_for_details": art.get("url", "-"),
                "publishedAt": art.get("publishedAt", "-"),
                "content": art.get("content", "-"),
            })

        return {
            "message": "News fetched successfully",
            "count": len(articles),
            "articles": articles,
        }

    except requests.exceptions.RequestException as e:
        return {"message": f"Request failed: {e}", "count": 0, "articles": []}
