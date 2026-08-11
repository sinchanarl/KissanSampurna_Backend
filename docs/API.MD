# Kisaan Sampurna API Documentation

## Overview
This document provides comprehensive documentation for the Kisaan Sampurna API, which offers endpoints for crop management, rule-based recommendations, and agricultural reports.

## Base URL
All API v1 endpoints are prefixed with `/api/v1`.

## Authentication
The API uses API key-based authentication. To access protected endpoints, you need to include your API key in the request headers:

```
X-API-Key: your_api_key_here
```

To obtain an API key, use the admin endpoints described below.

---

## Admin Endpoints

### Health Check
- **URL**: `/admin/health-check`
- **Method**: `GET`
- **Authentication**: Requires master key
- **Description**: Checks the health status of the application
- **Response**:
  ```json
  {
    "status": "string",
    "version": "string",
    "commit": "string",
    "branch": "string",
    "build_time": "string",
    "build_number": "string",
    "build_tags": ["string"]
  }
  ```

### Generate API Key
- **URL**: `/admin/generate-api-key`
- **Method**: `POST`
- **Authentication**: Requires master key
- **Description**: Generates a new API key with specified scopes
- **Request Body**:
  ```json
  {
    "scopes": ["string"]
  }
  ```
- **Response**:
  ```json
  {
    "uid": "string",
    "key": "string",
    "scopes": ["string"]
  }
  ```

### Revoke API Key
- **URL**: `/admin/revoke-api-key/{uid}`
- **Method**: `DELETE`
- **Authentication**: Requires master key
- **Description**: Revokes an API key by its UID
- **Path Parameters**:
  - `uid` (string): The UID of the API key to revoke
- **Response**:
  ```json
  {
    "status": "ok"
  }
  ```

---

## API v1 Endpoints

### Health Check
- **URL**: `/api/v1/health-check`
- **Method**: `GET`
- **Description**: Checks the health status of the application
- **Response**:
  ```json
  {
    "status": "string",
    "version": "string",
    "commit": "string",
    "branch": "string",
    "build_time": "string",
    "build_number": "string",
    "build_tags": ["string"]
  }
  ```

---

## Crop Endpoints

### Get All Crops
- **URL**: `/api/v1/crops`
- **Method**: `GET`
- **Description**: Retrieves all crops
- **Response**: List of crop objects
  ```json
  [
    {
      "uid": "string",
      "created_at": "datetime",
      "updated_at": "datetime",
      "name": "string",
      "scientific_name": "string",
      "crop_type": "string",
      "season": ["string"],
      "min_temperature": 0.0,
      "max_temperature": 0.0,
      "min_rainfall": 0.0,
      "max_rainfall": 0.0,
      "soil_type": ["string"],
      "ph_min": 0.0,
      "ph_max": 0.0,
      "growing_duration": 0,
      "water_requirement": "string",
      "fertilizer_requirement": "string",
      "pest_susceptibility": "string",
      "disease_susceptibility": "string",
      "average_yield": 0.0,
      "market_price_min": 0.0,
      "market_price_max": 0.0,
      "storage_life": 0
    }
  ]
  ```

### Get Crop by UID
- **URL**: `/api/v1/crops/{uid}`
- **Method**: `GET`
- **Description**: Retrieves a specific crop by its UID
- **Path Parameters**:
  - `uid` (string): The UID of the crop to retrieve
- **Response**: Crop object
  ```json
  {
    "uid": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "name": "string",
    "scientific_name": "string",
    "crop_type": "string",
    "season": ["string"],
    "min_temperature": 0.0,
    "max_temperature": 0.0,
    "min_rainfall": 0.0,
    "max_rainfall": 0.0,
    "soil_type": ["string"],
    "ph_min": 0.0,
    "ph_max": 0.0,
    "growing_duration": 0,
    "water_requirement": "string",
    "fertilizer_requirement": "string",
    "pest_susceptibility": "string",
    "disease_susceptibility": "string",
    "average_yield": 0.0,
    "market_price_min": 0.0,
    "market_price_max": 0.0,
    "storage_life": 0
  }
  ```

### Create Crop
- **URL**: `/api/v1/crops`
- **Method**: `POST`
- **Description**: Creates a new crop
- **Request Body**: Crop object without uid, created_at, and updated_at fields
  ```json
  {
    "name": "string",
    "scientific_name": "string",
    "crop_type": "string",
    "season": ["string"],
    "min_temperature": 0.0,
    "max_temperature": 0.0,
    "min_rainfall": 0.0,
    "max_rainfall": 0.0,
    "soil_type": ["string"],
    "ph_min": 0.0,
    "ph_max": 0.0,
    "growing_duration": 0,
    "water_requirement": "string",
    "fertilizer_requirement": "string",
    "pest_susceptibility": "string",
    "disease_susceptibility": "string",
    "average_yield": 0.0,
    "market_price_min": 0.0,
    "market_price_max": 0.0,
    "storage_life": 0
  }
  ```
- **Response**: Created crop object
  ```json
  {
    "uid": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "name": "string",
    "scientific_name": "string",
    "crop_type": "string",
    "season": ["string"],
    "min_temperature": 0.0,
    "max_temperature": 0.0,
    "min_rainfall": 0.0,
    "max_rainfall": 0.0,
    "soil_type": ["string"],
    "ph_min": 0.0,
    "ph_max": 0.0,
    "growing_duration": 0,
    "water_requirement": "string",
    "fertilizer_requirement": "string",
    "pest_susceptibility": "string",
    "disease_susceptibility": "string",
    "average_yield": 0.0,
    "market_price_min": 0.0,
    "market_price_max": 0.0,
    "storage_life": 0
  }
  ```

---

## Rule Endpoints

### Get All Rules
- **URL**: `/api/v1/rules`
- **Method**: `GET`
- **Description**: Retrieves all rules
- **Response**: List of rule objects
  ```json
  [
    {
      "uid": "string",
      "created_at": "datetime",
      "updated_at": "datetime",
      "total_farmland_area": "string",
      "primary_water_source": "string",
      "irrigation_available": true,
      "irrigation_type": "string",
      "budget_per_acre": "string",
      "market_access": "string",
      "preferred_crop_type": "string",
      "risk_appetite": "string",
      "fertilizer_used": "string",
      "pest_management": "string",
      "crop_cycle": "string",
      "rotation_intercropping": "string",
      "owns_livestock": "string",
      "livestock_type": "string",
      "smartphone_use": "string",
      "machinery_used": "string",
      "storage_facility": "string",
      "transport_access": "string",
      "temperature_range": "string",
      "altitude_range": "string",
      "primary_crop_uid": "string",
      "recommended_rabi_crops_rel": [],
      "recommended_summer_crops_rel": []
    }
  ]
  ```

### Create Rule
- **URL**: `/api/v1/rules`
- **Method**: `POST`
- **Description**: Creates a new rule
- **Query Parameters**:
  - `rabi_crops` (array of strings, optional): UIDs of rabi crops to associate with the rule
  - `summer_crops` (array of strings, optional): UIDs of summer crops to associate with the rule
- **Request Body**: Rule object without uid, created_at, and updated_at fields
  ```json
  {
    "total_farmland_area": "string",
    "primary_water_source": "string",
    "irrigation_available": true,
    "irrigation_type": "string",
    "budget_per_acre": "string",
    "market_access": "string",
    "preferred_crop_type": "string",
    "risk_appetite": "string",
    "fertilizer_used": "string",
    "pest_management": "string",
    "crop_cycle": "string",
    "rotation_intercropping": "string",
    "owns_livestock": "string",
    "livestock_type": "string",
    "smartphone_use": "string",
    "machinery_used": "string",
    "storage_facility": "string",
    "transport_access": "string",
    "temperature_range": "string",
    "altitude_range": "string",
    "primary_crop_uid": "string"
  }
  ```
- **Response**: Created rule object
  ```json
  {
    "uid": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "total_farmland_area": "string",
    "primary_water_source": "string",
    "irrigation_available": true,
    "irrigation_type": "string",
    "budget_per_acre": "string",
    "market_access": "string",
    "preferred_crop_type": "string",
    "risk_appetite": "string",
    "fertilizer_used": "string",
    "pest_management": "string",
    "crop_cycle": "string",
    "rotation_intercropping": "string",
    "owns_livestock": "string",
    "livestock_type": "string",
    "smartphone_use": "string",
    "machinery_used": "string",
    "storage_facility": "string",
    "transport_access": "string",
    "temperature_range": "string",
    "altitude_range": "string",
    "primary_crop_uid": "string",
    "recommended_rabi_crops_rel": [],
    "recommended_summer_crops_rel": []
  }
  ```

### Apply Rules
- **URL**: `/api/v1/rules/apply`
- **Method**: `POST`
- **Description**: Applies rules based on the provided parameters and returns a matching rule
- **Request Body**: Rule parameters to match
  ```json
  {
    "total_farmland_area": "string",
    "primary_water_source": "string",
    "irrigation_available": true,
    "irrigation_type": "string",
    "budget_per_acre": "string",
    "market_access": "string",
    "preferred_crop_type": "string",
    "risk_appetite": "string",
    "fertilizer_used": "string",
    "pest_management": "string",
    "crop_cycle": "string",
    "rotation_intercropping": "string",
    "owns_livestock": "string",
    "livestock_type": "string",
    "smartphone_use": "string",
    "machinery_used": "string",
    "storage_facility": "string",
    "transport_access": "string",
    "temperature_range": "string",
    "altitude_range": "string",
    "primary_crop_uid": "string"
  }
  ```
- **Response**: Matching rule object or 404 if no rules found
  ```json
  {
    "uid": "string",
    "created_at": "datetime",
    "updated_at": "datetime",
    "total_farmland_area": "string",
    "primary_water_source": "string",
    "irrigation_available": true,
    "irrigation_type": "string",
    "budget_per_acre": "string",
    "market_access": "string",
    "preferred_crop_type": "string",
    "risk_appetite": "string",
    "fertilizer_used": "string",
    "pest_management": "string",
    "crop_cycle": "string",
    "rotation_intercropping": "string",
    "owns_livestock": "string",
    "livestock_type": "string",
    "smartphone_use": "string",
    "machinery_used": "string",
    "storage_facility": "string",
    "transport_access": "string",
    "temperature_range": "string",
    "altitude_range": "string",
    "primary_crop_uid": "string",
    "recommended_rabi_crops_rel": [],
    "recommended_summer_crops_rel": []
  }
  ```

---

## Report Endpoints

### Generate Comprehensive Report
- **URL**: `/api/v1/reports/generate`
- **Method**: `POST`
- **Description**: Generates a comprehensive crop report based on crop name, farmer name, and location
- **Request Body**:
  ```json
  {
    "farmer_name": "Amit Singh",
    "lat": 28.6139,
    "lon": 77.2090,
    "crop_name": "Wheat"
  }
  ```
- **Response**:
  ```json
  {
    "weather_data": {
      "key1": "value1",
      "key2": "value2"
    },
    "llm_report": "Detailed crop report text..."
  }
  ```

### Get Current Weather
- **URL**: `/api/v1/reports/weather`
- **Method**: `GET`
- **Description**: Gets current weather data for a specific location
- **Query Parameters**:
  - `lat` (float, required): Latitude of the location (-90 to 90)
  - `lon` (float, required): Longitude of the location (-180 to 180)
- **Response**: Weather data object
  ```json
  {
    "key1": "value1",
    "key2": "value2"
  }
  ```

---

## Data Models

### Crop
```json
{
  "uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "name": "string",
  "scientific_name": "string",
  "crop_type": "string",
  "season": ["string"],
  "min_temperature": 0.0,
  "max_temperature": 0.0,
  "min_rainfall": 0.0,
  "max_rainfall": 0.0,
  "soil_type": ["string"],
  "ph_min": 0.0,
  "ph_max": 0.0,
  "growing_duration": 0,
  "water_requirement": "string",
  "fertilizer_requirement": "string",
  "pest_susceptibility": "string",
  "disease_susceptibility": "string",
  "average_yield": 0.0,
  "market_price_min": 0.0,
  "market_price_max": 0.0,
  "storage_life": 0
}
```

### Rule
```json
{
  "uid": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "total_farmland_area": "string",
  "primary_water_source": "string",
  "irrigation_available": true,
  "irrigation_type": "string",
  "budget_per_acre": "string",
  "market_access": "string",
  "preferred_crop_type": "string",
  "risk_appetite": "string",
  "fertilizer_used": "string",
  "pest_management": "string",
  "crop_cycle": "string",
  "rotation_intercropping": "string",
  "owns_livestock": "string",
  "livestock_type": "string",
  "smartphone_use": "string",
  "machinery_used": "string",
  "storage_facility": "string",
  "transport_access": "string",
  "temperature_range": "string",
  "altitude_range": "string",
  "primary_crop_uid": "string",
  "recommended_rabi_crops_rel": [],
  "recommended_summer_crops_rel": []
}
```

### ReportRequest
```json
{
  "farmer_name": "string",
  "lat": 0.0,
  "lon": 0.0,
  "crop_name": "string"
}
```

### ReportResponse
```json
{
  "weather_data": {
    "key1": "value1",
    "key2": "value2"
  },
  "llm_report": "string"
}
```

### HealthCheckResponse
```json
{
  "status": "string",
  "version": "string",
  "commit": "string",
  "branch": "string",
  "build_time": "string",
  "build_number": "string",
  "build_tags": ["string"]
}
```

### GenerateApiKeyRequest
```json
{
  "scopes": ["string"]
}
```

### GenerateApiKeyResponse
```json
{
  "uid": "string",
  "key": "string",
  "scopes": ["string"]
}
```

### StatusResponse
```json
{
  "status": "ok"
}
```
