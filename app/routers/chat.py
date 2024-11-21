from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from typing import Optional , List
from app.utils.open_api import get_chat_response , retrieve_chat_history

# Initialize the router
router = APIRouter() 


# Define the Pydantic models
class Message(BaseModel): 
    role: str 
    content: str 

class ChatRequest(BaseModel): 
    thread_id: Optional[str] = None 
    assist_id: str 
    messages: list[Message] 

class ChatResponse(BaseModel):
    thread_id: str 
    message_id: str 
    role : str 
    assist_id: Optional[str] 
    content: Optional[str] 

chat_threads = {}

# Define the route for the chat endpoint
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Extract the list of messages from the request
    thread_id = request.thread_id 
    assist_id = request.assist_id 
    messages = request.messages 

    
    try:
        # Get the last message content (assuming it's from the user)
        prompt = messages[0].content 
        
        # Get the assistant's response by calling the OpenAI function
        response_content , message_id , thread_id = get_chat_response(prompt,thread_id,assist_id)
        
        # Create a ChatResponse object with the assistant's reply
        response = ChatResponse(thread_id=thread_id, message_id=message_id,role="assistant", assist_id=assist_id,content=response_content)
            
        # Return the response
        return response
    except Exception as e: 
        # Handle any exceptions that occur during the process
        raise HTTPException(status_code=500, detail=str(e))
    
# Endpoint for retrieving chat history by thread_id
@router.get("/chat/{thread_id}", response_model=List[ChatResponse])
async def get_chat_history(thread_id: str):
    try:
        chat_history = retrieve_chat_history(thread_id) 
        if not chat_history:
            raise HTTPException(status_code=404, detail="No messages found for the thread.")
        return chat_history
    except HTTPException as e:
        raise e


    
# class UserInput(BaseModel): 
#     thread_id: str 
#     assisant_id: str 
#     input : str 
#     message_id: str 
#     thread_id: str 
#     sender: str 
#     content: str 


# asst_PVt5wmKc8jJ1ZrwjEFY3O47g