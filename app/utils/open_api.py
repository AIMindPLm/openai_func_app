# app/utils/openai_api.py

from fastapi import HTTPException
from openai import AzureOpenAI
from openai.types.beta.threads.run import Run
import json
from app.config.config import AZURE_ENDPOINT, API_KEY, API_VERSION
from .validator import valid_function_names
import logging
from time import sleep

client = AzureOpenAI(
    azure_endpoint=AZURE_ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)

#installizing assistant API 
def call_openai_function_calling(tools):
    try :
        logging.info("Calling OpenAI API with messages and tools.")
        response = client.beta.assistants.create(
         name="Arithmetic Assistant",
         instructions="You are an AI Chat bot by providing Response based on arthimetic operation as per user Request",
         tools=tools
         )
        
        logging.info("Received response from OpenAI API.")
        return response
    except Exception as e:
        logging.exception("Exception occurred while calling OpenAI API.", exc_info=e)

def run_conversation(run:Run,thread):

  print("\nrun.required_action\n",run.required_action)
  print("Run id ",run.id)
  if run.status == "requires_action":
    tools_calls = run.required_action.submit_tool_outputs.tool_calls

    tools_outputs = []
    for tool_call in tools_calls:
      Tool_id = tool_call.id
      tools_name = tool_call.function.name
      tools_args = json.loads(tool_call.function.arguments)
      print(f"Function_name {tools_name} and arguments {tools_args}")
      function_map = valid_function_names()  # Call the function to get the dictionary
      function_to_call = function_map.get(tools_name) 
      print(f"function_to_call{function_to_call}")
      response = function_to_call(**tools_args)
      print(f"Function Executed {response}")
      tools_outputs.append({
          "tool_call_id": Tool_id,
          "output": json.dumps(response)
      })
    if tools_outputs:
      run = client.beta.threads.runs.submit_tool_outputs_and_poll(
          thread_id=thread,
          run_id=run.id,
          tool_outputs=tools_outputs
      )
    else:
      print("No tools output to submit")
  return run

def create_message_and_run(assistant,query,thread):
  # if not thread:
  #   thread = client.beta.threads.create()
  
  client.beta.threads.messages.create(
    thread_id=thread,
    role="user",
    content=query
  )
  run = client.beta.threads.runs.create_and_poll(
    thread_id=thread,
    assistant_id=assistant
  )
  return run

def wait_on_run(run, thread):
  while run.status == "queued" or run.status == "in_progress":
    run = client.beta.threads.runs.retrieve(
        thread_id=thread,
        run_id=run.id
    )
    sleep(0.5)
  return run


def get_chat_response(prompt, thread, assistant):
    try:
        # Create a new thread if none is provided
        if not thread:
            thrd_id = client.beta.threads.create()
            thread = thrd_id.id
            logging.info(f"Thread created: {thread}")
            if not thread:
                raise ValueError("Failed to create a thread. No thread ID returned.")
        
        # Create and poll a conversation run
        conv_run = create_message_and_run(assistant=assistant, query=prompt, thread=thread)
        logging.info(f"Conversation run created: {conv_run}")
        
        # Handle required actions
        if conv_run.status == "requires_action":
            run = run_conversation(conv_run, thread)
            logging.info(f"Run after required actions: {run}")
        else:
            run = conv_run

        # Ensure the run is completed
        if run.status != "completed":
            raise ValueError(f"Run did not complete. Current status: {run.status}")
        
        # Retrieve messages from the thread
        messages = client.beta.threads.messages.list(thread_id=thread, order="asc")
        logging.info(f"Messages retrieved: {messages}")
        
        # Extract the assistant's response
        if not messages.data:
            raise ValueError("No messages retrieved from the thread.")
        messages_response = messages.data[-1].content[0].text.value
        last_message_id = messages.data[0].id
        print(f"respone from AI {messages_response}")

        return messages_response, last_message_id , thread

    except Exception as e:
        logging.error(f"Error in get_chat_response: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# def get_chat_response(prompt,thread,assistant):
  
#   # Need to impplement Last_msg_id for getting last message 
#   if thread is None:
#      thread = client.beta.threads.create()
     
#   conv_run = create_message_and_run(assistant=assistant , query=prompt, thread=thread)

#   if conv_run.status == "requires_action":
#      run = run_conversation(conv_run,thread)  

#   if run.status == "completed":
#      messages = client.beta.threads.messages.list(thread_id=thread , order="asc")

#   messages_response = messages.data[0].content[0].text.value
#   last_message_id = messages.data[0].id
  
#   return messages_response , last_message_id

















class ChatMessage:
    def __init__(self, thread_id: str, message_id: str, role: str, assist_id: str, content: str):
        self.thread_id = thread_id
        self.message_id = message_id
        self.role = role
        self.assist_id = assist_id
        self.content = content

    def to_dict(self):
        return {
            "thread_id": self.thread_id,
            "message_id": self.message_id,
            "role": self.role,
            "assist_id": self.assist_id,
            "content": self.content,
        }

def retrieve_chat_history(thread_id: str):
    try:
        # Retrieve messages using the client
        message_lst = client.beta.threads.messages.list(thread_id=thread_id)
        messages = message_lst.data

        # Parse and transform the messages
        chat_history = []
        for msg in messages:
            # Handle content safely
            content = None
            if msg.content:
                try:
                    # Extract the value of text if present
                    content = msg.content[0].text.value
                except (IndexError, AttributeError):
                    # If content structure is unexpected, leave as None
                    content = None

            chat_history.append(ChatMessage(
                thread_id=msg.thread_id,
                message_id=msg.id,
                role=msg.role,
                assist_id=getattr(msg, 'assistant_id', None),  # Use getattr for safe attribute access
                content=content,
            ).to_dict())
        
        return chat_history
    except Exception as e:
        raise Exception(f"Error retrieving chat history: {e}")
