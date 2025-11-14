import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    docs = PyPDFLoader(PDF_PATH).load()

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, add_start_index=False).split_documents(docs)

    if not splits:
        raise SystemExit(0)

    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]    

    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_MODEL","text-embedding-004"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PGVECTOR_COLLECTION"),
        connection=os.getenv("PGVECTOR_URL"),
        use_jsonb=True,
    )
    store.add_documents(documents=enriched)


if __name__ == "__main__":
    ingest_pdf()
