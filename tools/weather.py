def get_weather(city: str) -> str:
    if city.lower() == 'paris':
        return 'Sunny and 30°C'
    else:
        return 'Cloudy and 20°C'