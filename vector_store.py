from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma_db"

def create_vector_store(chunks, session_id):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=f"{CHROMA_PATH}/{session_id}"
    )
    print("Vector store created!")
    return vector_store

def load_vector_store(session_id):
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=f"{CHROMA_PATH}/{session_id}",
        embedding_function=embeddings
    )
    return vector_store