import openai
import os
from typing import *

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_embedding(text: str):
    """Create an embedding for the provided text."""
    embedding = openai.Embedding.create(
        model="text-embedding-ada-002", input=text)
    return text, embedding.data[0].embedding
