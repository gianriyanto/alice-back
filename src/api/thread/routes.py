from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import List

from .model import ThreadModel, ReactionModel, ResponseModel
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
async def get_threads(user_id: str = None, tags: str = None, channel: str = None, thread_status: str = None):
    threads = list(
        db["threads"].find({
            "tags": {"$in": [tags]} if tags else {"$ne": None},
            "channel": channel or {"$ne": None},
            "status": thread_status or {"$ne": None},
            "created_by._id": user_id or {"$ne": None},
        })
    )

    if not threads:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No threads found")
    return threads


@router.get("/thread/{thread_id}", response_description="Get thread by id", response_model=ThreadModel)
async def get_thread(thread_id: str):
    thread = db["threads"].find_one({"_id": thread_id})
    if not thread:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No thread found with ID {thread_id}")
    return thread


@router.post("/thread/{thread_id}/respond", response_description="Respond to a thread", response_model=ResponseModel)
async def respond_to_thread(thread_id: str, response: ResponseModel = Body(...)):
    response = jsonable_encoder(response)
    responded_thread = db["threads"].update({"_id": thread_id}, {
        "$push": {"responses": response}
    })

    # ORMs don't enable the creation of Rich Domain models, it simplifies the amount of (often repetitive) work. Making your domain model anemic with all business logic in services won't save you from boilerplate DTO mapping code.

    if responded_thread["ok"]:
        # # TODO get responses with id = response._id
        # responses = db["threads"].find_one({"_id": thread_id}, {"responses"})
        # if responses:
        return response

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to react to thread {thread_id}")


@router.post("/thread/{thread_id}/react", response_description="React to a thread", response_model=ReactionModel)
async def react_to_thread(thread_id: str, reaction: ReactionModel = Body(...)):
    # TODO: Handle user cannot plus_one more than once
    if reaction.action == 'look':
        reacted_thread = db["threads"].update_one({"_id": thread_id}, {"$push": {"looks": reaction.reacted_by}})
    elif reaction.action == 'plus_one':
        reacted_thread = db["threads"].update_one({"_id": thread_id}, {"$push": {"plus_ones": reaction.reacted_by}})
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"The action {reaction.action} does not exist"
        )

    if reacted_thread.modified_count == 1:
        reacted_thread = db["threads"].find_one({"_id": thread_id}, {"plus_ones": 1, "looks": 1})
        if reacted_thread:
            return {
                "action": reaction.action,
                "reacted_by": reaction.reacted_by,
                "plus_ones_count": len(reacted_thread["plus_ones"]),
                "looks_count": len(reacted_thread["looks"])
                # TODO: Return the latest look/plus_one count
            }

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to react to thread {thread_id}")


@router.post("/thread/{thread_id}/unreact", response_description="React to a thread", response_model=ReactionModel)
async def unreact_to_thread(thread_id: str, reaction: ReactionModel = Body(...)):
    # TODO: Create API for this...
    raise NotImplementedError()
