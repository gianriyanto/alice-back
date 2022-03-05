from fastapi import FastAPI

from . import health


def register_api_routes(app: FastAPI):
    """ register all your routers with the main app """

    app.include_router(health.router, tags=["API Health"])
    # app.include_router(cartonization_router, prefix="/api", tags=["Operations"])
