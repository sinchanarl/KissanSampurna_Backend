@echo off
title Kisaan Sampurna - Crop Disease Detection System
color 0A

echo.
echo ================================================================
echo 🌾 Kisaan Sampurna - Crop Disease Detection System
echo ================================================================
echo.

echo 🔍 Checking virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo 💡 Please run: python setup.py
    echo.
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo.

echo 🐍 Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 🚀 Starting Kisaan Sampurna System...
echo.

echo 📡 Starting backend API server...
echo    - Port: 8000
echo    - URL: http://localhost:8000
start "Kisaan Sampurna - Backend API" cmd /k "uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo ⏳ Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo 🌐 Starting frontend web server...
echo    - Port: 3000  
echo    - URL: http://localhost:3000/frontend.html
start "Kisaan Sampurna - Frontend" cmd /k "python -m http.server 3000"

echo.
echo ⏳ Waiting for frontend to start...
timeout /t 3 /nobreak > nul

echo.
echo ================================================================
echo ✅ System Started Successfully!
echo ================================================================
echo.
echo 🌐 Main Application: http://localhost:3000/frontend.html
echo 📚 API Documentation: http://localhost:8000/docs
echo 🧪 QA Testing: Run 'python test_qa_models.py' for http://localhost:8001
echo.
echo 💡 Tips:
echo    - Upload crop/fruit/vegetable images for analysis
echo    - Follow the 4-step process in the web interface
echo    - Check both QA and disease detection results
echo.
echo 🔄 To restart: Close all windows and run this script again
echo 🛑 To stop: Close the backend and frontend terminal windows
echo.

echo 🚀 Opening main application in browser...
timeout /t 2 /nobreak > nul
start http://localhost:3000/frontend.html

echo.
echo Press any key to exit this window (servers will keep running)...
pause > nul