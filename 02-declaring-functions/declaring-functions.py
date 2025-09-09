from google import genai
from google.genai import types
import requests

# Step 1: Define function declarations for API operations

# Function 1: Fetch list of users with options
fetch_users_declaration = {
    "name": "fetch_users",
    "description": "Fetches a list of users from JSONPlaceholder API with optional email inclusion",
    "parameters": {
        "type": "object",
        "properties": {
            "max_users": {
                "type": "integer",
                "description": "Maximum number of users to fetch (1-10)",
            },
            "include_email": {
                "type": "boolean",
                "description": "Whether to include email addresses in the response",
            },
        },
        "required": ["max_users", "include_email"],
    },
}

# Function 2: Get specific user details
get_user_details_declaration = {
    "name": "get_user_details",
    "description": "Retrieves detailed information for a specific user by their ID",
    "parameters": {
        "type": "object",
        "properties": {
            "user_id": {
                "type": "integer",
                "description": "The user ID to fetch details for (1-10)",
            },
        },
        "required": ["user_id"],
    },
}

# Step 2: Implement the actual functions

def fetch_users(max_users: int, include_email: bool) -> dict:
    """Fetch users from JSONPlaceholder API"""
    try:
        # Limit max_users to reasonable range
        max_users = min(max_users, 10)
        
        response = requests.get("https://jsonplaceholder.typicode.com/users")
        response.raise_for_status()
        
        all_users = response.json()
        limited_users = all_users[:max_users]
        
        # Format user list based on email preference
        user_list = []
        for user in limited_users:
            if include_email:
                user_list.append({
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                })
            else:
                user_list.append({
                    "id": user["id"],
                    "name": user["name"]
                })
        
        return {
            "users": user_list,
            "total_fetched": len(user_list),
            "emails_included": include_email
        }
    
    except requests.RequestException as e:
        return {"error": f"Failed to fetch users: {str(e)}"}

def get_user_details(user_id: int) -> dict:
    """Get detailed information for a specific user"""
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        response.raise_for_status()
        
        user = response.json()
        
        return {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
            "phone": user["phone"],
            "website": user["website"],
            "company": user["company"]["name"],
            "address": f"{user['address']['street']}, {user['address']['city']}"
        }
    
    except requests.RequestException as e:
        return {"error": f"Failed to fetch user details: {str(e)}"}

# Step 3: Set up Gemini with both functions
client = genai.Client()
tools = types.Tool(function_declarations=[fetch_users_declaration, get_user_details_declaration])
config = types.GenerateContentConfig(tools=[tools])

# Step 4: Test the first function - fetch users
print("=== DEMO 1: FETCH USERS ===")
user_question1 = "Can you get me a list of 5 users including their email addresses?"

response1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_question1,
    config=config,
)

# Show function call for first demo
function_call1 = response1.candidates[0].content.parts[0].function_call
print(f"Function suggested: {function_call1.name}")
print(f"Arguments: {dict(function_call1.args)}")

# Execute the function
if function_call1.name == "fetch_users":
    result1 = fetch_users(**function_call1.args)
    
    # Send result back to Gemini
    function_response1 = types.Part.from_function_response(
        name=function_call1.name,
        response={"result": result1},
    )
    
    contents1 = [
        types.Content(role="user", parts=[types.Part(text=user_question1)]),
        response1.candidates[0].content,
        types.Content(role="user", parts=[function_response1])
    ]
    
    final_response1 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents1,
        config=config,
    )
    
    print(f"Final answer: {final_response1.text}")

print("\n" + "="*50)

# Step 5: Test the second function - get user details
print("=== DEMO 2: GET USER DETAILS ===")
user_question2 = "Show me detailed information for user ID 3"

response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_question2,
    config=config,
)

# Show function call for second demo
function_call2 = response2.candidates[0].content.parts[0].function_call
print(f"Function suggested: {function_call2.name}")
print(f"Arguments: {dict(function_call2.args)}")

# Execute the function
if function_call2.name == "get_user_details":
    result2 = get_user_details(**function_call2.args)
    
    # Send result back to Gemini
    function_response2 = types.Part.from_function_response(
        name=function_call2.name,
        response={"result": result2},
    )
    
    contents2 = [
        types.Content(role="user", parts=[types.Part(text=user_question2)]),
        response2.candidates[0].content,
        types.Content(role="user", parts=[function_response2])
    ]
    
    final_response2 = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents2,
        config=config,
    )
    
    print(f"Final answer: {final_response2.text}")