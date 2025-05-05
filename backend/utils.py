import random
from database import questions_collection

def get_random_questions(class_level: int, num_questions: int = 10):
    """Fetches a random set of questions for a given class level without repetition."""
    all_questions = list(questions_collection.find({"class_level": class_level}, {"_id": 0}))
    random.shuffle(all_questions)
    return all_questions[:num_questions] if all_questions else []