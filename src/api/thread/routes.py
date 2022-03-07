from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from .model import ThreadModel
from database.pymongo_database import db

router = APIRouter()


@router.post("/thread", response_description="Start a new thread", response_model=ThreadModel)
async def create_thread(thread: ThreadModel = Body(...)):
    thread = jsonable_encoder(thread)
    try:
        new_thread = db["threads"].insert_one(thread)
        started_thread = db["threads"].find_one({"_id": new_thread.inserted_id})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create a new user")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=started_thread)


@router.get("/threads")
async def get_all_threads():
    raise NotImplementedError()


@router.get("/thread/{thread_id}")
async def get_thread():
    raise NotImplementedError()


@router.post("/thread/{thread_id}")
async def respond_to_thread():
    raise NotImplementedError()


@router.post("/thread/{thread_id}")
async def react_to_thread():
    raise NotImplementedError()


@router.post("/thread/{thread_id}/response/{response_id}")
async def react_to_response():
    raise NotImplementedError()
