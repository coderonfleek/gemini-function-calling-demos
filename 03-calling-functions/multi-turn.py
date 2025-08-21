"""
Email validation system

This example demonstrates a single function implementation for email validation
"""

from google import genai
from google.genai import types
import re

GEMINI_MODEL = "gemini-2.5-flash"

client = genai.Client()

# Declare the function
validate_email_declaration = {
    "name": "validate_email",
    "description": "Validates an email address and provides detailed information about its format and components",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address to validate (e.g., 'user@example.com')",
            },
            "check_domain": {
                "type": "boolean",
                "description": "Whether to perform additional domain format checks (default: true)",
                "default": True
            },
        },
        "required": ["email"],
    },
}

# Define the function
def validate_email(email: str, check_domain: bool = True) -> dict:
    """Validate email address and return detailed analysis"""
    
    # Basic email regex pattern
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    result = {
        "email": email,
        "is_valid": False,
        "local_part": "",
        "domain": "",
        "issues": []
    }
    
    # Check if email matches basic pattern
    if re.match(email_pattern, email):
        result["is_valid"] = True
        local_part, domain = email.split('@', 1)
        result["local_part"] = local_part
        result["domain"] = domain
        
        # Additional checks if requested
        if check_domain:
            if len(local_part) > 64:
                result["issues"].append("Local part exceeds 64 characters")
                result["is_valid"] = False
            
            if len(domain) > 253:
                result["issues"].append("Domain exceeds 253 characters")
                result["is_valid"] = False
                
            if '..' in domain:
                result["issues"].append("Domain contains consecutive dots")
                result["is_valid"] = False
    else:
        result["issues"].append("Invalid email format")
        
        # Try to identify specific issues
        if '@' not in email:
            result["issues"].append("Missing @ symbol")
        elif email.count('@') > 1:
            result["issues"].append("Multiple @ symbols")
        elif not email.split('@')[-1]:
            result["issues"].append("Missing domain")
        elif '.' not in email.split('@')[-1]:
            result["issues"].append("Domain missing top-level domain")
    
    # Summary message
    if result["is_valid"]:
        result["summary"] = f"✅ '{email}' is a valid email address"
    else:
        result["summary"] = f"❌ '{email}' is not valid: {', '.join(result['issues'])}"
    
    return result

# Set up the tool 
# this is required for function declarations, not needed for automatic FC
tools = types.Tool(function_declarations=[validate_email_declaration])

# Add the tool to the model generation configuration
config = types.GenerateContentConfig(
    tools = [tools]
)

# Configure the content to send a user message with a single text Part (The Prompt) 
valid_email_prompt = "Can you check if 'john.doe@company-mail.com' is a valid email address? I want to make sure it's properly formatted."

invalid_email_prompt = "Please check if the email 'jdub@@company' is valid"

contents = [
    types.Content(
        role="user",
        parts=[
            types.Part(
                text=invalid_email_prompt
            )
        ]
    )
]

print("=== EMAIL VALIDATION ASSISTANT ===\n")
response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents = contents,
    config = config,
)

# Get the function call suggestion from the model's response
print("Model's function call suggestion:")
function_call = response.candidates[0].content.parts[0].function_call

# Get the function's name
function_name = function_call.name
print(f"Function Name: {function_name}")

# Get the suggested arguments
function_arguments = function_call.args
print(f"Function Arguments: {dict(function_arguments)}")

# Execute the function with the delivered arguments

if function_name == "validate_email":
    result = validate_email(**function_arguments)

    # Print out the raw function results
    print(f"\nEmail Validation Result:")
    for key, value in result.items():
        print(f"{key}: {value}")
    print()

    """
    Multi-turn starts here
    """

    # Create a function response part to send the function's results to model
    # This will consist of the name of the function that was called and the result from it
    function_response_part = types.Part.from_function_response(
        name=function_name,
        response = {
            "result": result
        }
    )

    """ 
        LLMs are stateless so we need to send it the previous and new conversation
        Create a conversation history by adding the model's response and our function result to the initial "contents" prompt setup
    """

    # Model's response (function call suggestion)
    contents.append(response.candidates[0].content) 
    # Function call result
    contents.append(
        types.Content(
            role="user",
            parts= [function_response_part]
        )
    )

    # Use the new prompt history to generate a friendly response from the model
    final_response = client.models.generate_content(
        model=GEMINI_MODEL,
        config=config, # Use the same configuration
        contents=contents
    )

    print("Final response to the user")
    print(final_response.text)