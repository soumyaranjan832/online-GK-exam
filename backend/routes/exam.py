from fastapi import APIRouter, HTTPException, File, UploadFile,Depends
from pydantic import BaseModel
from typing import List
from database import questions_collection
import pandas as pd
import io

router = APIRouter()

class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_option: int
    class_level: int
class BulkQuestionsRequest(BaseModel):
    questions: List[Question]

@router.post("/add-questions-bulk")
def add_questions_bulk(request: BulkQuestionsRequest):
    try:
        if not request.questions:
            raise HTTPException(status_code=400, detail="No questions provided.")

        inserted = questions_collection.insert_many([q.dict() for q in request.questions])
        return {"message": f"{len(inserted.inserted_ids)} questions added successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/upload-questions")
async def upload_questions(file: UploadFile = File(...)):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Read the Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        # Check if required columns exist
        required_columns = ["question_text", "options", "correct_option", "class_level"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise HTTPException(status_code=400, detail=f"Missing columns: {missing_columns}")

        # Convert "options" from a string to a list
        questions = []
        for _, row in df.iterrows():
            try:
                question = {
                    "question_text": row["question_text"],
                    "options": row["options"].split(",") if isinstance(row["options"], str) else [],
                    "correct_option": int(row["correct_option"]),
                    "class_level": int(row["class_level"]),
                }
                questions.append(question)
            except Exception as e:
                print(f"Error processing row {row}: {e}")

        if not questions:
            raise HTTPException(status_code=400, detail="No valid questions found in the file.")

        # Insert into MongoDB
        questions_collection.insert_many(questions)

        return {"message": "Questions uploaded successfully!"}

    except Exception as e:
        print(f"Upload Error: {e}")  # Debugging in console
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-question")
def add_question(question: Question):
    """Add a manually entered question to MongoDB."""
    try:
        new_question = {
            "question_text": question.question_text,
            "options": question.options,
            "correct_option": question.correct_option,
            "class_level": question.class_level,
        }
        questions_collection.insert_one(new_question)
        return {"message": "Question added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))