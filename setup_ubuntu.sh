#!/bin/bash

# Ubuntu setup script for Activity Simulator
echo "Setting up Activity Simulator for Ubuntu..."

# Update package list
sudo apt-get update

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y wmctrl xdotool python3-pip python3-venv

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the simulator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the simulator: python server.py" 