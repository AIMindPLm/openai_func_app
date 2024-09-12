# utils/openai_api.py
import openai
from openai import AzureOpenAI
import json
from config import AZURE_ENDPOINT, API_KEY, API_VERSION, DEPLOYMENT
from function_map import function_map  # Import the function map
from tools import tools

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)



def call_openai_function_calling(messages, tools):
    response = client.chat.completions.create(
        model=DEPLOYMENT,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0
    )
    return response

def execute_function(function_name, function_args):
    # Use the function map to call the appropriate function
    function = function_map.get(function_name)
    if function:
        return function(**function_args)
    else:
        return "Function not recognized."


def get_chat_response(prompt, messages):
    messages.append({"role": "user", "content": prompt})

    response = call_openai_function_calling(messages, tools)
    print("API Response:", response) 
    response_message = response.choices[0].message
    messages.append(response_message)
    print("Response Message:", response_message)

    function_call = response_message.tool_calls
    print("Function Call:", function_call) 

    if function_call:
        function_name = function_call[0].function.name
        function_args = json.loads(function_call[0].function.arguments)
        function_result = execute_function(function_name, function_args)
        messages.append({
            "tool_call_id": function_call[0].id,
            "role": "tool",
            "name": function_name,
            "content": json.dumps(function_result),
        })
    else:
        return response.choices[0].message.content

    final_response = call_openai_function_calling(messages, tools)
    return final_response.choices[0].message.content
