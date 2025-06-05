# Main files
import gradio as gr
from agent import run_nutritionist_pipeline
import os
import re

def process_meal(username, meal_desc, dietary_preference):
    """
    Process a meal through the nutritionist pipeline.
    
    Args:
        username (str): Name of the user
        meal_desc (str): Description of the meal
        dietary_preference (str): User's dietary preference
        
    Returns:
        tuple: (formatted_output, image_path)
    """
    # Run the pipeline
    result = run_nutritionist_pipeline(username, meal_desc, dietary_preference)
    
    # Extract calories from the logged meal response
    calories = "Not available"
    if result['logged']:
        # First try to find calories in the format "X calories"
        calorie_match = re.search(r'(\d+)\s*calories', result['logged'], re.IGNORECASE)
        if calorie_match:
            calories = calorie_match.group(1)
        else:
            # Try to find any number in parentheses
            paren_match = re.search(r'\((\d+)\)', result['logged'])
            if paren_match:
                calories = paren_match.group(1)
            else:
                # Try to find any standalone number
                number_match = re.search(r'\b(\d+)\b', result['logged'])
                if number_match:
                    calories = number_match.group(1)
    
    # Map tool names to Mistral connectors
    connector_map = {
        "Web Search": "Web Search",
        "Image Description Generation": "Image Generation",
        "Meal Logging": "Chat Completion",
        "Next Meal Suggestion": "Chat Completion"
    }
    
    # Get unique connectors used
    connectors_used = set()
    for tool in result['tools_used']:
        if tool in connector_map:
            connectors_used.add(connector_map[tool])
    
    # Format the output
    output = f"""
# Meal Analysis Results

## Meal Details
- **Meal Description:** {meal_desc}
- **Estimated Calories:** {calories}

## Next Meal Suggestion
{result['next_meal_suggestion']}

## Tools Used
{', '.join(result['tools_used'])}

## Mistral Connectors Used
{', '.join(sorted(connectors_used))}
"""
    
    # Get the image path
    image_path = result['meal_image']
    
    # Check if the image path is valid
    if os.path.exists(image_path) and image_path.endswith('.png'):
        return output, image_path
    else:
        return output, None

# Create the Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🍽️ Nutritionist Assistant")
    
    with gr.Row():
        with gr.Column():
            username = gr.Textbox(label="Username", placeholder="Enter your name")
            meal_desc = gr.Textbox(label="Meal Description", placeholder="Describe your meal (e.g., 'Chicken salad with olive oil dressing')")
            dietary_preference = gr.Dropdown(
                choices=["vegetarian", "vegan", "Non-vegetarian", "gluten-free"],
                label="Dietary Preference",
                value="omnivore"
            )
            submit_btn = gr.Button("Process Meal", variant="primary")
        
        with gr.Column():
            output = gr.Markdown(label="Results")
            image_output = gr.Image(label="Generated Meal Image", type="filepath")
    
    submit_btn.click(
        fn=process_meal,
        inputs=[username, meal_desc, dietary_preference],
        outputs=[output, image_output]
    )

# Launch the app
if __name__ == "__main__":
    demo.launch() 