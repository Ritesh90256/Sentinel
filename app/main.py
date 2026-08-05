from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Optional
from app.rate_limiter import TokenBucket
from app.cache import ResponseCache


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

bucket = TokenBucket(
    capacity = 5,
    refill_rate = 1.0
)

cache = ResponseCache()

app = FastAPI(title="Sentinel : AI Gateway")

class ChatRequest(BaseModel):
    prompt: str
    provider: Optional[str] = "groq"

@app.post("/chat")
def chat(request: ChatRequest):

    cached_response = cache.get(
        request.prompt,
        request.provider
    )

    if cached_response is not None:
        return{
            "provider" : request.provider,
            "response" : cached_response,
            "cached" : True
        }

    if not bucket.allow_request():
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later."
        )

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

        cache.set(
            request.prompt,
            request.provider,
            response.choices[0].message.content
        )

        return {
            "provider": "openai",
            "response": response.choices[0].message.content,
            "cached": False
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

    cache.set(
        request.prompt,
        request.provider,
        response.choices[0].message.content
    )

    return {
        "provider": "groq",
        "response": response.choices[0].message.content,
        "cached": False
    }