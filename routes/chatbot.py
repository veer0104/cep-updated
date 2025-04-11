# from fastapi import APIRouter, Request
# from pydantic import BaseModel
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Configure Gemini
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Define the model with instructions
# model = genai.GenerativeModel(
#     "gemini-1.5-flash",
#     system_instruction=(
#         "You are a compassionate and empathetic AI mental health companion named MindMate. "
#         "Your goal is to support users emotionally, help them manage stress, anxiety, and emotional challenges. "
#         "Offer grounding techniques, breathing exercises, journaling prompts, and calm reassurances. "
#         "Do not give medical or legal advice. Encourage seeking professional help when needed. "
#         "Always respond with warmth, empathy, and supportive tone. Use bullet points when appropriate and bold important steps or advice."
#     )
# )

# router = APIRouter()

# # Pydantic model for request
# class Message(BaseModel):
#     message: str

# @router.post("/")
# async def chatbot_responder(data: Message, request: Request):
#     try:
#         context = request.session.get('incident_context', '')
#         message = f"Context: {context}\nUser message: {data.message}" if context else data.message

#         response = model.generate_content(message)
#         return {'response': response.text}
#     except Exception as e:
#         return {'error': str(e)}
    
    

# import google.generativeai as genai

# key = ''
# genai.configure(api_key=key)
# model = genai.GenerativeModel("models/gemini-1.5-flash")

# def ai_response(query):
#     try:
#         response = model.generate_content(query)
#         return response.text
#     except Exception as e:
#         return f"Error: {e}"

# if __name__ == "__main__":
    
#     while True:
#         user_input = input("You: ").strip()
#         if user_input.lower() in ['exit', 'quit']:
#             print("Goodbye! See you later.")
#             break
#         elif user_input == "":
#             print("Please enter something.")
#         else:
#             answer = ai_response(user_input)
#             print(f"Output: {answer}")


from fastapi import APIRouter, Request
from pydantic import BaseModel
import google.generativeai as genai
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model with instructions
model = genai.GenerativeModel(
    "gemini-1.5-flash",
    system_instruction=(
        "You are a compassionate and empathetic AI mental health companion named MindMate. "
        "Your goal is to support users emotionally, help them manage stress, anxiety, and emotional challenges. "
        "Offer grounding techniques, breathing exercises, journaling prompts, and calm reassurances. "
        "Do not give medical or legal advice. Encourage seeking professional help when needed. "
        "Always respond with warmth, empathy, and supportive tone. Use bullet points when appropriate and bold important steps or advice."
    )
)

# Define router
router = APIRouter()

# Request body model
class Message(BaseModel):
    message: str

# Reusable Gemini response logic
async def ai_response(query: str) -> str:
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, model.generate_content, query)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Chatbot API route
@router.post("/")
async def chatbot_responder(data: Message, request: Request):
    try:
        # Uncomment below if session middleware is used
        # context = request.session.get('incident_context', '')
        # full_prompt = f"Context: {context}\nUser message: {data.message}" if context else data.message
        
        full_prompt = data.message  # Simpler version without session
        result = await ai_response(full_prompt)
        return {'response': result}
    except Exception as e:
        return {'error': str(e)}