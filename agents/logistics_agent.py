# agents/logistics_agent.py

import anthropic
import json
from tools.logistic_tools import get_jumpers, get_aircraft, reserve_slot
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def run_logistics_agent(jump_date: str, location: str) -> str:
    """
    Logistics Agent: Allocate jumpers to aircraft and create jump schedule.
    """
    
    tools = [
        {
            "name": "get_jumpers",
            "description": "Get list of available jumpers for the event",
            "input_schema": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "Event date (YYYY-MM-DD)"
                    }
                },
                "required": ["date"]
            }
        },
        {
            "name": "get_aircraft",
            "description": "Get available aircraft and capacity",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Drop zone"
                    }
                },
                "required": ["location"]
            }
        },
        {
            "name": "reserve_slot",
            "description": "Book a jumper in an aircraft load",
            "input_schema": {
                "type": "object",
                "properties": {
                    "jumper_id": {"type": "string"},
                    "aircraft_id": {"type": "string"},
                    "jump_time": {"type": "string"}
                },
                "required": ["jumper_id", "aircraft_id", "jump_time"]
            }
        }
    ]
    
    messages = [
        {
            "role": "user",
            "content": f"""You are a skydiving event coordinator. Your job is to create an optimal jump schedule.

Date: {jump_date}
Location: {location}

RULES YOU MUST FOLLOW:
1. Aircraft must be at least 75% full before being scheduled to fly.
   - Example: A 14-seat Otter needs at least 11 jumpers before it flies.
   - Example: A 4-seat Cessna needs at least 3 jumpers before it flies.
   - If you don't have enough jumpers to meet this threshold, combine 
     jumpers into fewer loads rather than sending a mostly-empty aircraft.
2. Relative work (RW) teams need 3+ experienced jumpers minimum.
3. Beginner jumpers can do solo jumps.
4. A single aircraft load can carry multiple jumper groups of different 
   disciplines simultaneously, exiting in sequence. For example: an RW 
   team and a solo AFF jumper CAN share the same load/aircraft — the RW 
   team exits first, then the solo jumper exits afterward. Do not create 
   a separate load just because jumpers have different disciplines or 
   certifications, as long as the aircraft has capacity and exit order 
   is respected.
5. Before excluding any jumper from a load, check whether they could 
   exit as a separate group on the SAME aircraft rather than requiring 
   a new one. Maximizing aircraft fill rate takes priority over grouping 
   by discipline alone.
6. Organize jumpers into groups within the same plane. Exit order goes 
   by jump type, then group size within the jump discipline.
   - Discipline exit order: RW, Freefly, Tandem, Wingsuit, High Pull
   - Group Size exit order: largest to smallest
7. Do not overbook — check for conflicts before reserving a slot.

Your task:
1. Check available jumpers and their certifications
2. Check available aircraft and capacity
3. Determine how many loads are actually needed given the jumper count 
   and the 75% fill rule above. Prioritize combining different-discipline 
   groups onto the same aircraft over creating additional loads.
4. Create teams that are safe and balanced
5. Reserve slots for all jumpers
6. Before finalizing, VERIFY that your written summary matches exactly 
   what you reserved — cross-check jumper count per load against your 
   actual reserve_slot calls
7. Provide a final schedule showing:
   - Jump load number
   - Jumpers assigned (list each by name/ID), grouped by discipline group
   - Aircraft
   - Percent full
   - Jump time
   - Exit order (which group exits first, second, etc.)

Ensure no overbooking and all safety/capacity requirements are met.
Explain your reasoning for team composition and aircraft selection."""
        }
    ]
    
    # Same agentic loop pattern
    while True:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        
        if response.stop_reason == "tool_use":
            tool_results = []
            for content in response.content:
                if content.type == "tool_use":
                    tool_name = content.name
                    tool_input = content.input
                    
                    if tool_name  == "get_jumpers":
                        result = get_jumpers(tool_input["date"])
                    elif tool_name == "get_aircraft":
                        result = get_aircraft(tool_input["location"])
                    elif tool_name  == "reserve_slot":
                        result = reserve_slot(
                            tool_input["jumper_id"],
                            tool_input["aircraft_id"],
                            tool_input["jump_time"]
                        )
                    else:
                        result = {"error": f"Unknown tool: {tool_name}"}
                    
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": content.id,
                        "content": json.dumps(result)
                    })
            
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            final_response = ""
            for content in response.content:
                if hasattr(content, "text"):
                    final_response += content.text
            return final_response
        
if __name__ == "__main__":
    jump_date = "2024-02-15"
    location = "Skydive Arizona"
    
    print(f"Building jump schedule for {location} on {jump_date}\n")
    
    result = run_logistics_agent(jump_date, location)
    print(result)