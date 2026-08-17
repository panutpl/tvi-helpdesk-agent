"""อ่าน markdown -> หั่น -> แปลงเป็น vector -> เก็บลง Chroma

    python -m app.rag.ingest           # อัปเดตเฉพาะที่เปลี่ยน
    python -m app.rag.ingest --reset   # ล้างแล้วสร้างใหม่
"""

import argparse
from pathlib import Path

from ..config import get_settings
from .chunking import Chunk, split_markdown
from .embedder import embed_documents
from .store import get_collection, reset_collection



def load_chunks() -> list[Chunk]:
    """อ่าน .md ทุกไฟล์ใน knowledge base แล้วหั่นเป็น chunk"""
    kb_dir = Path(get_settings().knowledge_base_dir)
    chunks: list[Chunk] = []
    for path in sorted(kb_dir.glob("*.md")):
        chunks += split_markdown(path.read_text(encoding="utf-8"), path.name)
    return chunks


def run_ingest(reset: bool = False) -> int:
    """หั่น -> embed -> upsert ลง Chroma คืนจำนวนชิ้นที่เก็บ"""
    chunks = load_chunks()
    if not chunks:
        raise RuntimeError(f"ไม่พบไฟล์ .md ใน {get_settings().knowledge_base_dir}")

    collection = reset_collection() if reset else get_collection()
    
    print(f"กำลังแปลง {len(chunks)} ชิ้นเป็น vector...")
    collection.upsert(
        ids=[c.chunk_id for c in chunks],
        embeddings=embed_documents([c.text for c in chunks]),
        documents=[c.text for c in chunks],
        metadatas=[c.metadata for c in chunks],
    )

    return len(chunks)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="ล้าง collection ก่อน")
    args = parser.parse_args()

    print(f"model: {get_settings().embedding_model}")
    total = run_ingest(reset=args.reset)
    print(f"เสร็จแล้ว {total} ชิ้น")