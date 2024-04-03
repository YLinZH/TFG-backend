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

@app.post("/hello")
async def get_root(request: PromptRequest):
    return "Hello World " + request.prompt

@app.get("/zzz")
async def get_root():
    openai.api_key = os.getenv("API_KEY")
    return "Hello World " + openai.api_key

@app.post("/simplify-text")
async def simplify_text(request: PromptRequest):
    openai.api_key = os.getenv("API_KEY")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": "Ets un assistent útil dissenyat per simplificar textos complexos. El teu objectiu és convertir el text d'entrada en un nou text amb paraules i estructures més senzilles on cada frase és curta, mantenint el significat original. Recorda que el text que proporciones ha de utilitzar la idioma espanyol. Això ajudarà les persones amb dificultats cognitives a entendre millor el contingut. Proporciona únicament el text simplificat sense afegir cap introducció, comentari o paraules addicionals."
            },
            {
                "role": "user",
                "content": "Necessito ajuda per simplificar el següent text: " + request.prompt + ".\n Podries convertir-lo en un text més senzill i fàcil d'entendre? Utilitza paraules comunes i frases curtes."
            }
        ],
        n=1,
        stop=None,
        temperature=0.3,
    )

    # Extract the simplified text from the API response
    simplified_text = response.choices[0].message.content.strip()

    return simplified_text
