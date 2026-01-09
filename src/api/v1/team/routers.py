from fastapi import APIRouter
from .views import router as team_router

router = APIRouter(tags=['Team🧑‍🤝‍🧑'])
router.include_router(team_router)
