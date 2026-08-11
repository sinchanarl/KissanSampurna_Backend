#!/usr/bin/env python3
"""
QA Models Test Interface with Real Model Inference.
This script creates a FastAPI server with a simple HTML interface to test QA model endpoints.
"""

import os
import logging
import io
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# ML dependencies
try:
    import torch
    from ultralytics import YOLO
    from PIL import Image
    ML_AVAILABLE = True
    print("✅ ML dependencies loaded successfully")
except ImportError as e:
    ML_AVAILABLE = False
    print(f"❌ ML dependencies not available: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="QA Models Test Interface", version="1.0.0")

# Model paths
MODELS_BASE_PATH = Path(__file__).parent / "app" / "assets"
CROP_QA_PATH = MODELS_BASE_PATH / "crop_models" / "crop_qa_models"
FRUIT_QA_PATH = MODELS_BASE_PATH / "fruit_models" / "fruit_qa_models"
VEGETABLE_QA_PATH = MODELS_BASE_PATH / "vegetable_models" / "vegetable_qa_models"

def get_model_files(model_dir: Path) -> List[str]:
    """Get list of .pt files in a directory."""
    if not model_dir.exists():
        logger.warning(f"Model directory not found: {model_dir}")
        return []
    
    files = []
    for file in model_dir.glob("*.pt"):
        model_name = file.stem
        files.append(model_name)
    
    return sorted(files)

def get_available_models() -> Dict[str, List[str]]:
    """Get all available QA models by category."""
    return {
        "crop": get_model_files(CROP_QA_PATH),
        "fruit": get_model_files(FRUIT_QA_PATH),
        "vegetable": get_model_files(VEGETABLE_QA_PATH),
    }

@app.get("/", response_class=HTMLResponse)
async def get_test_interface():
    """Serve the test interface HTML page."""
    models = get_available_models()
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QA Models Test Interface</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #2ecc71;
                text-align: center;
                margin-bottom: 30px;
            }}
            .form-group {{
                margin-bottom: 20px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #333;
            }}
            select, input[type="file"] {{
                width: 100%;
                padding: 10px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }}
            button {{
                background-color: #2ecc71;
                color: white;
                padding: 12px 30px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                width: 100%;
            }}
            button:hover {{
                background-color: #27ae60;
            }}
            button:disabled {{
                background-color: #bdc3c7;
                cursor: not-allowed;
            }}
            .result {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }}
            .result.success {{
                background-color: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }}
            .result.error {{
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }}
            .model-info {{
                background-color: #e9ecef;
                padding: 15px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            .loading {{
                text-align: center;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌾 QA Models Test Interface</h1>
            
            <div class="model-info">
                <h3>Available Models:</h3>
                <p><strong>Crops:</strong> {len(models['crop'])} models</p>
                <p><strong>Fruits:</strong> {len(models['fruit'])} models</p>
                <p><strong>Vegetables:</strong> {len(models['vegetable'])} models</p>
            </div>
            
            <form id="testForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="category">Category:</label>
                    <select id="category" name="category" required onchange="updateModels()">
                        <option value="">Select Category</option>
                        <option value="crop">Crop</option>
                        <option value="fruit">Fruit</option>
                        <option value="vegetable">Vegetable</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="model">QA Model:</label>
                    <select id="model" name="model" required disabled>
                        <option value="">Select Model</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="image">Upload Image:</label>
                    <input type="file" id="image" name="image" accept="image/*" required>
                </div>
                
                <button type="submit" id="submitBtn">Test QA Model</button>
            </form>
            
            <div id="result" class="result"></div>
        </div>

        <script>
            const models = {models};
            
            function updateModels() {{
                const category = document.getElementById('category').value;
                const modelSelect = document.getElementById('model');
                
                modelSelect.innerHTML = '<option value="">Select Model</option>';
                modelSelect.disabled = !category;
                
                if (category && models[category]) {{
                    models[category].forEach(model => {{
                        const option = document.createElement('option');
                        option.value = model;
                        option.textContent = model;
                        modelSelect.appendChild(option);
                    }});
                }}
            }}
            
            document.getElementById('testForm').addEventListener('submit', async function(e) {{
                e.preventDefault();
                
                const submitBtn = document.getElementById('submitBtn');
                const resultDiv = document.getElementById('result');
                
                submitBtn.disabled = true;
                submitBtn.textContent = 'Testing...';
                resultDiv.style.display = 'none';
                
                const formData = new FormData();
                formData.append('category', document.getElementById('category').value);
                formData.append('model_name', document.getElementById('model').value);
                formData.append('image', document.getElementById('image').files[0]);
                
                try {{
                    const response = await fetch('/test-qa', {{
                        method: 'POST',
                        body: formData
                    }});
                    
                    const result = await response.json();
                    
                    resultDiv.className = 'result ' + (response.ok ? 'success' : 'error');
                    resultDiv.innerHTML = '<pre>' + JSON.stringify(result, null, 2) + '</pre>';
                    resultDiv.style.display = 'block';
                    
                }} catch (error) {{
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '<strong>Error:</strong> ' + error.message;
                    resultDiv.style.display = 'block';
                }} finally {{
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Test QA Model';
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html_content

@app.get("/models")
async def get_models():
    """Get all available QA models."""
    return get_available_models()

@app.get("/models/{category}")
async def get_models_by_category(category: str):
    """Get QA models for a specific category."""
    if category not in ["crop", "fruit", "vegetable"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    models = get_available_models()
    return {
        "category": category,
        "models": models[category],
        "count": len(models[category])
    }

def determine_qa_validity(class_name: str, class_names: dict, top_class: int, top_confidence: float) -> bool:
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

def run_real_qa_inference(model_path: Path, image_data: bytes, model_name: str) -> Dict[str, Any]:
    """Run real QA model inference using YOLO."""
    try:
        # Load the model
        logger.info(f"Loading model: {model_path}")
        model = YOLO(str(model_path))
        
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        logger.info(f"Image loaded: {image.size}")
        
        # Run inference with lower confidence threshold for QA models
        logger.info("Running inference...")
        results = model.predict(source=image, verbose=False, conf=0.01)  # Lower threshold
        
        if not results or len(results) == 0:
            return {
                "is_valid": False,
                "confidence": 0.0,
                "model_used": model_name,
                "raw_predictions": {},
                "error": "No results returned from model"
            }
        
        result = results[0]
        logger.info(f"Model result type: {type(result)}")
        logger.info(f"Result attributes: {dir(result)}")
        
        # Debug: Check what's available in the result
        debug_info = {
            "has_boxes": hasattr(result, 'boxes') and result.boxes is not None,
            "has_probs": hasattr(result, 'probs') and result.probs is not None,
            "has_masks": hasattr(result, 'masks') and result.masks is not None,
            "has_keypoints": hasattr(result, 'keypoints') and result.keypoints is not None,
        }
        
        if hasattr(result, 'boxes') and result.boxes is not None:
            debug_info["boxes_count"] = len(result.boxes)
        if hasattr(result, 'probs') and result.probs is not None:
            debug_info["probs_shape"] = str(result.probs.data.shape) if hasattr(result.probs, 'data') else "unknown"
        
        logger.info(f"Debug info: {debug_info}")
        
        # Handle classification results (probs)
        if hasattr(result, 'probs') and result.probs is not None:
            probs = result.probs
            if hasattr(probs, 'data') and probs.data is not None:
                # Classification model
                confidences = probs.data.cpu().numpy()
                top_class = int(confidences.argmax())  # Convert to Python int
                top_confidence = float(confidences[top_class])
                
                # Get class names if available
                class_names = model.names if hasattr(model, 'names') else {}
                class_name = class_names.get(top_class, str(top_class))
                
                # Smart QA logic based on class names
                is_valid = determine_qa_validity(class_name, class_names, top_class, top_confidence)
                
                return {
                    "is_valid": is_valid,
                    "confidence": top_confidence,
                    "model_used": model_name,
                    "class_id": top_class,
                    "class_name": class_name,
                    "model_type": "classification",
                    "raw_predictions": {
                        "all_confidences": confidences.tolist(),
                        "top_class": top_class,
                        "top_confidence": top_confidence,
                        "class_names": dict(class_names) if class_names else {},  # Convert to regular dict
                        "total_classes": len(confidences)
                    }
                }
        
        # Handle detection results (boxes)
        elif hasattr(result, 'boxes') and result.boxes is not None and len(result.boxes) > 0:
            boxes = result.boxes
            conf = boxes.conf[0].item() if len(boxes.conf) > 0 else 0.0
            cls = int(boxes.cls[0].item()) if len(boxes.cls) > 0 else 0
            
            # For QA models, typically class 1 = valid, class 0 = invalid
            is_valid = cls == 1 if hasattr(model, 'names') and model.names else conf > 0.5
            
            class_name = model.names.get(cls, str(cls)) if hasattr(model, 'names') and model.names else str(cls)
            
            return {
                "is_valid": is_valid,
                "confidence": float(conf),
                "model_used": model_name,
                "class_id": cls,
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
            # No valid predictions found
            return {
                "is_valid": False,
                "confidence": 0.0,
                "model_used": model_name,
                "model_type": "unknown",
                "raw_predictions": debug_info,
                "error": "No valid predictions found (no boxes or classification results)"
            }
            
    except Exception as e:
        logger.error(f"Inference failed: {str(e)}")
        return {
            "is_valid": False,
            "confidence": 0.0,
            "model_used": model_name,
            "error": f"Inference failed: {str(e)}"
        }

@app.post("/test-qa")
async def test_qa_model(
    category: str = Form(...),
    model_name: str = Form(...),
    image: UploadFile = File(...)
):
    """Test a QA model with an uploaded image."""
    
    # Validate category
    if category not in ["crop", "fruit", "vegetable"]:
        raise HTTPException(status_code=400, detail="Invalid category")
    
    # Check if model exists
    models = get_available_models()
    if model_name not in models[category]:
        raise HTTPException(
            status_code=404, 
            detail=f"Model '{model_name}' not found in category '{category}'"
        )
    
    # Validate image file
    if not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Read image data
    try:
        image_data = await image.read()
        image_size = len(image_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading image: {str(e)}")
    
    # Get model path
    model_paths = {
        "crop": CROP_QA_PATH,
        "fruit": FRUIT_QA_PATH,
        "vegetable": VEGETABLE_QA_PATH,
    }
    
    model_path = model_paths[category] / f"{model_name}.pt"
    
    # Check if model file exists
    if not model_path.exists():
        raise HTTPException(status_code=404, detail=f"Model file not found: {model_path}")
    
    # Model info
    model_info = {
        "category": category,
        "model_name": model_name,
        "model_path": str(model_path),
        "model_exists": True,
        "model_size_mb": round(model_path.stat().st_size / (1024*1024), 2)
    }
    
    # Image info
    image_info = {
        "filename": image.filename,
        "content_type": image.content_type,
        "size_bytes": image_size,
        "size_mb": round(image_size / (1024*1024), 2)
    }
    
    # Run inference
    if ML_AVAILABLE:
        qa_result = run_real_qa_inference(model_path, image_data, model_name)
        
        return {
            "status": "success",
            "message": "Real QA model inference completed",
            "ml_available": True,
            "model_info": model_info,
            "image_info": image_info,
            "qa_result": qa_result
        }
    else:
        # Fallback to mock result
        return {
            "status": "success",
            "message": "QA model test completed (mock result - ML dependencies not installed)",
            "ml_available": False,
            "model_info": model_info,
            "image_info": image_info,
            "mock_qa_result": {
                "is_valid": True,
                "confidence": 0.85,
                "model_used": model_name,
                "note": "This is a mock result. Install PyTorch and Ultralytics for real inference."
            }
        }

if __name__ == "__main__":
    print("🌾 Starting QA Models Test Interface...")
    print("📍 Open http://localhost:8001 in your browser")
    print("📁 Make sure model files are in app/assets/ directories")
    
    uvicorn.run(
        "test_qa_models:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )