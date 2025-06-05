#Image generation tool
import os
import re
from mistralai import Mistral, UserMessage, SystemMessage
from mistralai.models import ToolFileChunk
from tools.configs import client
from datetime import datetime

def generate_food_image(meal_description):
    """
    Generate a detailed visual description of the meal.
    
    Args:
        meal_description (str): Description of the meal
        
    Returns:
        str: Path to the saved image file
    """
    try:
        print(f"Starting image generation for: {meal_description}")
        
        # Create image generation agent
        image_agent = client.beta.agents.create(
            model="mistral-medium-2505",
            name="Food Image Generation Agent",
            description="Agent used to generate food images.",
            instructions="Use the image generation tool to create appetizing food images. Generate realistic and appetizing images of meals.",
            tools=[{"type": "image_generation"}],
            completion_args={
                "temperature": 0.3,
                "top_p": 0.95,
            }
        )
        print("Created image generation agent")

        # Start conversation with image generation
        response = client.beta.conversations.start(
            agent_id=image_agent.id,
            inputs=f"Generate an appetizing image of: {meal_description}",
            stream=False  # Ensure we get a complete response
        )
        print("Got response from image generation")

        # Create images directory if it doesn't exist
        os.makedirs("generated_images", exist_ok=True)

        # Process the response and save images
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_paths = []

        if hasattr(response, 'outputs'):
            print(f"Processing {len(response.outputs)} outputs")
            for output in response.outputs:
                if hasattr(output, 'content'):
                    print(f"Processing content of type: {type(output.content)}")
                    if isinstance(output.content, list):
                        for i, chunk in enumerate(output.content):
                            print(f"Processing chunk {i} of type: {type(chunk)}")
                            if isinstance(chunk, ToolFileChunk):
                                print(f"Found ToolFileChunk with file_id: {chunk.file_id}")
                                try:
                                    # Download the image
                                    file_bytes = client.files.download(file_id=chunk.file_id).read()
                                    
                                    # Save the image
                                    image_path = f"generated_images/meal_{timestamp}_{i}.png"
                                    with open(image_path, "wb") as file:
                                        file.write(file_bytes)
                                    image_paths.append(image_path)
                                    print(f"Successfully saved image to: {image_path}")
                                except Exception as e:
                                    print(f"Error processing image chunk: {str(e)}")
                    else:
                        print(f"Content is not a list: {output.content}")

        if image_paths:
            print(f"Successfully generated {len(image_paths)} images")
            return image_paths[0]  # Return the first image path
        else:
            print("No images were generated")
            return "No image was generated"
        
    except Exception as e:
        print(f"Error during image generation: {str(e)}")
        if hasattr(e, '__dict__'):
            print(f"Error details: {e.__dict__}")
        return f"Error generating image: {str(e)}" 