#!/usr/bin/env python3
"""
Simple mouse movement test script
"""

import time
import subprocess
import platform

print("=== Simple Mouse Movement Test ===")
print(f"Platform: {platform.system()}")

# Test 1: xdotool
print("\n--- Test 1: xdotool ---")
try:
    # Get current position
    result = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
    print(f"Current position: {result.stdout.strip()}")
    
    # Move mouse
    print("Moving mouse with xdotool...")
    subprocess.run(['xdotool', 'mousemove', '500', '500'])
    time.sleep(1)
    
    # Check new position
    result = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
    print(f"New position: {result.stdout.strip()}")
    print("✓ xdotool test completed")
    
except Exception as e:
    print(f"✗ xdotool failed: {e}")

# Test 2: pyautogui
print("\n--- Test 2: pyautogui ---")
try:
    import pyautogui
    
    # Get current position
    pos = pyautogui.position()
    print(f"Current position: {pos}")
    
    # Move mouse
    print("Moving mouse with pyautogui...")
    pyautogui.moveTo(600, 600, duration=1)
    time.sleep(1)
    
    # Check new position
    new_pos = pyautogui.position()
    print(f"New position: {new_pos}")
    print("✓ pyautogui test completed")
    
except Exception as e:
    print(f"✗ pyautogui failed: {e}")

# Test 3: Check if mouse actually moved
print("\n--- Test 3: Verification ---")
try:
    # Get final position with both methods
    xdotool_result = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
    pyautogui_pos = pyautogui.position()
    
    print(f"xdotool position: {xdotool_result.stdout.strip()}")
    print(f"pyautogui position: {pyautogui_pos}")
    
    # Check if positions are reasonable (should be around 500-600 range)
    if "x:500" in xdotool_result.stdout or "x:600" in xdotool_result.stdout:
        print("✓ Mouse appears to have moved!")
    else:
        print("⚠️  Mouse may not have moved as expected")
        
except Exception as e:
    print(f"✗ Verification failed: {e}")

print("\n=== Test Complete ===")
print("If mouse didn't move, possible issues:")
print("1. Running in a VM without proper display forwarding")
print("2. X11 permissions issues")
print("3. Display server configuration")
print("4. Running in a headless environment") 