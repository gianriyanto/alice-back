import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from version import __version__
from api import register_api_routes


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_app():
    app = FastAPI(
        title="Project Alice by Gian",
        description="A knowledge management platform for collaborators",
        version=__version__,
        debug=False
    )

    # register middlewares
    app.add_middleware(GZipMiddleware, minimum_size=10000)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routes(app)

    return app


def register_routes(app):
    @app.get("/")
    def read_root():
        """ This is an example docstring comment """
        return RedirectResponse("/docs")

    @app.on_event("shutdown")
    def shutdown_event():
        logger.info("Shutting down...")

    register_api_routes(app)


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8880, reload=True)
