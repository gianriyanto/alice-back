from fastapi import FastAPI
from .user.routes import router as user_router
from . import health, user


def register_api_routes(app: FastAPI):
    """ register all your routers with the main app """

    app.include_router(health.router, tags=["API Health"])
    app.include_router(user_router, prefix="/api", tags=["User"])
