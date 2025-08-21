"""
Calling Mutiple Functions at the same time
"""

from google import genai
from google.genai import types

GEMINI_MODEL="gemini-2.5-flash"

# Step 1: Define multiple independent functions with type hints and docstrings
def get_current_temperature(city: str) -> dict:
    """Gets the current temperature for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing temperature information for the city.
    """
    # Mock temperature data
    temperatures = {
        "new york": {"temp": 22, "unit": "°C", "condition": "sunny"},
        "london": {"temp": 15, "unit": "°C", "condition": "cloudy"},
        "tokyo": {"temp": 28, "unit": "°C", "condition": "humid"},
        "paris": {"temp": 18, "unit": "°C", "condition": "rainy"},
        "sydney": {"temp": 25, "unit": "°C", "condition": "clear"}
    }
    
    city_lower = city.lower()
    if city_lower in temperatures:
        result = temperatures[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "temp": "N/A", "unit": "°C", "condition": "unknown"}
    

def get_time_zone(city: str) -> dict:
    """Gets the time zone information for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing time zone information for the city.
    """
    # Mock timezone data
    timezones = {
        "new york": {"timezone": "EST (UTC-5)", "current_time": "14:30"},
        "london": {"timezone": "GMT (UTC+0)", "current_time": "19:30"},
        "tokyo": {"timezone": "JST (UTC+9)", "current_time": "04:30"},
        "paris": {"timezone": "CET (UTC+1)", "current_time": "20:30"},
        "sydney": {"timezone": "AEDT (UTC+11)", "current_time": "06:30"}
    }
    
    city_lower = city.lower()
    if city_lower in timezones:
        result = timezones[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "timezone": "UTC+0", "current_time": "Unknown"}
    
def get_population(city: str) -> dict:
    """Gets the population information for a given city.
    
    Args:
        city: The name of the city (e.g., 'New York', 'London')
    
    Returns:
        A dictionary containing population information for the city.
    """
    # Mock population data
    populations = {
        "new york": {"population": "8.3 million", "metro_area": "20.1 million"},
        "london": {"population": "9.0 million", "metro_area": "15.8 million"},
        "tokyo": {"population": "13.9 million", "metro_area": "37.4 million"},
        "paris": {"population": "2.2 million", "metro_area": "12.2 million"},
        "sydney": {"population": "5.3 million", "metro_area": "5.4 million"}
    }
    
    city_lower = city.lower()
    if city_lower in populations:
        result = populations[city_lower].copy()
        result["city"] = city
        return result
    else:
        return {"city": city, "population": "Unknown", "metro_area": "Unknown"}

# Define Client
client = genai.Client()

# Define configuration using automatic function calling
config = types.GenerateContentConfig(
    tools=[get_current_temperature, get_time_zone, get_population]
)

print("=== PARALLEL FUNCTION CALLING EXAMPLE ===\n")
print("User request: Get comprehensive information about Tokyo\n")

response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="I'm planning a trip to Tokyo. Can you give me the current temperature, time zone, and population information for Tokyo? I need all this information at once.",
    config=config
)

# Step 4: Display the final result
# Automatic function calling handles all parallel execution behind the scenes
print("Final response:")
print(response.text)

""" print("\n" + "="*65)
print("WHAT HAPPENED WITH PARALLEL FUNCTION CALLING:")
print("1. Model analyzed the request for Tokyo information")
print("2. Model identified need for temperature, timezone, AND population")
print("3. SDK executed ALL THREE functions simultaneously (in parallel)")
print("4. All function results were collected and sent back together")
print("5. Model generated comprehensive response using all results")
print("="*65) """

"""
Multiple Cities Example
"""
print("\n" + "="*65)
print("Multiple cities example")
print("="*65)

response2 = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="Compare the current temperature in New York and London right now.",
    config=config,
)

print("\nResponse for multiple cities:")
print(response2.text)