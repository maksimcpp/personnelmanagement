from fastapi import APIRouter
from .views import router as department_router

router = APIRouter(tags=['Department🏤'])
router.include_router(department_router)
