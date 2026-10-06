from pathlib import Path

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

from src.rag.document_loader import (
    load_policy_document,
    split_policy_document,
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent

VECTORSTORE_DIR = BASE_DIR / "vectorstore" / "faiss_index"


def get_embeddings():
    """
    Create Gemini embedding model.
    """

    return GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )


def create_vectorstore():
    """
    Create FAISS vector store from hospital policy PDF.
    """

    documents = load_policy_document()

    chunks = split_policy_document(documents)

    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(
        str(VECTORSTORE_DIR)
    )

    return vectorstore


def load_vectorstore():
    """
    Load existing FAISS index.
    """

    embeddings = get_embeddings()

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    return vectorstore


def get_vectorstore():
    """
    Load FAISS if it exists.
    Otherwise create it.
    """

    index_file = VECTORSTORE_DIR / "index.faiss"

    if index_file.exists():
        return load_vectorstore()

    return create_vectorstore()