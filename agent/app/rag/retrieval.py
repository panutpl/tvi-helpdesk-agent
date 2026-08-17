"""ค้นหาชิ้นข้อมูลที่เกี่ยวข้องกับคำถาม

นี่คือประตูเดียวที่ฝั่ง chat/ ใช้เข้าถึง knowledge base
ข้างในจะเปลี่ยนเป็น vector store ตัวอื่นหรือเพิ่ม reranker
ก็ไม่กระทบคนเรียก ขอแค่ยังคืน RetrievedChunk เหมือนเดิม
"""

from dataclasses import dataclass


from ..config import get_settings
from .embedder import embed_query
from .store import get_collection


@dataclass
class RetrievedChunk:
    text: str            # ข้อความเต็มพร้อมหัวข้อที่แปะไว้หน้า
    source: str          # ชื่อไฟล์ เช่น leave-policy.md
    section_path: str    # หัวข้อเต็ม
    lang: str
    score: float         # 0-1 ยิ่งสูงยิ่งใกล้


def _build_filter(source: str | None, lang: str | None) -> dict | None:
    """แปลงเงื่อนไขเป็นรูปแบบ where ของ Chroma

    Chroma ต้องการ $and เมื่อมีเงื่อนไขมากกว่าหนึ่งข้อ
    ถ้าส่ง dict สองคีย์ตรง ๆ จะ error
    """
    conditions = []
    if source:
        conditions.append({"source": source})
    if lang:
        conditions.append({"lang": lang})

    if not conditions:
        return None
    if len(conditions) == 1:
        return conditions[0]
    return {"$and": conditions}


def search(
    query: str,
    top_k: int | None = None,
    source: str | None = None,
    lang: str | None = None,
) -> list[RetrievedChunk]:
    """ค้น chunk ที่ใกล้คำถามที่สุด กรองตามไฟล์หรือภาษาได้"""
    collection = get_collection()
    total = collection.count()
    if total == 0:
        return []

    k = top_k or get_settings().retrieval_top_k
    # ขอเกินจำนวนที่มีจริงไม่ได้ Chroma จะ error
    k = min(k, total)

    result = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=k,
        where=_build_filter(source, lang),
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, distance in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        chunks.append(
            RetrievedChunk(
                text=text,
                source=meta["source"],
                section_path=meta["section_path"],
                lang=meta["lang"],
                # collection ตั้ง hnsw:space เป็น cosine
                # distance = 1 - similarity จึงกลับด้านได้ตรง ๆ
                score=round(1 - distance, 4),
            )
        )
    return chunks


def format_for_llm(chunks: list[RetrievedChunk]) -> str:
    """รวมผลค้นเป็นข้อความก้อนเดียวส่งให้ LLM

    ใส่หมายเลขกับที่มาทุกชิ้น เพื่อให้ LLM อ้างอิงได้และเราตรวจย้อนได้
    """
    if not chunks:
        return "ไม่พบข้อมูลที่เกี่ยวข้องใน knowledge base"

    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[{i}] ที่มา: {c.source} — {c.section_path}\n{c.text}")
    return "\n\n---\n\n".join(parts)


