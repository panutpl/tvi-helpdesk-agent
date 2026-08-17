"""แปลงข้อความเป็น vector

แยกฟังก์ชันของเอกสารกับของคำถามออกจากกัน เพราะบาง model
ต้องเติมคำนำหน้าคนละแบบ (e5 ต้องใช้ "query: " กับ "passage: ")
ถ้าเติมผิดหรือลืมเติม คุณภาพการค้นจะตกโดยไม่มีสัญญาณเตือน
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer

from ..config import get_settings


@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    """โหลด model ครั้งเดียวแล้วใช้ซ้ำ โหลดใหม่ทุกครั้งจะช้ามาก"""
    return SentenceTransformer(get_settings().embedding_model)


def embed_documents(texts: list[str]) -> list[list[float]]:
    """แปลงข้อความหลายชิ้นเป็น vector สำหรับเก็บลง store"""
    vectors = get_model().encode(
        texts,
        batch_size=8,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return vectors.tolist()


def embed_query(text: str) -> list[float]:
    """แปลงคำถามหนึ่งประโยคเป็น vector สำหรับค้น"""
    vector = get_model().encode(
        text,
        normalize_embeddings=True,
        show_progress_bar=False
    )
    return vector.tolist()