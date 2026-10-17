# import requests
# import os
#
# print('SSL_CERT_FILE=', os.getenv('SSL_CERT_FILE'))
# print('REQUESTS_CA_BUNDLE=', os.getenv('REQUESTS_CA_BUNDLE'))
#
# response = requests.get("https://www.google.com")
# print(response.status_code)


from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
# import random
from py_tools.tool_config import tool_config

from database.db_functions import get_all_todos, add_todo
from utils.tool_mapper import tool_mapper

print("Calling main app...")

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "models/gemini-3-flash-preview"

available_models = [
    model.name
    for model in client.models.list()
    if "generateContent" in model.supported_actions and model
]

print(available_models,"available models")

# MODEL = random.choice(available_models)

# print(MODEL, "selected model")

# chat = client.chats.create(
#     model=MODEL
# )

# response = chat.send_message(
#     prompt,
#
# )
#
# print(response.text)



while True:
    prompt = input("Ask your question (or type 'quit'): ")
    if prompt.lower() == "quit":
        break
    
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=tool_config
    )

    if response.function_calls:
        function_call = response.function_calls[0]
        tool_function = tool_mapper[function_call.name]
        function_response = types.Part.from_function_response(
            name=function_call.name,
            response={"result": tool_function()}
        )
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=prompt)]
                ),
                response.candidates[0].content,
                types.Content(role="user", parts=[function_response])
            ],
            config=tool_config
        )

    print(response.text or response)
