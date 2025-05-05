from fastapi import APIRouter, HTTPException
from database import questions_collection
import random

router = APIRouter()

def classify_question_difficulty(question_text):
    """
    AI-based function to classify question difficulty (Basic, Intermediate, Advanced).
    Future versions can use NLP models (BERT, TF-IDF, etc.).
    """
    easy_keywords = ["define", "simple", "basic", "example"]
    hard_keywords = ["explain", "analyze", "complex", "advanced"]
    
    if any(word in question_text.lower() for word in easy_keywords):
        return "Easy"
    elif any(word in question_text.lower() for word in hard_keywords):
        return "Hard"
    return "Medium"

@router.get("/ai-select-questions/{class_level}")
def ai_select_questions(class_level: int):
    print(f"Fetching AI-selected questions for class: {class_level}")  #  Debug log

    all_questions = list(questions_collection.find({"class_level": class_level}, {"_id": 0}))
    
    if not all_questions:
        print("No matching questions found!")  #  Debug log
        raise HTTPException(status_code=404, detail="No questions available")

    random.shuffle(all_questions)
    return all_questions[:15]  # Return up to 10 questions