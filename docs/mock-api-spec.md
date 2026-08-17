# Mock API Specification — TechCorp Internal Helpdesk

> Base URL: `http://localhost:8080/api`
> 
> This is the mock API that your agent should integrate with as "Tool 2" (external API call).
> You must implement this mock server yourself (a simple Express/FastAPI server is fine).

---

## Overview

This API simulates two internal TechCorp systems:
1. **HR System** — Employee leave balance
2. **IT Ticketing System** — IT support ticket status

Your agent should call these endpoints when users ask questions that require real-time data (e.g., "How many leave days do I have left?" or "What's the status of my IT ticket?").

---

## Authentication

All requests require a header:

```
Authorization: Bearer techcorp-mock-token-2025
```

Requests without this header should return:

```json
{
  "error": "Unauthorized",
  "message": "Missing or invalid authorization token"
}
```

HTTP Status: `401`

---

## Endpoints

### 1. GET /employees/{employee_id}/leave-balance

Returns the leave balance for a specific employee.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| employee_id | string | Employee ID (format: EMP-XXXX) |

**Example Request:**

```
GET /api/employees/EMP-1234/leave-balance
Authorization: Bearer techcorp-mock-token-2025
```

**Example Response (200 OK):**

```json
{
  "employee_id": "EMP-1234",
  "employee_name": "สมชาย วงศ์สวัสดิ์",
  "department": "Engineering",
  "position": "Senior Software Engineer",
  "years_of_service": 3,
  "leave_balance": {
    "annual_leave": {
      "total_entitlement": 12,
      "used": 4,
      "remaining": 8,
      "carried_over_from_last_year": 2,
      "pending_approval": 1
    },
    "sick_leave": {
      "total_entitlement": 30,
      "used": 2,
      "remaining": 28
    },
    "personal_leave": {
      "total_entitlement": 5,
      "used": 1,
      "remaining": 4,
      "paid_remaining": 2,
      "unpaid_remaining": 2
    }
  },
  "upcoming_leaves": [
    {
      "type": "annual_leave",
      "start_date": "2025-08-15",
      "end_date": "2025-08-15",
      "status": "pending_approval",
      "approver": "วิภาดา จิตรกุล (Director)"
    }
  ],
  "last_updated": "2025-07-10T09:00:00+07:00"
}
```

**Error Response — Employee Not Found (404):**

```json
{
  "error": "Not Found",
  "message": "Employee with ID 'EMP-9999' not found"
}
```

---

### 2. GET /tickets/{ticket_id}

Returns the status and details of an IT support ticket.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| ticket_id | string | Ticket ID (format: IT-YYYY-XXXX) |

**Example Request:**

```
GET /api/tickets/IT-2025-0042
Authorization: Bearer techcorp-mock-token-2025
```

**Example Response (200 OK):**

```json
{
  "ticket_id": "IT-2025-0042",
  "title": "VPN connection drops frequently",
  "description": "VPN disconnects every 30 minutes even though the 12-hour session limit hasn't been reached.",
  "status": "in_progress",
  "priority": "medium",
  "category": "Network & VPN",
  "created_by": {
    "employee_id": "EMP-1234",
    "name": "สมชาย วงศ์สวัสดิ์"
  },
  "assigned_to": {
    "employee_id": "EMP-0501",
    "name": "ธนพล เทคนิค",
    "team": "IT Infrastructure"
  },
  "created_at": "2025-07-08T14:30:00+07:00",
  "updated_at": "2025-07-09T11:00:00+07:00",
  "estimated_resolution": "2025-07-11T18:00:00+07:00",
  "comments": [
    {
      "author": "ธนพล เทคนิค",
      "timestamp": "2025-07-09T11:00:00+07:00",
      "message": "กำลังตรวจสอบ WireGuard config ครับ น่าจะเป็นปัญหา keep-alive interval ที่ตั้งต่ำเกินไป"
    }
  ],
  "resolution": null
}
```

**Possible `status` values:**

| Status | Description |
|--------|-------------|
| `open` | Ticket created, not yet assigned |
| `assigned` | Assigned to IT staff, not started |
| `in_progress` | Being worked on |
| `waiting_on_user` | IT needs more info from reporter |
| `resolved` | Fix applied, awaiting confirmation |
| `closed` | Confirmed resolved by reporter |

**Error Response — Ticket Not Found (404):**

```json
{
  "error": "Not Found",
  "message": "Ticket with ID 'IT-2025-9999' not found"
}
```

---

### 3. GET /employees/{employee_id}/tickets

Returns all IT tickets created by a specific employee.

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| employee_id | string | Employee ID (format: EMP-XXXX) |

**Example Request:**

```
GET /api/employees/EMP-1234/tickets
Authorization: Bearer techcorp-mock-token-2025
```

**Example Response (200 OK):**

```json
{
  "employee_id": "EMP-1234",
  "tickets": [
    {
      "ticket_id": "IT-2025-0042",
      "title": "VPN connection drops frequently",
      "status": "in_progress",
      "priority": "medium",
      "created_at": "2025-07-08T14:30:00+07:00",
      "updated_at": "2025-07-09T11:00:00+07:00"
    },
    {
      "ticket_id": "IT-2025-0043",
      "title": "Request for additional monitor",
      "status": "assigned",
      "priority": "low",
      "created_at": "2025-07-08T16:00:00+07:00",
      "updated_at": "2025-07-09T09:00:00+07:00"
    },
    {
      "ticket_id": "IT-2025-0046",
      "title": "Request GitHub access for new project",
      "status": "waiting_on_user",
      "priority": "medium",
      "created_at": "2025-07-09T10:00:00+07:00",
      "updated_at": "2025-07-09T16:00:00+07:00"
    }
  ],
  "total": 3
}
```

**Response when employee has no tickets (200 OK):**

```json
{
  "employee_id": "EMP-4567",
  "tickets": [],
  "total": 0
}
```

**Error Response — Employee Not Found (404):**

```json
{
  "error": "Not Found",
  "message": "Employee with ID 'EMP-9999' not found"
}
```

---

## Mock Data to Seed

Implement your mock server with the following seed data:

### Employees

| employee_id | name | department | years_of_service | annual_leave_used | sick_leave_used | personal_leave_used | carried_over |
|-------------|------|-----------|-----------------|-------------------|-----------------|---------------------|--------------|
| EMP-1234 | สมชาย วงศ์สวัสดิ์ | Engineering | 3 | 4 | 2 | 1 | 2 |
| EMP-2345 | พรพิมล ศรีสุข | Product | 5 | 8 | 1 | 3 | 3 |
| EMP-3456 | John Smith | Engineering | 1 | 3 | 5 | 0 | 0 |
| EMP-4567 | นภาพร แก้วมณี | HR | 7 | 10 | 0 | 2 | 5 |
| EMP-5678 | ธนกร พัฒนกิจ | Finance | 2 | 2 | 3 | 1 | 0 |

**Notes for leave entitlement calculation:**
- Use the leave policy rules: Year 1 = 6 days, Year 2-3 = 10, Year 4-6 = 14, Year 7+ = 18
- `carried_over` = วันลาพักร้อนที่สะสมมาจากปีก่อน (สูงสุด 5 วันตาม policy)
- `total_entitlement` ใน response = entitlement ตามปีที่ทำงาน + carried_over
- EMP-1234: entitlement 10 + carried_over 2 = total 12, used 4 → remaining 8
- EMP-3456 (1 year): entitlement 6 + carried_over 0 = total 6, used 3 → remaining 3
- EMP-4567 (7 years): entitlement 18 + carried_over 5 = total 23, used 10 → remaining 13

### IT Tickets

| ticket_id | title | status | priority | created_by | assigned_to |
|-----------|-------|--------|----------|------------|-------------|
| IT-2025-0042 | VPN connection drops frequently | in_progress | medium | EMP-1234 | ธนพล เทคนิค |
| IT-2025-0043 | Request for additional monitor | assigned | low | EMP-1234 | สุรศักดิ์ ฮาร์ดแวร์ |
| IT-2025-0044 | Cannot access staging environment | resolved | high | EMP-3456 | ธนพล เทคนิค |
| IT-2025-0045 | Laptop keyboard not working | in_progress | high | EMP-5678 | สุรศักดิ์ ฮาร์ดแวร์ |
| IT-2025-0046 | Request GitHub access for new project | waiting_on_user | medium | EMP-1234 | ธนพล เทคนิค |

---

## Implementation Notes for Candidates

1. **You must implement this mock server yourself.** A simple server that returns hardcoded/seeded data is perfectly fine. The focus is on how your agent integrates with it, not the server's complexity.

2. **Suggested approach:**
   - Python: FastAPI or Flask with in-memory data (dict/list)
   - TypeScript: Express with a JSON file as data store

3. **The mock server should:**
   - Validate the Authorization header
   - Return appropriate HTTP status codes (200, 401, 404)
   - Return JSON responses matching the schema above

4. **Docker Compose setup:**
   Your `docker-compose.yml` should run both the agent and the mock API server. Example structure:
   ```yaml
   services:
     agent:
       build: ./agent
       ports:
         - "3000:3000"
       depends_on:
         - mock-api
     mock-api:
       build: ./mock-api
       ports:
         - "8080:8080"
   ```

---

## Sample Queries for Testing

These are example questions your agent should handle by combining RAG (knowledge base) and Tool Calling (API):

| # | User Query | Expected Behavior |
|---|-----------|-------------------|
| 1 | "ผมเหลือวันลาพักร้อนกี่วัน?" (assume EMP-1234) | Call leave-balance API → return 8 days remaining |
| 2 | "ticket IT-2025-0042 ของผมถึงไหนแล้ว?" | Call tickets API → return "in_progress", show latest comment |
| 3 | "ผมอยากลาพักร้อน 5 วัน ต้องขอใครอนุมัติ?" | RAG (leave policy: 3+ days needs Director) + Tool (check if enough balance) |
| 4 | "VPN ต่อไม่ได้ทำไงดี?" | RAG (IT security: VPN troubleshooting steps) |
| 5 | "เบิกค่าแท็กซี่ไปพบลูกค้าได้เท่าไหร่?" | RAG (reimbursement: taxi 500 baht/trip for business) |
| 6 | "พนักงานใหม่ต้องทำอะไรวันแรก?" | RAG (onboarding: Day 1 schedule) |
| 7 | "ขอ monitor เพิ่มต้องทำยังไง สถานะ request ผมเป็นไง?" | RAG (reimbursement: monitor 8,000 THB, need IT+Manager approval) + Tool (ticket IT-2025-0043 status) |
| 8 | "Gym ออฟฟิศเปิดกี่โมง?" | RAG (facilities: Mon-Fri 6:30-21:00) |
| 9 | "ผมจะเอา ChatGPT มาใช้ในงานได้มั้ย?" | RAG (IT security: AI tools policy — approved with conditions) |
| 10 | "นโยบายลาป่วยเป็นยังไง ถ้าลา 2 วันต้องมีใบรับรองแพทย์มั้ย?" | RAG (leave policy: ใบรับรองแพทย์ต้องใช้เมื่อลา 3 วันขึ้นไป → 2 วันไม่ต้อง) |
