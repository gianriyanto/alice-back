from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List

from .model import ThreadModel, ReactionModel
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


@router.get("/threads", response_description="Get a list of threads with filters", response_model=List[ThreadModel])
async def get_threads(user_id: str = None, tag: str = None, channel: str = None, _status: str = None):
    # TODO: get threads by tag, channel, and status filter
    threads = list(db["threads"].find({}))

    if not threads:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No threads found")
    return threads


@router.post("/thread/{thread_id}/respond")
async def respond_to_thread():
    raise NotImplementedError()


@router.post("/thread/{thread_id}/react", response_description="React to a thread", response_model=ReactionModel)
async def react_to_thread(thread_id: str, reaction: ReactionModel = Body(...)):
    """ Users can 'look' or '+1' a thread """
    thread = db["threads"].find_one({"_id": thread_id})
    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No threads found")

    if reaction.action == 'look':
        reacted_thread = db["threads"].update_one(
            {"_id": thread_id}, {"$push": {"looks": reaction.reacted_by}}
        )
    elif reaction.action == 'plus_one':
        reacted_thread = db["threads"].update_one(
            {"_id": thread_id}, {"$push": {"plus_ones": reaction.reacted_by}}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"The action {reaction.action} does not exist"
        )

    if reacted_thread.modified_count == 1:
        reacted_thread = db["threads"].find_one({"_id": thread_id})
        if reacted_thread:
            return {
                "action": reaction.action,
                "reacted_at": reaction.reacted_at,
                "reacted_by": reaction.reacted_by
            }

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to react to thread {thread_id}")


@router.post("/thread/{thread_id}/response/{response_id}")
async def react_to_response():
    raise NotImplementedError()
