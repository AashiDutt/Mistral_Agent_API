#Meal suggestions
from datetime import datetime
from tools.configs import client, create_chat_completion
from mistralai import SystemMessage, UserMessage
import re

def estimate_calories(meal_desc):
    """
    Estimate calories in a meal using the Mistral model.
    
    Args:
        meal_desc (str): Description of the meal
        
    Returns:
        int: Estimated calories
    """
    try:
        # Create messages for calorie estimation
        messages = [
            SystemMessage(content="You are a nutrition expert. Estimate calories in meals. Return ONLY a single number representing total calories."),
            UserMessage(content=f"Estimate calories in: {meal_desc}")
        ]

        # Get the response using a smaller model
        response = client.chat.complete(
            model="mistral-small-latest",  # Using smaller model to avoid rate limits
            messages=messages,
            temperature=0.1,
            max_tokens=50
        )

        # Extract the number from the response
        content = response.choices[0].message.content
        numbers = re.findall(r'\d+', content)
        
        if numbers:
            return int(numbers[0])
        return 0
        
    except Exception as e:
        print(f"Error during calorie estimation: {str(e)}")
        return 0

def log_meal(username, meal, calories):
    """
    Log a meal with its calorie count.
    
    Args:
        username (str): Name of the user
        meal (str): Description of the meal
        calories (int): Number of calories
        
    Returns:
        str: Confirmation message
    """
    try:
        # Create messages for meal logging
        messages = [
            SystemMessage(content="You are a meal logging assistant. Log the user's meal with calories."),
            UserMessage(content=f"Log this meal: {meal} with {calories} calories for user {username} at {datetime.utcnow().isoformat()}")
        ]

        # Get the response using a smaller model
        response = client.chat.complete(
            model="mistral-small-latest",  # Using smaller model to avoid rate limits
            messages=messages,
            temperature=0.1,
            max_tokens=100
        )

        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error during meal logging: {str(e)}")
        return f"Logged {meal} ({calories} calories) for {username}"

def suggest_next_meal(calories, dietary_preference):
    """
    Suggest the next meal based on calories and dietary preference.
    
    Args:
        calories (int): Current meal calories
        dietary_preference (str): User's dietary preference
        
    Returns:
        str: Suggested next meal
    """
    try:
        # Create messages for meal suggestion
        messages = [
            SystemMessage(content="You are a nutrition expert. Suggest healthy meals based on calorie intake and dietary preferences."),
            UserMessage(content=f"Suggest a {dietary_preference} meal that would be a good next meal after consuming {calories} calories. Make it specific and appetizing.")
        ]

        # Get the response using a smaller model
        response = client.chat.complete(
            model="mistral-small-latest",  # Using smaller model to avoid rate limits
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Error during meal suggestion: {str(e)}")
        return "Unable to suggest next meal at this time."
