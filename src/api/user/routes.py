from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from .model import UserModel, UpdateUserModel
from database.pymongo_database import db

router = APIRouter()


@router.post("/user", response_description="Add new user", response_model=UserModel)
async def create_user(user: UserModel = Body(...)):
    user = jsonable_encoder(user)
    try:
        new_user = db["users"].insert_one(user)
        created_user = db["users"].find_one({"_id": new_user.inserted_id})
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create a new user")

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.put("/user/{id}", response_description="Update a user", response_model=UserModel)
async def update_user(user_id: str, user: UpdateUserModel = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    updated_result = db["users"].update_one({"_id": user_id}, {"$set": user})

    if updated_result.modified_count == 1:
        updated_user = db["users"].find_one({"_id": user_id})
        if updated_user:
            return updated_user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")


@router.get("/user/{user_id}", response_description="Get a user by id", response_model=UserModel)
async def get_user(user_id: str):
    user = db["users"].find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    return user
