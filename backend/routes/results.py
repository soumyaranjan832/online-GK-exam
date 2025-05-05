from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import results_collection, questions_collection, students_collection
from typing import List
from datetime import datetime

router = APIRouter()

class Answer(BaseModel):
    question_text: str
    selected_option: int
    class_level: int

class ExamSubmission(BaseModel):
    student_email: str
    answers: List[Answer]

@router.post("/submit-exam")
def submit_exam(submission: ExamSubmission):
    student = students_collection.find_one({"email": submission.student_email})
    if not student:
        raise HTTPException(status_code=400, detail="Student not found")
    
    student_name = student.get("name", "Unknown")
    total_questions = len(submission.answers)
    correct_answers = 0

    for answer in submission.answers:
        question = questions_collection.find_one({
            "question_text": answer.question_text,
            "class_level": answer.class_level
        })
        if question and question["correct_option"] == answer.selected_option:
            correct_answers += 1

    mark_obtained = correct_answers  #  Each correct answer = 1 mark
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    #  Save in MongoDB
    results_collection.insert_one({
        "student_email": submission.student_email,
        "student_name": student_name,
        "total_questions": total_questions,
        "correct_answers": correct_answers,  #  Ensure this is saved
        "score": score,
        "exam_date": datetime.utcnow()
    })

    return {"message": "Exam submitted successfully", "score": score, "correct_answers": correct_answers}
@router.get("/get-all")
def get_all_results():
    results = list(results_collection.find({}, {"_id": 0}))  #  Ensure all fields are included

    if not results:
        return []
    
    return results  #  Ensure "mark_obtained" is present in the response