import httpx
import logging
from typing import Optional, Dict, Any
from fastapi import HTTPException
from app.config import get_settings
import os

# Configure logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("uvicorn")

settings = get_settings()

class WeatherService:
    def __init__(self):
        self.client = httpx.Client()
        self.api_key = os.getenv("WEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetch current weather data using latitude and longitude.
        """
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric"  # Optional: for temperature in °C
            }

            response = self.client.get(self.base_url, params=params)

            if response.status_code != 200:
                error_msg = f"Failed to fetch weather data: {response.status_code} - {response.text}"
                logger.error(error_msg)
                raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")

            return response.json()

        except httpx.RequestError as e:
            error_msg = f"HTTP request error fetching weather: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail="Weather service temporarily unavailable")

        except Exception as e:
            error_msg = f"Unexpected error in weather service: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)



