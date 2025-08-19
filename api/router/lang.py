from http import HTTPStatus
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from api.db.chromadb import ingest_documents, search_documents
from langchain_core.documents import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from PyPDF2 import PdfReader
import io

router = APIRouter(prefix="/chat",tags=["Chat"])

class Question(BaseModel):
    ques: str

@router.post("/ingest", status_code=HTTPStatus.OK)
async def ingest_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        return {"error": "Only PDF files are allowed"}
    
    content = await file.read()
    pdf_reader = PdfReader(io.BytesIO(content))
    
    documents = []
    for i, page in enumerate(pdf_reader.pages):
        text = page.extract_text()
        if text.strip():
            doc = Document(
                page_content=text,
                metadata={"source": file.filename, "page": i + 1}
            )
            documents.append(doc)
    
    ingest_documents(documents)
    return {"message": f"Successfully ingested {len(documents)} pages from {file.filename}"}

@router.post("/chat", status_code=HTTPStatus.OK)
async def ask_question(question: Question):
    results = search_documents(question.ques, n_results=3)
    
    context = "\n".join(results['documents'][0])
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0
    )
    
    prompt = f"Context: {context}\n\nQuestion: {question.ques}\n\nAnswer based on the context:"
    response = llm.invoke(prompt)
    
    return {"answer": response.content}


