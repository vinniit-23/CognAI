from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model("gemini-1.5-flash", model_provider="google_genai")
response = model.invoke("capital of india")
print(response.content)