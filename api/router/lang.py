from http import HTTPStatus
from unittest import result
from fastapi import APIRouter
from pydantic import BaseModel
from api.db.chromadb import collection
from langchain_groq import ChatGroq



router=APIRouter(prefix="/chat")
class Question(BaseModel):
    ques:str

@router.post("/ask",status_code=HTTPStatus.OK)
async def ask_ques(que:Question):
    results = collection.query(
    query_texts=[que.ques], 
    n_results=4 
    )

    llm = ChatGroq(
    model="deepseek-r1-distill-llama-70b",
    temperature=0,
    max_tokens=None,
    reasoning_format="parsed",
    timeout=None,
    max_retries=2,
    
    # other params...
)
    messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]
    ai_msg = llm.invoke(messages)

    return ai_msg



