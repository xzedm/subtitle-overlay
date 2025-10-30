#!/bin/bash

echo "Starting Subtitle Overlay Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Checking dependencies..."
python3 -c "import PyQt6; import websockets" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "Starting application..."
echo "The app will minimize to the system tray."
echo ""

python3 app/main.py



