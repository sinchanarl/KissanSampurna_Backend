from fastapi import APIRouter, Depends,Query
from typing import Dict, Any

from app.models import *
from services.weatherService import WeatherService
from services.llmService import LLMReportService

# ---------------------------------------------------------------------------
# 1. Define Pydantic Models for Request and Response
# ---------------------------------------------------------------------------


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)



@router.post(
    "/generate",
    response_model=ReportResponse,
    summary="Generate a Comprehensive Crop Report"
)
async def generate_comprehensive_report(
    payload: ReportRequest,
    weather_service: WeatherService = Depends(),
    llm_service: LLMReportService = Depends()
):
    """
    Generates a full agricultural report for a given crop and location.

    This endpoint orchestrates calls to two backend services:
    1.  **WeatherService**: Fetches current weather conditions based on latitude and longitude.
    2.  **LLMReportService**: Uses the weather data and user inputs to generate a detailed, AI-powered report.

    A `POST` request is used because this operation triggers a complex, state-changing action (generating data)
    and requires a structured request body with multiple parameters.
    """
    weather_json = weather_service.get_weather(lat=payload.lat, lon=payload.lon)

    location_str = f"Latitude: {payload.lat}, Longitude: {payload.lon}"

    report_content = llm_service.generate_crop_report(
        crop=payload.crop_name,
        farmer=payload.farmer_name,
        location=location_str,
        weather_json=weather_json
    )

    return ReportResponse(
        weather_data=weather_json,
        llm_report=report_content
    )

@router.get(
    "/weather",
    response_model=Dict[str, Any],
    summary="Fetch Current Weather Data by Coordinates"
)
async def get_current_weather(
    lat: float = Query(
        ...,
        ge=-90,  # ge = greater than or equal to
        le=90,   # le = less than or equal to
        description="Latitude of the location.",
        example=28.6139
    ),
    lon: float = Query(
        ...,
        ge=-180,
        le=180,
        description="Longitude of the location.",
        example=77.2090
    ),

    weather_service: WeatherService = Depends()
):
    """
    Provides direct access to the weather service to fetch current weather
    data for a specific geographical coordinate (latitude and longitude).

    This is a simple proxy endpoint that exposes the functionality of the
    internal `WeatherService`.
    """
    weather_data = weather_service.get_weather(lat=lat, lon=lon)
    return weather_data