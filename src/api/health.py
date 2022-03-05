from fastapi import APIRouter

from version import __version__

router = APIRouter()


@router.get("/healthz")
def liveness_check():
    return {
        "version": __version__
    }


@router.get("/readyz")
def readiness_check():
    # TODO: test db connection
    return {
        "version": __version__
    }
