

from http import HTTPStatus
from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.db import get_db
from api.model.model import Workout


router=APIRouter(prefix="/workout",tags=["Workout"])

class WorkoutCreate(BaseModel):
    user_id:int
    plan_name:str
    date:str
    exercises:str
    duration:str

class WorkoutUpdate(BaseModel):
    plan_name: str | None = None
    date: str | None = None
    exercises: str | None = None
    duration: str | None = None


@router.post("/",status_code=HTTPStatus.CREATED)
async def create_workout(request:WorkoutCreate,db:AsyncSession=Depends(get_db)):
    new_workout = Workout(
        user_id=request.user_id,
        plan_name=request.plan_name,
        date=request.date,
        exercises=request.exercises,
        duration=request.duration
    )

    db.add(new_workout)
    await db.commit()  
    await db.refresh(new_workout) 
    return new_workout





@router.put("/{workout_id}") 
async def update_workout(
    workout_id: UUID,  
    request: WorkoutUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Workout).filter(Workout.id == workout_id))
    db_workout = result.scalar_one_or_none()

    if db_workout is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Workout not found")

    update_data = request.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
        setattr(db_workout, key, value) 

    db.add(db_workout) 
    await db.commit()  
    await db.refresh(db_workout)  

    return db_workout

@router.get("/{user_id}") 
async def get_workout(
    user_id: int,  
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Workout).filter(Workout.user_id == user_id))
    db_workout = result.scalars().all()


    return db_workout
