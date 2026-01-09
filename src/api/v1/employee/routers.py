from fastapi import APIRouter

from .views import router as employee_router

router = APIRouter(tags=['Employee👷‍♂️'])
router.include_router(employee_router)
