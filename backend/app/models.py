from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum
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

class Status(str, Enum):
    Sent = "Sent"
    Delivered = "Delivered"
    Read = "Read"

class Message(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    message_id: str
    sender: EmailStr
    recipient: EmailStr
    content: str
    timestamp: datetime
    status: Status
    is_bot_response: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
