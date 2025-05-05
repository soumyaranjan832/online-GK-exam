from fastapi import APIRouter, HTTPException
from database import results_collection
import pandas as pd
from database import students_collection

router = APIRouter()

@router.get("/progress/{student_email}")
def get_student_progress(student_email: str):
    results = list(results_collection.find({"student_email": student_email}, {"_id": 0}))

    if len(results) < 2:
        raise HTTPException(status_code=404, detail="Not enough results to compare progress")

    # Sort results by date
    df = pd.DataFrame(results).sort_values("exam_date")

    progress_data = {
        "student_email": student_email,
        "scores": df[["exam_date", "score"]].to_dict(orient="records"),
    }

    return progress_data
@router.get("/get-students")
def get_all_students():
    students = list(students_collection.find({}, {"_id": 0, "name": 1, "email": 1}))
    if not students:
        return []
    return students
