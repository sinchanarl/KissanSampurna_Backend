# 🌾 Kisaan Sampurna - Crop Disease Detection System

AI-powered crop disease detection system with quality assessment and disease classification.

## 📋 System Requirements

### Hardware Requirements
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: At least 5GB free space for models
- **CPU**: Multi-core processor (GPU optional but recommended)

### Software Requirements
- **Python**: 3.11 or 3.12 (3.11 recommended)
- **Operating System**: Windows 10+, macOS 10.15+, or Linux Ubuntu 18.04+

## 🚀 Quick Start Guide

### Step 1: Extract and Navigate
```bash
# Extract the zip file
unzip kisaan-sampurna-system.zip
cd kisaansampurna-backend
```

### Step 2: Create Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# For GPU support (optional):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Step 4: Verify Model Files
```bash
# Check if all model files are present
python check_models.py
```

### Step 5: Start the System
```bash
# Terminal 1: Start the main backend API
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start the frontend server
python -m http.server 3000

# Terminal 3 (Optional): Start QA testing interface
python test_qa_models.py
```

### Step 6: Access the Application
- **Main Application**: http://localhost:3000/frontend.html
- **QA Testing Interface**: http://localhost:8001 (if running)
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
kisaansampurna-backend/
├── app/                          # Main application
│   ├── assets/                   # Model files
│   │   ├── crop_models/
│   │   │   ├── crop_qa_models/   # Quality assessment models
│   │   │   └── crop_obt_models/  # Disease detection models
│   │   ├── fruit_models/
│   │   └── vegetable_models/
│   ├── routers/                  # API endpoints
│   ├── services/                 # Business logic
│   └── app.py                    # Main application
├── frontend.html                 # Web interface
├── test_qa_models.py            # QA model testing
├── check_models.py              # Model verification
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Model Configuration
MODEL_CONFIDENCE_THRESHOLD=0.25
QA_CONFIDENCE_THRESHOLD=0.01

# CORS Settings
ALLOWED_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 🧪 Testing the System

### 1. Test Individual QA Models
```bash
# Start QA testing interface
python test_qa_models.py

# Open http://localhost:8001 in browser
# Upload test images to verify QA models work
```

### 2. Test Complete Pipeline
```bash
# Open main application
# http://localhost:3000/frontend.html

# Follow the 4-step process:
# 1. Select category (crop/fruit/vegetable)
# 2. Choose QA and disease detection models
# 3. Upload an image
# 4. View results
```

### 3. Test API Endpoints
```bash
# Get available models
curl http://localhost:8000/api/v1/analyze/crops/qa-models

# Test image analysis (replace with actual image file)
curl -X POST "http://localhost:8000/api/v1/analyze/crops?qa_model=rice_crop_qa&obt_model=rice_crop_model" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
```

## 📊 Available Models

### Crop Models (13 QA + 13 Disease Detection)
- Rice, Cotton, Tomato, Potato, Corn, Cucumber
- Grape, Orange, Strawberry, Sugarcane, Pepperbell
- Cashew, Paddy

### Fruit Models (7 QA + 7 Disease Detection)
- Grape, Orange, Strawberry, Tomato
- Cashew, Cotton, Paddy

### Vegetable Models (4 QA + 4 Disease Detection)
- Corn, Cucumber, Pepperbell, Potato

## 🔍 How It Works

### Quality Assessment (QA) Pipeline
1. **Input**: User uploads an image
2. **QA Model**: Validates if image contains the expected crop/fruit/vegetable
3. **Smart Logic**: Interprets class names (e.g., "Cotton_Leaf" = valid, "Not_Cotton_Leaf" = invalid)
4. **Output**: Boolean validity + confidence score

### Disease Detection (OBT) Pipeline
1. **Input**: QA-validated image
2. **Disease Model**: Detects diseases/conditions in the image
3. **Processing**: Identifies disease classes with bounding boxes
4. **Output**: Disease name + confidence + detection details

### Combined Results
- **Valid Image**: QA passes → Disease detection runs → Full results
- **Invalid Image**: QA fails → Disease detection skipped → QA-only results
- **Error Handling**: Comprehensive error messages and fallbacks

## 🚨 Troubleshooting

### Common Issues

#### 1. "No module named 'torch'"
```bash
# Install PyTorch
pip install torch torchvision

# For CPU-only (smaller download):
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

#### 2. "Model file not found"
```bash
# Verify model files exist
python check_models.py

# Ensure all .pt files are in correct directories
ls app/assets/crop_models/crop_qa_models/
```

#### 3. "Port already in use"
```bash
# Use different ports
uvicorn app.app:app --port 8001
python -m http.server 3001
```

#### 4. "CORS error in browser"
- Ensure both frontend (port 3000) and backend (port 8000) are running
- Check browser console for specific error messages
- Try accessing http://localhost:3000/frontend.html (not 127.0.0.1)

#### 5. "Memory error during inference"
```bash
# Reduce batch size or use CPU-only mode
export CUDA_VISIBLE_DEVICES=""  # Force CPU usage
```

### Performance Optimization

#### For Better Speed
1. **Use GPU**: Install CUDA-enabled PyTorch
2. **Model Caching**: Models are cached after first load
3. **Reduce Image Size**: Resize large images before upload

#### For Lower Memory Usage
1. **CPU Mode**: Use CPU-only PyTorch installation
2. **Close Unused Services**: Stop QA testing interface if not needed

## 📞 Support

### Log Files
- Backend logs: Check terminal running uvicorn
- Model inference logs: Check terminal output during analysis
- Browser logs: Open Developer Tools → Console

### Debug Mode
```bash
# Run with debug logging
uvicorn app.app:app --log-level debug --reload
```

### API Documentation
- Interactive API docs: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## 🔄 Updates and Maintenance

### Adding New Models
1. Place `.pt` files in appropriate directories:
   - QA models: `app/assets/{category}_models/{category}_qa_models/`
   - Disease models: `app/assets/{category}_models/{category}_obt_models/`
2. Restart the backend server
3. Models will be automatically detected

### Updating Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade ultralytics
```

## 📄 License

This project is for educational and research purposes. Please ensure you have proper licenses for all model files and dependencies.

## 🤝 Contributing

For issues, improvements, or questions, please contact the development team.

---

**Happy Disease Detection! 🌾🔬**