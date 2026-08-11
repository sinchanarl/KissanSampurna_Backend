# 📦 Distribution Commands - Quick Reference

## 🚀 For You (Package Creator)

### 1. Create Distribution Package
```bash
# Navigate to your project
cd kisaansampurna-backend

# Create the distribution package
python create_package.py
```

This will create:
- `../kisaan-sampurna-distribution/` folder
- `kisaan-sampurna-system_YYYYMMDD_HHMMSS.zip` file
- `PACKAGE_INFO.md` with instructions

### 2. Share with Others
Send these files to recipients:
- ✅ `kisaan-sampurna-system_YYYYMMDD_HHMMSS.zip` (main package)
- ✅ `PACKAGE_INFO.md` (quick start guide)

---

## 👥 For Recipients (People Testing Your System)

### Option A: Automated Setup (Recommended)
```bash
# 1. Extract package
unzip kisaan-sampurna-system_*.zip
cd kisaansampurna-backend

# 2. Run automated setup
python setup.py

# 3. Start system
# Windows:
start_system.bat

# macOS/Linux:
./start_system.sh
```

### Option B: Manual Setup
```bash
# 1. Extract package
unzip kisaan-sampurna-system_*.zip
cd kisaansampurna-backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify models
python check_models.py

# 6. Start backend (Terminal 1)
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload

# 7. Start frontend (Terminal 2)
python -m http.server 3000

# 8. Open application
# http://localhost:3000/frontend.html
```

---

## 🧪 Testing Commands

### Test QA Models Only
```bash
python test_qa_models.py
# Then open: http://localhost:8001
```

### Test API Endpoints
```bash
# Get available models
curl http://localhost:8000/api/v1/analyze/crops/qa-models

# API documentation
curl http://localhost:8000/docs
```

### Verify Installation
```bash
# Check models
python check_models.py

# Test imports
python -c "import torch, ultralytics, fastapi; print('✅ All imports successful')"
```

---

## 🔧 System Requirements

### Minimum Requirements:
- **Python**: 3.11+ (download from python.org)
- **RAM**: 8GB minimum
- **Storage**: 5GB free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### Installation Links:
- **Python**: https://python.org/downloads/
- **Git** (optional): https://git-scm.com/downloads

---

## 🚨 Common Issues & Solutions

### "Python not found"
```bash
# Install Python 3.11+ from python.org
# Ensure it's added to PATH during installation
python --version  # Should show 3.11+
```

### "pip not found"
```bash
# Usually comes with Python, but if missing:
python -m ensurepip --upgrade
```

### "torch installation fails"
```bash
# Try CPU-only version (smaller, more compatible)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### "Port already in use"
```bash
# Use different ports
uvicorn app.app:app --port 8001
python -m http.server 3001
```

### "No model files found"
```bash
# Verify extraction
python check_models.py
# Ensure .pt files are in app/assets/ subdirectories
```

---

## 📞 Support Checklist

Before asking for help, please run:
```bash
# 1. Check Python version
python --version

# 2. Check model files
python check_models.py

# 3. Test basic imports
python -c "import sys; print('Python:', sys.version)"
python -c "import torch; print('PyTorch:', torch.__version__)"
python -c "import ultralytics; print('Ultralytics: OK')"
python -c "import fastapi; print('FastAPI: OK')"

# 4. Check system resources
python -c "import psutil; print('RAM:', psutil.virtual_memory().percent, '%')"
```

Include this output when reporting issues!

---

**Package Version**: 1.0.0  
**Last Updated**: [Current Date]  
**Contact**: [Your Contact Info]