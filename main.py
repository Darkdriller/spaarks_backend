from fastapi import FastAPI, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from models import RestaurantOutput, Location, UserInDB
from auth import get_current_user, authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import restaurant_collection
from datetime import datetime, timedelta 

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def calculate_average_rating(grades):
    if not grades:
        return None, 0
    total_score = sum(grade['score'] for grade in grades)
    return total_score / len(grades), len(grades)

@app.get("/restaurants/", response_model=List[RestaurantOutput])
async def get_restaurants(lat: float, lon: float, radius: float, current_user: UserInDB = Depends(get_current_user)):
    query = {
        "address.coord": {
            "$geoWithin": {
                "$centerSphere": [[lon, lat], radius / 6378100.0]
            }
        }
    }
    restaurants = list(restaurant_collection.find(query))
    
    result = []
    for restaurant in restaurants:
        avg_rating, no_of_ratings = calculate_average_rating(restaurant.get('grades', []))
        restaurant_data = RestaurantOutput(
            name=restaurant["name"],
            description=restaurant["cuisine"],
            location=Location(
                latitude=restaurant["address"]["coord"][1],
                longitude=restaurant["address"]["coord"][0],
            ),
            average_rating=avg_rating,
            no_of_ratings=no_of_ratings
        )
        result.append(restaurant_data)
    
    return result

@app.get("/restaurants/range/", response_model=List[RestaurantOutput])
async def get_restaurants_range(lat: float, lon: float, min_distance: float, max_distance: float, current_user: UserInDB = Depends(get_current_user)):
    if min_distance < 0 or max_distance < 0:
        raise HTTPException(status_code=400, detail="Distances should be positive")

    if min_distance >= max_distance:
        raise HTTPException(status_code=400, detail="min_distance should be less than max_distance")

    query = {
        "address.coord": {
            "$geoWithin": {
                "$centerSphere": [
                    [lon, lat],
                    max_distance / 6378100.0  # Convert meters to radians for max distance
                ]
            }
        },
        "$and": [
            {"address.coord": {
                "$geoWithin": {
                    "$centerSphere": [
                        [lon, lat],
                        max_distance / 6378100.0
                    ]
                }
            }},
            {"address.coord": {
                "$not": {
                    "$geoWithin": {
                        "$centerSphere": [
                            [lon, lat],
                            min_distance / 6378100.0  # Convert meters to radians for min distance
                        ]
                    }
                }
            }}
        ]
    }
    
    restaurants = list(restaurant_collection.find(query))
    
    result = []
    for restaurant in restaurants:
        avg_rating, no_of_ratings = calculate_average_rating(restaurant.get('grades', []))
        restaurant_data = RestaurantOutput(
            name=restaurant["name"],
            description=restaurant["cuisine"],
            location=Location(
                latitude=restaurant["address"]["coord"][1],
                longitude=restaurant["address"]["coord"][0],
            ),
            average_rating=avg_rating,
            no_of_ratings=no_of_ratings
        )
        result.append(restaurant_data)
    
    return result
