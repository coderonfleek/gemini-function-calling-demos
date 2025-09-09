from google import genai
from google.genai import types
import json

# Step 1: Define a minimal function
simple_function_declaration = {
    "name": "say_hello",
    "description": "Returns a greeting message",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name to greet",
            }
        },
        "required": ["name"],
    },
}

# Step 2: Set up Gemini
client = genai.Client()
tools = types.Tool(function_declarations=[simple_function_declaration])
config = types.GenerateContentConfig(tools=[tools])

# Step 3: Make a simple request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello to Alice",
    config=config,
)

print("=== COMPLETE RESPONSE INSPECTION ===\n")

# Function to convert response to dictionary for JSON display
def response_to_dict(response):
    """Convert response object to dictionary for JSON serialization"""
    result = {}
    
    # Basic response info
    if hasattr(response, 'candidates') and response.candidates:
        candidate = response.candidates[0]
        
        result["candidate"] = {}
        
        # Content parts
        if hasattr(candidate, 'content') and candidate.content:
            result["candidate"]["content"] = {
                "role": candidate.content.role,
                "parts": []
            }
            
            for part in candidate.content.parts:
                part_dict = {}
                
                if hasattr(part, 'text') and part.text:
                    part_dict["text"] = part.text
                
                if hasattr(part, 'function_call') and part.function_call:
                    part_dict["function_call"] = {
                        "name": part.function_call.name,
                        "args": dict(part.function_call.args)
                    }
                
                result["candidate"]["content"]["parts"].append(part_dict)
        
        # Finish reason
        if hasattr(candidate, 'finish_reason'):
            result["candidate"]["finish_reason"] = str(candidate.finish_reason)
    
    # Usage metadata
    if hasattr(response, 'usage_metadata'):
        usage = response.usage_metadata
        result["usage_metadata"] = {
            "prompt_token_count": getattr(usage, 'prompt_token_count', 0),
            "candidates_token_count": getattr(usage, 'candidates_token_count', 0),
            "total_token_count": getattr(usage, 'total_token_count', 0)
        }
    
    return result

# Convert and display the response
response_dict = response_to_dict(response)

print("1. FORMATTED JSON RESPONSE:")
print("=" * 50)
print(json.dumps(response_dict, indent=2, ensure_ascii=False))
# print(response)