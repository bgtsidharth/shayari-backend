from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import openai

# Initialize FastAPI app
app = FastAPI()

# CORS setup so your GitHub Pages frontend can call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your domain for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your OpenAI key (set this securely in Render as an environment variable)
openai.api_key = "your-openai-api-key"

# Define request model
class QRData(BaseModel):
    keyword: str
    emotion: str = "romantic"

# Route to generate shayari
@app.post("/generate")
async def generate_shayari(data: QRData):
    prompt = f"Write a short Hindi shayari about '{data.keyword}' with a '{data.emotion}' mood. Keep it poetic, 2 to 4 lines."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        shayari = response.choices[0].message.content.strip()
        return {"text": shayari}
    except Exception as e:
        return {"text": "Sorry, couldn't generate shayari.", "error": str(e)}
