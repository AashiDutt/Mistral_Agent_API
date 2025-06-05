# Web search tool
import re
from mistralai import Mistral, UserMessage, SystemMessage
from tools.configs import client

def search_calories(meal_desc):
    """
    Search for calorie information about a meal using web search.
    
    Args:
        meal_desc (str): Description of the meal
        
    Returns:
        int: Estimated calories or 0 if search fails
    """
    try:
        # Create web search agent
        websearch_agent = client.beta.agents.create(
            model="mistral-medium-2505",
            description="Agent able to search for nutritional information and calorie content of meals",
            name="Nutrition Search Agent",
            instructions="You have the ability to perform web searches with `web_search` to find accurate calorie information. Return ONLY a single number representing total calories.",
            tools=[{"type": "web_search"}],
            completion_args={
                "temperature": 0.3,
                "top_p": 0.95,
            }
        )

        # Start conversation with web search
        response = client.beta.conversations.start(
            agent_id=websearch_agent.id,
            inputs=f"What are the total calories in {meal_desc}? Respond with ONLY a single number."
        )

        # Print the raw response for debugging
        print("Raw response:", response)

        # Extract the number from the response
        if hasattr(response, 'outputs'):
            for output in response.outputs:
                if hasattr(output, 'content'):
                    # If content is a string, try to extract numbers directly
                    if isinstance(output.content, str):
                        numbers = re.findall(r'\d+', output.content)
                        if numbers:
                            return int(numbers[0])
                    # If content is a list, check each chunk
                    elif isinstance(output.content, list):
                        for chunk in output.content:
                            if hasattr(chunk, 'text'):
                                numbers = re.findall(r'\d+', chunk.text)
                                if numbers:
                                    return int(numbers[0])

        print("No calorie information found in web search response")
        return 0
        
    except Exception as e:
        print(f"Error during web search: {str(e)}")
        return 0
