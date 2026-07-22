def get_jumpers(date: str) -> dict:
    """Get list of available jumpers for the event.
    
    For now, this returns fake data (mock).
    In production, you'd query a real database or booking system.
    """
    return {
        "date": date,
        "total_jumpers": 8,
        "jumpers": [
            {
                "id": "J001",
                "name": "Alice",
                "certifications": ["AFF", "RW", "Canopy-Expert"],
                "experience_jumps": 500,
                "available": True
            },
            {
                "id": "J002",
                "name": "Bob",
                "certifications": ["AFF"],
                "experience_jumps": 45,
                "available": True
            },
            {
                "id": "J003",
                "name": "Carla",
                "certifications": ["AFF", "RW"],
                "experience_jumps": 320,
                "available": True
            },
            {
                "id": "J004",
                "name": "Dave",
                "certifications": ["AFF", "RW", "Canopy-Expert"],
                "experience_jumps": 800,
                "available": True
            }
        ],
        "summary": {
            "experienced_rw": 2,
            "intermediate": 1,
            "beginners": 1,
            "conflicts": []
        }
    }


def get_aircraft(location: str) -> dict:
    """Get available aircraft and capacity for a location."""
    return {
        "location": location,
        "aircraft": [
            {
                "id": "A001",
                "type": "Cessna 182",
                "capacity": 4,
                "available_times": ["09:00", "10:00", "11:00", "13:00"]
            },
            {
                "id": "A002",
                "type": "Twin Otter",
                "capacity": 14,
                "available_times": ["10:00", "12:00", "14:00"]
            }
        ]
    }


def reserve_slot(jumper_id: str, aircraft_id: str, time: str) -> dict:
    """Book a jumper into an aircraft load.
    
    For now, this just returns a success confirmation (mock).
    In production, this would write to a real scheduling database
    and check for conflicts before booking.
    """
    return {
        "status": "confirmed",
        "jumper_id": jumper_id,
        "aircraft_id": aircraft_id,
        "time": time,
        "message": f"Jumper {jumper_id} reserved on {aircraft_id} at {time}"
    }


def check_conflicts(jumper_id: str, time: str) -> dict:
    """Verify a jumper isn't double-booked at this time.
    
    Mock version always returns no conflict.
    """
    return {
        "jumper_id": jumper_id,
        "time": time,
        "has_conflict": False
    }