"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # Load embeddings and IDs
    embeddings_path = PROCESSED_DIR / "embeddings.npy"
    ids_path = PROCESSED_DIR / "embedding_ids.json"
    corpus_path = RAW_DIR / "corpus.jsonl"
    
    if not embeddings_path.exists():
        raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
    if not ids_path.exists():
        raise FileNotFoundError(f"IDs file not found: {ids_path}")
    if not corpus_path.exists():
        raise FileNotFoundError(f"Corpus file not found: {corpus_path}")
    
    embeddings = np.load(embeddings_path)
    with open(ids_path, encoding="utf-8") as f:
        ids = json.load(f)
    
    # Load texts from corpus
    id_to_text = {}
    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            id_to_text[doc["id"]] = doc["text"]
    
    # Connect to Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise ValueError("PINECONE_API_KEY not found in environment")
    
    index_name = os.getenv("PINECONE_INDEX", "ragsession")
    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)
    
    # Batch upsert
    total = len(ids)
    upserted = 0
    
    for i in range(0, total, BATCH_SIZE):
        batch_ids = ids[i:i + BATCH_SIZE]
        batch_embeddings = embeddings[i:i + BATCH_SIZE]
        
        vectors_to_upsert = []
        for doc_id, embedding in zip(batch_ids, batch_embeddings):
            text = id_to_text.get(doc_id, "")
            # Truncate text for metadata
            if len(text) > TEXT_LIMIT:
                text = text[:TEXT_LIMIT]
            
            vectors_to_upsert.append({
                "id": doc_id,
                "values": embedding.tolist(),
                "metadata": {"text": text}
            })
        
        # Upsert batch
        index.upsert(vectors=vectors_to_upsert)
        upserted += len(vectors_to_upsert)
        
        if progress_callback:
            progress_callback(upserted, total)
    
    return upserted


if __name__ == "__main__":
    ingest()
