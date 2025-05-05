from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, admin, exam, results, question_selector, progress, question_generator

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])  #  Admin router added
app.include_router(exam.router, prefix="/exam", tags=["Exam"])
app.include_router(results.router, prefix="/results", tags=["Results"])
app.include_router(question_selector.router, tags=["Question Selector"])
app.include_router(progress.router, tags=["Progress"])
app.include_router(question_generator.router, prefix="/question_generator", tags=["Question Generator"])

@app.get("/")
def home():
    return {"message": "Welcome to the School GK Exam System"}
