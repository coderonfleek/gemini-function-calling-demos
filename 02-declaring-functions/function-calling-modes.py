from google import genai
from google.genai import types

# Step 1: Define a simple function for demonstration
get_time_declaration = {
    "name": "get_current_time",
    "description": "Gets the current time in a specified timezone",
    "parameters": {
        "type": "object",
        "properties": {
            "timezone": {
                "type": "string",
                "description": "Timezone (e.g., 'UTC', 'EST', 'PST')",
            }
        },
        "required": ["timezone"],
    },
}



# Step 2: Set up client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[get_time_declaration])

print("=== FUNCTION CALLING MODES DEMONSTRATION ===\n")

# Test prompt that could use the function
test_prompt = "Hello, how are you?"
function_mode = "AUTO"

# MODE 1: AUTO (Default) - Model decides whether to call function

print(f" {function_mode} MODE Demo")
print("-" * 30) 
print(f"Prompt: {test_prompt}")

generation_config = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode=function_mode)
    ),
    
)

# ANY Config
""" 
tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode='ANY')
),
"""

# NONE Config
""" 
tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode='NONE')
), 
"""


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=test_prompt,
    config=generation_config,
)

# Check if function was called
if hasattr(response.candidates[0].content.parts[0], 'function_call') and response.candidates[0].content.parts[0].function_call is not None:
    print("✓ Model chose to call function")
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function: {function_call.name}")
    print(f"Arguments: {dict(function_call.args)}")
else:
    print("✗ Model chose to respond without calling function")
    print(f"Direct response: {response.text}")

print()

"""
# MODE 2: ANY - Force the model to call a function
print("2. ANY MODE")
print("-" * 30)
print("Forces model to always call a function")

config_any = types.GenerateContentConfig(
    tools=[tools],
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode='ANY')
    ),
)

response_any = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=test_prompt,
    config=config_any,
)

# ANY mode guarantees a function call
if hasattr(response_any.candidates[0].content.parts[0], 'function_call') and response_any.candidates[0].content.parts[0].function_call is not None:
    function_call = response_any.candidates[0].content.parts[0].function_call
    print("✓ Function call forced (as expected)")
    print(f"Function: {function_call.name}")
    print(f"Arguments: {dict(function_call.args)}")
else:
    print("✗ Unexpected: No function call in ANY mode")

print()

# MODE 3: NONE - Prevent function calling
print("3. NONE MODE")
print("-" * 30)
print("Prohibits model from calling any functions")

config_none = types.GenerateContentConfig(
    tools=[tools],  # Functions are available but won't be used
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(mode='NONE')
    ),
)

response_none = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=test_prompt,
    config=config_none,
)

# NONE mode prevents function calls
if hasattr(response_none.candidates[0].content.parts[0], 'function_call') and response_none.candidates[0].content.parts[0].function_call is not None:
    function_call = response_any.candidates[0].content.parts[0].function_call
    print("✓ Function call")
    print(f"Function: {function_call.name}")
    print(f"Arguments: {dict(function_call.args)}")
else:
    print("✓ No function call")
    print(f"Direct response: {response_none.text}")

print() 
"""

# Demonstration with different prompts
""" 
print("=" * 50)
print("TESTING DIFFERENT PROMPTS WITH AUTO MODE")
print("=" * 50)

prompts = [
    "What time is it in PST?",  # Likely to trigger function
    "Hello, how are you?",     # Unlikely to trigger function
    "Get me the current time in EST"  # Likely to trigger function
]

for i, prompt in enumerate(prompts, 1):
    print(f"\nTest {i}: '{prompt}'")
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config_auto,
    )
    
    if hasattr(response.candidates[0].content.parts[0], 'function_call'):
        print("  → Function called ✓")
    else:
        print("  → Direct response ✗")

print()
print("=" * 50)
print("MODE SUMMARY")
print("=" * 50)
print("AUTO:  Model decides based on context (flexible)")
print("ANY:   Always calls a function (guaranteed execution)")
print("NONE:  Never calls functions (text-only responses)")
print()
print("💡 Use AUTO for normal operation")
print("💡 Use ANY when you need guaranteed function execution")
print("💡 Use NONE to temporarily disable function calling") 
"""