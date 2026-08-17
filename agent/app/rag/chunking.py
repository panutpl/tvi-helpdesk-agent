"""หั่นไฟล์ markdown เป็นชิ้นเล็ก ๆ เพื่อเอาไป embed

ทำงาน 4 ขั้น: หั่นตามหัวข้อ -> หั่นตาม "**ถาม:" -> รวมชิ้นสั้น -> แปะหัวข้อ
"""

import hashlib
import re
from dataclasses import dataclass, field

from langchain_text_splitters import MarkdownHeaderTextSplitter

MAX_CHARS = 1200   # ชิ้นที่รวมกันแล้วต้องไม่เกินนี้
MIN_CHARS = 120   # สั้นกว่านี้ถือว่าไม่มีความหมายในตัวเอง ต้องรวมกับชิ้นถัดไป

HEADERS = [("#", "h1"), ("##", "h2"), ("###", "h3")]
THAI = re.compile(r"[\u0E00-\u0E7F]")


@dataclass
class Section:
    """หัวข้อหนึ่งอันระหว่างทาง ยังไม่ใช่ผลลัพธ์สุดท้าย"""
    path: list[str]   # ["นโยบายการลา", "1. ประเภทการลา", "1.1 ลาพักร้อน"]
    body: str


@dataclass
class Chunk:
    """ผลลัพธ์สุดท้าย 1 ชิ้นที่จะเอาไป embed"""
    text: str
    metadata: dict = field(default_factory=dict)

    @property
    def chunk_id(self) -> str:
        """id จากที่มา ทำให้ ingest ซ้ำแล้ว upsert ทับของเดิม ไม่เกิดข้อมูลซ้ำ"""
        m = self.metadata
        key = f"{m['source']}::{m['section_path']}::{m['chunk_index']}"
        return hashlib.sha256(key.encode()).hexdigest()[:32]

def _pick_path(a: list[str], b: list[str]) -> list[str]:
    """เลือกป้ายหัวข้อให้ชิ้นที่รวมกันแล้ว

    แม่ดูดลูก -> ใช้ป้ายลูกเพราะเจาะจงกว่า
    พี่น้องรวมกัน -> ถอยไปใช้ป้ายแม่ ไม่ยืมชื่อฝ่ายใดฝ่ายหนึ่ง
    """
    if a == b[:len(a)]:
        return b

    common = []
    for x, y in zip(a, b):
        if x != y:
            break
        common.append(x)
    return common or a


def _split_by_heading(raw: str) -> list[Section]:
    """ขั้น 1 — หั่นตาม # ## ###"""
    splitter = MarkdownHeaderTextSplitter(HEADERS, strip_headers=True)
    sections = []
    for doc in splitter.split_text(raw):
        path = [doc.metadata[k] for k in ("h1", "h2", "h3") if k in doc.metadata]
        body = doc.page_content.strip()
        if body:
            sections.append(Section(path, body))
    return sections


def _split_by_question(sections: list[Section]) -> list[Section]:
    """ขั้น 2 — ซอยต่อตาม "**ถาม:" สำหรับไฟล์ที่ใช้ bold แทน heading

    office-facilities.md ใช้ ## อย่างเดียว ไม่ซอยจะได้ Gym ทั้งหัวข้อเป็นชิ้นเดียว
    """
    out = []
    for s in sections:
        for part in re.split(r"\n(?=\*\*ถาม[:：])", s.body):
            if part.strip():
                out.append(Section(s.path, part.strip()))
    return out


def _merge_small(sections: list[Section]) -> list[Section]:
    """ขั้น 3 — ชิ้นสั้นกว่า MIN_CHARS ให้ดูดชิ้นถัดไปมารวม

    รวมเฉพาะที่อยู่ใต้หัวข้อใหญ่เดียวกัน ไม่งั้น VPN จะไปรวมกับ Device Policy
    """
    out: list[Section] = []
    for s in sections:
        prev = out[-1] if out else None
        can_merge = (
            prev is not None
            and len(prev.body) < MIN_CHARS
            and prev.path[:2] == s.path[:2]
            and len(prev.body) + len(s.body) <= MAX_CHARS
        )
        if can_merge:
            prev.body += "\n\n" + s.body
            prev.path = _pick_path(prev.path, s.path)
        else:
            out.append(Section(list(s.path), s.body))
    return out


def split_markdown(raw: str, source: str) -> list[Chunk]:
    """หั่น markdown 1 ไฟล์เป็น Chunk พร้อม metadata — entry point ของโมดูลนี้

    ขั้น 4 คือแปะ section path ไว้หน้าเนื้อหาก่อน embed เพราะแถวตาราง
    "| แท็กซี่ | 500 บาท/เที่ยว |" ไม่มีคำว่า "เบิก" อยู่เลย ถ้าไม่แปะจะค้นไม่เจอ
    """
    title = re.search(r"^#\s+(.+)$", raw, flags=re.MULTILINE)
    doc_title = title.group(1).strip() if title else source

    sections = _split_by_heading(raw)
    
    sections = _split_by_question(sections)
    sections = _merge_small(sections)

    chunks = []
    for i, s in enumerate(sections):
        section_path = " > ".join(s.path or [doc_title])
        chunks.append(
            Chunk(
                text=f"{section_path}\n\n{s.body}",
                metadata={
                    "source": source,
                    "doc_title": doc_title,
                    "section_path": section_path,
                    "lang": "th" if THAI.search(s.body) else "en",
                    "chunk_index": i,
                },
            )
        )
    return chunks