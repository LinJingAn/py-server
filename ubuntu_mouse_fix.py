#!/usr/bin/env python3
"""
Ubuntu Mouse Movement Troubleshooting Script
"""

import platform
import subprocess
import os
import sys

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n--- {description} ---")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Success: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_environment():
    """Check the current environment"""
    print("=== Environment Check ===")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.version}")
    print(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    print(f"USER: {os.environ.get('USER', 'Not set')}")
    print(f"XDG_CURRENT_DESKTOP: {os.environ.get('XDG_CURRENT_DESKTOP', 'Not set')}")

def check_x11():
    """Check X11 setup"""
    print("\n=== X11 Check ===")
    
    # Check if X11 is running
    run_command("xset q", "X11 Server Status")
    
    # Check display permissions
    run_command("xhost", "X11 Display Permissions")
    
    # Check if we can connect to X11
    run_command("xrandr", "X11 Display Info")

def check_tools():
    """Check if required tools are installed"""
    print("\n=== Tools Check ===")
    
    tools = [
        ("xdotool", "xdotool --version"),
        ("xte", "xte --help"),
        ("wmctrl", "wmctrl --version"),
        ("python3-tk", "python3 -c 'import tkinter; print(\"tkinter available\")'"),
        ("python-xlib", "python3 -c 'import Xlib; print(\"Xlib available\")'"),
        ("pynput", "python3 -c 'import pynput; print(\"pynput available\")'"),
    ]
    
    for tool, cmd in tools:
        run_command(cmd, f"{tool} Check")

def test_mouse_movement():
    """Test different mouse movement methods"""
    print("\n=== Mouse Movement Tests ===")
    
    # Test xdotool
    print("\n--- Testing xdotool ---")
    current_pos = subprocess.run("xdotool getmouselocation", shell=True, capture_output=True, text=True)
    print(f"Current position: {current_pos.stdout.strip()}")
    
    run_command("xdotool mousemove 500 500", "xdotool absolute movement")
    run_command("xdotool mousemove_relative 100 100", "xdotool relative movement")
    
    # Test xte
    print("\n--- Testing xte ---")
    run_command("xte 'mousemove 600 600'", "xte mouse movement")
    
    # Test pyautogui
    print("\n--- Testing pyautogui ---")
    try:
        import pyautogui
        print("✓ pyautogui imported")
        pos = pyautogui.position()
        print(f"Current position: {pos}")
        pyautogui.moveTo(700, 700, duration=1)
        print("✓ pyautogui movement test")
    except Exception as e:
        print(f"✗ pyautogui failed: {e}")
    
    # Test pynput
    print("\n--- Testing pynput ---")
    try:
        from pynput import mouse
        controller = mouse.Controller()
        pos = controller.position
        print(f"Current position: {pos}")
        controller.position = (800, 800)
        print("✓ pynput movement test")
    except Exception as e:
        print(f"✗ pynput failed: {e}")

def fix_common_issues():
    """Try to fix common issues"""
    print("\n=== Fixing Common Issues ===")
    
    # Set DISPLAY if not set
    if not os.environ.get('DISPLAY'):
        os.environ['DISPLAY'] = ':0'
        print("Set DISPLAY=:0")
    
    # Allow local connections
    run_command("xhost +local:", "Allow local X11 connections")
    
    # Check if running as root
    if os.geteuid() == 0:
        print("⚠️  Running as root - this may cause issues")
        print("Try running as regular user")

def provide_solutions():
    """Provide solutions based on test results"""
    print("\n=== Solutions ===")
    print("If mouse movement still doesn't work:")
    print()
    print("1. Install missing packages:")
    print("   sudo apt-get install xdotool xautomation python3-tk python3-xlib")
    print("   pip install pynput python-xlib")
    print()
    print("2. Set up X11 permissions:")
    print("   export DISPLAY=:0")
    print("   xhost +local:")
    print()
    print("3. If running in VM/container:")
    print("   - Enable display forwarding")
    print("   - Install guest additions")
    print("   - Configure X11 forwarding")
    print()
    print("4. Alternative: Use Wayland instead of X11")
    print("   echo $XDG_SESSION_TYPE")
    print("   If 'wayland', try: export DISPLAY=:1")
    print()
    print("5. Last resort: Run with sudo (not recommended)")
    print("   sudo python3 server.py")

if __name__ == "__main__":
    print("Ubuntu Mouse Movement Troubleshooting")
    print("=" * 50)
    
    check_environment()
    check_x11()
    check_tools()
    fix_common_issues()
    test_mouse_movement()
    provide_solutions()
    
    print("\n=== Summary ===")
    print("Run this script to diagnose mouse movement issues.")
    print("The simulator will work even without mouse movement,")
    print("focusing on keyboard input, scrolling, and window switching.") 