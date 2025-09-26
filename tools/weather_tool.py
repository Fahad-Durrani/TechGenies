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
def get_weather(
    location: str,
    include_humidity: bool = False,
    include_wind_speed: bool = False,
) -> Dict[str, Any]:
    """
    Get current weather for a location using WeatherAPI.com.
    Returns structured data with optional fields based on user query.

    ### Usage Rules for LLM:
    - The `location` parameter can be either a **city name** or a **country name**.
    - If both are present in the user query (e.g., "New York, USA"), always prioritize the **city**.
    - By default, only essential weather details (temperature, condition, last updated) are returned.
    - If the user explicitly asks about humidity or wind speed, set:
        - `include_humidity=True`
        - `include_wind_speed=True`

    ### Args:
    - **location (str):** City or country name for which to fetch weather.  
                         If both are mentioned, prioritize the city.  
    - **include_humidity (bool, optional):** Whether to include humidity in the response.  
                                            Only set to True if explicitly asked.  
    - **include_wind_speed (bool, optional):** Whether to include wind speed in the response.  
                                               Only set to True if explicitly asked.  

    ### Returns:
    dict: {
        "message": str,
        "data": {
            "city": str,
            "country": str,
            "temperature": float,
            "condition": str,   # e.g. "Sunny", "Rainy"
            "last_updated": str,
            "humidity": int,    # only if include_humidity=True
            "wind_speed": float # only if include_wind_speed=True
        }
    }
    """
    weather_api_key = keys_settings.weather_api_key
    if not weather_api_key:
        return {"message": "Error: WEATHER_API_KEY not set", "data": {}}

    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": weather_api_key, "q": location}

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {
                "message": f"Error: {response.status_code} - {response.text}",
                "data": {},
            }

        data = response.json()
        weather_info = {
            "city": data["location"]["name"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "last_updated": data["current"]["last_updated"],
        }

        if include_humidity:
            weather_info["humidity"] = data["current"]["humidity"]

        if include_wind_speed:
            weather_info["wind_speed"] = data["current"]["wind_kph"]

        return {"message": f"Weather fetched successfully for {location} ", "data": weather_info}

    except requests.exceptions.RequestException as e:
        return {"message": f"Request failed: {e}", "data": {}}

