"""Seed data ตาม mock-api-spec.md

เก็บเป็น raw table ตามที่ spec ให้มา ไม่ pre-compute
การคำนวณ entitlement ทำใน main.py เพื่อให้เห็นว่ากฎมาจาก leave-policy.md
"""

from typing import TypedDict


class Employee(TypedDict):
    name: str
    department: str
    position: str
    years_of_service: int
    annual_used: int
    sick_used: int
    personal_used: int
    carried_over: int


DATA_AS_OF = "2025-07-10T09:00:00+07:00"

EMPLOYEES: dict[str, Employee] = {
    "EMP-1234": {
        "name": "สมชาย วงศ์สวัสดิ์",
        "department": "Engineering",
        "position": "Senior Software Engineer",
        "years_of_service": 3,
        "annual_used": 4,
        "sick_used": 2,
        "personal_used": 1,
        "carried_over": 2,
    },
    "EMP-2345": {
        "name": "พรพิมล ศรีสุข",
        "department": "Product",
        "position": "Product Manager",
        "years_of_service": 5,
        "annual_used": 8,
        "sick_used": 1,
        "personal_used": 3,
        "carried_over": 3,
    },
    "EMP-3456": {
        "name": "John Smith",
        "department": "Engineering",
        "position": "Software Engineer",
        "years_of_service": 1,
        "annual_used": 3,
        "sick_used": 5,
        "personal_used": 0,
        "carried_over": 0,
    },
    "EMP-4567": {
        "name": "นภาพร แก้วมณี",
        "department": "HR",
        "position": "HR Manager",
        "years_of_service": 7,
        "annual_used": 10,
        "sick_used": 0,
        "personal_used": 2,
        "carried_over": 5,
    },
    "EMP-5678": {
        "name": "ธนกร พัฒนกิจ",
        "department": "Finance",
        "position": "Financial Analyst",
        "years_of_service": 2,
        "annual_used": 2,
        "sick_used": 3,
        "personal_used": 1,
        "carried_over": 0,
    },
}


# กฎจาก leave-policy.md ข้อ 1.1 — (ปีสูงสุดที่เข้าเงื่อนไข, สิทธิ์วัน)
ANNUAL_LEAVE_TIERS: list[tuple[int, int]] = [(1, 6), (3, 10), (6, 14), (999, 18)]

SICK_LEAVE_ENTITLEMENT = 30
PERSONAL_LEAVE_ENTITLEMENT = 5
PERSONAL_LEAVE_PAID = 3


UPCOMING_LEAVES: dict[str, list[dict]] = {
    "EMP-1234": [
        {
            "type": "annual_leave",
            "start_date": "2025-08-15",
            "end_date": "2025-08-15",
            "status": "pending_approval",
            "approver": "วิภาดา จิตรกุล (Director)",
        }
    ],
    "EMP-5678": [
            {
                "type": "annual_leave",
                "start_date": "2025-08-20",
                "end_date": "2025-08-21",
                "status": "pending_approval",
                "approver": "วิภาดา จิตรกุล (Director)",
            }
        ],
}


TICKETS: dict[str, dict] = {
    "IT-2025-0042": {
        "title": "VPN connection drops frequently",
        "description": (
            "VPN disconnects every 30 minutes even though the 12-hour "
            "session limit hasn't been reached."
        ),
        "status": "in_progress",
        "priority": "medium",
        "category": "Network & VPN",
        "created_by": "EMP-1234",
        "assigned_to": {
            "employee_id": "EMP-0501",
            "name": "ธนพล เทคนิค",
            "team": "IT Infrastructure",
        },
        "created_at": "2025-07-08T14:30:00+07:00",
        "updated_at": "2025-07-09T11:00:00+07:00",
        "estimated_resolution": "2025-07-11T18:00:00+07:00",
        "comments": [
            {
                "author": "ธนพล เทคนิค",
                "timestamp": "2025-07-09T11:00:00+07:00",
                "message": (
                    "กำลังตรวจสอบ WireGuard config ครับ "
                    "น่าจะเป็นปัญหา keep-alive interval ที่ตั้งต่ำเกินไป"
                ),
            }
        ],
        "resolution": None,
    },
    "IT-2025-0043": {
        "title": "Request for additional monitor",
        "description": "Requesting a second 27-inch monitor for the workstation.",
        "status": "assigned",
        "priority": "low",
        "category": "Hardware",
        "created_by": "EMP-1234",
        "assigned_to": {
            "employee_id": "EMP-0502",
            "name": "สุรศักดิ์ ฮาร์ดแวร์",
            "team": "IT Support",
        },
        "created_at": "2025-07-08T16:00:00+07:00",
        "updated_at": "2025-07-09T09:00:00+07:00",
        "estimated_resolution": None,
        "comments": [],
        "resolution": None,
    },
    "IT-2025-0044": {
        "title": "Cannot access staging environment",
        "description": "Getting 403 when accessing staging via VPN.",
        "status": "resolved",
        "priority": "high",
        "category": "Access & Permissions",
        "created_by": "EMP-3456",
        "assigned_to": {
            "employee_id": "EMP-0501",
            "name": "ธนพล เทคนิค",
            "team": "IT Infrastructure",
        },
        "created_at": "2025-07-07T10:00:00+07:00",
        "updated_at": "2025-07-08T15:00:00+07:00",
        "estimated_resolution": "2025-07-08T18:00:00+07:00",
        "comments": [],
        "resolution": "Added user to staging-access AD group.",
    },
    "IT-2025-0045": {
        "title": "Laptop keyboard not working",
        "description": "Several keys unresponsive after liquid spill.",
        "status": "in_progress",
        "priority": "high",
        "category": "Hardware",
        "created_by": "EMP-5678",
        "assigned_to": {
            "employee_id": "EMP-0502",
            "name": "สุรศักดิ์ ฮาร์ดแวร์",
            "team": "IT Support",
        },
        "created_at": "2025-07-09T08:30:00+07:00",
        "updated_at": "2025-07-09T13:00:00+07:00",
        "estimated_resolution": "2025-07-12T18:00:00+07:00",
        "comments": [],
        "resolution": None,
    },
    "IT-2025-0046": {
        "title": "Request GitHub access for new project",
        "description": "Need write access to the new payments repository.",
        "status": "waiting_on_user",
        "priority": "medium",
        "category": "Access & Permissions",
        "created_by": "EMP-1234",
        "assigned_to": {
            "employee_id": "EMP-0501",
            "name": "ธนพล เทคนิค",
            "team": "IT Infrastructure",
        },
        "created_at": "2025-07-09T10:00:00+07:00",
        "updated_at": "2025-07-09T16:00:00+07:00",
        "estimated_resolution": None,
        "comments": [],
        "resolution": None,
    },
}
