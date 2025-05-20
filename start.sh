#!/bin/bash

# Check for Python 3
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi
echo "Python 3 found."

# Virtual Environment
if [ ! -d "venv" ]; then
    echo "Creating Python 3 virtual environment 'venv'..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
    echo "Virtual environment 'venv' created."
else
    echo "Virtual environment 'venv' already exists."
fi

# Activate Virtual Environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi
echo "Virtual environment activated."

# Install Dependencies
echo "Installing dependencies from requirements.txt..."
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found."
    # Deactivate venv on error
    deactivate
    exit 1
fi
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    # Deactivate venv on error
    deactivate
    exit 1
fi
echo "Dependencies installed successfully or were already up-to-date."

# Start Application
echo "Starting Docling-webui.py in the background..."
python3 Docling-webui.py &
if [ $? -ne 0 ]; then
    echo "Error: Failed to start Docling-webui.py."
    # Deactivate venv on error
    deactivate
    exit 1
fi
echo "Docling-webui.py is starting. Check its console output for the exact URL and port."

# Open Browser
echo "Waiting for the server to start..."
sleep 5 # Wait for 5 seconds

# Attempt to open the browser
echo "Attempting to open http://localhost:7860 in your browser."
echo "Please check the console output from Docling-webui.py for the actual address if it's different."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:7860
elif command -v open &> /dev/null; then
    open http://localhost:7860
else
    echo "Could not find xdg-open or open. Please open http://localhost:7860 (or the address shown in the Docling-webui.py console) in your browser manually."
fi

echo "Script finished. The application should be running in the background."
# Note: The virtual environment remains active in the current shell if this script is sourced.
# If the script is run directly (./start.sh), the venv activation is local to the script.
# For Docling-webui.py running in the background, it uses the activated venv.
