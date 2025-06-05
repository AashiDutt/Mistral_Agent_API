# Pipeline logic file
from tools import estimate_calories, log_meal, suggest_next_meal, search_calories
from tools.image_gen import generate_food_image
from datetime import datetime
import time

def run_nutritionist_pipeline(username, meal_desc, dietary_preference):
    tools_used = set()
    
    print(f"Searching for calories for: {meal_desc}")
    calories_text = search_calories(meal_desc)
    tools_used.add("Web Search")
    
    # If web search fails, fall back to estimation
    if calories_text == 0:
        print("Web search failed, falling back to estimation...")
        time.sleep(1)  # Add delay to avoid rate limits
        calories_text = estimate_calories(meal_desc)
        tools_used.add("Calorie Estimation")
    
    # calories_text is now an int
    estimated_calories = calories_text
    print(f"Estimated calories: {estimated_calories}")
    
    print(f"Logging meal for {username}...")
    time.sleep(1)  # Add delay to avoid rate limits
    log_response = log_meal(username, meal_desc, estimated_calories)
    tools_used.add("Meal Logging")
    
    print("Generating next meal suggestion...")
    time.sleep(1)  # Add delay to avoid rate limits
    suggestion = suggest_next_meal(estimated_calories, dietary_preference)
    tools_used.add("Next Meal Suggestion")
    
    print("Generating image description for suggested meal...")
    time.sleep(1)  # Add delay to avoid rate limits
    meal_image = generate_food_image(suggestion)
    tools_used.add("Image Description Generation")
    
    return {
        "logged": log_response,
        "next_meal_suggestion": suggestion,
        "meal_image": meal_image,
        "tools_used": sorted(list(tools_used))
    }

# Example run
if __name__ == "__main__":
    output = run_nutritionist_pipeline(username="aashi", meal_desc="paneer tikka with paratha", dietary_preference="vegetarian")
    print("Final Output:", output)
