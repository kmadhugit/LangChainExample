tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_weather',
            'description': 'Get the weather for a city',
            'parameters': {
                'type': 'object',
                'properties': {'city': {'type': 'string'}},
                'required': ['city']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_uv_index',
            'description': 'Get the UV index for the city',
            'parameters': {
                'type': 'object',
                'properties': {'city': {'type': 'string'}},
                'required': ['city']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'should_wear_sunscreen',
            'description': 'Advise if sunscreen is needed based on weather and UV index',
            'parameters': {
                'type': 'object',
                'properties': {
                    'weather': {'type': 'string'},
                    'uv_index': {'type': 'number'}
                },
                'required': ['weather', 'uv_index']
            }
        }
    }
]


