from google import genai
from google.genai import types

# Step 1: Define function declarations
check_balance_declaration = {
    "name": "check_balance",
    "description": "Checks the account balance for a given account ID",
    "parameters": {
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The account ID to check (e.g., 'ACC123')",
            }
        },
        "required": ["account_id"],
    },
}

transfer_money_declaration = {
    "name": "transfer_money",
    "description": "Transfers money between accounts",
    "parameters": {
        "type": "object",
        "properties": {
            "from_account": {
                "type": "string",
                "description": "Source account ID",
            },
            "to_account": {
                "type": "string",
                "description": "Destination account ID",
            },
            "amount": {
                "type": "number",
                "description": "Amount to transfer",
            }
        },
        "required": ["from_account", "to_account", "amount"],
    },
}

# Step 2: Implement functions
def check_balance(account_id: str) -> dict:
    """Mock function to check account balance"""
    balances = {
        "ACC123": 1500.00,
        "ACC456": 800.00,
        "ACC789": 2200.00
    }
    
    balance = balances.get(account_id, 0.00)
    return {
        "account_id": account_id,
        "balance": balance,
        "currency": "USD"
    }

def transfer_money(from_account: str, to_account: str, amount: float) -> dict:
    """Mock function to transfer money"""
    return {
        "transaction_id": "TXN987654",
        "from_account": from_account,
        "to_account": to_account,
        "amount": amount,
        "status": "completed",
        "fee": 2.50
    }

# Step 3: Set up Gemini
client = genai.Client()
tools = types.Tool(function_declarations=[check_balance_declaration, transfer_money_declaration])
config = types.GenerateContentConfig(tools=[tools])

print("=== MULTI-TURN FUNCTION CALLING DEMO ===\n")

# Step 4: Start a conversation that will require multiple function calls
conversation_history = []

# First turn
print("TURN 1: User asks for balance check")
print("-" * 40)
user_message1 = "What's the balance in account ACC123?"

conversation_history.append(
    types.Content(role="user", parts=[types.Part(text=user_message1)])
)

response1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=config,
)

# Process first function call
function_call1 = response1.candidates[0].content.parts[0].function_call
print(f"Function called: {function_call1.name}")
print(f"Arguments: {dict(function_call1.args)}")

result1 = check_balance(**function_call1.args)

# Add model response and function result to history
conversation_history.append(response1.candidates[0].content)
conversation_history.append(
    types.Content(role="user", parts=[
        types.Part.from_function_response(
            name=function_call1.name,
            response={"result": result1}
        )
    ])
)

# Get model's response after function execution
final_response1 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=config,
)

print(f"Model response: {final_response1.text}")
conversation_history.append(final_response1.candidates[0].content)

print("\n" + "="*50)

# Second turn - user asks for transfer
print("TURN 2: User requests money transfer")
print("-" * 40)
user_message2 = "Transfer $200 from ACC123 to ACC456"

conversation_history.append(
    types.Content(role="user", parts=[types.Part(text=user_message2)])
)

response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=config,
)

# Process second function call
function_call2 = response2.candidates[0].content.parts[0].function_call
print(f"Function called: {function_call2.name}")
print(f"Arguments: {dict(function_call2.args)}")

result2 = transfer_money(**function_call2.args)

# Add to conversation history
conversation_history.append(response2.candidates[0].content)
conversation_history.append(
    types.Content(role="user", parts=[
        types.Part.from_function_response(
            name=function_call2.name,
            response={"result": result2}
        )
    ])
)

# Get final response
final_response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=conversation_history,
    config=config,
)

print(f"Model response: {final_response2.text}")
conversation_history.append(final_response2.candidates[0].content)

print("\n" + "="*50)