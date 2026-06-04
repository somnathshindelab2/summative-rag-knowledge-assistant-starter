from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List


@dataclass
class DocumentChunk:
    """A small piece of a source document prepared for retrieval."""

    id: str
    text: str
    source: str
    title: str
    chunk_index: int


def load_text_documents(folder_path: str) -> list[dict]:
    """
    Load plain text files from the provided knowledge base folder.

    Returns:
        A list of dictionaries with title, source filename, and text.
    """
    folder = Path(folder_path)

    if not folder.exists():
        raise FileNotFoundError(f"Knowledge base folder not found: {folder.resolve()}")

    documents = []

    for file_path in sorted(folder.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8").strip()
        title = _extract_title(text, fallback=file_path.stem.replace("_", " ").title())

        documents.append(
            {
                "title": title,
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


def build_chunks(
    documents: Iterable[dict],
    chunk_size: int = 120,
    overlap: int = 25,
) -> List[DocumentChunk]:
    """
    Convert loaded documents into overlapping word chunks.

    This helper is provided so you can focus on the vector store
    and RAG workflow.
    """
    chunks: list[DocumentChunk] = []

    for document in documents:
        text_chunks = chunk_text(
            document["text"],
            chunk_size=chunk_size,
            overlap=overlap,
        )

        for index, chunk_text_value in enumerate(text_chunks):
            chunk_id = f"{document['source']}::chunk-{index}"

            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    text=chunk_text_value,
                    source=document["source"],
                    title=document["title"],
                    chunk_index=index,
                )
            )

    return chunks


def chunk_text(text: str, chunk_size: int = 120, overlap: int = 25) -> list[str]:
    """
    Split text into overlapping chunks by word count.

    Args:
        text: Full document text.
        chunk_size: Approximate number of words per chunk.
        overlap: Number of words to repeat between chunks.
    """
    words = text.split()

    if not words:
        return []

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        if end >= len(words):
            break

        start = max(end - overlap, start + 1)

    return chunks


def _extract_title(text: str, fallback: str) -> str:
    """Use the first non-empty line as the document title."""
    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned:
            return cleaned
    return fallback
