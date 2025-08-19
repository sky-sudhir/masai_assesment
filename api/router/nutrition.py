
from http import HTTPStatus
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.db import get_db
from api.model.model import Nutrition
# from api.db.chromadb import collection


router=APIRouter(prefix="/nutrition",tags=["Nutrition"])

class NutritionCreate(BaseModel):
    user_id:int
    plan_name:str
    date:str
    meals:str
class NutritionUpdate(BaseModel):
    plan_name:str
    date:str
    meals:str

@router.post("/",status_code=HTTPStatus.CREATED)
async def create_nutrition(request:NutritionCreate,db:AsyncSession=Depends(get_db)):
    new_nutrition=Nutrition(
         user_id=request.user_id,
        plan_name=request.plan_name,
        date=request.date,
        meals=request.meals
    )
    json_of_nutrition=f"nutrition:  plan name: {request.plan_name}, date: {request.date}, meals:{request.meals}"

    # collection.add(documents=[json_of_nutrition],ids=["1"])

    db.add(new_nutrition)
    await db.commit()  
    await db.refresh(new_nutrition) 
    return new_nutrition



@router.put("/{n_id}",status_code=HTTPStatus.OK)
async def update_nutrition(n_id:int,request:NutritionUpdate,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Nutrition).filter(Nutrition.id ==n_id ))
    nutrition = result.scalar_one_or_none()

    if nutrition is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="nutrition not found")
    
    update_data = request.model_dump(exclude_unset=True) 


    for key, value in update_data.items():
        setattr(nutrition, key, value) 


    db.add(nutrition) 
    await db.commit()  
    await db.refresh(nutrition)  

    return nutrition

@router.get("/{user_id}") 
async def get_nutrition(
    user_id: int,  
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Nutrition).filter(Nutrition.user_id == user_id))
    db_nutrition = result.scalars().all()


    return db_nutrition