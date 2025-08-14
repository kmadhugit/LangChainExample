def should_wear_sunscreen(weather: str, uv_index: int) -> str:
    if 'sunny' in weather.lower():
        if uv_index >= 6:
            return 'sunscreen is needed\n'
        if uv_index >= 3:
            return 'Yes, consider sunscreen, especially midday.'
    return 'Sunscreen is optional today.'