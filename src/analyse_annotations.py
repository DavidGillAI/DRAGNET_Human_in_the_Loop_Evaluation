import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "exports" / "annotated_dataset.csv"
OUTPUT_FILE = PROJECT_ROOT / "exports" / "annotation_analysis.json"

SCORE_COLUMNS = {
    "evidence_grounding": "evidence_grounding.responses",
    "reasoning_consistency": "reasoning_consistency.responses",
    "uncertainty_handling": "uncertainty_handling.responses",
    "clarity": "clarity.responses",
}


def first_response(raw_value):
    responses = json.loads(raw_value)
    if not responses:
        raise ValueError("A required response is missing")
    return responses[0]


def optional_comment(raw_value):
    if not raw_value:
        return ""
    responses = json.loads(raw_value)
    return responses[0] if responses else ""


with INPUT_FILE.open(encoding="utf-8-sig", newline="") as csv_file:
    rows = list(csv.DictReader(csv_file))

if len(rows) != 16:
    raise RuntimeError(f"Expected 16 records but found {len(rows)}")

scored_records = []
criterion_scores = defaultdict(list)
topic_totals = defaultdict(list)

for row in rows:
    scores = {
        criterion: int(first_response(row[column]))
        for criterion, column in SCORE_COLUMNS.items()
    }

    total_score = sum(scores.values())

    record = {
        "example_id": row["example_id"],
        "topic": row["topic"],
        "model_classification": row["model_classification"],
        "scores": scores,
        "total_score": total_score,
        "reviewer_comment": optional_comment(
            row["reviewer_comment.responses"]
        ),
    }

    scored_records.append(record)
    topic_totals[row["topic"]].append(total_score)

    for criterion, score in scores.items():
        criterion_scores[criterion].append(score)

analysis = {
    "record_count": len(scored_records),
    "maximum_score_per_record": 8,
    "mean_scores": {
        criterion: round(mean(scores), 2)
        for criterion, scores in criterion_scores.items()
    },
    "mean_total_score": round(
        mean(record["total_score"] for record in scored_records), 2
    ),
    "perfect_score_records": sum(
        record["total_score"] == 8 for record in scored_records
    ),
    "topic_mean_totals": {
        topic: round(mean(totals), 2)
        for topic, totals in sorted(topic_totals.items())
    },
    "records_below_full_score": [
        record
        for record in scored_records
        if record["total_score"] < 8
    ],
}

with OUTPUT_FILE.open("w", encoding="utf-8") as output_file:
    json.dump(analysis, output_file, indent=2, ensure_ascii=False)

print(json.dumps(analysis, indent=2, ensure_ascii=False))
print(f"\nSaved analysis to: {OUTPUT_FILE}")