from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .model import UserModel
from database.pymongo_database import db

router = APIRouter()


@router.post("/create_user", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    try:
        new_user = db["users"].insert_one(user)
        created_user = db["users"].find_one({"_id": new_user.inserted_id})
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create a new user")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)
