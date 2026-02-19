from pypdf import PdfReader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def load_documents(data_path="data/"):
    """Load all PDFs directly using pypdf - no langchain loaders"""
    documents = []
    
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(data_path, file)
            reader = PdfReader(file_path)
            
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    doc = Document(
                        page_content=text,
                        metadata={
                            "source": file,
                            "page": page_num + 1
                        }
                    )
                    documents.append(doc)
            
            print(f"Loaded: {file}")
    
    print(f"Total pages loaded: {len(documents)}")
    return documents

def split_documents(documents):
    """Split documents into smaller chunks"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks")
    return chunks