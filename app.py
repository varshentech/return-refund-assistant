import streamlit as st

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Load policy file
loader = TextLoader("policy.txt")
documents = loader.load()

# Split text into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

docs = text_splitter.split_documents(documents)

# Create embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Store vectors in ChromaDB
vectordb = Chroma.from_documents(
    docs,
    embedding
)

# Streamlit UI
st.title("AI Return & Refund Assistant")

question = st.text_input("Ask your question:")

if st.button("Submit"):

    if question:

        # Semantic similarity search
        results = vectordb.similarity_search(question, k=1)

        st.write("### AI Response:")

        for result in results:
            st.write(result.page_content)

    else:
        st.write("Please enter a question.")