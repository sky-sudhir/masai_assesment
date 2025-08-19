

from http import HTTPStatus
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.db import get_db
from api.model.model import User


router=APIRouter(prefix="/auth")




class UserResponse(BaseModel):
    username: str
    email:EmailStr
    age:Optional[int]=None
    weight:Optional[int]=None
    height:Optional[int]=None
    goals:Optional[str]=None

class LoginInput(BaseModel):
    username:str
    password:str

class UserCreate(BaseModel):
    username: str
    email:EmailStr
    password: str
    age:Optional[int]=None
    weight:Optional[int]=None
    height:Optional[int]=None
    goals:Optional[str]=None

@router.post("/register",status_code=HTTPStatus.CREATED)
async def register_user(request:UserCreate ,db:AsyncSession=Depends(get_db)):

    new_user=User(email=request.email,password=request.password, username=request.username)
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except Exception as e:
        await db.rollback() 
        raise HTTPException(status_code=500, detail=f" {e}")


    return UserCreate(id=new_user.id, email=new_user.email, username=new_user.username)




@router.post("/login",status_code=HTTPStatus.OK)
async def login(request: LoginInput,db:AsyncSession=Depends(get_db))->UserResponse:
    user_result = await db.execute(select(User).where(User.username == request.username))
    user = user_result.scalar_one_or_none() 
    if not user:
        raise HTTPException(status_code=400,detail="Invalid user")

    if user.password!=request.password:
        raise HTTPException(status_code=400,detail="Invalid password")

    return user
@router.post("/user/{user_id}",status_code=HTTPStatus.OK)
async def login(user_id:int,db:AsyncSession=Depends(get_db))->UserResponse:
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none() 
    if not user:
        raise HTTPException(status_code=404,detail="Not found")

    return user




