import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).resolve().parent.parent / ".env.local")
# load_dotenv(Path(__file__).resolve().parent.parent / ".env")


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# api_key=os.environ["GEMINI_API_KEY"]

MODEL = "models/gemini-3.1-flash-lite-preview"
