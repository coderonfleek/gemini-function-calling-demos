"""
Mock e-commerce inventory system

In this scenario, the model can check the stock and price of a product by calling a function named get_product_details.
"""

from google import genai
from google.genai import types

client = genai.Client()

# Declare the function
get_product_details_declaration = {
    "name": "get_product_details", # The actual function name
    "description": "Get the price, name, and stock information for a specific product ID",
    "parameters": { # Define the arguments
        "type": "object",
        "properties": { # Define each property un the argument object 
            "product_id": {
                "type": "string",
                "description": "The unique identifier of the product, e.g., PROD-101"
            }
        },
        "required": ["product_id"] # List of required arguments
    }
}

# Define the function
def get_product_details(product_id: str) -> dict:
    """Gets product details using the product ID"""

    # Sample product database
    products = {
        "PROD-101": {"name": "Wireless Noise-Cancelling Headphones", "price": 249.99, "in_stock": 150},
        "PROD-205": {"name": "Smart Fitness Tracker", "price": 89.95, "in_stock": 75},
        "PROD-315": {"name": "4K Ultra HD Streaming Device", "price": 49.99, "in_stock": 0},
        "PROD-404": {"name": "Portable Bluetooth Speaker", "price": 119.00, "in_stock": 210},
    }

    return products.get(product_id.upper(), {"error": "Product not found"})


# Set up the tool 
# this is required for function declarations, not needed for automatic FC
tools = types.Tool(function_declarations=[get_product_details_declaration])

# Add the tool to the model generation configuration
config = types.GenerateContentConfig(
    tools = [tools]
)

# Create a simple string content (The Prompt) 
# this can also be created in a more elaborate using content parts that can take different data types and even tool response parts
content = "Is PROD-315 in stock, if so, how much does it cost"

response = client.models.generate_content(
    model="gemini-2.5-flash", # This is one of the supported models fo FC
    contents = content,
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