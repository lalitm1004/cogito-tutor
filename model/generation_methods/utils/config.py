from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
        OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
        OPENAI_CLIENT: OpenAI = OpenAI(api_key = OPENAI_API_KEY)
        MODEL_NAME: str = "gpt-4o-mini-2024-07-18"
        NUM_FLASHCARDS: int = 20
        NUM_QUIZ_QUESTIONS: int = 10