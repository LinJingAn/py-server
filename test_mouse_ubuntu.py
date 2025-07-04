#!/usr/bin/env python3
"""
Test script to diagnose mouse movement issues on Ubuntu
"""

import platform
import time
import subprocess
import sys

print(f"Platform: {platform.system()}")
print(f"Python version: {sys.version}")

try:
    import pyautogui
    print("✓ pyautogui imported successfully")
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    print(f"Screen size: {screen_width}x{screen_height}")
    
    # Get current mouse position
    current_x, current_y = pyautogui.position()
    print(f"Current mouse position: ({current_x}, {current_y})")
    
    # Test simple mouse movement
    print("Testing mouse movement...")
    target_x = min(current_x + 100, screen_width - 10)
    target_y = min(current_y + 100, screen_height - 10)
    
    print(f"Moving mouse to: ({target_x}, {target_y})")
    pyautogui.moveTo(target_x, target_y, duration=1.0)
    
    new_x, new_y = pyautogui.position()
    print(f"New mouse position: ({new_x}, {new_y})")
    
    if (new_x, new_y) != (current_x, current_y):
        print("✓ Mouse movement successful!")
    else:
        print("✗ Mouse movement failed - cursor didn't move")
        
except ImportError as e:
    print(f"✗ Failed to import pyautogui: {e}")
    print("Try installing: pip install pyautogui")

# Check for X11 display
if platform.system() != "Windows":
    print("\n--- X11 Display Check ---")
    try:
        result = subprocess.run(['echo', '$DISPLAY'], capture_output=True, text=True, shell=True)
        print(f"DISPLAY variable: {result.stdout.strip()}")
        
        result = subprocess.run(['xset', 'q'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ X11 display is accessible")
        else:
            print("✗ X11 display not accessible")
            print("Try: export DISPLAY=:0")
            
    except Exception as e:
        print(f"Error checking X11: {e}")

# Alternative mouse movement methods
print("\n--- Alternative Solutions ---")
print("If mouse movement doesn't work, try these alternatives:")

print("\n1. Install additional dependencies:")
print("   sudo apt-get install python3-tk python3-dev python3-xlib")

print("\n2. Set DISPLAY variable:")
print("   export DISPLAY=:0")

print("\n3. Use xdotool for mouse movement:")
print("   sudo apt-get install xdotool")
print("   xdotool mousemove 500 500")

print("\n4. Check if running in a virtual environment or container")
print("   Some environments may not support mouse movement")

print("\n5. Try running with sudo (not recommended but may work):")
print("   sudo python3 test_mouse_ubuntu.py") 