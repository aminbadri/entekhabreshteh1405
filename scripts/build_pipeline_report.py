from pathlib import Path
import json, csv, datetime

ROOT = Path(__file__).resolve().parents[1]
site = ROOT / "site/data"

job = json.loads((site / "jobvision_metrics.json").read_text(encoding="utf-8"))
matches = json.loads((site / "matches.json").read_text(encoding="utf-8"))
review = ROOT / "data/metadata/jobvision_review_queue.csv"

review_count = 0
if review.exists():
    with review.open(encoding="utf-8-sig", newline="") as f:
        review_count = max(0, sum(1 for _ in csv.reader(f)) - 1)

report = {
    "schema_version": "1.0",
    "source_year": 1405,
    "generated_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "jobvision": {
        "expected_pages": 263,
        "mapped_records": len(job.get("records", [])),
        "review_queue_pages": review_count,
    },
    "matching": matches.get("counts", {}),
    "policy": {
        "synthetic_values": False,
        "ambiguous_matches_are_not_promoted": True,
        "unmatched_records_are_not_promoted": True,
    },
}
(site / "pipeline_status.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
