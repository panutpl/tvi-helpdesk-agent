"""กฎการคำนวณสิทธิ์วันลา — แปลงมาจาก knowledge-base/leave-policy.md ข้อ 1

แยกออกจาก main.py เพราะนี่คือ business logic ตัวเดียวใน mock server
ส่วน main.py เป็น HTTP layer ล้วน แยกแล้วทดสอบฟังก์ชันนี้ตรงๆ ได้
โดยไม่ต้องยิง request
"""

from .data import (
    ANNUAL_LEAVE_TIERS,
    PERSONAL_LEAVE_ENTITLEMENT,
    PERSONAL_LEAVE_PAID,
    SICK_LEAVE_ENTITLEMENT,
    UPCOMING_LEAVES,
    Employee,
)


def annual_entitlement(years_of_service: int) -> int:
    """สิทธิ์ลาพักร้อนตามอายุงาน (ยังไม่รวมวันสะสม)

    leave-policy.md 1.1: ปีที่ 1 = 6 / ปีที่ 2-3 = 10 / ปีที่ 4-6 = 14 / ปีที่ 7+ = 18
    """
    for max_year, days in ANNUAL_LEAVE_TIERS:
        if years_of_service <= max_year:
            return days
    return ANNUAL_LEAVE_TIERS[-1][1]


def count_pending_annual(employee_id: str) -> int:
    """นับใบลาพักร้อนที่รออนุมัติ — ไม่ hardcode เลข

    ถ้าเพิ่ม upcoming leave อีกใบใน data.py ตัวเลขต้องขยับเอง
    """
    return sum(
        1
        for leave in UPCOMING_LEAVES.get(employee_id, [])
        if leave["type"] == "annual_leave" and leave["status"] == "pending_approval"
    )


def build_leave_balance(employee_id: str, emp: Employee) -> dict:
    """ประกอบวันลาคงเหลือทั้ง 3 ประเภทของพนักงานหนึ่งคน

    ลากิจตัดจากโควตาที่ได้ค่าจ้าง (3 วัน) ก่อน ส่วนที่เกินจึงลงโควตาไม่ได้ค่าจ้าง (2 วัน)
    """
    annual_total = annual_entitlement(emp["years_of_service"]) + emp["carried_over"]
    personal_used = emp["personal_used"]
    paid_remaining = max(0, PERSONAL_LEAVE_PAID - personal_used)
    unpaid_used = max(0, personal_used - PERSONAL_LEAVE_PAID)
    unpaid_remaining = max(
        0, (PERSONAL_LEAVE_ENTITLEMENT - PERSONAL_LEAVE_PAID) - unpaid_used
    )

    return {
        "annual_leave": {
            "total_entitlement": annual_total,
            "used": emp["annual_used"],
            "remaining": annual_total - emp["annual_used"],
            "carried_over_from_last_year": emp["carried_over"],
            "pending_approval": count_pending_annual(employee_id),
        },
        "sick_leave": {
            "total_entitlement": SICK_LEAVE_ENTITLEMENT,
            "used": emp["sick_used"],
            "remaining": SICK_LEAVE_ENTITLEMENT - emp["sick_used"],
        },
        "personal_leave": {
            "total_entitlement": PERSONAL_LEAVE_ENTITLEMENT,
            "used": personal_used,
            "remaining": PERSONAL_LEAVE_ENTITLEMENT - personal_used,
            "paid_remaining": paid_remaining,
            "unpaid_remaining": unpaid_remaining,
        },
    }