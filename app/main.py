from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Optional


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI(title="Sentinel : AI Gateway")

class ChatRequest(BaseModel):
    prompt: str
    provider: Optional[str] = "groq"

@app.post("/chat")
def chat(request: ChatRequest):

    if request.provider == "openai":
        response = openai_client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {
                    "role" : "user",
                    "content" : request.prompt
                }
            ]
        )

        return {
            "provider": "openai",
            "response": response.choices[0].message.content
        }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": request.prompt
            }
        ]
    )

    return {
        "provider": "groq",
        "response": response.choices[0].message.content
    }