import streamlit as st
import time
import random

from src.utils import utilities
from src.components.summarization.summarizer import summarizer_model
from src.components.chat_model.chat import chat_model
from transformers import pipeline

# Set page configuration
st.set_page_config(
    page_title="Document Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Objects, Methods we need to load while the app Loads
@st.cache_resource
def load_llms():
    tiny_llama = chat_model().init_model()
    return tiny_llama
tiny_llama = load_llms() #Loading tiny llama


# Custom CSS for better UI
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton button {
        background-color: #f7f7f8 !important;
        border: 1px solid #d9d9e3;
        border-radius: 12px;
        padding: 10px 16px;
        font-size: 14px;
        color: #1c1c1f;
        cursor: pointer;
        transition: background-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stButton button:hover {
        background-color: #efefef !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }
    .stButton button:active {
        background-color: #e5e5e5 !important;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    }
    .chat-container {
        border-radius: 15px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .bot-message {
        background-color: #E3E6E8;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .summary-container {
        border-radius: 15px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    }
    .file-uploader {
        border-radius: 15px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .header {
        color: #2E7D32;
        margin-bottom: 4rem;
    }
</style>
""", unsafe_allow_html=True)

def clear_input():
        st.session_state.Question = ""

def main():
    # Initialize session state
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Default"

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'summary_displayed' not in st.session_state:
        st.session_state.summary_displayed = False
    
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = []

    if 'Question' not in st.session_state:
        st.session_state.Question = ""
    
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    # Clear input BEFORE rendering text_input
    if st.session_state.clear_input:
        st.session_state.Question = ""
        st.session_state.clear_input = False

    # Header
    st.markdown("<h1 class='header'>📚 Interactive Document Assistant</h1>", unsafe_allow_html=True)
    
    # Create two columns for layout
    col1, col2 = st.columns([1, 3])
    
    # Sidebar content
    with col1:
        st.markdown("<div>", unsafe_allow_html=True)
        st.markdown("<h4>📁 Upload Documents</h4>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload a document and choose an action.", accept_multiple_files=False, type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            st.success(f"files uploaded successfully!")
            st.session_state.uploaded_file = uploaded_file
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Function selection buttons
        st.subheader("🔍 Choose Action")
        summarize_btn = st.button("Summarize Document", key="summarize_button", use_container_width=True)
        chat_btn = st.button("Chat with Document", key="chat_button", use_container_width=True)
        
        if chat_btn:
            if uploaded_file:
                st.session_state.current_tab = "Chat"
                st.session_state.summary_displayed = False
            else:
                @st.dialog("Please upload the document to chat. 😊", width="large")
                def pop_modal():
                    pass
                pop_modal()

        
        if summarize_btn:
            if uploaded_file:
                st.session_state.current_tab = "Summarize"
                st.session_state.summary_displayed = True
            else:
                @st.dialog("Please upload the document to summarize. 😊", width="large")
                def pop_modal():
                    pass
                pop_modal()
    
    # Main content area
    with col2:
        # If File is  not Uploaded so Display Below Template
        if st.session_state.current_tab == "Default":
            st.markdown("<div>", unsafe_allow_html=True)
            st.info("👈 Please upload documents first")
            
            # Show sample UI elements
            
            st.subheader("Welcome to Document Assistant!")
            st.write("This tool helps you to summarize and chat with your documents. Start by uploading files on the left panel.")
            
            # Animated loading placeholders
            cols = st.columns(2)
    
            with cols[0]:
                st.markdown("#### Supported formats:")
                st.markdown("✅ PDF documents (.pdf)")
                st.markdown("✅ Word documents (.docx)")
                st.markdown("✅ Text files (.txt)")
            
        
            with cols[1]:
                st.markdown("#### Features:")
                # st.markdown("✅ Upload multiple document types")
                st.markdown("✅ Interactive chat interface")
                st.markdown("✅ Quick document summarization")
            st.markdown("</div>", unsafe_allow_html=True)
        
        else:
            # Chat tab
            if st.session_state.current_tab == "Chat":
                st.markdown("<div>", unsafe_allow_html=True)
                st.subheader("💬 Chat with your Documents")

                # Display chat history
                for message in st.session_state.chat_history:
                    if message["role"] == "user":
                        st.markdown(f"<div class='user-message'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='bot-message'><strong>Assistant:</strong> {message['content']}</div>", unsafe_allow_html=True)

                # Chat input
                Question = st.text_input("Ask a question about the document:", key="Question", placeholder="Ask Anything")
                
                if st.button("Send", key="send_btn"):
                    if Question:
                        # Add user message to chat history
                        st.session_state.chat_history.append({"role": "user", "content": Question})
                        
                        # Simulate processing
                        with st.spinner("Processing your question..."):
                            utils = utilities()
                            chat = chat_model()
                            chunks = utils.Operation_handler(uploaded_file)
                            encoded_chunks = chat.encode_data(chunks)
                            similar_results = chat.similarity_results(
                                            data=encoded_chunks, user_query=Question, chunks=chunks
                                            )
                            context = " ".join(similar_results)
                            cleaned_context = utils.clean_context(context)
                            prompt = f""" Answer the question from the given context

Context:
{cleaned_context}

Question:
{Question}
    
Answer:
"""
                            answers = chat.generate_inference(tiny_llama, prompt)
                            # Add bot response to chat history
                            st.session_state.chat_history.append({"role": "assistant", "content": answers})
                            
                        st.session_state.clear_input = True
                        st.rerun()  

                st.markdown("</div>", unsafe_allow_html=True)


            # Summarize tab
            elif st.session_state.current_tab == "Summarize":
                st.markdown("<div>", unsafe_allow_html=True)
                st.subheader("📝 Document Summary")
                
                with st.spinner("Generating summary..."):
                    time.sleep(2)  # Simulate summary generation
                    
                    # Display the summary (simulated)
                    st.markdown("### Executive Summary")
                    st.markdown("""
                    This is a simulated document summary. In a real implementation, this would contain actual summaries of your uploaded documents.
                    
                    **Key Points:**
                    1. First main point extracted from the document
                    2. Second important concept identified
                    3. Third significant finding from analysis
                    
                    **Topics Covered:**
                    - Topic A with 25% coverage
                    - Topic B with 40% coverage
                    - Topic C with 35% coverage
                    """)
                    
                    # Simulated visualization
                    st.subheader("Document Insights")
                    cols = st.columns(2)
                    
                    with cols[0]:
                        st.markdown("#### Document Statistics:")
                        st.markdown("- **Pages:** 42")
                        st.markdown("- **Word Count:** 12,568")
                        st.markdown("- **Main Entities:** Company X, Project Y, Technology Z")
                        st.markdown("- **Sentiment:** Mostly positive")
                    
                    with cols[1]:
                        st.markdown("#### Top Keywords:")
                        st.markdown("- innovation (24 mentions)")
                        st.markdown("- analysis (18 mentions)")
                        st.markdown("- development (15 mentions)")
                        st.markdown("- strategy (12 mentions)")
                
                st.markdown("</div>", unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()