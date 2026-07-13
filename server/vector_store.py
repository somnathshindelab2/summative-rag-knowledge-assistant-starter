from typing import Any, List

import chromadb
import requests

from config import Config
from documents import DocumentChunk, build_chunks, load_text_documents


def get_chroma_client():
    """Create and return a persistent Chroma client."""
    return chromadb.PersistentClient(path=Config.CHROMA_PATH)


def get_or_create_collection():
    """Get or create the Chroma collection for the knowledge assistant."""
    client = get_chroma_client()
    return client.get_or_create_collection(name=Config.COLLECTION_NAME)


def get_embedding(text: str) -> list[float]:
    """Create an embedding for a piece of text using the local model service."""
    response = requests.post(
        f"{Config.OLLAMA_BASE_URL.rstrip('/')}/api/embed",
        json={"model": Config.EMBEDDING_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    embedding = payload.get("embedding")

    if isinstance(embedding, list):
        return embedding

    result = payload.get("result")
    if isinstance(result, list):
        return result

    embeddings = payload.get("embeddings")
    if isinstance(embeddings, list) and embeddings:
        first = embeddings[0]
        if isinstance(first, list):
            return first

    return []


def ensure_knowledge_base_loaded() -> int:
    """Load and index the knowledge base if the collection is empty."""
    collection = get_or_create_collection()
    if collection.count() > 0:
        return collection.count()

    documents = load_text_documents(Config.KNOWLEDGE_BASE_PATH)
    chunks = build_chunks(documents)
    return seed_vector_store(chunks)


def seed_vector_store(chunks: List[DocumentChunk]) -> int:
    """Add document chunks to the Chroma collection with their metadata."""
    if not chunks:
        return 0

    collection = get_or_create_collection()
    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas = [
        {"source": chunk.source, "title": chunk.title, "chunk_index": chunk.chunk_index}
        for chunk in chunks
    ]
    embeddings = [get_embedding(chunk.text) for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(chunks)


def retrieve_relevant_chunks(question: str, top_k: int | None = None) -> list[dict[str, Any]]:
    """Retrieve relevant chunks for a user question."""
    ensure_knowledge_base_loaded()
    collection = get_or_create_collection()

    if collection.count() == 0:
        return []

    query_embedding = get_embedding(question)
    if not query_embedding:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k or Config.TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    returned_documents = results.get("documents", [[]])[0]
    returned_metadatas = results.get("metadatas", [[]])[0]
    returned_distances = results.get("distances", [[]])[0]

    relevant_chunks = []

    for index, text in enumerate(returned_documents):
        metadata = returned_metadatas[index] if index < len(returned_metadatas) else {}
        distance = returned_distances[index] if index < len(returned_distances) else None

        relevant_chunks.append(
            {
                "text": text,
                "source": metadata.get("source", "unknown"),
                "title": metadata.get("title", "Unknown Source"),
                "chunk_index": metadata.get("chunk_index", index),
                "distance": distance,
            }
        )

    return relevant_chunks
