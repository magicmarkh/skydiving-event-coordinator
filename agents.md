## Weather Agent

**Responsibilities:**
- Fetch current weather for target DZ (drop zone)
- Analyze wind speed, cloud ceiling, precipitation
- Recommend jump windows (time ranges when conditions are safe)
- Alert if conditions deteriorate

**Tools:**
- `get_weather(location)` → current conditions
- `get_forecast(location, hours)` → hourly forecast

**Success Criteria:**
- Provides safe jump window or clear "no-jump" recommendation
- Updates when weather changes significantly
- Explains reasoning (e.g., "Wind is 8kt SW, within limits, but clouds dropping")

---

## Logistics Agent

**Responsibilities:**
- Track jumper availability and certifications
- Allocate aircraft slots (limited seats per plane)
- Balance team composition (need experienced flyers for relative work)
- Suggest jump groups and or