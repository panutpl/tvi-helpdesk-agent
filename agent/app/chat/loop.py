"""Agent loop — เรียก LLM วนจนได้คำตอบ

เขียน loop เองด้วย tool-use ของ Anthropic SDK แทนใช้ LangGraph
เพราะกราฟจริงมีแค่ 2 node (llm <-> tools) การเพิ่ม abstraction layer
แลกกับความสามารถในการอธิบายและแก้โค้ดสดตอนสัมภาษณ์ไม่คุ้ม
"""

import logging
import re
import time
from dataclasses import dataclass, field

from anthropic import AsyncAnthropic

from ..config import get_settings
from .memory import Conversation
from .prompts import SYSTEM_PROMPT
from .tools import TOOL_SCHEMAS, dispatch

logger = logging.getLogger(__name__)

# ดึงชื่อไฟล์กับหัวข้อออกจากบรรทัด "[1] ที่มา: leave-policy.md — นโยบาย > 1.1"
# ที่ format_for_llm ใส่ไว้ เพื่อคืนแหล่งอ้างอิงให้ผู้ใช้ตรวจสอบได้
_SOURCE_LINE = re.compile(r"^\[\d+\] ที่มา: (\S+) — (.+)$", re.MULTILINE)


@dataclass
class AgentReply:
    text: str
    tools_used: list[str] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)


def _client() -> AsyncAnthropic:
    """สร้าง Anthropic client จาก config"""
    s = get_settings()
    return AsyncAnthropic(api_key=s.anthropic_api_key, base_url=s.anthropic_base_url)


def _text_of(blocks) -> str:
    """ดึงเฉพาะ text block ออกจาก content ที่ LLM ตอบมา"""
    return "\n".join(b.text for b in blocks if b.type == "text").strip()


async def run(message: str, conv: Conversation) -> AgentReply:
    """วนเรียก LLM -> ทำ tool -> ส่งผลกลับ จนได้คำตอบหรือครบจำนวนรอบ"""
    s = get_settings()
    client = _client()

    
    conv.add("user", message)
    conv.trim()

    tools_used: list[str] = []
    sources: list[dict] = []

    for turn in range(s.agent_max_iterations):

        response = await client.messages.create(
            model=s.llm_model,
            max_tokens=s.llm_max_tokens,
            temperature=s.llm_temperature,
            system=SYSTEM_PROMPT,
            messages=conv.messages,
            tools=TOOL_SCHEMAS,
        )
       

        # ต้องเก็บ content ดิบทั้งก้อน ไม่ใช่เฉพาะ text
        # เพราะรอบถัดไปต้องมี tool_use เดิมอยู่ให้ tool_result อ้างถึง
        conv.add("assistant", [b.model_dump() for b in response.content])

        if response.stop_reason != "tool_use":
            return AgentReply(_text_of(response.content), tools_used, sources)

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue

            started = time.perf_counter()
            output = await dispatch(block.name, block.input, conv.employee_id)
            elapsed = (time.perf_counter() - started) * 1000
            

            tools_used.append(block.name)
            logger.info(
                "tool=%s args=%s ms=%.0f len=%d",
                block.name, block.input, elapsed, len(output),
            )

            if block.name == "search_knowledge":
                sources += [
                    {"source": src, "section_path": path}
                    for src, path in _SOURCE_LINE.findall(output)
                ]

            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                }
            )

        # ต้องส่งผลกลับให้ครบทุก tool_use ในรอบเดียว ไม่งั้น API reject
        conv.add("user", results)
        

    # ครบจำนวนรอบแล้วยังไม่ได้คำตอบ ดีกว่าปล่อยให้วนไม่จบ
    logger.warning("ครบ %d รอบแล้วยังไม่จบ", s.agent_max_iterations)
    return AgentReply(
        "ขออภัยครับ ผมหาคำตอบให้ไม่ได้ในตอนนี้ รบกวนถามใหม่ให้เจาะจงขึ้น "
        "หรือติดต่อ HR/IT โดยตรงครับ",
        tools_used,
        sources,
    )