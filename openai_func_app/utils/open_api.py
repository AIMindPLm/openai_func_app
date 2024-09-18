# utils/openai_api.py
import openai
from openai import AzureOpenAI
import json
from config import AZURE_ENDPOINT, API_KEY, API_VERSION, DEPLOYMENT
from utils.validator import valid_function_names
from tools import tools
from .helpers import is_within_scope

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
    valid = valid_function_names()
    function = valid.get(function_name)
    if function:
        return function(**function_args)
    else:
        return "Function not implemented"


# Function to get a chat response from OpenAI
def get_chat_response(prompt, messages):
    # Initialize messages with system role
    messages.append({"role": "user", "content": prompt})

    # Get the response from OpenAI
    response = call_openai_function_calling(messages, tools)
    response_message = response.choices[0].message
    messages.append(response_message)

    # Check if there is a function call
    function_call = response_message.tool_calls

    if function_call:
        # Get the function name and arguments
        function_name = function_call[0].function.name
        print(f"Fecthing Function_name{function_name}")
        function_args = json.loads(function_call[0].function.arguments)
        print(f"Fetching Function_args{function_args}")

        valid_functions = valid_function_names()
        # Execute the function and store the result
        if function_name in valid_functions:

            function_result = execute_function(function_name, function_args)


            # Append the result of the function execution to the messages
            messages.append({
                "tool_call_id": function_call[0].id,
                "role": "tool",
                "name": function_name,
                "content": str(function_result),
            })
             # Second API call: Get the final response from the model
            final_response = call_openai_function_calling(messages, tools)

            return final_response.choices[0].message.content
        else:
            # Handle the case where the function name is not valid
            print(f"Out-of-scope function call: {function_name}")

            return "Sorry, I can only provide data related to the application."

    else:
        # No function call, use the response content directly
        if is_within_scope(prompt):
            print("No tool calls were made by the model.")
            return response_message.content

        else:
             print("Out-of-scope query.")
            #  return "Sorry, I can only provide data related to the application."
             return response.choices[0].message.content
