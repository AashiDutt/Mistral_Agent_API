# Mistral Agents API: AI Nutrition Coach Demo

This project showcases how to build an intelligent, multi-agent assistant using the new [Mistral Agents API](https://console.mistral.ai). You'll learn to combine LLM reasoning with web search, calorie estimation, logging, and image generation tools — all orchestrated through agentic workflows.


---

## What You'll Learn

- How to use **Mistral's Agents API** to build action-taking AI agents
- The difference between **agents vs. models**, **connectors vs. custom tools**
- How to manage **persistent conversations**, **handoffs**, and **tool orchestration**
- How to use built-in connectors: `web_search`, `image_generation`
- How to wrap everything into a real-time **Gradio web app**

---

## Demo Use Case: AI Nutrition Coach

This assistant performs the following steps:

1. The user inputs a meal description.
2. The **Web Search Agent** queries real-time calorie information.
3. If unavailable, a fallback **calorie estimator** guesses the value.
4. The **Logger Agent** stores this entry with calories and timestamp.
5. The **Next Meal Agent** suggests a follow-up meal.
6. The **Image Generation Agent** visualizes the suggestion.

---

## Getting Started

1. Clone the Repository

```bash
git clone https://github.com/AashiDutt/Mistral_Agent_API.git
cd Mistral_Agent_API
```
2. Set Up the Environment
   
Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file:

```dotenv
MISTRAL_API_KEY=your_api_key_here
```

4. Run the App

```bash
python app.py
```
## Project Structure

Mistral_Agent_API/
│
├── tools/                      # All tools and agents

│   ├── configs.py              # Mistral client, tool schemas

│   ├── image_gen.py            # Food image generation logic

│   ├── next.py                 # Calorie estimator, logger, next meal suggester

│   └── web_search.py           # Web search agent using built-in connector
│
├── agent.py                    # Main pipeline logic for chaining tools


├── app.py                      # Gradio frontend interface

├── .env                        # API key config (not to be shared)

├── requirements.txt            # Project dependencies

└── generated_images/           # Stores generated meal images

