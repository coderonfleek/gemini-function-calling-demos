from google import genai
from google.genai import types

print("=== GEMINI CODE EXECUTION EXAMPLE ===\n")

# Step 1: Configure the client
client = genai.Client()

# Step 2: Enable code execution tool
# This allows the model to generate and run Python code automatically
config = types.GenerateContentConfig(
    tools=[types.Tool(code_execution=types.ToolCodeExecution)]
)

# Step 3: Make a request that requires simple computation
user_query = "Calculate the area of a circle with radius 7. Show your work step by step."

print(f"User Query: {user_query}\n")
print("Processing... (Model will generate and execute code)\n")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_query,
    config=config,
)

# Step 4: Process and display the response parts
print("="*60)
print("MODEL RESPONSE WITH CODE EXECUTION:")
print("="*60)

for i, part in enumerate(response.candidates[0].content.parts):
    if part.text is not None:
        print(f"📝 Text Part {i+1}:")
        print(part.text)
        print()
    
    if part.executable_code is not None:
        print(f"💻 Generated Code Part {i+1}:")
        print("```python")
        print(part.executable_code.code)
        print("```")
        print()
    
    if part.code_execution_result is not None:
        print(f"▶️ Code Execution Result Part {i+1}:")
        print("Output:")
        print(part.code_execution_result.output)
        print()

""" 
print("="*60)
print("HOW CODE EXECUTION WORKS:")
print("1. Model analyzes the request for computational needs")
print("2. Model generates appropriate Python code")
print("3. Code is automatically executed in secure environment")
print("4. Model sees the execution results")
print("5. Model provides final explanation with results")
print("="*60) 
"""