from datetime import datetime, timezone


def get_weather(location: str) -> dict:
    """Fetch current weather conditions for a drop zone.
    
    Includes data freshness validation so the agent doesn't have to
    infer staleness on its own — it's handed the answer directly.
    """
    mock_data = {
        "location": location,
        "temp_f": 72,
        "wind_speed_kt": 8,
        "wind_direction": "SW",
        "cloud_ceiling_ft": 3500,
        "visibility_mi": 10,
        "precipitation": None,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    data_time = datetime.fromisoformat(mock_data["timestamp"])
    age_minutes = (datetime.now(timezone.utc) - data_time).total_seconds() / 60

    mock_data["data_age_minutes"] = round(age_minutes, 1)
    mock_data["is_stale"] = age_minutes > 15

    return mock_data


def get_forecast(location: str, hours: int = 6) -> list:
    """Get hourly weather forecast for the next N hours.
    
    Each hour includes its own generated timestamp and freshness check,
    since forecast data should be treated the same way as current
    conditions — the agent shouldn't assume it's automatically valid.
    """
    now = datetime.now(timezone.utc)
    forecast = []

    for i in range(hours):
        wind_speed = 8 + (i * 0.5)
        forecast_time = now  # forecast generated "now"; hour offset is what it predicts

        forecast.append({
            "hour": i,
            "forecast_for": f"+{i}h from now",
            "wind_speed_kt": wind_speed,
            "cloud_ceiling_ft": 3500 - (i * 200),
            "safe_to_jump": wind_speed < 15,
            "generated_at": forecast_time.isoformat(),
            "data_age_minutes": 0.0,  # freshly generated at call time
            "is_stale": False
        })

    return forecast