import json
from pathlib import Path
from collections import defaultdict

def load_logs():
    logs = []
    for f in Path("logs").glob("run_*.json"):
        with open(f, "r", encoding="utf-8") as fh:
            logs.append(json.load(fh))
    return logs

def compute_metrics(logs):
    total = len(logs)
    if total == 0:
        print("No logs found.")
        return

    success_count = sum(1 for l in logs if l.get("status") == "success")
    escalated_count = sum(1 for l in logs if l.get("status") == "escalated")

    by_attempt = defaultdict(lambda: {"success": 0, "total": 0})
    for l in logs:
        n = l.get("attempts", 0)
        by_attempt[n]["total"] += 1
        if l.get("status") == "success":
            by_attempt[n]["success"] += 1

    print(f"Total runs: {total}")
    print(f"Success rate: {success_count/total:.0%}")
    print(f"Escalation rate: {escalated_count/total:.0%}")
    print("\nSuccess rate by attempt count:")
    for n in sorted(by_attempt):
        s = by_attempt[n]
        print(f"  {n} attempts: {s['success']}/{s['total']} ({s['success']/s['total']:.0%})")

if __name__ == "__main__":
    metrics = compute_metrics(load_logs())