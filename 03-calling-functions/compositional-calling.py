from google import genai
from google.genai import types

# Step 1: Define sequential functions that depend on each other's results
def get_user_location(user_id: str) -> dict:
    """Gets the stored location for a user by their ID.
    
    Args:
        user_id: The unique identifier for the user
    
    Returns:
        A dictionary containing the user's location information.
    """
    # Mock user database
    user_locations = {
        "user123": {"city": "Seattle", "state": "WA", "country": "USA"},
        "user456": {"city": "London", "state": "", "country": "UK"},
        "user789": {"city": "Toronto", "state": "ON", "country": "Canada"},
        "admin001": {"city": "San Francisco", "state": "CA", "country": "USA"}
    }
    
    if user_id in user_locations:
        result = user_locations[user_id].copy()
        result["user_id"] = user_id
        result["location_found"] = True
        # Format location string for next function
        if result["state"]:
            result["full_location"] = f"{result['city']}, {result['state']}"
        else:
            result["full_location"] = f"{result['city']}, {result['country']}"
        return result
    else:
        return {
            "user_id": user_id,
            "location_found": False,
            "error": "User not found",
            "full_location": ""
        }

def get_weather_forecast(location: str, days: int) -> dict:
    """Gets the weather forecast for a specific location and number of days.
    
    Args:
        location: The location string (e.g., 'Seattle, WA' or 'London, UK')
        days: Number of days to forecast (1-7)
    
    Returns:
        A dictionary containing weather forecast information.
    """
    # Mock weather data based on location
    weather_patterns = {
        "seattle": {"base_temp": 15, "condition": "rainy", "variation": 3},
        "london": {"base_temp": 12, "condition": "cloudy", "variation": 2},
        "toronto": {"base_temp": 8, "condition": "snowy", "variation": 4},
        "san francisco": {"base_temp": 18, "condition": "sunny", "variation": 1}
    }
    
    # Find matching weather pattern
    location_key = None
    for city in weather_patterns:
        if city in location.lower():
            location_key = city
            break
    
    if not location_key:
        return {
            "location": location,
            "error": "Weather data not available for this location",
            "forecast": []
        }
    
    pattern = weather_patterns[location_key]
    forecast = []
    
    for day in range(1, min(days + 1, 8)):  # Max 7 days
        temp_variation = (day % 3 - 1) * pattern["variation"]
        forecast.append({
            "day": day,
            "temperature": pattern["base_temp"] + temp_variation,
            "condition": pattern["condition"],
            "description": f"Day {day}: {pattern['base_temp'] + temp_variation}°C, {pattern['condition']}"
        })
    
    return {
        "location": location,
        "days_requested": days,
        "forecast": forecast,
        "summary": f"{days}-day forecast for {location}"
    }

def send_notification(user_id: str, message: str) -> dict:
    """Sends a notification message to a user.
    
    Args:
        user_id: The unique identifier for the user
        message: The notification message to send
    
    Returns:
        A dictionary containing the notification status.
    """
    notification_details = {}
    # Mock notification system
    if len(message) > 500:
        notification_details = {
            "user_id": user_id,
            "status": "failed",
            "error": "Message too long (max 500 characters)",
            "message_length": len(message)
        }
    
    notification_details = {
        "user_id": user_id,
        "status": "sent",
        "message": message,
        "timestamp": "2025-09-01 14:30:00",
        "delivery_method": "push_notification"
    }
    print("===== Final Notification Sent =====")
    print(notification_details)

    return notification_details

# Step 2: Configure the client with automatic function calling
client = genai.Client()

# Pass all Python functions - SDK will handle sequential calling automatically
config = types.GenerateContentConfig(
    tools=[get_user_location, get_weather_forecast, send_notification]
)

print("=== COMPOSITIONAL FUNCTION CALLING EXAMPLE ===\n")
print("User request: Get weather for user123's location and notify them\n")

# Step 3: Make request that requires sequential function calls
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Can you look up where user123 is located, get a 3-day weather forecast for their city, and then send them a notification with the weather summary?",
    config=config,
)

# Step 4: Display the final result
print("Final response:")
print(response.text)

""" 
print("\n" + "="*70)
print("COMPOSITIONAL FUNCTION CALLING SEQUENCE:")
print("1. get_user_location(user_id='user123')")
print("   → Returns: Seattle, WA")
print("2. get_weather_forecast(location='Seattle, WA', days=3)")
print("   → Returns: 3-day forecast data")
print("3. send_notification(user_id='user123', message='Weather forecast...')")
print("   → Returns: Notification sent successfully")
print("")
print("Each function call depends on the result of the previous one!")
print("="*70) 
"""

""" 
# Alternative example with different task
print("\n" + "="*70)
print("BONUS: Another compositional example")
print("="*70)

response2 = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Find admin001's location, get a 5-day weather forecast, and notify them about any rainy days coming up.",
    config=config,
)

print("\nResponse for admin001:")
print(response2.text) 
"""