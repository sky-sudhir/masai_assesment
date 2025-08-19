from http import HTTPStatus
from unittest import result
from fastapi import APIRouter
from pydantic import BaseModel
from api.db.chromadb import collection



router=APIRouter(prefix="/chat")
class Question(BaseModel):
    ques:str

@router.post("/ask",status_code=HTTPStatus.OK)
async def ask_ques(que:Question):
    results = collection.query(
    query_texts=[que.ques], 
    n_results=4 
    )

    return results



