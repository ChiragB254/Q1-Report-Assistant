#!/usr/bin/env python3
"""
Streamlit Frontend for Production RAG System

This Streamlit app provides a user-friendly interface to interact with 
the RAG API deployed on Azure. Users can upload documents, ask questions,
and manage the document database.
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
import pandas as pd
from typing import Dict, List, Optional

# Configure Streamlit page
st.set_page_config(
    page_title="RAG Document Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

def check_secrets():
    """Check if required secrets are configured"""
    if "API_BASE_URL" not in st.secrets:
        st.error("⚠️ API_BASE_URL not configured in Streamlit secrets")
        st.info("""
        Please configure the API_BASE_URL in your Streamlit app settings:
        1. Go to your app settings
        2. Click on 'Secrets'
        3. Add: API_BASE_URL = "http://4.156.129.231:8000"
        """)
        st.stop()
    return st.secrets["API_BASE_URL"]

# Configuration
API_BASE_URL = check_secrets()

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
}
.answer-box {
    background-color: #2d3748;
    color: #e2e8f0;
    padding: 1.5rem;
    border-left: 4px solid #1f77b4;
    border-radius: 0.5rem;
    margin: 1rem 0;
}
.answer-box strong {
    color: #63b3ed;
    font-weight: 600;
}
.answer-box ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}
.answer-box li {
    margin: 0.3rem 0;
    color: #cbd5e0;
}
.answer-box p {
    margin: 0.8rem 0;
    line-height: 1.6;
}
.source-box {
    background-color: #f8f9fa;
    padding: 1rem;
    border-radius: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid #dee2e6;
}
.error-message {
    background-color: #ffe6e6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #ff4444;
    color: #cc0000;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

class RAGClient:
    """Client for interacting with the RAG API"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self) -> bool:
        """Check if the API is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            return response.status_code == 200
        except Exception as e:
            st.error(f"Health check failed: {str(e)}")
            return False
    
    def query(self, question: str, top_k: int = 5, answer_style: str = "concise") -> Dict:
        """Query the RAG system"""
        try:
            payload = {
                "question": question,
                "top_k": top_k,
                "answer_style": answer_style
            }
            response = requests.post(
                f"{self.base_url}/query", 
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.")
            return None
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to the API. Please check if the service is running.")
            return None
        except requests.exceptions.RequestException as e:
            st.error(f"Query failed: {str(e)}")
            return None
    
    def upload_document(self, file, force_reprocess: bool = False) -> Dict:
        """Upload and process a document"""
        try:
            files = {"file": (file.name, file, file.type)}
            data = {"force_reprocess": force_reprocess}
            
            response = requests.post(
                f"{self.base_url}/upload",
                files=files,
                data=data,
                timeout=300  # 5 minutes timeout for processing
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")
            return None
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        try:
            response = requests.get(f"{self.base_url}/stats", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error("Failed to get stats")
            return None
    
    def list_documents(self) -> List[Dict]:
        """List all processed documents"""
        try:
            response = requests.get(f"{self.base_url}/documents", timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error("Failed to list documents")
            return []
    
    def delete_document(self, filename: str) -> bool:
        """Delete a document"""
        try:
            response = requests.delete(f"{self.base_url}/documents/{filename}", timeout=30)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to delete document: {str(e)}")
            return False

# Initialize client
@st.cache_resource
def get_rag_client():
    return RAGClient(API_BASE_URL)

def format_answer(answer_text):
    """Format the answer text with proper styling"""
    if not answer_text:
        return ""
    
    import re
    # Replace markdown-style bold with HTML
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', answer_text)
    
    # Replace bullet points with HTML list items
    lines = formatted_text.split('\n')
    formatted_lines = []
    in_list = False
    
    for line in lines:
        line = line.strip()
        if line.startswith('*') or line.startswith('-'):
            if not in_list:
                formatted_lines.append('<ul>')
                in_list = True
            formatted_lines.append(f'<li>{line[1:].strip()}</li>')
        else:
            if in_list:
                formatted_lines.append('</ul>')
                in_list = False
            if line:
                formatted_lines.append(f'<p>{line}</p>')
    
    if in_list:
        formatted_lines.append('</ul>')
    
    return ''.join(formatted_lines)

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown('<h1 class="main-header">📚 Bank Q1 Report RAG Assistant</h1>', unsafe_allow_html=True)
    
    # Initialize client
    client = get_rag_client()
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        # API Health Check
        with st.spinner("Checking API connection..."):
            api_healthy = client.health_check()
        
        if api_healthy:
            st.success("✅ API Connected")
        else:
            st.error("❌ API Disconnected")
            st.warning(f"Cannot connect to API at: {API_BASE_URL}")
            st.info("Please check if the API service is running and accessible.")
        
        # Answer Style Selection
        answer_style = st.selectbox(
            "Answer Style",
            ["concise", "detailed", "explanatory"],
            help="Choose the style of answers you prefer"
        )
        
        # Number of sources
        top_k = st.slider(
            "Number of Sources",
            min_value=1,
            max_value=10,
            value=5,
            help="Number of document chunks to consider for answers"
        )
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "📄 Upload Documents", "📊 Database Stats", "🔧 Management"])
    
    with tab1:
        chat_interface(client, answer_style, top_k, api_healthy)
    
    with tab2:
        upload_interface(client, api_healthy)
    
    with tab3:
        stats_interface(client, api_healthy)
    
    with tab4:
        management_interface(client, api_healthy)

def chat_interface(client: RAGClient, answer_style: str, top_k: int, api_healthy: bool):
    """Chat interface for asking questions"""
    
    st.header("Ask Questions About Your Documents")
    
    if not api_healthy:
        st.warning("⚠️ API is not available. Please check the connection.")
        return
    
    # Sample questions
    with st.expander("💡 Sample Questions"):
        sample_questions = [
            "What were Scotiabank's capital ratios in Q1 2025?",
            "What was the net income for the quarter?",
            "What are the main risk factors mentioned?",
            "How did the bank perform in international markets?",
            "What were the key financial highlights?"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(question, key=f"sample_{i}"):
                st.session_state["query_input"] = question
    
    # Query input
    query = st.text_area(
        "Enter your question:",
        height=100,
        key="query_input",
        placeholder="E.g., What were the Q1 2025 financial results?"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        search_button = st.button("🔍 Search", type="primary", disabled=not api_healthy)
    
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state["query_input"] = ""
            st.rerun()
    
    # Process query
    if search_button and query and api_healthy:
        with st.spinner("Searching documents..."):
            result = client.query(query, top_k, answer_style)
        
        if result:
            # Display answer with dark background
            formatted_answer = format_answer(result['answer'])
            st.markdown(f"""
            <div class="answer-box">
                <h3>📝 Answer:</h3>
                {formatted_answer}
            </div>
            """, unsafe_allow_html=True)
            
            # Display metadata
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sources Used", result['num_sources'])
            
            with col2:
                st.metric("Query Variations", result['processing_info'].get('query_variations', 'N/A'))
            
            with col3:
                st.metric("Processing Method", result['processing_info'].get('fusion_method', 'Standard'))
            
            # Show sources in expander
            with st.expander(f"📚 View Sources ({result['num_sources']})"):
                for i, source in enumerate(result.get('results', []), 1):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {i}:</strong> {source['metadata']['source_file']}<br>
                        <strong>Section:</strong> {source['metadata'].get('header', 'No header')}<br>
                        <strong>Type:</strong> {source['metadata']['chunk_type']}<br>
                        <strong>Relevance:</strong> {source['score']:.3f}<br>
                        <strong>Content Preview:</strong> {source['content'][:200]}...
                    </div>
                    """, unsafe_allow_html=True)

def upload_interface(client: RAGClient, api_healthy: bool):
    """Document upload interface"""
    
    st.header("Upload and Process Documents")
    
    if not api_healthy:
        st.warning("⚠️ API is not available. Upload functionality is disabled.")
        return
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a document to upload",
        type=['pdf', 'docx', 'doc', 'txt', 'md', 'html'],
        help="Supported formats: PDF, Word, Text, Markdown, HTML"
    )
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**File:** {uploaded_file.name}")
            st.info(f"**Size:** {uploaded_file.size:,} bytes")
            st.info(f"**Type:** {uploaded_file.type}")
        
        with col2:
            force_reprocess = st.checkbox(
                "Force reprocess",
                help="Reprocess even if document already exists in database"
            )
        
        if st.button("📤 Upload and Process", type="primary"):
            with st.spinner("Processing document... This may take a few minutes."):
                start_time = time.time()
                result = client.upload_document(uploaded_file, force_reprocess)
                end_time = time.time()
            
            if result:
                st.success("✅ Document processed successfully!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Chunks Created", result['chunks_created'])
                
                with col2:
                    st.metric("Processing Time", f"{end_time - start_time:.1f}s")
                
                with col3:
                    status = "Skipped" if result['skipped_processing'] else "Processed"
                    st.metric("Status", status)
                
                # Show optimization info
                if result.get('used_existing_markdown'):
                    st.info("💡 Used existing markdown file (faster processing)")
                
                if result.get('skipped_processing'):
                    st.info("⚡ Document already exists in database (processing skipped)")

def stats_interface(client: RAGClient, api_healthy: bool):
    """Database statistics interface"""
    
    st.header("Database Statistics")
    
    if not api_healthy:
        st.warning("⚠️ API is not available. Cannot retrieve statistics.")
        return
    
    # Get stats
    stats = client.get_stats()
    
    if stats:
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Chunks", stats['total_chunks'])
        
        with col2:
            st.metric("Unique Documents", stats['unique_documents'])
        
        with col3:
            st.metric("Collection Status", stats['collection_status'])
        
        # Document list
        if stats['document_names']:
            st.subheader("Processed Documents")
            
            # Create DataFrame for better display
            df = pd.DataFrame(stats['document_names'], columns=['Document Name'])
            df.index += 1
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No documents found in database")
    
    # Detailed document info
    documents = client.list_documents()
    
    if documents:
        st.subheader("Detailed Document Information")
        
        # Create detailed DataFrame
        doc_data = []
        for doc in documents:
            doc_data.append({
                'Document': doc['source_file'],
                'Chunks': doc['chunk_count'],
                'Types': ', '.join(doc['chunk_types']),
                'Sections': len(doc['headers']),
                'Last Updated': doc['created_dates'][-1] if doc['created_dates'] else 'Unknown'
            })
        
        df = pd.DataFrame(doc_data)
        st.dataframe(df, use_container_width=True)

def management_interface(client: RAGClient, api_healthy: bool):
    """Database management interface"""
    
    st.header("Database Management")
    
    if not api_healthy:
        st.warning("⚠️ API is not available. Management functionality is disabled.")
        return
    
    # List documents for management
    documents = client.list_documents()
    
    if documents:
        st.subheader("Document Management")
        
        # Create management table
        for doc in documents:
            with st.expander(f"📄 {doc['source_file']} ({doc['chunk_count']} chunks)"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Chunk Types:** {', '.join(doc['chunk_types'])}")
                    st.write(f"**Sections:** {len(doc['headers'])}")
                    if doc['headers']:
                        st.write(f"**Sample Sections:** {', '.join(doc['headers'][:3])}{'...' if len(doc['headers']) > 3 else ''}")
                
                with col2:
                    if st.button(f"🗑️ Delete", key=f"delete_{doc['source_file']}"):
                        if client.delete_document(doc['source_file']):
                            st.success(f"Deleted {doc['source_file']}")
                            st.rerun()
    else:
        st.info("No documents found in database")
    
    # Database actions
    st.subheader("Database Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Refresh Stats", type="secondary"):
            st.rerun()
    
    with col2:
        st.warning("⚠️ Bulk operations not implemented")
        st.button("🗑️ Clear All Data", disabled=True, help="Not implemented for safety")

if __name__ == "__main__":
    main()