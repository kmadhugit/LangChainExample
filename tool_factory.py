from langchain_core.tools import StructuredTool


# --- Define tool functions ---
def get_weather(city: str) -> str:
    if city.lower() == "paris":
        return "Sunny and 30°C"
    return "Cloudy and 20°C"


def get_uv_index(city: str) -> int:
    if city.lower() == "paris":
        return 8
    return 3


def should_wear_sunscreen(weather: str, uv_index: int) -> str:
    if "rain" in (weather or "").lower():
        return "No sunscreen needed due to rain."
    if "sunny" in (weather or "").lower() and uv_index >= 6:
        return "Yes, wear sunscreen."
    if "sunny" in (weather or "").lower() and uv_index >= 3:
        return "Consider sunscreen midday."
    if uv_index >= 6:
        return "Yes, UV index is high; wear sunscreen."
    if uv_index >= 3:
        return "UV is moderate; consider sunscreen."
    return "No sunscreen needed."


# --- Wrap functions as Structured tools (include arg schema) ---
weather_tool = StructuredTool.from_function(
    func=get_weather,
    name="get_weather",
    description="Get the current weather for a city",
)

uv_tool = StructuredTool.from_function(
    func=get_uv_index,
    name="get_uv_index",
    description="Get the UV index for a city",
)

sunscreen_tool = StructuredTool.from_function(
    func=should_wear_sunscreen,
    name="should_wear_sunscreen",
    description="Advise if sunscreen is needed based on weather and UV index",
)

tools = [weather_tool, uv_tool, sunscreen_tool]

__all__ = [
    "get_weather",
    "get_uv_index",
    "should_wear_sunscreen",
    "weather_tool",
    "uv_tool",
    "sunscreen_tool",
    "tools",
]