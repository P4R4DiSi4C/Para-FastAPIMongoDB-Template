import uuid
from typing import Optional
from pydantic import BaseModel, Field


class RestaurantModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    desc: Optional[str]

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "Holy Cow",
                "desc": "Burger of Switzerland",
            }
        }


class UpdateRestaurantModel(BaseModel):
    name: Optional[str]
    desc: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "King Burger",
                "desc": "The burger of the king",
            }
        }
