"""รูปแบบ request/response ของ agent API

แยกออกมาเพราะทั้ง main.py และ eval script ต้องรู้จักโครงสร้างเดียวกัน
ถ้าฝังไว้ใน main.py จะ import ข้ามไปมาแล้วเกิด circular import
"""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    employee_id: str = Field(examples=["EMP-1234"])
    message: str
    session_id: str | None = None


class Source(BaseModel):
    source: str
    section_path: str


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    tools_used: list[str] = []
    sources: list[Source] = []
