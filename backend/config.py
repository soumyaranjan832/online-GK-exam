import os
from dotenv import load_dotenv

# Load environment variables


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your_google_gemini_api_key")



MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "school_gk_exam"
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


