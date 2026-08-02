from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sentinel : AI Gateway")

class ChatRequest(BaseModel):
    prompt: str

@app.post("/chat")
def chat(request: ChatRequest):
    return {
        "message": "request received successfully",
        "prompt": request.prompt
    }