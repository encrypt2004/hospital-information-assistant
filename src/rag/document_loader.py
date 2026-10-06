from pathlib import Path

from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).resolve().parent.parent.parent

POLICY_PATH = BASE_DIR / "policy" / "VinCare_Hospital_Policies.pdf"


def load_policy_document():
    """
    Load the hospital policy PDF.
    """

    reader = PdfReader(str(POLICY_PATH))

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": "VinCare_Hospital_Policies.pdf",
                        "page": page_number,
                    },
                )
            )

    return documents


def split_policy_document(documents):
    """
    Split PDF pages into smaller chunks for vector search.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120,
    )

    chunks = splitter.split_documents(documents)

    return chunks