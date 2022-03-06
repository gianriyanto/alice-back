from fastapi import APIRouter


router = APIRouter()


# TODO: Reconsider API route string
@router.post("/thread")
async def create_thread():
    raise NotImplementedError()


@router.get("/threads")
async def get_all_threads():
    raise NotImplementedError()


@router.get("/thread/{thread_id}")
async def get_thread():
    raise NotImplementedError()
