#!/bin/bash

# Ubuntu setup script for Activity Simulator
echo "Setting up Activity Simulator for Ubuntu..."

# Update package list
sudo apt-get update

# Install required system packages
echo "Installing system dependencies..."
sudo apt-get install -y wmctrl xdotool python3-pip python3-venv python3-tk python3-dev python3-xlib xautomation

# Install additional mouse control tools
echo "Installing additional mouse control tools..."
sudo apt-get install -y x11-utils x11-apps

# Set up X11 permissions
echo "Setting up X11 permissions..."
xhost +local: || echo "Warning: Could not set xhost permissions"

# Set DISPLAY variable if not set
if [ -z "$DISPLAY" ]; then
    export DISPLAY=:0
    echo "Set DISPLAY to :0"
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install additional Python packages for better Ubuntu support
echo "Installing additional Python packages..."
pip install python-xlib pynput

# Test mouse movement
echo "Testing mouse movement..."
python3 test_mouse_ubuntu.py

echo "Setup complete!"
echo ""
echo "=== Troubleshooting Mouse Movement ==="
echo "If mouse movement still doesn't work, try these steps:"
echo ""
echo "1. Check if running in a desktop environment:"
echo "   echo \$XDG_CURRENT_DESKTOP"
echo ""
echo "2. Set display manually:"
echo "   export DISPLAY=:0"
echo "   xhost +local:"
echo ""
echo "3. Test individual tools:"
echo "   xdotool mousemove 500 500"
echo "   xte 'mousemove 500 500'"
echo ""
echo "4. Check X11 permissions:"
echo "   xset q"
echo ""
echo "5. If running in VM/container, ensure:"
echo "   - Display forwarding is enabled"
echo "   - Guest additions are installed"
echo "   - X11 forwarding is configured"
echo ""
echo "6. Alternative: Run with sudo (not recommended):"
echo "   sudo python3 server.py"
echo ""
echo "To run the simulator:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the simulator: python server.py" 