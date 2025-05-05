from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import json
import re  

# ✅ Set API Key manually
API_KEY = "AIzaSyD9GpZuJtMhWRbVF9kRGIA8cmWKXZkKML0"
genai.configure(api_key=API_KEY)

router = APIRouter()

# ✅ Define Request Model
class QuestionRequest(BaseModel):
    prompt: str
    class_level: int

@router.post("/generate")
def generate_question(request: QuestionRequest):
    if not request.prompt or request.class_level not in range(6, 11):
        raise HTTPException(status_code=400, detail="Invalid prompt or class level")

    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        system_prompt = f"""
        Generate 10 multiple-choice questions for Class {request.class_level}.
        Return JSON format:
        {{hmm
            "questions": [
                {{
                    "question_text": "What is the capital of France?",
                    "options": ["London", "Paris", "Berlin", "Madrid"],
                    "correct_option": 1,
                    "class_level": {request.class_level}
                }},
                ...
            ]
        }}
        """

        response = model.generate_content([system_prompt, request.prompt])
        generated_text = response.text.strip()

        # ✅ Remove markdown code block (```json ... ```)
        cleaned_text = re.sub(r"```json\n(.*?)\n```", r"\1", generated_text, flags=re.DOTALL)

        try:
            generated_questions = json.loads(cleaned_text)
            return {"message": "Questions Generated!", "questions": generated_questions["questions"]}
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to parse AI response: {cleaned_text}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

