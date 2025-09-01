from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
import os
from pydantic import BaseModel

app = FastAPI()

#setting gemini api key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)


'''Made class Named as ChatRequest and ChatResponse which
 have two attributes One for incoming data from client side named as user_prompt
 while other is outgoing data from server side named as ai_reponse both should be string
 which validation is done bye base model class from pydantic'''
class ChatRequest(BaseModel):
    user_prompt : str

class ChatResponse(BaseModel):
    ai_response : str

''''''
@app.post("/chat", response_model=ChatResponse)
def chat(prompt : ChatRequest):
    model= genai.GenerativeModel('gemini-1.5-flash')
    try:
      response =model.generate_content(prompt.user_prompt)
      return ChatResponse(ai_response = response.text)
    except Exception as e:
      return "Something went wrong didn't get the response from AI"