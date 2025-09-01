from google import genai
from google.genai import types

# Step 1: Configure the client
client = genai.Client()

# Step 2: Define the Google Search grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Step 3: Configure generation settings with the search tool
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

print("=== GOOGLE SEARCH GROUNDING EXAMPLE ===\n")

# Step 4: Make a request that requires real-time information
user_query = "What are the latest developments in AI technology in 2025?"
print(f"User Query: {user_query}\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_query,
    config=config,
)

# Step 5: Display the grounded response
print("Grounded Response:")
print(response.text)
print()