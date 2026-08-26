import csv
import json
import os
from pathlib import Path

import argilla as rg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = PROJECT_ROOT / "exports"
EXPORT_FILE = EXPORT_DIR / "annotated_dataset.csv"
DATASET_NAME = "dragnet-justification-quality"


def serialize(value):
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


load_dotenv(PROJECT_ROOT / ".env")

client = rg.Argilla(
    api_url=os.getenv("ARGILLA_API_URL"),
    api_key=os.getenv("ARGILLA_API_KEY"),
)

workspace = client.workspaces("default")
dataset = client.datasets(DATASET_NAME, workspace=workspace)

if dataset is None:
    raise RuntimeError(f'Dataset "{DATASET_NAME}" was not found')

records = dataset.records.to_list(flatten=True)

if len(records) != 16:
    raise RuntimeError(f"Expected 16 records but found {len(records)}")

fieldnames = sorted(
    {field_name for record in records for field_name in record}
)

EXPORT_DIR.mkdir(exist_ok=True)

with EXPORT_FILE.open("w", newline="", encoding="utf-8-sig") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(
        {
            field_name: serialize(record.get(field_name, ""))
            for field_name in fieldnames
        }
        for record in records
    )

print(f"Exported {len(records)} annotated records.")
print(f"Saved to: {EXPORT_FILE}")
print("Columns:")
for field_name in fieldnames:
    print(f"- {field_name}")