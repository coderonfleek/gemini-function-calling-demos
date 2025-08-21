"""
Automatic Function Calling (Only available to Python SDK)

No function declarations needed
Proper Docstrings and type hints replace declarations
"""

from google import genai
from google.genai import types
import re

# Define the function with docstring instead of having a separate declaration
# This function cannot have default values if you want to use automatic function calling
def validate_email(email: str, check_domain: bool) -> dict:
    """Validates an email address and provides detailed information about its format and components.
    
    Args:
        email: The email address to validate (e.g., 'user@example.com')
        check_domain: Whether to perform additional domain format checks (default: true)
    
    Returns:
        A dictionary containing validation results, components, and any issues found.
    """
    
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

# Setup the client
client = genai.Client()

# Pass the functions directly to the 'tools' property of the configuration
# No need to create a tools list with types.Tool()
config = types.GenerateContentConfig(
    tools=[validate_email]
)

print("=== EMAIL VALIDATION ASSISTANT (Automatic Function Calling) ===\n")
print("User request: Validate 'john.doe@company-mail.com'\n")

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents="Can you check if 'john.doe@company-mail.com' is a valid email address? I want to make sure it's properly formatted.",
    config=config
)

# Display the final response, automatic function calling has handled everything
print("Final response:")
print(response.text)