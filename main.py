from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os

# Initialize FastAPI app
app = FastAPI()

# CORS setup for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain for more control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Request schema
class QRData(BaseModel):
    keyword: str
    emotion: str = "romantic"

# POST route to generate shayari
@app.post("/generate")
async def generate_shayari(data: QRData):
    prompt = (
        f"Write a short Hindi shayari with a '{data.emotion}' mood about '{data.keyword}'. "
        "It should be poetic, 2 to 4 lines, and emotionally impactful."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        shayari = response.choices[0].message.content.strip()
        return {"text": shayari}
    except Exception as e:
        return {"text": "Sorry, couldn't generate shayari.", "error": str(e)}
