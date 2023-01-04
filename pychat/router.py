from fastapi import APIRouter

from pychat.auth import routes as auth_routes
from pychat.user import routes as user_routes

router = APIRouter()
api_router = APIRouter(prefix="/api")

api_router.include_router(auth_routes.api_router)
router.include_router(auth_routes.view_router, tags=[""])

api_router.include_router(user_routes.api_router)
router.include_router(user_routes.view_router)
