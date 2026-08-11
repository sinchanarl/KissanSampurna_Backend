#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header() {
    echo
    echo "================================================================"
    echo "🌾 Kisaan Sampurna - Crop Disease Detection System"
    echo "================================================================"
    echo
}

# Cleanup function
cleanup() {
    echo
    print_info "Shutting down servers..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        print_status "Backend server stopped"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        print_status "Frontend server stopped"
    fi
    echo
    print_status "System shutdown complete"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

print_header

# Check if virtual environment exists
print_info "Checking virtual environment..."
if [ ! -f "venv/bin/activate" ]; then
    print_error "Virtual environment not found!"
    print_info "Please run: python setup.py"
    echo
    exit 1
fi

print_status "Virtual environment found"
echo

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi

print_status "Virtual environment activated"
echo

print_info "Starting Kisaan Sampurna System..."
echo

# Start backend server
print_info "Starting backend API server..."
print_info "  - Port: 8000"
print_info "  - URL: http://localhost:8000"

uvicorn app.app:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 5

# Check if backend is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    print_error "Backend server failed to start"
    print_info "Check backend.log for details"
    exit 1
fi

print_status "Backend server started (PID: $BACKEND_PID)"
echo

# Start frontend server
print_info "Starting frontend web server..."
print_info "  - Port: 3000"
print_info "  - URL: http://localhost:3000/frontend.html"

python -m http.server 3000 > frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a moment for frontend to start
sleep 3

# Check if frontend is running
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    print_error "Frontend server failed to start"
    print_info "Check frontend.log for details"
    cleanup
    exit 1
fi

print_status "Frontend server started (PID: $FRONTEND_PID)"
echo

# Success message
echo "================================================================"
print_status "System Started Successfully!"
echo "================================================================"
echo
print_info "🌐 Main Application: http://localhost:3000/frontend.html"
print_info "📚 API Documentation: http://localhost:8000/docs"
print_info "🧪 QA Testing: Run 'python test_qa_models.py' for http://localhost:8001"
echo
print_info "💡 Tips:"
print_info "   - Upload crop/fruit/vegetable images for analysis"
print_info "   - Follow the 4-step process in the web interface"
print_info "   - Check both QA and disease detection results"
echo
print_info "🔄 To restart: Press Ctrl+C and run this script again"
print_info "🛑 To stop: Press Ctrl+C"
echo

# Try to open browser (works on macOS and some Linux distributions)
if command -v open >/dev/null 2>&1; then
    print_info "Opening main application in browser..."
    sleep 2
    open http://localhost:3000/frontend.html
elif command -v xdg-open >/dev/null 2>&1; then
    print_info "Opening main application in browser..."
    sleep 2
    xdg-open http://localhost:3000/frontend.html
else
    print_info "Please open http://localhost:3000/frontend.html in your browser"
fi

echo
print_info "Press Ctrl+C to stop all servers"
echo

# Wait for interrupt
while true; do
    sleep 1
    # Check if processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        print_error "Backend server stopped unexpectedly"
        break
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        print_error "Frontend server stopped unexpectedly"
        break
    fi
done

cleanup