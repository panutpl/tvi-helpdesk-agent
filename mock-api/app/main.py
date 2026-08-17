"""Mock API server — TechCorp Internal Helpdesk

จำลอง 2 ระบบภายใน: HR (leave balance) และ IT ticketing
สโคปตาม docs/mock-api-spec.md — อ่านอย่างเดียว ไม่มี write endpoint
"""

import os

from fastapi import APIRouter, Depends, FastAPI, Header, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from .data import DATA_AS_OF, EMPLOYEES, TICKETS, UPCOMING_LEAVES
from .leave import build_leave_balance

MOCK_API_TOKEN = os.getenv("MOCK_API_TOKEN", "techcorp-mock-token-2025")

app = FastAPI(title="TechCorp Mock API", version="1.0.0")


# ---------------------------------------------------------------- errors
class ApiError(Exception):
    """error ที่มี shape ตาม spec: {"error": ..., "message": ...}"""

    def __init__(self, status_code: int, error: str, message: str) -> None:
        self.status_code = status_code
        self.error = error
        self.message = message


@app.exception_handler(ApiError)
async def api_error_handler(_: Request, exc: ApiError) -> JSONResponse:
    """แปลง ApiError เป็น JSON response ตาม shape ที่ spec กำหนด"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error, "message": exc.message},
    )


@app.exception_handler(StarletteHTTPException)
async def http_error_handler(_: Request, exc: StarletteHTTPException) -> JSONResponse:
    """ครอบ error ที่ framework โยนเอง (เช่น 404 route ไม่มีอยู่)
    ให้ shape เหมือนกันทั้ง API — client จะ parse ทางเดียวได้เสมอ
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Error", "message": str(exc.detail)},
    )


# ---------------------------------------------------------------- auth
def require_token(authorization: str | None = Header(default=None)) -> None:
    """ตรวจ Authorization: Bearer <token>

    เขียนเองแทน fastapi.security.HTTPBearer เพราะ HTTPBearer คืน 403
    เมื่อไม่มี header แต่ spec ระบุ 401 และ body ต้องเป็น shape ของเรา
    """
    expected = f"Bearer {MOCK_API_TOKEN}"
    if authorization != expected:
        raise ApiError(401, "Unauthorized", "Missing or invalid authorization token")


# ---------------------------------------------------------------- lookups
def get_employee_or_404(employee_id: str) -> dict:
    """หาพนักงานจาก id ไม่เจอโยน 404"""
    emp = EMPLOYEES.get(employee_id)
    if emp is None:
        raise ApiError(404, "Not Found", f"Employee with ID '{employee_id}' not found")
    return emp


def ticket_summary(ticket_id: str, ticket: dict) -> dict:
    """subset สำหรับ list endpoint — ไม่มี description/comments/assigned_to"""
    return {
        "ticket_id": ticket_id,
        "title": ticket["title"],
        "status": ticket["status"],
        "priority": ticket["priority"],
        "created_at": ticket["created_at"],
        "updated_at": ticket["updated_at"],
    }


def ticket_detail(ticket_id: str, ticket: dict) -> dict:
    """object เต็มสำหรับ GET /tickets/{id}"""
    creator_id = ticket["created_by"]
    creator = EMPLOYEES.get(creator_id, {})
    return {
        "ticket_id": ticket_id,
        "title": ticket["title"],
        "description": ticket["description"],
        "status": ticket["status"],
        "priority": ticket["priority"],
        "category": ticket["category"],
        "created_by": {
            "employee_id": creator_id,
            "name": creator.get("name", "Unknown"),
        },
        "assigned_to": ticket["assigned_to"],
        "created_at": ticket["created_at"],
        "updated_at": ticket["updated_at"],
        "estimated_resolution": ticket["estimated_resolution"],
        "comments": ticket["comments"],
        "resolution": ticket["resolution"],
    }


# ---------------------------------------------------------------- routes
@app.get("/health")
def health() -> dict[str, str]:
    """อยู่นอก /api และไม่ต้องใช้ token — compose healthcheck ต้องเรียกได้"""
    return {"status": "ok"}


api = APIRouter(prefix="/api", dependencies=[Depends(require_token)])


@api.get("/employees/{employee_id}/leave-balance")
def leave_balance(employee_id: str) -> dict:
    """วันลาคงเหลือ + ใบลาที่กำลังจะถึงของพนักงานคนหนึ่ง"""
    emp = get_employee_or_404(employee_id)
    return {
        "employee_id": employee_id,
        "employee_name": emp["name"],
        "department": emp["department"],
        "position": emp["position"],
        "years_of_service": emp["years_of_service"],
        "leave_balance": build_leave_balance(employee_id, emp),
        "upcoming_leaves": UPCOMING_LEAVES.get(employee_id, []),
        "last_updated": DATA_AS_OF,
    }


@api.get("/employees/{employee_id}/tickets")
def employee_tickets(employee_id: str) -> dict:
    """ticket ทั้งหมดที่พนักงานคนนี้เป็นคนแจ้ง — คืนข้อมูลย่อ"""
    get_employee_or_404(employee_id)  # ต้อง 404 ถ้าไม่มีคนนี้ ก่อนจะ filter
    tickets = [
        ticket_summary(tid, t)
        for tid, t in TICKETS.items()
        if t["created_by"] == employee_id
    ]
    return {"employee_id": employee_id, "tickets": tickets, "total": len(tickets)}



@api.get("/tickets/{ticket_id}")
def ticket(ticket_id: str) -> dict:
    """รายละเอียดเต็มของ ticket หนึ่งใบ"""
    t = TICKETS.get(ticket_id)
    if t is None:
        raise ApiError(404, "Not Found", f"Ticket with ID '{ticket_id}' not found")
    return ticket_detail(ticket_id, t)


app.include_router(api)