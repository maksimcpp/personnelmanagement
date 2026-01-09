from fastapi import APIRouter
from .user import routers as user_router
from .auth import routers as auth_router
from .department import routers as department_router
from .team import routers as team_router
from .employee import routers as employee_router

router = APIRouter(prefix='/api/v1')
router.include_router(user_router.router)
router.include_router(auth_router.router)
router.include_router(department_router.router)
router.include_router(team_router.router)
router.include_router(employee_router.router)
