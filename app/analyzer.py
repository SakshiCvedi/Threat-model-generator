import json
import os
from groq import Groq
from dotenv import load_dotenv
from app.prompts import THREAT_MODEL_SYSTEM_PROMPT
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")


def generate_threat_model(parsed_input: dict) -> dict:
    """
    Takes the parsed input dict from parser.py
    Sends it to Groq API (LLaMA 3 model)
    Returns a structured threat model as a Python dict
    """

    # Step 1: Create Groq client
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    # Step 2: Build the user message
    user_message = f"""
Please analyze this architecture and generate a threat model:

{parsed_input['content']}
"""

    # Step 3: Call Groq API
    print("Contacting Groq API...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": THREAT_MODEL_SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.7,
        max_tokens=2000
    )

    # Step 4: Extract raw text
    raw_text = response.choices[0].message.content.strip()

    # Step 5: Clean markdown fences if model added them
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        if "```" in raw_text:
            raw_text = raw_text.split("```")[0]

    raw_text = raw_text.strip()

    # Step 6: Parse into Python dict
    try:
        threat_model = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"\nJSON parsing failed. Raw response was:\n{raw_text}")
        raise e

    return threat_model