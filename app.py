import streamlit as st
import uuid
import os
from document_processor import load_documents, split_documents
from vector_store import create_vector_store
from rag_pipeline import create_rag_chain, get_answer

# Page config
st.set_page_config(
    page_title="SmartDocs RAG Chatbot",
    page_icon="🤖",
    layout="wide"
)

st.title(" SmartDocs RAG Chatbot")
st.markdown("Upload your PDF and chat with it using AI!")

# Generate unique session ID for each user
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

if "docs_processed" not in st.session_state:
    st.session_state.docs_processed = False

# ---- SIDEBAR ----
with st.sidebar:
    st.header(" Upload Your PDF")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=["pdf"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process Documents", type="primary"):
            with st.spinner("Processing your documents..."):
                
                # Save uploaded files to data folder
                os.makedirs("data", exist_ok=True)
                for file in uploaded_files:
                    with open(f"data/{file.name}", "wb") as f:
                        f.write(file.getbuffer())
                
                # Process pipeline
                docs = load_documents()
                chunks = split_documents(docs)
                create_vector_store(chunks, st.session_state.session_id)
                
                # Create RAG chain
                st.session_state.rag_chain = create_rag_chain(
                    st.session_state.session_id
                )
                st.session_state.docs_processed = True
                st.session_state.messages = []
                
                st.success(f" {len(uploaded_files)} document(s) ready!")
    
    st.divider()
    st.markdown("**How it works:**")
    st.markdown("1. Upload your PDF")
    st.markdown("2. Click Process Documents")
    st.markdown("3. Ask any question!")
    
    # Show session info
    st.divider()
    st.caption(f"Session ID: {st.session_state.session_id[:8]}...")

# ---- MAIN CHAT AREA ----

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    
    if not st.session_state.docs_processed:
        st.warning(" Please upload and process your PDF first!")
    else:
        # Show user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer, sources = get_answer(
                    st.session_state.rag_chain, prompt
                )
                st.markdown(answer)
                
                # Show source documents
                if sources:
                    with st.expander(" View Sources"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Source {i+1}:** {doc.metadata.get('source', 'Unknown')}")
                            st.markdown(f"**Page:** {doc.metadata.get('page', 'Unknown')}")
                            st.markdown(f"*...{doc.page_content[:300]}...*")
                            st.divider()
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })