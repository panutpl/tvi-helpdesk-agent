"""Evaluation script — ยิงคำถามจริงเข้า agent แล้วสรุปผลเป็นตาราง

    pip install -r eval/requirements.txt
    python eval/run_eval.py                          # รันทุกเคส
    python eval/run_eval.py --url http://localhost:3000
    python eval/run_eval.py --filter xling           # เฉพาะ id ที่มีคำนี้
    python eval/run_eval.py --verbose                # แสดงคำตอบเต็ม
    python eval/run_eval.py --json out.json          # บันทึกผลดิบ

รันจากนอก container ยิง REST เข้า agent
เหตุผล: ทดสอบผ่าน interface เดียวกับที่ผู้ใช้ใช้จริง ไม่ต้อง docker compose exec

ใช้ assertion แบบ keyword ไม่ใช้ LLM-as-judge เพราะผลคงที่ทุกรอบ
อธิบายได้ว่าทำไมผ่าน/ไม่ผ่าน และไม่เสียค่า API เพิ่ม
"""

import argparse
import json
import time
from pathlib import Path

import httpx
import yaml
from rich.console import Console
from rich.table import Table

CASES_FILE = Path(__file__).parent / "test_cases.yaml"
console = Console()


def check(case: dict, reply: str, tools: list[str], sources: list[dict]) -> list[str]:
    """คืนรายการเหตุผลที่ไม่ผ่าน ถ้าว่างแปลว่าผ่าน

    คืนเหตุผลไม่ใช่ True/False เพราะตอนพังต้องรู้ว่าพังเพราะอะไร
    'ค้นไม่เจอ' กับ 'ค้นเจอแต่ตอบผิด' เป็นคนละปัญหาและแก้คนละทาง
    """
    fails = []

    for word in case.get("expect_all", []):
        if word not in reply:
            fails.append(f"ไม่พบ {word!r}")

    any_of = case.get("expect_any", [])
    if any_of and not any(w in reply for w in any_of):
        fails.append(f"ไม่พบสักตัวใน {any_of}")

    for word in case.get("expect_absent", []):
        if word in reply:
            fails.append(f"ไม่ควรมี {word!r}")

    want_sources = set(case.get("expect_source", []))
    if want_sources:
        got = {s["source"] for s in sources}
        missing = want_sources - got
        if missing:
            fails.append(f"ไม่ได้ดึงจาก {sorted(missing)} (ได้ {sorted(got) or 'ไม่มี'})")

    want_tools = case.get("expect_tools")
    if want_tools is not None:
        missing = set(want_tools) - set(tools)
        if missing:
            fails.append(f"ไม่ได้เรียก {sorted(missing)} (เรียก {tools or 'ไม่มี'})")

    for tool in case.get("forbid_tools", []):
        if tool in tools:
            fails.append(f"ไม่ควรเรียก {tool}")

    return fails


def run_case(client: httpx.Client, case: dict, default_emp: str) -> dict:
    """ยิงคำถามหนึ่งข้อเข้า agent แล้วตรวจผลตามเงื่อนไขของเคสนั้น"""
    session_id = f"eval-{case['id']}"
    # ล้างประวัติก่อนทุกเคส ไม่ให้คำถามก่อนหน้าปนเข้าบริบท
    client.delete(f"/chat/{session_id}")

    started = time.perf_counter()
    try:
        res = client.post(
            "/chat",
            json={
                "employee_id": case.get("employee_id", default_emp),
                "message": case["query"],
                "session_id": session_id,
            },
        )
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        return {**case, "reply": f"[ERROR] {e}", "tools": [], "sources": [],
                "fails": [str(e)], "seconds": time.perf_counter() - started}

    fails = check(case, data["reply"], data["tools_used"], data["sources"])
    return {
        **case,
        "reply": data["reply"],
        "tools": data["tools_used"],
        "sources": data["sources"],
        "fails": fails,
        "seconds": time.perf_counter() - started,
    }


def main() -> int:
    """รันทุกเคส พิมพ์ตารางสรุป คืน exit code 1 ถ้ามีเคสพังโดยไม่คาด"""
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", default="http://localhost:3000")
    ap.add_argument("--filter", default="")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--json", dest="json_out", default="")
    args = ap.parse_args()

    spec = yaml.safe_load(CASES_FILE.read_text(encoding="utf-8"))
    default_emp = spec.get("default_employee_id", "EMP-1234")
    cases = [c for c in spec["cases"] if args.filter in c["id"]]

    console.print(f"[bold]รัน {len(cases)} เคส[/] → {args.url}\n")

    results = []
    with httpx.Client(base_url=args.url, timeout=120.0) as client:
        for i, case in enumerate(cases, 1):
            console.print(f"[dim]{i}/{len(cases)} {case['id']}…[/]", end="\r")
            results.append(run_case(client, case, default_emp))

    table = Table(show_lines=args.verbose)
    table.add_column("", width=2)
    table.add_column("id", style="cyan", no_wrap=True)
    table.add_column("query", max_width=34)
    table.add_column("actual", max_width=44)
    table.add_column("tools", max_width=22)
    table.add_column("s", justify="right", width=4)

    for r in results:
        passed = not r["fails"]
        known = r.get("known_failure", False)
        mark, style = ("✓", "green") if passed else (("~", "yellow") if known else ("✗", "red"))

        reply = r["reply"] if args.verbose else r["reply"][:120].replace("\n", " ")
        if r["fails"]:
            reply += "\n[red]" + " · ".join(r["fails"]) + "[/]"

        table.add_row(
            f"[{style}]{mark}[/]", r["id"], r["query"], reply,
            ", ".join(r["tools"]) or "-",
            f"{r['seconds']:.1f}",
        )

    console.print(table)

    passed = [r for r in results if not r["fails"]]
    known_fail = [r for r in results if r["fails"] and r.get("known_failure")]
    real_fail = [r for r in results if r["fails"] and not r.get("known_failure")]
    normal_total = len([c for c in cases if not c.get("known_failure")])

    console.print(
        f"\n[bold]ผ่าน {len(passed)}/{len(cases)}[/]"
        f" · เคสปกติ {len(passed)}/{normal_total}"
        f" · [yellow]known failure {len(known_fail)}[/]"
        f" · [red]พังจริง {len(real_fail)}[/]"
        f" · รวม {sum(r['seconds'] for r in results):.0f}s"
    )

    if real_fail:
        console.print("\n[red bold]เคสที่พังโดยไม่คาดคิด:[/]")
        for r in real_fail:
            console.print(f"  [red]{r['id']}[/] — {' · '.join(r['fails'])}")

    if args.json_out:
        Path(args.json_out).write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        console.print(f"\nบันทึกผลดิบที่ {args.json_out}")

    return 1 if real_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())