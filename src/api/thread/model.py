from pydantic import BaseModel, Field
from ..user.model import UserModel
from typing import List
from bson import ObjectId


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
    response: str = Field(...)
    created_date = str = Field(...)
    created_by: UserModel = Field(...)
    plus_ones: int = Field(...)
    # tags: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "response": "This is my answer",
                "description": "This is the explanation for my answer.",
                "created_date": "2022-03-07 21:23:20.127219",
                "created_by": {
                    "_id": "6223314c47c738b032cfd829",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "email": "jdoe@example.com"
                },
                "plus_ones": 0
            }
        }


class ThreadModel(BaseModel):
    # Create a new thread, ask a new question
    title: str = Field(...)
    description: str = Field(...)
    status: str = Field("open")  # open, closed
    created_date: str = Field(...)
    created_by: UserModel = Field(...)
    looks: int = Field(...)
    plus_ones: int = Field(...)
    tags: List[str]
    channel: str = Field(...)
    responses: List[ResponseModel]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Title of my thread",
                "description": "Here's a bit of description for this thread",
                "status": "open",
                "created_date": "2022-03-07 21:30:10.838420",
                "created_by": {
                    "_id": "8311314c47c738b032cfd354",
                    "first_name": "Dave",
                    "last_name": "Smith",
                    "email": "dsmith@example.com"
                },
                "likes": 0,
                "looks": 1,
                "plus_ones": 2,
                "tags": ["tag_1", "tag_2"],
                "channel": "this_channel",
                "responses": [
                    {
                        "_id": "9923314c47c738b032cfd830",
                        "response": "This is my answer",
                        "description": "This is the explanation for my answer.",
                        "created_date": "2022-03-07 21:23:20.127219",
                        "created_by": {
                            "_id": "6223314c47c738b032cfd829",
                            "first_name": "Jane",
                            "last_name": "Doe",
                            "email": "jdoe@example.com"
                        },
                        "plus_ones": 0
                    }
                ]
            }
        }
