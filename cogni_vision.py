import pyautogui
import cv2
import numpy as np
from google import genai
from google.genai import types
import time
import os

# --- 1. CONFIGURATION: SAFE LOADING ---
def load_api_key():
    """Safely loads the API key from a local text file to avoid hardcoding."""
    try:
        if os.path.exists("keys.txt"):
            with open("keys.txt", "r") as f:
                key = f.read().strip()
                if key:
                    return key
        return "YOUR_API_KEY_HERE"  # Placeholder for GitHub/Deployment
    except Exception as e:
        print(f"Error loading keys.txt: {e}")
        return "YOUR_API_KEY_HERE"

API_KEY = load_api_key()
client = genai.Client(api_key=API_KEY, http_options=types.HttpOptions(api_version='v1alpha'))

def capture_and_blur():
    # Take a screenshot of the whole screen
    screenshot = pyautogui.screenshot()
    
    # Convert the screenshot to a format OpenCV understands (BGR)
    frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    
    # --- PRIVACY LAYER ---
    # We will blur the bottom 10% of the screen where taskbars/notifications live
    height, width, _ = frame.shape
    roi_top = int(height * 0.9)
    # Apply a heavy Gaussian Blur to that area
    frame[roi_top:height, 0:width] = cv2.GaussianBlur(frame[roi_top:height, 0:width], (51, 51), 0)
    
    # Save the processed image locally so you can check it
    cv2.imwrite("current_view.jpg", frame)
    return "current_view.jpg"

def get_ai_advice(image_path):
    # Prepare the vision prompt
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_level="HIGH")
            ),
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                "I am working on the task shown in this image. Do you notice any errors, or do you have a 'pro tip' to make this faster?"
            ]
        )
        return response.text
    except Exception as e:
        return f"AI Error: {e}. Check if your API key in keys.txt is valid."

# --- RUN THE LOOP ---
print("CogniStream is now watching... (Press Ctrl+C to stop)")
try:
    while True:
        img = capture_and_blur()
        print("Analyzing your workflow...")
        advice = get_ai_advice(img)
        
        print("\n--- GEMINI'S ADVICE ---")
        print(advice)
        print("-" * 30)
        
        # Wait 30 seconds before the next check to stay in the free tier
        time.sleep(30)
except KeyboardInterrupt:
    print("\nCogniStream stopped.")