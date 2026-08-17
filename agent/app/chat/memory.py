"""เก็บประวัติบทสนทนา

เก็บใน process memory พอสำหรับโจทย์นี้ ไม่ต้องใช้ Redis

กับดักที่ต้องระวัง: ประวัติของ tool-use ไม่ใช่ข้อความธรรมดา
แต่ละรอบที่เรียก tool จะได้ message คู่กันเสมอ

    {"role": "assistant", "content": [... tool_use id=X ...]}
    {"role": "user",      "content": [... tool_result tool_use_id=X ...]}

ถ้าตัดประวัติแล้ว tool_use ขาดคู่กับ tool_result
Anthropic API จะ reject ทั้ง request ทันที
"""

import logging
from dataclasses import dataclass, field

from ..config import get_settings

logger = logging.getLogger(__name__)


def _has_tool_result(message: dict) -> bool:
    """message นี้เป็นฝั่งผลลัพธ์ของ tool หรือไม่"""
    content = message.get("content")
    if not isinstance(content, list):
        return False
    return any(
        isinstance(block, dict) and block.get("type") == "tool_result"
        for block in content
    )


@dataclass
class Conversation:
    """ประวัติของ session เดียว"""

    employee_id: str
    messages: list[dict] = field(default_factory=list)

    def add(self, role: str, content) -> None:
        """ต่อ message เข้าท้ายประวัติ"""
        self.messages.append({"role": role, "content": content})

    def trim(self) -> None:
        """ตัดประวัติให้เหลือ N ตาล่าสุด โดยไม่ให้ tool_result ขาดคู่กับ tool_use"""
        max_turns = get_settings().memory_max_turns

        starts = []
        for i, m in enumerate(self.messages):
            if m["role"] == "user" and not _has_tool_result(m):
                starts.append(i)

        if len(starts) <= max_turns:
            return

        cut = starts[-max_turns]


        while cut < len(self.messages) and _has_tool_result(self.messages[cut]):
            cut += 1
            

        self.messages = self.messages[cut:]
        logger.info("ตัดประวัติแล้วเหลือ %d message", len(self.messages))


class ConversationStore:
    """เก็บหลาย session ไว้ในหน่วยความจำ"""

    def __init__(self) -> None:
        self._sessions: dict[str, Conversation] = {}

    def get(self, session_id: str, employee_id: str) -> Conversation:
        """คืน conversation ของ session นี้ ไม่มีก็สร้างใหม่"""
        conv = self._sessions.get(session_id)
        # เปลี่ยนคนกลางคัน ให้เริ่มใหม่ ไม่เอาประวัติของคนเก่ามาปน
        if conv is None or conv.employee_id != employee_id:
            conv = Conversation(employee_id=employee_id)
            self._sessions[session_id] = conv
        return conv

    def reset(self, session_id: str) -> None:
        """ทิ้งประวัติของ session นี้"""
        self._sessions.pop(session_id, None)