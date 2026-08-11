"""
API endpoints for model inference (QA and OBT predictions).

Endpoints:
- GET /crops/models/qa - Get available QA models for crops
- GET /crops/models/obt - Get available OBT models for crops
- POST /crops/analyze - Analyze crop image (QA + OBT pipeline)
- Similar endpoints for fruits and vegetables
"""

from fastapi import APIRouter, File, UploadFile, Query, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from app.services.modelService import ModelInferenceService

logger = logging.getLogger("uvicorn")

# Initialize service
model_service = ModelInferenceService()

# Create router
router = APIRouter(prefix="/analyze")


# ==================== Request/Response Models ====================

class QAModelListResponse(BaseModel):
    """Response for listing available QA models."""
    category: str
    models: List[str]
    description: str = "Binary classification models for quality assessment"


class OBTModelListResponse(BaseModel):
    """Response for listing available OBT models."""
    category: str
    models: List[str]
    description: str = "Object detection models for disease classification"


class QAPredictionResponse(BaseModel):
    """Response from QA model prediction."""
    is_valid: bool
    confidence: float
    model_used: str
    class_name: Optional[str] = None
    raw_predictions: Dict[str, Any]
    error: Optional[str] = None


class OBTPredictionResponse(BaseModel):
    """Response from OBT model prediction."""
    detections: List[Dict[str, Any]]
    disease_class: str
    confidence: float
    model_used: str
    image_analyzed: bool
    total_detections: Optional[int] = None
    error: Optional[str] = None


class DetectionDetail(BaseModel):
    """Details of a detected disease."""
    disease: str
    class_id: int
    confidence: float
    bbox: Optional[List[float]] = None


class AnalysisResponse(BaseModel):
    """Complete analysis response (QA + OBT pipeline)."""
    status: str  # "success", "invalid_image", "error"
    category: str
    qa_result: Optional[QAPredictionResponse] = None
    obt_result: Optional[OBTPredictionResponse] = None
    final_diagnosis: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ==================== Crop Endpoints ====================

@router.get("/crops/qa-models", response_model=QAModelListResponse)
async def get_crop_qa_models():
    """Get list of available QA models for crops."""
    try:
        models = model_service.get_available_qa_models("crop")
        return {
            "category": "crop",
            "models": models,
            "description": "Quality assessment models for crops"
        }
    except Exception as e:
        logger.error(f"Error fetching crop QA models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crops/obt-models", response_model=OBTModelListResponse)
async def get_crop_obt_models():
    """Get list of available OBT models for crops."""
    try:
        models = model_service.get_available_obt_models("crop")
        return {
            "category": "crop",
            "models": models,
            "description": "Disease detection models for crops"
        }
    except Exception as e:
        logger.error(f"Error fetching crop OBT models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/crops", response_model=AnalysisResponse)
async def analyze_crop_image(
    file: UploadFile = File(...),
    qa_model: str = Query(..., description="QA model name (without .pt extension)"),
    obt_model: str = Query(..., description="OBT model name (without .pt extension)")
):
    """
    Analyze a crop image using QA and OBT models.
    
    Stage 1: QA model validates if image is valid crop
    Stage 2: OBT model detects disease/condition
    
    Query params:
    - qa_model: QA model name (e.g., "rice_crop_qa")
    - obt_model: OBT model name (e.g., "rice_crop_model")
    """
    try:
        # Read file
        image_data = await file.read()
        
        if not image_data:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Run analysis pipeline
        result = model_service.analyze_image(
            category="crop",
            qa_model_name=qa_model,
            obt_model_name=obt_model,
            image_data=image_data
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Crop analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Fruit Endpoints ====================

@router.get("/fruits/qa-models", response_model=QAModelListResponse)
async def get_fruit_qa_models():
    """Get list of available QA models for fruits."""
    try:
        models = model_service.get_available_qa_models("fruit")
        return {
            "category": "fruit",
            "models": models,
            "description": "Quality assessment models for fruits"
        }
    except Exception as e:
        logger.error(f"Error fetching fruit QA models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fruits/obt-models", response_model=OBTModelListResponse)
async def get_fruit_obt_models():
    """Get list of available OBT models for fruits."""
    try:
        models = model_service.get_available_obt_models("fruit")
        return {
            "category": "fruit",
            "models": models,
            "description": "Disease detection models for fruits"
        }
    except Exception as e:
        logger.error(f"Error fetching fruit OBT models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/fruits", response_model=AnalysisResponse)
async def analyze_fruit_image(
    file: UploadFile = File(...),
    qa_model: str = Query(..., description="QA model name"),
    obt_model: str = Query(..., description="OBT model name")
):
    """Analyze a fruit image using QA and OBT models."""
    try:
        image_data = await file.read()
        
        if not image_data:
            raise HTTPException(status_code=400, detail="Empty file")
        
        result = model_service.analyze_image(
            category="fruit",
            qa_model_name=qa_model,
            obt_model_name=obt_model,
            image_data=image_data
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Fruit analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Vegetable Endpoints ====================

@router.get("/vegetables/qa-models", response_model=QAModelListResponse)
async def get_vegetable_qa_models():
    """Get list of available QA models for vegetables."""
    try:
        models = model_service.get_available_qa_models("vegetable")
        return {
            "category": "vegetable",
            "models": models,
            "description": "Quality assessment models for vegetables"
        }
    except Exception as e:
        logger.error(f"Error fetching vegetable QA models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vegetables/obt-models", response_model=OBTModelListResponse)
async def get_vegetable_obt_models():
    """Get list of available OBT models for vegetables."""
    try:
        models = model_service.get_available_obt_models("vegetable")
        return {
            "category": "vegetable",
            "models": models,
            "description": "Disease detection models for vegetables"
        }
    except Exception as e:
        logger.error(f"Error fetching vegetable OBT models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vegetables", response_model=AnalysisResponse)
async def analyze_vegetable_image(
    file: UploadFile = File(...),
    qa_model: str = Query(..., description="QA model name"),
    obt_model: str = Query(..., description="OBT model name")
):
    """Analyze a vegetable image using QA and OBT models."""
    try:
        image_data = await file.read()
        
        if not image_data:
            raise HTTPException(status_code=400, detail="Empty file")
        
        result = model_service.analyze_image(
            category="vegetable",
            qa_model_name=qa_model,
            obt_model_name=obt_model,
            image_data=image_data
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Vegetable analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
