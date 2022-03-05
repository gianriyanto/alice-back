from fastapi import APIRouter

from version import __version__
from database.pymongo_database import get_server

router = APIRouter()


@router.get("/healthz")
def liveness_check():
    return {
        "version": __version__,
        "database_server": bool(get_server()["version"])
    }


@router.get("/readyz")
def readiness_check():
    return {
        "version": __version__,
        "database_server": bool(get_server()["version"])
    }
