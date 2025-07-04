#!/bin/bash

# Ubuntu setup script for Activity Simulator
echo "Setting up Activity Simulator for Ubuntu..."

# Update package list
sudo apt-get update

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y wmctrl xdotool python3-pip python3-venv python3-tk python3-dev python3-xlib

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Test mouse movement
echo "Testing mouse movement..."
python3 test_mouse_ubuntu.py

echo "Setup complete!"
echo "To run the simulator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the simulator: python server.py"
echo ""
echo "If mouse movement doesn't work, try:"
echo "1. export DISPLAY=:0"
echo "2. xhost +local:"
echo "3. Run the test script: python test_mouse_ubuntu.py" 