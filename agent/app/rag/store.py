"""เชื่อมต่อ ChromaDB

รวมการเปิด collection ไว้ที่เดียว ทั้ง ingest และ retrieval เรียกตัวนี้
จะได้ไม่ตั้งค่าคนละแบบจนหาไม่เจอว่าทำไมผลไม่ตรงกัน
"""

import chromadb
from chromadb.api.models.Collection import Collection

from ..config import get_settings


def get_collection() -> Collection:
    """เปิด collection เดิม ถ้ายังไม่มีให้สร้างใหม่"""
    s = get_settings()
    client = chromadb.PersistentClient(path=s.chroma_persist_dir)
    return client.get_or_create_collection(
        name=s.chroma_collection,
        metadata={"hnsw:space": "cosine"},
    )


def reset_collection() -> Collection:
    """ลบ collection ทิ้งแล้วสร้างใหม่ — ใช้ตอน ingest --reset"""
    s = get_settings()
    client = chromadb.PersistentClient(path=s.chroma_persist_dir)
    try:
        client.delete_collection(s.chroma_collection)
    except Exception:
        pass
    return client.get_or_create_collection(
        name=s.chroma_collection,
        metadata={"hnsw:space": "cosine"},
    )