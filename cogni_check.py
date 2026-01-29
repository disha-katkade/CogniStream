from google import genai
from google.genai import types

# PASTE YOUR KEY HERE
CLIENT_KEY = "AIzaSyCos" 

# We set the version to v1alpha to unlock Gemini 3's special features
client = genai.Client(
    api_key=CLIENT_KEY,
    http_options=types.HttpOptions(api_version='v1alpha')
)

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

