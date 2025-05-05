from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Connect to MongoDB
client = MongoClient(MONGO_URI)

db = client["school_gk_exam"]

# Collections
students_collection = db["students"]
admins_collection = db["admins"]
questions_collection = db["questions"]
results_collection = db["results"]
