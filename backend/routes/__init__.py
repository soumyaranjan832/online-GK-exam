from .auth import router as auth_router
from .admin import router as admin_router
from .exam import router as exam_router
from .results import router as results_router
from .progress import router as progress_router
from .question_selector import router as question_selector_router
from .question_generator import router as question_generator_router  #  Import here

#  Make routers accessible when importing `routes`
__all__ = [
    "auth_router",
    "admin_router",
    "exam_router",
    "results_router",
    "progress_router",
    "question_selector_router",
    "question_generator_router",
]
