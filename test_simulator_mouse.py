#!/usr/bin/env python3
"""
Simplified simulator test - mouse movement only
"""

import pyautogui
import random
import time
import subprocess
import platform

# Safety feature
pyautogui.FAILSAFE = True

class SimpleMouseTest:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.platform = platform.system()
        print(f"Screen size: {self.screen_width}x{self.screen_height}")
        print(f"Platform: {self.platform}")
    
    def test_xdotool_movement(self):
        """Test xdotool mouse movement"""
        print("\n--- Testing xdotool movement ---")
        try:
            # Get current position
            result = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
            print(f"Starting position: {result.stdout.strip()}")
            
            # Move to random position
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(100, self.screen_height - 100)
            print(f"Moving to: ({x}, {y})")
            
            subprocess.run(['xdotool', 'mousemove', str(x), str(y)])
            time.sleep(1)
            
            # Check new position
            result = subprocess.run(['xdotool', 'getmouselocation'], capture_output=True, text=True)
            print(f"New position: {result.stdout.strip()}")
            return True
            
        except Exception as e:
            print(f"xdotool failed: {e}")
            return False
    
    def test_pyautogui_movement(self):
        """Test pyautogui mouse movement"""
        print("\n--- Testing pyautogui movement ---")
        try:
            # Get current position
            pos = pyautogui.position()
            print(f"Starting position: {pos}")
            
            # Move to random position
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(100, self.screen_height - 100)
            print(f"Moving to: ({x}, {y})")
            
            pyautogui.moveTo(x, y, duration=1)
            time.sleep(1)
            
            # Check new position
            new_pos = pyautogui.position()
            print(f"New position: {new_pos}")
            return True
            
        except Exception as e:
            print(f"pyautogui failed: {e}")
            return False
    
    def run_test(self, duration_seconds=30):
        """Run mouse movement test for specified duration"""
        print(f"Starting mouse movement test for {duration_seconds} seconds...")
        print("Move mouse to corner to stop early")
        
        start_time = time.time()
        xdotool_success = 0
        pyautogui_success = 0
        total_attempts = 0
        
        while time.time() - start_time < duration_seconds:
            total_attempts += 1
            print(f"\n--- Attempt {total_attempts} ---")
            
            # Try xdotool
            if self.test_xdotool_movement():
                xdotool_success += 1
            
            time.sleep(2)
            
            # Try pyautogui
            if self.test_pyautogui_movement():
                pyautogui_success += 1
            
            time.sleep(2)
        
        # Print results
        print(f"\n=== Test Results ===")
        print(f"Total attempts: {total_attempts}")
        print(f"xdotool successes: {xdotool_success}")
        print(f"pyautogui successes: {pyautogui_success}")
        print(f"xdotool success rate: {xdotool_success/total_attempts*100:.1f}%")
        print(f"pyautogui success rate: {pyautogui_success/total_attempts*100:.1f}%")

if __name__ == "__main__":
    test = SimpleMouseTest()
    test.run_test(duration_seconds=30) 