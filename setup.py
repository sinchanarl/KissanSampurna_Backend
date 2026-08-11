#!/usr/bin/env python3
"""
Setup script for Kisaan Sampurna - Crop Disease Detection System
This script helps users set up the environment and verify the installation.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    print("=" * 60)
    print("🌾 Kisaan Sampurna - Crop Disease Detection System")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major != 3 or version.minor < 11:
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  Python 3.11 or higher is required")
        print("📥 Please install Python 3.11+ from https://python.org")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_pip():
    """Check if pip is available."""
    print("\n📦 Checking pip...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✅ pip is available")
        return True
    except subprocess.CalledProcessError:
        print("❌ pip is not available")
        print("📥 Please install pip: https://pip.pypa.io/en/stable/installation/")
        return False

def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    print("\n🏗️  Setting up virtual environment...")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_activation_command():
    """Get the command to activate virtual environment."""
    system = platform.system().lower()
    if system == "windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install required dependencies."""
    print("\n📚 Installing dependencies...")
    
    # Determine pip executable
    system = platform.system().lower()
    if system == "windows":
        pip_exe = "venv\\Scripts\\pip"
    else:
        pip_exe = "venv/bin/pip"
    
    if not Path(pip_exe).exists():
        print("⚠️  Virtual environment not activated. Using system pip.")
        pip_exe = sys.executable + " -m pip"
    
    try:
        # Upgrade pip first
        print("📈 Upgrading pip...")
        subprocess.run(f"{pip_exe} install --upgrade pip", shell=True, check=True)
        
        # Install requirements
        print("📦 Installing packages from requirements.txt...")
        subprocess.run(f"{pip_exe} install -r requirements.txt", shell=True, check=True)
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running manually:")
        print(f"   {get_activation_command()}")
        print(f"   pip install -r requirements.txt")
        return False

def check_model_files():
    """Check if model files are present."""
    print("\n🤖 Checking model files...")
    
    model_dirs = [
        "app/assets/crop_models/crop_qa_models",
        "app/assets/crop_models/crop_obt_models",
        "app/assets/fruit_models/fruit_qa_models",
        "app/assets/fruit_models/fruits_obt_models",
        "app/assets/vegetable_models/vegetable_qa_models",
        "app/assets/vegetable_models/vegetables_obt_models",
    ]
    
    total_models = 0
    for model_dir in model_dirs:
        path = Path(model_dir)
        if path.exists():
            pt_files = list(path.glob("*.pt"))
            total_models += len(pt_files)
            print(f"✅ {model_dir}: {len(pt_files)} models")
        else:
            print(f"⚠️  {model_dir}: Directory not found")
    
    print(f"\n📊 Total models found: {total_models}")
    
    if total_models == 0:
        print("❌ No model files found!")
        print("📁 Please ensure model files (.pt) are in the correct directories")
        return False
    
    return True

def test_imports():
    """Test if critical imports work."""
    print("\n🧪 Testing critical imports...")
    
    imports_to_test = [
        ("fastapi", "FastAPI web framework"),
        ("uvicorn", "ASGI server"),
        ("torch", "PyTorch ML framework"),
        ("ultralytics", "YOLO models"),
        ("PIL", "Image processing"),
    ]
    
    failed_imports = []
    
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\n⚠️  Failed imports: {', '.join(failed_imports)}")
        print("💡 Try reinstalling dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_startup_scripts():
    """Create convenient startup scripts."""
    print("\n📝 Creating startup scripts...")
    
    # Windows batch file
    windows_script = """@echo off
echo Starting Kisaan Sampurna System...
echo.

echo Activating virtual environment...
call venv\\Scripts\\activate

echo Starting backend server...
start "Backend API" cmd /k "uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo Starting frontend server...
start "Frontend Server" cmd /k "python -m http.server 3000"

echo.
echo ✅ System started successfully!
echo 🌐 Open http://localhost:3000/frontend.html in your browser
echo 📚 API docs: http://localhost:8000/docs
echo.
pause
"""
    
    # Unix shell script
    unix_script = """#!/bin/bash
echo "Starting Kisaan Sampurna System..."
echo

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting backend server..."
uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

sleep 3

echo "Starting frontend server..."
python -m http.server 3000 &
FRONTEND_PID=$!

echo
echo "✅ System started successfully!"
echo "🌐 Open http://localhost:3000/frontend.html in your browser"
echo "📚 API docs: http://localhost:8000/docs"
echo
echo "Press Ctrl+C to stop all servers"

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
"""
    
    try:
        with open("start_system.bat", "w") as f:
            f.write(windows_script)
        print("✅ Created start_system.bat (Windows)")
        
        with open("start_system.sh", "w") as f:
            f.write(unix_script)
        os.chmod("start_system.sh", 0o755)
        print("✅ Created start_system.sh (Unix/Linux/macOS)")
        
        return True
    except Exception as e:
        print(f"⚠️  Could not create startup scripts: {e}")
        return False

def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete! Next Steps:")
    print("=" * 60)
    
    system = platform.system().lower()
    
    print("\n1️⃣  Activate virtual environment:")
    if system == "windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2️⃣  Start the system:")
    print("   Option A - Use startup script:")
    if system == "windows":
        print("     start_system.bat")
    else:
        print("     ./start_system.sh")
    
    print("\n   Option B - Manual start:")
    print("     Terminal 1: uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload")
    print("     Terminal 2: python -m http.server 3000")
    
    print("\n3️⃣  Access the application:")
    print("   🌐 Main App: http://localhost:3000/frontend.html")
    print("   📚 API Docs: http://localhost:8000/docs")
    print("   🧪 QA Testing: python test_qa_models.py (then http://localhost:8001)")
    
    print("\n4️⃣  Test with sample images:")
    print("   - Upload crop/fruit/vegetable images")
    print("   - Follow the 4-step process in the web interface")
    print("   - Check both QA and disease detection results")
    
    print("\n📞 Need help? Check README.md for troubleshooting")
    print("=" * 60)

def main():
    """Main setup function."""
    print_header()
    
    # Check prerequisites
    if not check_python_version():
        return False
    
    if not check_pip():
        return False
    
    # Setup environment
    if not create_virtual_environment():
        return False
    
    if not install_dependencies():
        return False
    
    # Verify installation
    if not check_model_files():
        print("⚠️  Continuing without model verification...")
    
    if not test_imports():
        return False
    
    # Create convenience scripts
    create_startup_scripts()
    
    # Show next steps
    print_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)