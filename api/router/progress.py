
from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.db import get_db
from api.model.model import Progress


class ProgressCreate(BaseModel):
    user_id:int
    workout_id:int
    sets:int
    reps:int
    weights:int
    notes:str
class ProgressUpdate(BaseModel):
    sets:int
    reps:int
    weights:int
    notes:str



router=APIRouter(prefix="/progess",tags=["Progress"])



@router.post("/",status_code=HTTPStatus.CREATED)
async def create(request:ProgressCreate,db:AsyncSession=Depends(get_db)):
    new=Progress(
        user_id=request.user_id,
        workout_id=request.workout_id,
        sets=request.sets,
        weights=request.weights,
        notes=request.notes
    )

    db.add(new)
    await db.commit()  
    await db.refresh(new) 
    return new



@router.put("/{n_id}",status_code=HTTPStatus.OK)
async def update(n_id:int,request:ProgressUpdate,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(Progress).filter(Progress.id ==n_id ))
    progress = result.scalar_one_or_none()

    if progress is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="progress not found")
    
    update_data = request.model_dump(exclude_unset=True) 


    for key, value in update_data.items():
        setattr(progress, key, value) 


    db.add(progress) 
    await db.commit()  
    await db.refresh(progress)  

    return progress


@router.get("/{user_id}") 
async def get_nutrition(
    user_id: int,  
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Progress).filter(Progress.user_id == user_id))
    progresses = result.scalars().all()


    return progresses