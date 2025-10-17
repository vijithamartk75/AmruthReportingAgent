from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME", "AI Agent"))

origins = [os.getenv("CORS_ORIGINS", "*")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": f"Hello from {os.getenv('APP_NAME')} backend!"}

@app.post("/chat")
def chat(message: dict):
    user_message = message.get("text", "")
    return {"reply": f"You said '{user_message}'"}
