import os
import logging
from typing import Dict, Any
from fastapi import HTTPException
from litellm import completion
from app.config import get_settings

# Configure logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("uvicorn")

settings = get_settings()

class LLMReportService:
    def __init__(self):
        os.environ["TOGETHERAI_API_KEY"] = os.getenv("TOGETHERAI_API_KEY")
        self.model = "together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo"

    def generate_crop_report(
        self,
        crop: str,
        farmer: str,
        location: str,
        weather_json: Dict[str, Any]
    ) -> str:
        """
        Generate a detailed crop report using the LLM.
        """
        try:
            system_prompt = (
                "You are an expert agricultural assistant. Generate a detailed, sectioned crop report for a farmer, "
                "using only the provided crop name, farmer's name, location, and current weather data (in JSON format). "
                "Infer all other relevant details based on best agricultural practices for the region and crop.\n\n"
                "Structure the report as follows:\n"
                "1. Crop Overview: State the crop name, farmer's name, location, and an estimated success rate.\n"
                "2. Soil Benefits: Suggest soil suitability and fertilizer needs based on the crop and region.\n"
                "3. Economic Benefits: Estimate profit potential and market stability for the crop in this location.\n"
                "4. Weather Suitability: Analyze the provided weather JSON to report on rainfall, sunlight, and soil compatibility, rating each as Ideal, Good, or Average.\n"
                "5. Action Steps: List clear next steps for the farmer (e.g., buy seeds, sowing window, etc.).\n"
                "6. Risks & Solutions: Identify likely risks (e.g., pests, weather extremes) and recommend solutions.\n"
                "7. Key Tips: Provide actionable farming tips, each with an urgency rating (High/Medium/Low).\n\n"
                "Use clear headers, bullet points, and concise, expert language. Format the report for easy readability."
            )

            user_prompt = (
                f"Crop: {crop}\n"
                f"Farmer: {farmer}\n"
                f"Location: {location}\n"
                f"Weather Data (JSON):\n{weather_json}"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = completion(model=self.model, messages=messages)
            return response["choices"][0]["message"]["content"]

        except Exception as e:
            error_msg = f"Failed to generate crop report: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

