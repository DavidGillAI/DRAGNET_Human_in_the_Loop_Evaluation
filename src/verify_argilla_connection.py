import os

import argilla as rg
from dotenv import load_dotenv


load_dotenv()

api_url = os.getenv("ARGILLA_API_URL")
api_key = os.getenv("ARGILLA_API_KEY")

if not api_url or not api_key:
    raise RuntimeError("ARGILLA_API_URL or ARGILLA_API_KEY is missing from .env")

client = rg.Argilla(
    api_url=api_url,
    api_key=api_key,
)

print("Connected to Argilla successfully.")
print(f"Authenticated user: {client.me.username}")