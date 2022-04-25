from pydantic import BaseModel, Field
from ..user.model import UserModel
from typing import List
from bson import ObjectId
from enum import Enum
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ResponseModel(BaseModel):
    # Respond to a thread, answer a question
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    body: str = Field(...)
    created_date: str = Field(str(datetime.now()))
    created_by: UserModel = Field(...)
    plus_ones: List[str] = Field(...)
    # verified: Boolean

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "body": "This is my answer",
                "created_by": {
                    "_id": "6223314c47c738b032cfd829",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jdoe@example.com"
                },
                "plus_ones": []
            }
        }


class ThreadModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    status: str = Field("open")  # open, closed
    created_date: str = Field(str(datetime.now()))
    created_by: UserModel = Field(...)
    looks: List[str] = Field(...)
    plus_ones: List[str] = Field(...)
    tags: List[str] = Field(...)
    channel: str = Field(...)
    responses: List[dict] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Title of my thread",
                "description": "Here's a bit of description for this thread",
                "status": "open",
                "created_by": {
                    "_id": "8311314c47c738b032cfd354",
                    "first_name": "Dave",
                    "last_name": "Smith",
                    "email": "dsmith@example.com"
                },
                "looks": [],
                "plus_ones": [],
                "tags": ["tag_1", "tag_2"],
                "channel": "this_channel",
                "responses": []
            }
        }


class ActionEnum(str, Enum):
    look = 'look'
    plus_one = 'plus_one'


class ReactionModel(BaseModel):
    action: str = Field(...)
    reacted_at: str = Field(str(datetime.now()))
    reacted_by: str = Field(...)
    plus_ones_count: int = Field(0)
    looks_count: int = Field(0)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "action": "plus_one",
                "reacted_by": "6227df43aa9525f6f7171c10"
            }
        }

