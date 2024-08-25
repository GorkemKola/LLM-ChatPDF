import streamlit as st
import base64
from PyPDF2 import PdfReader
#from src.chatpdf.components import pdf_processing, text_splitting, embedding, vector_store, qa_chain

def display_pdf(file):
    # Read PDF file
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    
    # Embed PDF viewer
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def main():
    st.set_page_config(layout="wide")
    st.title("ChatPDF: Interact with Your PDF")

    # File upload
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Create two columns
        col1, col2 = st.columns([2, 1])  # Adjust the ratio as needed

        with col1:
            st.subheader("PDF Viewer")
            display_pdf(uploaded_file)

        with col2:
            st.subheader("Chat with Your PDF")
            # Reset file pointer and process the PDF
            uploaded_file.seek(0)
            #raw_text = pdf_processing.process_pdf(uploaded_file)
            #chunks = text_splitting.split_text(raw_text)
            
            # Generate embeddings and store in vector store
            #embeddings = embedding.generate_embeddings(chunks)
            #vector_store.store_embeddings(embeddings)

        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask a question about your PDF:"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            #with st.chat_message("assistant"):
            #    answer = qa_chain.get_answer(prompt)
            #    st.markdown(answer)
            #st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()