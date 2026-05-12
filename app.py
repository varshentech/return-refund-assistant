# =========================
# SQLITE FIX FOR CHROMADB
# =========================
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# =========================
# IMPORTS
# =========================
import streamlit as st

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import HuggingFaceHub
from langchain.docstore.document import Document

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Return & Refund Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Return & Refund Assistant")

# =========================
# LOAD DATA
# =========================
@st.cache_resource
def load_vector_db():

    with open("data.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Convert to document
    docs = [Document(page_content=text)]

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    split_docs = splitter.split_documents(docs)

    # Embeddings
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector DB
    vectordb = Chroma.from_documents(
        documents=split_docs,
        embedding=embedding,
        persist_directory="./chroma_db"
    )

    return vectordb

# =========================
# LOAD VECTOR DB
# =========================
vectordb = load_vector_db()

# =========================
# USER INPUT
# =========================
query = st.text_input(
    "Ask your question about returns/refunds:"
)

# =========================
# QA SYSTEM
# =========================
if query:

    docs = vectordb.similarity_search(query, k=3)

    # FREE HF MODEL
    llm = HuggingFaceHub(
        repo_id="google/flan-t5-base",
        huggingfacehub_api_token=st.secrets["HUGGINGFACE_API_TOKEN"],
        model_kwargs={
            "temperature": 0.5,
            "max_length": 256
        }
    )

    chain = load_qa_chain(llm, chain_type="stuff")

    response = chain.run(
        input_documents=docs,
        question=query
    )

    st.success(response)
