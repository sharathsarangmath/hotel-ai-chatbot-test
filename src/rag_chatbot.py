import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.anthropic import Anthropic
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

def build_rag_engine():
    """Build the RAG engine from hotel policy documents."""

    # Set the embedding model — free, runs locally
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

    # Set the LLM — Claude Haiku
    Settings.llm = Anthropic(
        model="claude-haiku-4-5",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    # Load hotel policy documents from docs/ folder
    documents = SimpleDirectoryReader("docs").load_data()

    # Build the vector index from documents
    index = VectorStoreIndex.from_documents(documents)

    # Return a query engine
    return index.as_query_engine()


def ask_rag_concierge(question: str, engine=None) -> str:
    """Send a question to the RAG concierge and return the response."""
    if engine is None:
        engine = build_rag_engine()
    response = engine.query(question)
    return str(response)