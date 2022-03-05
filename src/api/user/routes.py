from fastapi import APIRouter
from .model import UserModel

router = APIRouter()


@router.post("/", response_description="Add new user", response_model=UserModel)
async def create_student(user: UserModel):
    raise NotImplementedError()
