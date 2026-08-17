"""FastAPI entrypoint ของ agent"""

import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI

from pathlib import Path
from fastapi.responses import FileResponse

from .chat.loop import run
from .chat.memory import ConversationStore
from .config import get_settings
from .rag.ingest import run_ingest
from .rag.store import get_collection
from .schemas import ChatRequest, ChatResponse, Source

STATIC_DIR = Path(__file__).parent / "static"

logging.basicConfig(
    level=get_settings().log_level,
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

sessions = ConversationStore()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """ingest อัตโนมัติถ้ายังไม่มีข้อมูล

    เช็คก่อนว่ามีอยู่แล้วหรือยัง จะได้ไม่เสียเวลา 30-60 วินาทีทุกครั้งที่ restart
    ทำให้ reviewer รัน docker compose up แล้วใช้ได้เลย ไม่ต้องรันคำสั่งเพิ่ม
    """
    count = get_collection().count()
    if count == 0:
        logger.info("knowledge base ว่าง กำลัง ingest...")
        count = run_ingest()
    logger.info("พร้อมใช้งาน มี %d ชิ้นใน knowledge base", count)
    yield


app = FastAPI(title="TechCorp Helpdesk Agent", version="1.0.0", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """หน้าแชทอย่างง่าย — รีเฟรชหน้าคือเริ่ม session ใหม่"""
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health() -> dict[str, str | int]:
    """compose healthcheck เรียกตัวนี้ บอกด้วยว่า knowledge base พร้อมไหม"""
    try:
        chunks = get_collection().count()
    except Exception:
        chunks = -1
    return {"status": "ok", "chunks": chunks}


@app.get("/config")
def config() -> dict[str, str | int]:
    """ตรวจว่า container อ่าน env ถูกจริง (ไม่คืน secret)"""
    s = get_settings()
    return {
        "llm_model": s.llm_model,
        "embedding_model": s.embedding_model,
        "retrieval_top_k": s.retrieval_top_k,
        "mock_api_base_url": s.mock_api_base_url,
        "knowledge_base_dir": s.knowledge_base_dir,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    """รับคำถาม เดิน agent loop แล้วคืนคำตอบพร้อม tool ที่ใช้และแหล่งอ้างอิง"""
    # ไม่ส่ง session_id มา = เริ่มบทสนทนาใหม่ ผู้ใช้ส่ง id ที่ได้กลับไป
    # ในครั้งถัดไปเพื่อให้ agent จำบริบทเดิมได้
    session_id = req.session_id or str(uuid.uuid4())
    conv = sessions.get(session_id, req.employee_id)
  
    logger.info("chat session=%s emp=%s q=%r", session_id[:8], req.employee_id, req.message)
    reply = await run(req.message, conv)

    # ตัดแหล่งอ้างอิงที่ซ้ำกันออก แต่รักษาลำดับตามคะแนนที่ค้นได้
    seen, unique = set(), []
    for s in reply.sources:
        key = (s["source"], s["section_path"])
        if key not in seen:
            seen.add(key)
            unique.append(Source(**s))

    return ChatResponse(
        reply=reply.text,
        session_id=session_id,
        tools_used=reply.tools_used,
        sources=unique,
    )


@app.post("/admin/reingest")
def reingest(reset: bool = False) -> dict[str, int | str]:
    """สั่ง ingest ใหม่ตอน runtime — reset=true คือล้าง collection ก่อน"""
    before = get_collection().count()
    total = run_ingest(reset=reset)
    logger.info("re-ingest: %d -> %d ชิ้น (reset=%s)", before, total, reset)
    return {"before": before, "after": total, "reset": str(reset)}


@app.delete("/chat/{session_id}")
def reset_session(session_id: str) -> dict[str, str]:
    """ล้างประวัติ ใช้ตอน eval เพื่อไม่ให้แต่ละเคสปนกัน"""
    sessions.reset(session_id)
    return {"status": "reset", "session_id": session_id}