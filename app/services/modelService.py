"""
Model Inference Service for Quality Assessment (QA) and Object Detection (OBT) models.

This service handles:
1. Loading YOLO models for quality assessment (binary classification)
2. Loading YOLO models for disease/object detection
3. Running inference on uploaded images
4. Processing and formatting predictions
"""

import os
import logging
try:
    import torch
    TORCH_AVAILABLE = True
except Exception:  # pragma: no cover - optional dependency
    torch = None
    TORCH_AVAILABLE = False

import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image
import io

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None

logger = logging.getLogger("uvicorn")

# Model paths
MODELS_BASE_PATH = Path(__file__).parent.parent / "assets"
CROP_QA_PATH = MODELS_BASE_PATH / "crop_models" / "crop_qa_models"
CROP_OBT_PATH = MODELS_BASE_PATH / "crop_models" / "crop_obt_models"
FRUIT_QA_PATH = MODELS_BASE_PATH / "fruit_models" / "fruit_qa_models"
FRUIT_OBT_PATH = MODELS_BASE_PATH / "fruit_models" / "fruits_obt_models"
VEGETABLE_QA_PATH = MODELS_BASE_PATH / "vegetable_models" / "vegetable_qa_models"
VEGETABLE_OBT_PATH = MODELS_BASE_PATH / "vegetable_models" / "vegetables_obt_models"


class ModelInferenceService:
    """Service for running inference with QA and OBT models."""

    def __init__(self):
        """Initialize the model inference service."""
        if TORCH_AVAILABLE:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Model service initialized. Using device: {self.device}")
        else:
            self.device = "cpu"
            logger.warning("Torch not available in this environment; model inference disabled.")

        # Cache for loaded models to avoid reloading
        self.qa_models_cache: Dict[str, Any] = {}
        self.obt_models_cache: Dict[str, Any] = {}

        # Model configuration
        self.model_config = {
            "crop": {
                "qa_path": CROP_QA_PATH,
                "obt_path": CROP_OBT_PATH,
                "qa_models": self._get_model_files(CROP_QA_PATH),
                "obt_models": self._get_model_files(CROP_OBT_PATH),
            },
            "fruit": {
                "qa_path": FRUIT_QA_PATH,
                "obt_path": FRUIT_OBT_PATH,
                "qa_models": self._get_model_files(FRUIT_QA_PATH),
                "obt_models": self._get_model_files(FRUIT_OBT_PATH),
            },
            "vegetable": {
                "qa_path": VEGETABLE_QA_PATH,
                "obt_path": VEGETABLE_OBT_PATH,
                "qa_models": self._get_model_files(VEGETABLE_QA_PATH),
                "obt_models": self._get_model_files(VEGETABLE_OBT_PATH),
            },
        }

    @staticmethod
    def _get_model_files(model_dir: Path) -> List[str]:
        """Get list of .pt files in a directory."""
        if not model_dir.exists():
            logger.warning(f"Model directory not found: {model_dir}")
            return []
        
        files = []
        for file in model_dir.glob("*.pt"):
            # Extract model name without extension
            model_name = file.stem
            files.append(model_name)
        
        return sorted(files)

    def get_available_qa_models(self, category: str) -> List[str]:
        """Get list of available QA models for a category."""
        if category not in self.model_config:
            raise ValueError(f"Invalid category: {category}. Must be one of: crop, fruit, vegetable")
        
        return self.model_config[category]["qa_models"]

    def get_available_obt_models(self, category: str) -> List[str]:
        """Get list of available OBT (disease detection) models for a category."""
        if category not in self.model_config:
            raise ValueError(f"Invalid category: {category}. Must be one of: crop, fruit, vegetable")
        
        return self.model_config[category]["obt_models"]

    def _load_qa_model(self, category: str, model_name: str) -> Any:
        """Load QA model with caching."""
        cache_key = f"{category}_{model_name}_qa"
        
        if cache_key in self.qa_models_cache:
            logger.debug(f"Loading QA model from cache: {cache_key}")
            return self.qa_models_cache[cache_key]

        model_path = self.model_config[category]["qa_path"] / f"{model_name}.pt"
        
        if not model_path.exists():
            raise FileNotFoundError(f"QA model not found: {model_path}")

        if not TORCH_AVAILABLE or YOLO is None:
            raise RuntimeError("Model loading not available: torch or ultralytics not installed")

        logger.info(f"Loading QA model: {model_path}")
        try:
            model = YOLO(str(model_path))
            model.to(self.device)
            self.qa_models_cache[cache_key] = model
            return model
        except Exception as e:
            logger.error(f"Failed to load QA model {model_path}: {str(e)}")
            raise

    def _load_obt_model(self, category: str, model_name: str) -> Any:
        """Load OBT model with caching."""
        cache_key = f"{category}_{model_name}_obt"
        
        if cache_key in self.obt_models_cache:
            logger.debug(f"Loading OBT model from cache: {cache_key}")
            return self.obt_models_cache[cache_key]

        model_path = self.model_config[category]["obt_path"] / f"{model_name}.pt"
        
        if not model_path.exists():
            raise FileNotFoundError(f"OBT model not found: {model_path}")

        if not TORCH_AVAILABLE or YOLO is None:
            raise RuntimeError("Model loading not available: torch or ultralytics not installed")

        logger.info(f"Loading OBT model: {model_path}")
        try:
            model = YOLO(str(model_path))
            model.to(self.device)
            self.obt_models_cache[cache_key] = model
            return model
        except Exception as e:
            logger.error(f"Failed to load OBT model {model_path}: {str(e)}")
            raise

    def _determine_qa_validity(self, class_name: str, class_names: dict, top_class: int, top_confidence: float) -> bool:
        """
        Determine if the QA result indicates valid/good quality based on class names.
        
        Logic:
        - If class name contains crop/fruit/vegetable name (e.g., "Cotton_Leaf", "Tomato_Fruit") = VALID
        - If class name contains "Not_", "Bad", "Invalid", "Poor" = INVALID  
        - If class name contains "Good", "Valid", "Healthy" = VALID
        - Fallback: class 1 = valid, class 0 = invalid
        """
        if not class_name or not isinstance(class_name, str):
            # Fallback to simple class ID logic
            return bool(top_class == 1 if len(class_names) == 2 else top_confidence > 0.5)
        
        class_name_lower = class_name.lower()
        
        # Check for explicit invalid indicators
        invalid_indicators = ['not_', 'bad', 'invalid', 'poor', 'unhealthy', 'disease', 'defect']
        for indicator in invalid_indicators:
            if indicator in class_name_lower:
                return False
        
        # Check for explicit valid indicators  
        valid_indicators = ['good', 'valid', 'healthy', 'fresh', 'quality']
        for indicator in valid_indicators:
            if indicator in class_name_lower:
                return True
        
        # Check if it's a crop/fruit/vegetable name (positive class)
        crop_indicators = ['leaf', 'fruit', 'crop', 'vegetable', 'plant', 'cotton', 'tomato', 'rice', 'corn', 'grape', 'orange', 'potato', 'cucumber']
        for indicator in crop_indicators:
            if indicator in class_name_lower and 'not_' not in class_name_lower:
                return True
        
        # Fallback to confidence-based or class ID logic
        return bool(top_class == 1 if len(class_names) == 2 else top_confidence > 0.5)

    def predict_qa(
        self,
        category: str,
        model_name: str,
        image_data: bytes
    ) -> Dict[str, Any]:
        """
        Run QA (quality assessment) prediction on an image.
        
        Args:
            category: One of "crop", "fruit", "vegetable"
            model_name: Model name without .pt extension
            image_data: Image bytes
            
        Returns:
            Dict with keys:
            - is_valid: bool - Whether image is valid (positive class)
            - confidence: float - Confidence score (0-1)
            - model_used: str - Name of model used
            - raw_predictions: dict - Raw model output
        """
        try:
            # Load model
            model = self._load_qa_model(category, model_name)
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            
            # Run inference with lower confidence threshold
            logger.info(f"Running QA inference with {model_name}")
            results = model.predict(source=image, verbose=False, conf=0.01)
            
            if not results or len(results) == 0:
                return {
                    "is_valid": False,
                    "confidence": 0.0,
                    "model_used": model_name,
                    "raw_predictions": {},
                    "error": "No results returned from model"
                }
            
            result = results[0]
            
            # Handle classification results (probs)
            if hasattr(result, 'probs') and result.probs is not None:
                probs = result.probs
                if hasattr(probs, 'data') and probs.data is not None:
                    # Classification model
                    confidences = probs.data.cpu().numpy()
                    top_class = int(confidences.argmax())
                    top_confidence = float(confidences[top_class])
                    
                    # Get class names if available
                    class_names = model.names if hasattr(model, 'names') else {}
                    class_name = class_names.get(top_class, str(top_class))
                    
                    # Smart QA logic based on class names
                    is_valid = self._determine_qa_validity(class_name, class_names, top_class, top_confidence)
                    
                    return {
                        "is_valid": is_valid,
                        "confidence": top_confidence,
                        "model_used": model_name,
                        "class_name": class_name,
                        "model_type": "classification",
                        "raw_predictions": {
                            "all_confidences": confidences.tolist(),
                            "top_class": top_class,
                            "top_confidence": top_confidence,
                            "class_names": dict(class_names) if class_names else {},
                            "total_classes": len(confidences)
                        }
                    }
            
            # Handle detection results (boxes) - fallback
            elif hasattr(result, 'boxes') and result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes
                conf = boxes.conf[0].item() if len(boxes.conf) > 0 else 0.0
                cls = int(boxes.cls[0].item()) if len(boxes.cls) > 0 else 0
                
                class_names = model.names if hasattr(model, 'names') else {}
                class_name = class_names.get(cls, str(cls))
                
                # Smart QA logic for detection models too
                is_valid = self._determine_qa_validity(class_name, class_names, cls, conf)
                
                return {
                    "is_valid": is_valid,
                    "confidence": float(conf),
                    "model_used": model_name,
                    "class_name": class_name,
                    "model_type": "detection",
                    "raw_predictions": {
                        "total_boxes": len(boxes),
                        "confidence": float(conf),
                        "class_id": cls,
                        "class_name": class_name,
                        "all_confidences": [float(c) for c in boxes.conf] if len(boxes.conf) > 0 else [],
                        "all_classes": [int(c) for c in boxes.cls] if len(boxes.cls) > 0 else []
                    }
                }
            else:
                return {
                    "is_valid": False,
                    "confidence": 0.0,
                    "model_used": model_name,
                    "raw_predictions": {},
                    "error": "No valid predictions found"
                }
                
        except Exception as e:
            logger.error(f"QA prediction failed: {str(e)}")
            raise

    def predict_obt(
        self,
        category: str,
        model_name: str,
        image_data: bytes
    ) -> Dict[str, Any]:
        """
        Run OBT (object detection) prediction to identify disease.
        
        Args:
            category: One of "crop", "fruit", "vegetable"
            model_name: Model name without .pt extension
            image_data: Image bytes
            
        Returns:
            Dict with keys:
            - detections: List[Dict] - List of detected objects/diseases
            - disease_class: str - Primary detected disease
            - confidence: float - Confidence of primary detection
            - model_used: str - Name of model used
            - image_analyzed: bool - Whether image was analyzed
        """
        try:
            # Load model
            model = self._load_obt_model(category, model_name)
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            
            # Run inference
            logger.info(f"Running OBT inference with {model_name}")
            results = model.predict(source=image, verbose=False, conf=0.25)
            
            if not results or len(results) == 0:
                return {
                    "detections": [],
                    "disease_class": "unknown",
                    "confidence": 0.0,
                    "model_used": model_name,
                    "image_analyzed": False,
                    "error": "No detections found"
                }
            
            result = results[0]
            
            # Process OBT predictions (disease detection)
            detections = []
            
            if result.boxes is not None and len(result.boxes) > 0:
                boxes = result.boxes
                
                for i in range(len(boxes)):
                    conf = boxes.conf[i].item() if i < len(boxes.conf) else 0.0
                    cls = int(boxes.cls[i].item()) if i < len(boxes.cls) else 0
                    
                    detection = {
                        "disease": model.names.get(cls, str(cls)) if model.names else str(cls),
                        "class_id": cls,
                        "confidence": float(conf),
                        "bbox": boxes.xyxy[i].tolist() if i < len(boxes.xyxy) else []
                    }
                    detections.append(detection)
                
                # Sort by confidence and get top detection
                detections = sorted(detections, key=lambda x: x["confidence"], reverse=True)
                primary_detection = detections[0]
                
                return {
                    "detections": detections,
                    "disease_class": primary_detection["disease"],
                    "confidence": primary_detection["confidence"],
                    "model_used": model_name,
                    "image_analyzed": True,
                    "total_detections": len(detections)
                }
            else:
                return {
                    "detections": [],
                    "disease_class": "healthy",
                    "confidence": 0.0,
                    "model_used": model_name,
                    "image_analyzed": True,
                    "error": "No disease detected"
                }
                
        except Exception as e:
            logger.error(f"OBT prediction failed: {str(e)}")
            raise

    def analyze_image(
        self,
        category: str,
        qa_model_name: str,
        obt_model_name: str,
        image_data: bytes
    ) -> Dict[str, Any]:
        """
        Full pipeline: QA validation -> OBT disease detection.
        
        Returns combined results from both stages.
        """
        try:
            # Stage 1: QA validation
            qa_result = self.predict_qa(category, qa_model_name, image_data)
            
            if not qa_result.get("is_valid", False):
                return {
                    "status": "invalid_image",
                    "qa_result": qa_result,
                    "obt_result": None,
                    "error": "Image failed quality assessment"
                }
            
            # Stage 2: OBT disease detection
            obt_result = self.predict_obt(category, obt_model_name, image_data)
            
            return {
                "status": "success",
                "qa_result": qa_result,
                "obt_result": obt_result,
                "category": category,
                "final_diagnosis": {
                    "disease_class": obt_result.get("disease_class", "unknown"),
                    "confidence": obt_result.get("confidence", 0.0),
                    "crop_class": qa_model_name.split("_")[0],  # Extract crop name from model name
                }
            }
            
        except Exception as e:
            logger.error(f"Image analysis pipeline failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "qa_result": None,
                "obt_result": None
            }
