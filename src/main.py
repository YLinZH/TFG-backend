from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

origins = [
    "https://tfg-frontend-zeta.vercel.app",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str
    language: str

class PromptGenerateStory(BaseModel):
    name: str
    age: int
    gender: str
    situation: str
    hobbies: str
    challenges: str
    outcomes: str
    language: str



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
                "content": "Ets un assistent útil dissenyat per simplificar textos complexos. El teu objectiu és convertir el text d'entrada en un nou text amb paraules i estructures més senzilles on cada frase és curta, mantenint el significat original. Això ajudarà les persones amb dificultats cognitives a entendre millor el contingut. Proporciona únicament el text simplificat sense afegir cap introducció, comentari o paraules addicionals."
            },
            {
                "role": "user",
                "content": "Necessito ajuda per simplificar el següent text: \n" + request.prompt + "\n\n Podries convertir-lo en un text més senzill i fàcil d'entendre? Utilitza paraules comunes i frases curtes. El text que has generat ha de ser en " + request.language + "."
            }
        ],
        n=1,
        stop=None,
        temperature=0.3,
    )

    # Extract the simplified text from the API response
    simplified_text = response.choices[0].message.content

    return simplified_text

@app.post("/generate-story")
async def generate_story(request: PromptGenerateStory):
    openai.api_key = os.getenv("API_KEY")
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant that specializes in creating personalized social stories to help individuals with autism or social communication challenges navigate various social situations. Your role is to provide clear, step-by-step guidance, tips, and positive reinforcement to help the user build confidence and skills in social interactions. When generating a social story, consider the specific situation, the individual's needs, potential challenges they may face, and their personal information. Use a supportive and encouraging tone throughout the story."
            },
            {
                "role": "user",
                "content": "generate a small story"
                # "content": "Please generate a social story to help me navigate the following situation: " + request.situation + "." + 
                # "\nHere is some information about me to help you create a more personalized story:" +
                # "\nName: " + request.name +
                # "\nAge: " + str(request.age) +
                # "\nGender: " + request.gender +
                # "\nInterests and hobbies: " + request.hobbies +
                # "Specific challenges related to the situation: " + request.challenges +
                # "\nDesired outcome: " + request.outcomes +
                # "\nPlease include steps, and tips to guide me through the process and help me feel more confident in this social situation. Tailor the story to my age, interests, and specific challenges to make it more relatable and helpful for me. I want you generate the story using the languege: " + request.language + "."
            }
        ],

        n=1,
        stop=None,
        temperature=0.7,
    )
    story = response.choices[0].message.content

    return story
