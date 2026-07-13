from typing import Any

import requests

from config import Config
from vector_store import retrieve_relevant_chunks


def answer_question(question: str) -> dict[str, Any]:
    """Run the RAG workflow for a user question."""
    try:
        chunks = retrieve_relevant_chunks(question, top_k=Config.TOP_K)
    except Exception as exc:
        return {
            "answer": (
                "I could not retrieve enough context from the knowledge base to answer that "
                "question because the retrieval service is unavailable."
            ),
            "sources": [],
            "metadata": {"error": str(exc)},
        }

    if not chunks:
        return {
            "answer": (
                "I could not find enough relevant information in the provided knowledge base "
                "to answer that question."
            ),
            "sources": [],
            "metadata": {
                "model": Config.GENERATION_MODEL,
                "retrieved_chunks": 0,
                "embedding_model": Config.EMBEDDING_MODEL,
            },
        }

    prompt = build_prompt(question, chunks)
    answer = call_generation_model(prompt)

    return {
        "answer": answer,
        "sources": format_sources(chunks),
        "metadata": {
            "model": Config.GENERATION_MODEL,
            "retrieved_chunks": len(chunks),
            "embedding_model": Config.EMBEDDING_MODEL,
        },
    }


def build_prompt(question: str, chunks: list[dict[str, Any]]) -> str:
    """Build a prompt that asks the model to answer using only retrieved context."""
    context_blocks = []

    for index, chunk in enumerate(chunks, start=1):
        title = chunk.get("title", "Unknown Source")
        source = chunk.get("source", "unknown")
        text = chunk.get("text", "")

        context_blocks.append(f"[Source {index}: {title} | {source}]\n{text}")

    context = "\n\n".join(context_blocks)

    return f"""
You are a helpful internal knowledge assistant.

Use only the provided context to answer the user's question.
If the context does not contain enough information, say that you do not have enough information from the knowledge base.

Keep the answer clear and practical.
Do not invent policies, steps, or facts that are not supported by the context.

Context:
{context}

User question:
{question}

Answer:
""".strip()


def call_generation_model(prompt: str) -> str:
    """Send the final prompt to the configured generation model."""
    payload = {
        "model": Config.GENERATION_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": Config.TEMPERATURE},
    }

    try:
        response = requests.post(
            f"{Config.OLLAMA_BASE_URL.rstrip('/')}/api/generate",
            json=payload,
            timeout=120,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data.get("response"), str):
            return data["response"].strip()

        if isinstance(data.get("output"), str):
            return data["output"].strip()

        results = data.get("results")
        if isinstance(results, list) and results:
            first = results[0]
            if isinstance(first, dict):
                if isinstance(first.get("content"), str):
                    return first["content"].strip()
                if isinstance(first.get("response"), str):
                    return first["response"].strip()
            if isinstance(first, str):
                return first.strip()

        if isinstance(data.get("text"), str):
            return data["text"].strip()

        return "I could not generate a response."
    except requests.RequestException:
        return (
            "I could not reach the local model service. Please confirm that Ollama is running "
            "and that the configured model is available."
        )


def format_sources(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Format retrieved chunks for the frontend."""
    sources = []

    for chunk in chunks:
        text = chunk.get("text", "")
        excerpt = text[:280] + "..." if len(text) > 280 else text

        sources.append(
            {
                "title": chunk.get("title", "Unknown Source"),
                "source": chunk.get("source", "unknown"),
                "chunk_index": chunk.get("chunk_index"),
                "excerpt": excerpt,
                "content": excerpt,
                "metadata": {
                    "path": f"knowledge_base/{chunk.get('source', 'unknown')}",
                },
            }
        )

    return sources
