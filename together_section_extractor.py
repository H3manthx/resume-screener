import os
import requests
import json
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
TOGETHER_API_KEY = os.getenv("API_KEY")
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

PROMPT_TEMPLATE = """
You are a resume parser. Extract the following fields from the resume below and return valid JSON:
- objective
- skills
- experience
- education
- projects

If a field is missing, use an empty string.
Return only a valid JSON object.

Resume:
{resume_text}
"""

def extract_resume_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def query_together(prompt, model="mistralai/Mistral-7B-Instruct-v0.1"):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You extract structured data from resumes."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }
    res = requests.post(TOGETHER_URL, headers=headers, json=body)
    if res.status_code != 200:
        print("❌ Error:", res.status_code, res.text)
        return {}

    raw = res.json()["choices"][0]["message"]["content"]
    try:
        json_start = raw.find("{")
        return json.loads(raw[json_start:])
    except Exception as e:
        print("❌ Parsing error:", e)
        return {}