import os
from pathlib import Path

import argilla as rg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_NAME = "dragnet-justification-quality"

load_dotenv(PROJECT_ROOT / ".env")

client = rg.Argilla(
    api_url=os.getenv("ARGILLA_API_URL"),
    api_key=os.getenv("ARGILLA_API_KEY"),
)

workspace = client.workspaces("default")
dataset = client.datasets(DATASET_NAME, workspace=workspace)

if dataset is None:
    raise RuntimeError(f'Dataset "{DATASET_NAME}" was not found')

dataset.settings.guidelines = (
    PROJECT_ROOT / "annotator_guidelines.md"
).read_text(encoding="utf-8")

dataset.update()

print("Live Argilla guidelines updated successfully.")