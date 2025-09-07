#drafter.py
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatGoogleGenerativeAI(model = 'gemini-1.5-flash')
 
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an email assistant. Your task is to write an email on behalf of the user."),
    ("user", "sender email: {from}\nreceiver email: {to}\nsubject: {subject}\n\nWrite the full email body.")
])

prompt = prompt_template.invoke({
    "from": "abc@gmail.com",
    "to": "xyz@gmail.com",
    "subject": "Seeking leave for personal reasons"
})

response = model.invoke(prompt)
print(response.content)

