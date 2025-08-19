import chromadb
from langchain.vectorstores import Chroma
from langchain.embeddings import OllamaEmbeddings
from langchain_core.documents import Document
from chromadb.utils import embedding_functions

CHROMA_API_KEY="ck-Gcs4QirnRarSDJHkg5QTRSDoJdLqPAVvMwntVskqU8Y9"
CHROMA_TENANT_ID="4d85fc60-287d-4c5b-8d60-710393526739"
CHROMA_DATABASE_ID="hrm"

embedding_fn = OllamaEmbeddings(model="nomic-embed-text")
chroma_embedding_fn = embedding_functions.DefaultEmbeddingFunction()

def create_chroma_client():
    chroma_client = chromadb.CloudClient(
        api_key=CHROMA_API_KEY,
        tenant=CHROMA_TENANT_ID,
        database=CHROMA_DATABASE_ID
        )

    return chroma_client

chroma_client = create_chroma_client()

def create_vectorstore():
    try:
        vectorstore = Chroma(
            client=chroma_client,
            collection_name="masai_eval",
            embedding_function=embedding_fn
        )
        
            
        return vectorstore
        
    except Exception as e:
        raise e

VECTORSTORE = create_vectorstore()

collection = chroma_client.get_or_create_collection(
    name="masai_eval",
    embedding_function=chroma_embedding_fn
)

def ingest_documents(documents):
    texts = [doc.page_content for doc in documents]
    metadatas = [doc.metadata for doc in documents]
    import uuid
    ids = [str(uuid.uuid4()) for _ in range(len(texts))]
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

def search_documents(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results





def format_for_vectorstore(summaries, embeddings, metadatas):
    return [
        Document(page_content=summary, metadata=metadata, embedding=embed)
        for summary, metadata, embed in zip(summaries, metadatas, embeddings)
    ]

def embed_texts(texts):
    return embedding_fn.embed_documents(texts)