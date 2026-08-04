from fastapi import APIRouter

from .routes import auth, system, token, user

router = APIRouter()

router.include_router(system.router)
router.include_router(user.router,  prefix="/user")
router.include_router(auth.router)
router.include_router(token.router, prefix="/token")
