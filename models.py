from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Address(BaseModel):
    building: Optional[str]
    coord: List[float]
    street: Optional[str]
    zipcode: Optional[str]

class Grade(BaseModel):
    date: datetime
    grade: str
    score: int

class Restaurant(BaseModel):
    name: str
    borough: str
    cuisine: str
    address: Address
    grades: List[Grade]

class RestaurantInDB(Restaurant):
    id: str = Field(..., alias="_id")

class Location(BaseModel):
    latitude: float
    longitude: float

class RestaurantOutput(BaseModel):
    name: str
    description: str  # This will be the cuisine type in this case
    location: Location
    average_rating: Optional[float] = None
    no_of_ratings: int = 0

class User(BaseModel):
    username: str

class UserInDB(User):
    hashed_password: str
