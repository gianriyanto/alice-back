from fastapi import APIRouter

router = APIRouter()


@router.get("/channels")
async def get_channels():
    raise NotImplementedError()


@router.get("/tags")
async def get_tags():
    raise NotImplementedError()
