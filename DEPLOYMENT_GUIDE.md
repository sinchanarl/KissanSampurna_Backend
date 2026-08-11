# 🚀 Deployment Guide - Kisaan Sampurna

Complete guide for packaging and distributing the Kisaan Sampurna system.

## 📦 Creating Distribution Package

### Step 1: Prepare the Package
```bash
# Navigate to project root
cd kisaansampurna-backend

# Clean up unnecessary files
rm -rf __pycache__ .pytest_cache .DS_Store
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

### Step 2: Create ZIP Package
```bash
# Create distribution directory
mkdir -p ../kisaan-sampurna-distribution

# Copy all necessary files
cp -r . ../kisaan-sampurna-distribution/kisaansampurna-backend/

# Navigate to distribution directory
cd ../kisaan-sampurna-distribution

# Create ZIP file
zip -r kisaan-sampurna-system.zip kisaansampurna-backend/ \
    -x "kisaansampurna-backend/.git/*" \
    -x "kisaansampurna-backend/venv/*" \
    -x "kisaansampurna-backend/.venv/*" \
    -x "kisaansampurna-backend/__pycache__/*" \
    -x "kisaansampurna-backend/.pytest_cache/*" \
    -x "kisaansampurna-backend/*.log"
```

## 📋 Distribution Checklist

### Essential Files to Include:
- ✅ `README.md` - Complete setup instructions
- ✅ `requirements.txt` - Python dependencies
- ✅ `setup.py` - Automated setup script
- ✅ `frontend.html` - Web interface
- ✅ `test_qa_models.py` - QA testing interface
- ✅ `check_models.py` - Model verification
- ✅ `app/` directory - Complete backend application
- ✅ `app/assets/` - All model files (.pt files)
- ✅ Startup scripts (`start_system.bat`, `start_system.sh`)

### Files to Exclude:
- ❌ `.git/` - Git repository
- ❌ `venv/`, `.venv/` - Virtual environments
- ❌ `__pycache__/` - Python cache
- ❌ `.pytest_cache/` - Test cache
- ❌ `*.log` - Log files
- ❌ `.DS_Store` - macOS system files
- ❌ `node_modules/` - If any Node.js dependencies

## 📧 Distribution Instructions for Recipients

### Quick Start Commands
```bash
# 1. Extract the package
unzip kisaan-sampurna-system.zip
cd kisaansampurna-backend

# 2. Run automated setup
python setup.py

# 3. Start the system (after setup completes)
# Windows:
start_system.bat
# macOS/Linux:
./start_system.sh
```

### Manual Setup (if automated setup fails)
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify models
python check_models.py

# 5. Start backend
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

# 6. Start frontend (new terminal)
python -m http.server 3000

# 7. Access application
# http://localhost:3000/frontend.html
```

## 🔧 System Requirements for Recipients

### Minimum Requirements:
- **Python**: 3.11+ (3.12 recommended)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 5GB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Internet**: Required for initial package installation

### Recommended Setup:
- **CPU**: Multi-core processor (4+ cores)
- **GPU**: NVIDIA GPU with CUDA support (optional)
- **RAM**: 16GB or more
- **SSD**: For faster model loading

## 🧪 Testing Instructions for Recipients

### 1. Verify Installation
```bash
# Check Python version
python --version

# Verify all models are present
python check_models.py

# Test imports
python -c "import torch, ultralytics, fastapi; print('All imports successful')"
```

### 2. Test QA Models Only
```bash
# Start QA testing interface
python test_qa_models.py

# Open http://localhost:8001
# Upload test images to verify QA models work
```

### 3. Test Complete System
```bash
# Start full system
# Backend: uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload
# Frontend: python -m http.server 3000

# Open http://localhost:3000/frontend.html
# Test the 4-step process with sample images
```

### 4. API Testing
```bash
# Test API endpoints
curl http://localhost:8000/api/v1/analyze/crops/qa-models
curl http://localhost:8000/docs  # Interactive API documentation
```

## 🚨 Common Issues and Solutions

### Issue 1: Python Version Incompatibility
**Problem**: "Python 3.x is not supported"
**Solution**: 
```bash
# Install Python 3.11 or 3.12
# Windows: Download from python.org
# macOS: brew install python@3.11
# Ubuntu: sudo apt install python3.11
```

### Issue 2: PyTorch Installation Fails
**Problem**: "Could not find a version that satisfies the requirement torch"
**Solution**:
```bash
# Install CPU-only version (smaller, more compatible)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Or for CUDA support:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Issue 3: Model Files Missing
**Problem**: "Model file not found"
**Solution**:
```bash
# Verify extraction
python check_models.py

# Ensure .pt files are in correct directories:
# app/assets/crop_models/crop_qa_models/*.pt
# app/assets/crop_models/crop_obt_models/*.pt
# etc.
```

### Issue 4: Port Already in Use
**Problem**: "Address already in use"
**Solution**:
```bash
# Use different ports
uvicorn app.app:app --port 8001
python -m http.server 3001

# Or kill existing processes:
# Windows: netstat -ano | findstr :8000
# macOS/Linux: lsof -ti:8000 | xargs kill
```

### Issue 5: CORS Errors in Browser
**Problem**: "Access blocked by CORS policy"
**Solution**:
- Ensure both servers are running
- Access via http://localhost:3000 (not 127.0.0.1)
- Check browser console for specific errors

## 📊 Performance Optimization

### For Better Speed:
1. **GPU Acceleration**: Install CUDA-enabled PyTorch
2. **SSD Storage**: Store models on SSD for faster loading
3. **More RAM**: Increase system RAM for better caching

### For Lower Resource Usage:
1. **CPU-Only Mode**: Use CPU-only PyTorch installation
2. **Reduce Concurrent Users**: Limit simultaneous analyses
3. **Close Unused Services**: Stop QA testing interface when not needed

## 📞 Support Information

### Log Files Location:
- Backend logs: Terminal output where uvicorn is running
- Model inference: Check console output during analysis
- Browser errors: Developer Tools → Console

### Debug Commands:
```bash
# Verbose logging
uvicorn app.app:app --log-level debug

# Check system info
python -c "import sys, torch; print(f'Python: {sys.version}'); print(f'PyTorch: {torch.__version__}')"

# Memory usage
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"
```

### Contact Information:
- Include your contact details here
- GitHub repository (if applicable)
- Email for technical support
- Documentation website (if available)

## 🔄 Updates and Maintenance

### Adding New Models:
1. Place `.pt` files in appropriate directories
2. Restart backend server
3. Models automatically detected

### Updating System:
1. Replace files with new version
2. Update requirements.txt if needed
3. Run setup.py again
4. Restart services

---

**Package prepared by**: [Your Name]  
**Date**: [Current Date]  
**Version**: 1.0.0  
**Contact**: [Your Contact Information]