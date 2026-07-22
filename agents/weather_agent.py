# agents/weather_agent.py

import anthropic
import json
from tools.weather_tools import get_weather, get_forecast
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
from datetime import datetime, timedelta

current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
target_jump_time = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def run_weather_agent(location: str, target_jump_time: str) -> str:
    """
    Weather Agent: Analyze conditions and recommend jump windows.
    
    Why use agentic reasoning here?
    - Weather changes throughout the day
    - Agent should check forecast, not just current conditions
    - Agent should explain its reasoning (trust for customers)
    - Agent might need to check multiple times/locations
    
    The agent will:
    1. Get current weather
    2. Get forecast
    3. Analyze safety
    4. Recommend action
    """
    
    # Define tools the agent can use
    tools = [
        {
            "name": "get_current_weather",
            "description": "Fetch current weather conditions for a drop zone",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Drop zone name (e.g., 'Skydive Arizona')"
                    }
                },
                "required": ["location"]
            }
        },
        {
            "name": "get_forecast",
            "description": "Get hourly weather forecast for the next N hours",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Drop zone name"
                    },
                    "hours": {
                        "type": "integer",
                        "description": "Number of hours to forecast (1-24)"
                    }
                },
                "required": ["location", "hours"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"""Current date/time: {current_time}
            You are a skydiving weather expert. Analyze conditions for a jump event.

Location: {location}
Target jump time: {target_jump_time}

Requirements:
- Wind must be under 15 knots
- Cloud ceiling must be above 3000 feet
- No precipitation

Your task:
1. Check current conditions
2. Get a 6-hour forecast
3. Recommend whether to jump now, wait for a specific time, or cancel today
4. Explain your reasoning clearly

The jumpers are waiting for your decision."""
        }
    ]
    
    # Agentic loop: Keep calling Claude until it doesn't request tools
    while True:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = []
            
            for content in response.content:
                if content.type  == "tool_use":
                    tool_name = content.name
                    tool_input = content.input
                    
                    # Execute the tool
                    if tool_name == "get_current_weather":
                        result = get_weather(tool_input["location"])
                    elif tool_name == "get_forecast":
                        result = get_forecast(
                            tool_input["location"],
                            tool_input.get("hours", 6)
                        )
                    else:
                        result = {"error": f"Unknown tool: {tool_name}"}
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": json.dumps(result)
                    })
            
            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
            
        else:
            # Claude is done thinking; extract final response
            final_response = ""
            for content in response.content:
                if hasattr(content, "text"):
                    final_response += content.text
            
            return final_response

# Test it
if __name__ == "__main__":
    location = "Skydive Arizona"
    jump_time = (datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    result = run_weather_agent(location, jump_time)
    print(result)