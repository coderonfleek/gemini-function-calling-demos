from google import genai
from google.genai.types import GenerateContentConfig

print("=== GEMINI URL CONTEXT TOOL EXAMPLE ===\n")

# Step 1: Configure the client
client = genai.Client()
model_id = "gemini-2.5-flash"

# Step 2: Define the URL context tool
tools = [
    {"url_context": {}},
]

# Step 3: Define URLs to analyze (using accessible roast chicken recipes)
url1 = "https://www.foodnetwork.com/recipes/ina-garten/perfect-roast-chicken-recipe-1940592"
url2 = "https://www.thepioneerwoman.com/food-cooking/recipes/a10727/roast-chicken/"

user_query = f"Compare the ingredients and cooking times from the recipes at {url1} and {url2}"
print(f"User Query: Compare two roast chicken recipes\n")
print(f"URLs to analyze:")
print(f"1. Food Network (Ina Garten): {url1}")
print(f"2. Pioneer Woman (Ree Drummond): {url2}")
print("\nProcessing... (Model will fetch and analyze URL content)\n")

# Step 4: Make the request with URL context tool
response = client.models.generate_content(
    model=model_id,
    contents=user_query,
    config=GenerateContentConfig(
        tools=tools,
    )
)

# Step 5: Display the response
print("="*70)
print("MODEL RESPONSE WITH URL CONTEXT:")
print("="*70)

for part in response.candidates[0].content.parts:
    print(part.text)

print()