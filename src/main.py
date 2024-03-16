from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def get_root():
    return "Hello World"


@app.post("/generate-text")
async def generate_text(request: PromptRequest):
    openai.api_key = "YOUR_API_KEY"
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=request.prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    generated_text = response.choices[0].text.strip()
    return {"text": generated_text}


@app.get("/testText")
async def getTestText():
    api_key = os.getenv("API_KEY")
    return api_key
    