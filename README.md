# SmartDocs RAG Chatbot

An intelligent document Q&A chatbot built with RAG (Retrieval-Augmented Generation) architecture. Upload any PDF and ask questions about it in natural language — the AI will find the most relevant information and give you accurate, sourced answers.

---

## Demo

> Upload a PDF → Ask questions → Get AI-powered answers with sources

---

## Features

- Upload one or multiple PDF documents
- Ask questions in plain natural language
- Get accurate answers based only on your uploaded documents
- See exactly which page and document the answer came from
- Maintains conversation memory within a session
- Each user gets their own isolated session — documents are never mixed
- Completely free to run using Groq's free API

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| RAG Framework | LangChain |
| LLM | Groq (Llama 3.1) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF |
| Frontend | Streamlit |

---

## How It Works

1. User uploads a PDF document
2. The document is split into small chunks
3. Each chunk is converted into a vector embedding using HuggingFace
4. Embeddings are stored in ChromaDB vector database
5. When user asks a question, it is converted to an embedding
6. ChromaDB finds the most similar chunks to the question
7. Retrieved chunks are passed to Groq LLM with the question
8. LLM generates an accurate answer based on the document context

---

## Project Structure

```
smartdocs-rag-chatbot/
|
|-- app.py                  # Main Streamlit UI
|-- rag_pipeline.py         # Core RAG logic and LLM chain
|-- document_processor.py   # PDF loading and chunking
|-- vector_store.py         # ChromaDB vector store management
|-- requirements.txt        # Project dependencies
|-- .env                    # API keys (not included in repo)
|-- .gitignore              # Files excluded from Git
|-- data/                   # Uploaded PDFs stored here
|-- chroma_db/              # Vector database (auto-created)
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/smartdocs-rag-chatbot.git
cd smartdocs-rag-chatbot
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install langchain==0.2.16 langchain-groq==0.1.9 langchain-community==0.2.16 langchain-chroma==0.1.4 sentence-transformers==2.7.0 chromadb==0.4.24 streamlit==1.31.0 pypdf==3.17.4 python-dotenv==1.0.0 tiktoken==0.7.0 httpx==0.27.0
```

### 4. Set up your API key

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your-groq-api-key-here
```

Get your free Groq API key at: https://console.groq.com

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at: http://localhost:8501

---

## Usage

1. Open the app in your browser
2. Click Browse files in the left sidebar
3. Upload one or more PDF files
4. Click Process Documents and wait for confirmation
5. Type your question in the chat input
6. Get AI-powered answers with source references

---

## Use Cases

- Research paper analysis
- Legal document Q&A
- Study assistant for textbooks
- Business report analysis
- Technical documentation search

---

## License

MIT License — free to use and modify.

---

## Author

Built by Keyur
