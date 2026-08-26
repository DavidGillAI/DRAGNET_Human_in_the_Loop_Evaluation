import csv
import json
import os
from pathlib import Path

import argilla as rg
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = PROJECT_ROOT / "source_data" / "langsmith_v2_traced_results.csv"
GUIDELINES_FILE = PROJECT_ROOT / "annotator_guidelines.md"
DATASET_NAME = "dragnet-justification-quality"


def load_evaluation_records():
    records = []

    with SOURCE_FILE.open(newline="", encoding="utf-8-sig") as csv_file:
        for row in csv.DictReader(csv_file):
            if row["status"] != "success":
                continue

            inputs = json.loads(row["inputs"])
            model_output = json.loads(row["outputs"])
            run = json.loads(row["run"])
            metadata = run["extra"]["metadata"]

            records.append(
                {
                    "record_id": row["id"],
                    "claim": inputs["claim"],
                    "evidence": inputs["evidence"],
                    "model_classification": model_output["classification"],
                    "model_justification": model_output["justification"],
                    "example_id": metadata["ls_example_example_id"],
                    "topic": metadata["ls_example_topic"],
                    "difficulty": metadata["ls_example_difficulty"],
                }
            )

    if not records:
        raise RuntimeError("No successful LangSmith records were found")

    return records


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_url = os.getenv("ARGILLA_API_URL")
    api_key = os.getenv("ARGILLA_API_KEY")

    if not api_url or not api_key:
        raise RuntimeError("ARGILLA_API_URL or ARGILLA_API_KEY is missing from .env")

    client = rg.Argilla(api_url=api_url, api_key=api_key)
    workspace = client.workspaces("default")

    if workspace is None:
        workspace = rg.Workspace(name="default", client=client)
        workspace.create()

    if client.datasets(DATASET_NAME, workspace=workspace) is not None:
        raise RuntimeError(
            f'Dataset "{DATASET_NAME}" already exists. '
            "Refusing to create a duplicate."
        )

    evaluation_records = load_evaluation_records()
    guidelines = GUIDELINES_FILE.read_text(encoding="utf-8")

    settings = rg.Settings(
        guidelines=guidelines,
        fields=[
            rg.TextField(
                name="claim",
                title="Claim",
                use_markdown=True,
                required=True,
            ),
            rg.TextField(
                name="evidence",
                title="Supplied Evidence",
                use_markdown=True,
                required=True,
            ),
            rg.TextField(
                name="model_classification",
                title="Model Classification",
                required=True,
            ),
            rg.TextField(
                name="model_justification",
                title="Model Justification",
                use_markdown=True,
                required=True,
            ),
        ],
        questions=[
            rg.RatingQuestion(
                name="evidence_grounding",
                values=[0, 1, 2],
                title="Evidence grounding",
                description=(
                    "0 = unsupported or contradictory, "
                    "1 = partly supported, 2 = fully supported"
                ),
                required=True,
            ),
            rg.RatingQuestion(
                name="reasoning_consistency",
                values=[0, 1, 2],
                title="Reasoning consistency",
                description=(
                    "0 = inconsistent, 1 = plausible with a gap, "
                    "2 = fully coherent"
                ),
                required=True,
            ),
            rg.RatingQuestion(
                name="uncertainty_handling",
                values=[0, 1, 2],
                title="Uncertainty handling",
                description=(
                    "0 = misrepresents uncertainty, "
                    "1 = partly recognises it, 2 = handles it accurately"
                ),
                required=True,
            ),
            rg.RatingQuestion(
                name="clarity",
                values=[0, 1, 2],
                title="Clarity",
                description=(
                    "0 = unclear, 1 = understandable but flawed, "
                    "2 = clear and concise"
                ),
                required=True,
            ),
            rg.TextQuestion(
                name="reviewer_comment",
                title="Reviewer comment",
                description="Required by the guidelines when any criterion scores 0.",
                required=False,
            ),
        ],
        metadata=[
            rg.TermsMetadataProperty(
                name="topic",
                options=sorted({record["topic"] for record in evaluation_records}),
                title="Topic",
                visible_for_annotators=True,
            ),
            rg.TermsMetadataProperty(
                name="difficulty",
                options=sorted(
                    {record["difficulty"] for record in evaluation_records}
                ),
                title="Difficulty",
                visible_for_annotators=True,
            ),
            rg.TermsMetadataProperty(
                name="example_id",
                options=sorted(
                    {record["example_id"] for record in evaluation_records}
                ),
                title="Example ID",
                visible_for_annotators=True,
            ),
        ],
    )

    dataset = rg.Dataset(
        name=DATASET_NAME,
        workspace=workspace,
        settings=settings,
        client=client,
    )
    dataset.create()

    argilla_records = [
        rg.Record(
            id=record["record_id"],
            fields={
                "claim": record["claim"],
                "evidence": record["evidence"],
                "model_classification": record["model_classification"],
                "model_justification": record["model_justification"],
            },
            metadata={
                "topic": record["topic"],
                "difficulty": record["difficulty"],
                "example_id": record["example_id"],
            },
        )
        for record in evaluation_records
    ]

    dataset.records.log(argilla_records)

    print(f'Created dataset "{DATASET_NAME}".')
    print(f"Uploaded {len(argilla_records)} records.")


if __name__ == "__main__":
    main()