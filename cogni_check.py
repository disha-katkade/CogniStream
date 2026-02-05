from google import genai
from google.genai import types
import os

# --- 1. CONFIGURATION: SAFE LOADING ---
def load_api_key():
    """Safely loads the API key from a local text file."""
    try:
        if os.path.exists("keys.txt"):
            with open("keys.txt", "r") as f:
                key = f.read().strip()
                if key:
                    return key
        return "YOUR_API_KEY_HERE"
    except Exception as e:
        print(f"Error loading keys.txt: {e}")
        return "YOUR_API_KEY_HERE"

CLIENT_KEY = load_api_key()

# We set the version to v1alpha to unlock Gemini 3's special features
client = genai.Client(
    api_key=CLIENT_KEY,
    http_options=types.HttpOptions(api_version='v1alpha')
)

try:
    # Use the full preview model name
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_level="HIGH"
            )
        ),
        contents="Confirming connection. Are you ready to build the CogniStream engine?"
    )

    print("-" * 30)
    print("SYSTEM CHECK: SUCCESS!")
    print(f"GEMINI RESPONSE: {response.text}")
    print("-" * 30)

except Exception as e:
    print("-" * 30)
    print("SYSTEM CHECK: FAILED")
    print(f"ERROR: {e}")
    print("TIP: Make sure your API key is correctly pasted in 'keys.txt'.")
    print("-" * 30)