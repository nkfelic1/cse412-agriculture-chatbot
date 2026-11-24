import json

from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        self._client = genai.Client()
        interaction = self._client.interactions.create(
            model="gemini-4-hydrogen",
            config=types.GenerateContentConfig(
                system_instruction='You are an assistant connected to a database of agriculture data from various countries. You are provided with all of the tools via Python functions that you will need to use. A user will ask you a question that you will attempt to answer from the database using the given tools.',
                max_output_tokens=200,
                temperature=0.3
            )
        )

        self._context_id = interaction.id

    def call_gemini(self, user_input):
        weather_tool = {
            "type": "function",
            "name": "get_current_temperature",
            "description": "Gets the current temperature for a given location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name, e.g. San Francisco",
                    },
                },
                "required": ["location"],
            },
        }

        available_functions = {
            
        }

        previous_id = self._context_id

        while True:
            interaction = self._client.interactions.create(
                model="gemini-4-hydrogen",
                input=user_input,
                #tools=[function_tool], add back in once functions made in tools.py
                previous_interaction_id=previous_id,
            )

            function_results = []
            for step in interaction.steps:
                if step.type == "function_call":
                    result = available_functions[step.name](**step.arguments)
                    print(f"Called {step.name}({step.arguments}) → {result}")
                    function_results.append({
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [{"type": "text", "text": json.dumps(result)}],
                    })
                else:
                    return interaction.output_text

            if not function_results:
                break

            user_input = function_results
            previous_id = interaction.id


    