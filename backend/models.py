from pydantic import BaseModel
from typing import List
from pydantic import EmailStr

class Student(BaseModel):
    name: str
    email: str
    password: str
    student_class: int

class Question(BaseModel):
    question_text: str
    options: List[str]
    correct_option: int  # Index of correct option (0-based index)
    class_level: int  # Class level (1-10)

class Answer(BaseModel):
    question_text: str
    selected_option: int
    class_level: int
class ExamSubmission(BaseModel):
    student_name: str  #  Ensure student name is included
    student_email: str
    answers: List[Answer]
class Token(BaseModel):
    access_token: str
    token_type: str
class Question(BaseModel):
    question_text: str
    options: list[str]
    correct_option: int
    class_level: int
class AdminRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    secret_code: str
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    class_level: int  #  Ensure class_level is included
