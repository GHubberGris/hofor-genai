import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from pdf_loader import load_pdfs
from chunking import chunk_documents

def main():
    """
    Load pdf documents. Define chunker and chunk documents.
    Define embedding model. Upload embeddings to Qdrant
    """
    env_path = Path(__file__).parent.parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    PDF_DIR = Path("pdf_downloads")
    docs = load_pdfs(PDF_DIR)

    chunks = chunk_documents(docs, chunk_size=800, chunk_overlap=100)
    
    openai_kwargs = {"api_key": os.getenv("OPENAI_API_KEY")} if os.getenv("OPENAI_API_KEY") else {}
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", **openai_kwargs)

    
    QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
        collection_name=os.getenv("QDRANT_COLLECTION"),
)


    print(f"Ingested {len(chunks)} chunks into Qdrant collection '{os.getenv("QDRANT_COLLECTION")}'")


if __name__ == "__main__":
    main()
