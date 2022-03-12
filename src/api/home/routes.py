from fastapi import APIRouter, HTTPException, status
from database.pymongo_database import db

router = APIRouter()


@router.get("/channels", response_description="Get all unique channels")
async def get_channels():
    channels = db["threads"].distinct("tags")
    if not channels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No channels found")
    return channels


@router.get("/tags", response_description="Get all unique tags")
async def get_tags():
    tags = db["threads"].distinct("tags")
    if not tags:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No tags found")
    return tags
