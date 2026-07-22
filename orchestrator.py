# orchestrator.py

from agents.weather_agent import run_weather_agent
from agents.logistics_agent import run_logistics_agent
import json
from datetime import datetime

def coordinate_event(location: str, jump_date: str, target_time: str) -> dict:
    """
    Orchestrator: The director of the agent team.
    
    Why a separate orchestrator?
    - Agents have specific expertise (weather, logistics)
    - Orchestrator handles communication between them
    - Easier to test each agent independently
    - Easier to add new agents later
    
    Pattern: Sequential execution with information passing
    Future pattern: Parallel execution (agents run simultaneously)
    """
    
    print(f"\n{'='*60}")
    print(f"SKYDIVING EVENT COORDINATOR")
    print(f"Event: {location} on {jump_date}")
    print(f"{'='*60}\n")
    
    # STEP 1: Weather Agent decides if we can jump
    print("[PHASE 1] Checking weather conditions...")
    print("-" * 60)
    
    weather_report = run_weather_agent(location, target_time)
    print(f"\nWeather Agent Report:\n{weather_report}\n")
    
    # Parse if jump is possible (in production, structure output better)
    can_jump = "safe" in weather_report.lower() or "recommend jump" in weather_report.lower()
    
    if not can_jump:
        print("\n⚠️  Weather unsafe. Canceling event.")
        return {
            "status": "CANCELED",
            "reason": "unsafe_weather",
            "weather_report": weather_report,
            "jumpers_assigned": []
        }
    
    # STEP 2: Logistics Agent creates schedule
    print("\n[PHASE 2] Building jump schedule...")
    print("-" * 60)
    
    logistics_report = run_logistics_agent(jump_date, location)
    print(f"\nLogistics Agent Report:\n{logistics_report}\n")
    
    # STEP 3: Combine reports
    final_report = {
        "status": "GO",
        "event_date": jump_date,
        "location": location,
        "weather_approved": True,
        "weather_report": weather_report,
        "logistics_report": logistics_report,
        "generated_at": datetime.now().isoformat()
    }
    
    return final_report

if __name__ == "__main__":
    # Example usage
    event = coordinate_event(
        location="Skydive Arizona",
        jump_date="2024-02-15",
        target_time="10:00 AM"
    )
    
    print("\n" + "="*60)
    print("FINAL EVENT STATUS")
    print("="*60)
    print(json.dumps(event, indent=2))