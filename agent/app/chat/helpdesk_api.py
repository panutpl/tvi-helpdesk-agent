"""HTTP client เรียก mock API ของ HR/IT

ไฟล์นี้รู้เรื่อง HTTP อย่างเดียว ไม่รู้จัก LLM
แยกจาก tools.py เพื่อให้ทดสอบ client ตรง ๆ ได้โดยไม่ต้องมี API key
"""

import httpx

from ..config import get_settings


class HelpdeskApiError(Exception):
    """ข้อผิดพลาดที่บอกผู้ใช้ได้เลย ไม่ใช่ stack trace

    ตัว agent จะเอาข้อความนี้ส่งกลับให้ LLM อ่านแล้วเรียบเรียงต่อ
    จึงต้องเขียนให้คนอ่านรู้เรื่อง ไม่ใช่ศัพท์เทคนิค
    """


def _client() -> httpx.AsyncClient:
    """สร้าง http client ที่ใส่ token กับ timeout ไว้แล้ว"""
    s = get_settings()
    return httpx.AsyncClient(
        base_url=s.mock_api_base_url,
        headers={"Authorization": f"Bearer {s.mock_api_token}"},
        # ต้องมี timeout เสมอ ถ้า mock API ค้าง agent จะรอไม่จบ
        timeout=s.mock_api_timeout,
    )


async def _get(path: str) -> dict:
    """ยิง GET แล้วแปลง error เป็นข้อความที่ส่งต่อให้ LLM อ่านได้"""
    try:
        async with _client() as client:
            response = await client.get(path)
    except httpx.RequestError:
        raise HelpdeskApiError("ระบบ HR ไม่ตอบสนอง กรุณาลองใหม่อีกครั้ง")

    if response.status_code == 404:
        # ให้ผู้เรียกเป็นคนบอกว่า "ไม่พบอะไร" เพราะมันรู้บริบทดีกว่า
        raise HelpdeskApiError("NOT_FOUND")
    if response.status_code == 401:
        raise HelpdeskApiError("ไม่มีสิทธิ์เข้าถึงระบบ HR (token ไม่ถูกต้อง)")
    if response.status_code >= 400:
        raise HelpdeskApiError(f"ระบบ HR ตอบกลับผิดปกติ (HTTP {response.status_code})")

    return response.json()


async def get_leave_balance(employee_id: str) -> dict:
    """ดึงวันลาคงเหลือของพนักงาน"""
    try:
        return await _get(f"/employees/{employee_id}/leave-balance")
    except HelpdeskApiError as e:
        if str(e) == "NOT_FOUND":
            raise HelpdeskApiError(f"ไม่พบข้อมูลพนักงานรหัส {employee_id}")
        raise


async def get_employee_tickets(employee_id: str) -> dict:
    """ดึงรายการ ticket ของพนักงาน"""
    try:
        return await _get(f"/employees/{employee_id}/tickets")
    except HelpdeskApiError as e:
        if str(e) == "NOT_FOUND":
            raise HelpdeskApiError(f"ไม่พบข้อมูลพนักงานรหัส {employee_id}")
        raise


async def get_ticket(ticket_id: str) -> dict:
    """ดึงรายละเอียด ticket ตามหมายเลข"""
    try:
        return await _get(f"/tickets/{ticket_id}")
    except HelpdeskApiError as e:
        if str(e) == "NOT_FOUND":
            raise HelpdeskApiError(f"ไม่พบ ticket หมายเลข {ticket_id}")
        raise