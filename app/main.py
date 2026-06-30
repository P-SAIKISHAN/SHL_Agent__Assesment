from fastapi import FastAPI
from app.schemas import ChatRequest
from app.agent import handle_messages

app = FastAPI(title="SHL Assessment Recommendation Agent")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):
    return handle_messages(request.messages)