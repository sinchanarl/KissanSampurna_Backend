import csv
import httpx
import asyncio
import difflib
import re
from typing import Dict, List

CSV_PATH = "rules.csv"
BASE_URL = "http://localhost:8000/api/v1"
RULES_URL = f"{BASE_URL}/rules"
CROPS_URL = f"{BASE_URL}/crops"

# Map CSV columns to API fields
FIELD_MAP = {
    "Current Crop": "primary_crop_uid",
    "Landholding": "total_farmland_area",
    "Irrigation": "irrigation_available",
    "Water Source": "primary_water_source",
    "Budget/acre (₹)": "budget_per_acre",
    "Risk Appetite": "risk_appetite",
    "Crop Cycle": "crop_cycle",
    "Crop Rotation / Intercropping": "rotation_intercropping",
}

# Enum value mapping from CSV to API Enum values
ENUM_MAP = {
    "total_farmland_area": {
        'Small (<2 ha)': 'Small (<2 ha)',
        'Medium (2–5 ha)': 'Medium (2–5 ha)',
        'Large (>5 ha)': 'Large (>5 ha)',
        'Medium to Large (>2 ha)': 'Medium (2–5 ha)',
        'Small to Medium': 'Medium (2–5 ha)',
        'Small to Medium (<5 ha)': 'Medium (2–5 ha)',
        'Medium': 'Medium (2–5 ha)',
        'Small': 'Small (<2 ha)',
        'Large': 'Large (>5 ha)',
        'Medium to Large': 'Medium (2–5 ha)',
    },
    "primary_water_source": {
        'Borewell/Canal': 'Borewell/Canal',
        'Borewell + Rain': 'Borewell + Rain',
        'Rainfed + River': 'Rainfed + River',
        'Rainfed / Borewell': 'Borewell + Rain',
        'Rainfed': 'Rainfed + River',
        'Borewell + Canal': 'Borewell + Canal',
        'Borewell / Canal': 'Borewell/Canal',
        'Borewell + Pond': 'Rainfed + Pond',
        'Canal / Borewell': 'Borewell + Canal',
        'Canal + Borewell': 'Borewell + Canal',
        'Rainfed / Canal': 'Borewell/Canal',
        'Rainfed + Pond': 'Rainfed + Pond',
    },
    "budget_per_acre": {
        '<10,000': '<10,000',
        '10,000–15,000': '10,000–15,000',
        '12,000–20,000': '12,000–20,000',
        '15,000–18,000': '15,000–18,000',
        '20,000+': '20,000+',
        '<15,000': '<15,000',
        '30,000+': '20,000+',
        '>20,000': '20,000+',
        '<12,000': '<10,000',
    },
    "risk_appetite": {
        'Low': 'Low',
        'Medium': 'Medium',
        'Medium-High': 'Medium-High',
        'Medium to High': 'Medium to High',
        'High': 'High',
        'Low to Medium': 'Medium',
    },
    "crop_cycle": {
        'Short-Medium': 'Short-Medium',
        'Medium': 'Medium',
        'Short': 'Short-Medium',
        'Medium-Long': 'Medium',
        'Long': 'Medium',
        'Long (12–18 months)': 'Medium',
        'Short to Medium': 'Short-Medium',
    },
    "rotation_intercropping": {
        'Yes': 'Yes',
        'No': 'No',
    },
}

DEFAULT_VALUES = {
    "irrigation_type": "N/A",
    "market_access": "Yes",
    "preferred_crop_type": "string",
    "fertilizer_used": "organic",
    "pest_management": "chemical",
    "owns_livestock": "Yes",
    "livestock_type": "string",
    "smartphone_use": "Yes",
    "machinery_used": "Light",
    "storage_facility": "Yes",
    "transport_access": "Yes",
    "temperature_range": "25–35",
    "altitude_range": "0–1000",
}


def normalize(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9]', '', s or '').lower()


def get_nearest_enum(field: str, value: str) -> str:
    if not value or field not in ENUM_MAP:
        return None
    value_norm = normalize(value)
    enum_dict = ENUM_MAP[field]

    # Try exact match first
    for k, v in enum_dict.items():
        if normalize(k) == value_norm or normalize(v) == value_norm:
            return v

    # Try substring match
    for k, v in enum_dict.items():
        if value_norm in normalize(k) or value_norm in normalize(v):
            return v

    # Use difflib for closest match
    all_keys = list(enum_dict.keys()) + list(enum_dict.values())
    matches = difflib.get_close_matches(value, all_keys, n=1, cutoff=0.6)
    if matches:
        match = matches[0]
        return enum_dict.get(match, match)

    # Fallback: pick the first enum value
    return list(enum_dict.values())[0]


def convert_value(field: str, value: str, row_idx: int = None) -> any:
    if field == "irrigation_available":
        return value.strip().lower() == "yes"
    if field in ENUM_MAP:
        mapped = get_nearest_enum(field, value.strip())
        return mapped
    return value


async def fetch_all_crops(client: httpx.AsyncClient) -> Dict[str, str]:
    """Fetch all crops and return a mapping of crop names to their UIDs"""
    try:
        response = await client.get(CROPS_URL)
        response.raise_for_status()
        crops = response.json()
        return {crop['name'].lower(): crop['uid'] for crop in crops["items"]}
    except httpx.HTTPError as e:
        print(f"Error fetching crops: {str(e)}")
        return {}


def parse_crop_list(crop_string: str) -> List[str]:
    """Parse comma-separated crop string into list of crop names"""
    if not crop_string:
        return []
    return [crop.strip() for crop in crop_string.split(',') if crop.strip()]


async def create_rule(client: httpx.AsyncClient, row: dict, crop_map: Dict[str, str], row_idx: int) -> None:
    # Prepare base payload with default values
    payload = DEFAULT_VALUES.copy()

    # Add mapped values from CSV
    for csv_col, api_field in FIELD_MAP.items():
        if csv_col in row:
            value = row[csv_col]
            if api_field == "primary_crop_uid":
                crop_name = value.lower()
                payload[api_field] = crop_map.get(crop_name)
            else:
                payload[api_field] = convert_value(api_field, value, row_idx)

    # Prepare crop lists
    rabi_crops = [uid for name, uid in crop_map.items()
                  for crop in parse_crop_list(row.get("Recommended Rabi Crop", ""))
                  if normalize(crop) == normalize(name)]

    summer_crops = [uid for name, uid in crop_map.items()
                    for crop in parse_crop_list(row.get("Recommended Summer Crop", ""))
                    if normalize(crop) == normalize(name)]

    try:
        # Create rule with crop associations
        resp = await client.post(
            RULES_URL,
            json={
                "payload": payload,
                "rabi_crops": rabi_crops,
                "summer_crops": summer_crops
            }
        )
        resp.raise_for_status()
        print(f"Created rule for row {row_idx}: {resp.status_code}")
    except httpx.HTTPError as e:
        print(f"Error creating rule for row {row_idx}: {str(e)}")


async def main():
    async with httpx.AsyncClient() as client:
        # First fetch all crops
        crop_map = await fetch_all_crops(client)
        if not crop_map:
            print("Failed to fetch crops. Exiting.")
            return

        # Read CSV and create rules
        with open(CSV_PATH, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for idx, row in enumerate(reader, 1):
                await create_rule(client, row, crop_map, idx)


if __name__ == "__main__":
    asyncio.run(main())
