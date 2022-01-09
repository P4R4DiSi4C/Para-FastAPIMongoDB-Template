from fastapi import APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.restaurant import RestaurantModel, UpdateRestaurantModel

router = APIRouter()


@router.post("/", response_description="Add new restaurant")
async def create_restaurant(request: Request, restaurant: RestaurantModel = Body(...)):
    restaurant = jsonable_encoder(restaurant)
    new_restaurant = await request.app.mongodb["restaurants"].insert_one(restaurant)
    created_task = await request.app.mongodb["restaurants"].find_one(
        {"_id": new_restaurant.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_task)


@router.get("/", response_description="List all restaurants")
async def list_restaurants(request: Request):
    restaurants = []
    for restaurant in await request.app.mongodb["restaurants"].find().to_list(length=100):
        restaurants.append(restaurant)
    return restaurants


@router.get("/{id}", response_description="Get a single restaurant")
async def show_restaurant(id: str, request: Request):
    if (restaurant := await request.app.mongodb["restaurants"].find_one({"_id": id})) is not None:
        return restaurant
    raise HTTPException(status_code=404, detail=f"Restaurant {id} not found")


@router.put("/{id}", response_description="Update a restaurant")
async def update_restaurant(id: str, request: Request, restaurant: UpdateRestaurantModel = Body(...)):
    restaurant = {k: v for k, v in restaurant.dict().items() if v is not None}

    if len(restaurant) >= 1:
        update_result = await request.app.mongodb["restaurants"].update_one(
            {"_id": id}, {"$set": restaurant}
        )

        if update_result.modified_count == 1:
            if (
                updated_restaurant := await request.app.mongodb["restaurants"].find_one({"_id": id})
            ) is not None:
                return updated_restaurant

    if (
        existing_restaurant := await request.app.mongodb["restaurants"].find_one({"_id": id})
    ) is not None:
        return existing_restaurant

    raise HTTPException(status_code=404, detail=f"Restaurant {id} not found")


@router.delete("/{id}", response_description="Delete Restaurant")
async def delete_restaurant(id: str, request: Request):
    delete_result = await request.app.mongodb["restaurants"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Restaurant {id} not found")
