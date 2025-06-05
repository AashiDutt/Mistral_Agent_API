#Configuration file
from mistralai import Mistral, UserMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Mistral model
mistral_model = "mistral-large-latest"

# Mistral client
client = Mistral(api_key=os.environ.get("MISTRAL_API_KEY"))

# Agent IDs
web_search_id = "web_search_agent"
food_logger_id = "food_logger_agent"
user_assistant_id = "user_assistant_agent"
image_generator_id = "image_generator_agent"

# Tool definitions
tools = {
    "log_meal": {
        "name": "log_meal",
        "description": "Log a user's meal with calorie count",
        "input_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "meal": {"type": "string"},
                "calories": {"type": "number"},
                "timestamp": {"type": "string", "format": "date-time"}
            },
            "required": ["username", "meal", "calories", "timestamp"]
        }
    },
    "web_search": {
        "name": "web_search",
        "description": "Search the web for information about a meal",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
}

def create_chat_completion(messages, model=mistral_model):
    """Helper function to create chat completions"""
    # Convert messages to new format
    formatted_messages = []
    for msg in messages:
        if msg["role"] == "system":
            formatted_messages.append(SystemMessage(content=msg["content"]))
        else:
            formatted_messages.append(UserMessage(content=msg["content"]))
    
    return client.chat.complete(
        model=model,
        messages=formatted_messages
    )

# Register tools
def register_tools():
    for tool_name, tool in tools.items():
        print(f"Registered tool: {tool_name}")

# Register agents
def register_agents():
    print("Registered User Assistant Agent")
    print("Registered Web Search Agent")
    print("Registered Food Logger Agent")

# Initialize everything
def initialize():
    register_tools()
    register_agents()
    check_client()

# Check if the client is initialized
def is_client_initialized():
    return client is not None and os.environ.get("MISTRAL_API_KEY") is not None

def check_client():
    if not is_client_initialized():
        print("Mistral client is not initialized. Please check your API key.")
        return False
    print("Mistral client is initialized.")
    return True

# Initialize everything when the module is imported
initialize()
