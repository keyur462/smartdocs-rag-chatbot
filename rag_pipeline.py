from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from vector_store import load_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

def create_rag_chain(session_id):
    vector_store = load_vector_store(session_id)
    
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are a helpful assistant that answers questions based on the uploaded documents.
        If the answer is not found in the documents, say "I could not find this in your uploaded documents."
        
        Context from documents:
        {context}
        
        Question: {question}
        
        Answer clearly and concisely:
        """
    )
    
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
    return chain

def get_answer(chain, question):
    response = chain({"question": question})
    answer = response["answer"]
    sources = response.get("source_documents", [])
    return answer, sources