# DRAGNET Human-in-the-Loop Evaluation

This project uses Argilla to conduct a human evaluation of claim-classification justifications produced by `gpt-4o-mini`. It extends the DRAGNET LangSmith evaluation by assessing not only whether the model selected the correct label, but whether its explanation was grounded, logically consistent, appropriately uncertain and clearly written.

## Evaluation Design

The dataset contains 16 model responses covering sport, politics, medicine and pop culture. Each record displays:

- the isolated claim
- the supplied evidence
- the model classification
- the model justification

The hidden LangSmith reference answer was excluded from the annotation interface to reduce reviewer bias.

One human reviewer scored each response from 0 to 2 on four criteria:

1. Evidence grounding
2. Reasoning consistency
3. Uncertainty handling
4. Clarity

Each response could receive a maximum total score of 8.

## Results

Fourteen of the 16 responses received the maximum score of 8. The remaining two each scored 3, producing an overall mean of 7.38 out of 8.

| Criterion | Mean score |
|---|---:|
| Evidence grounding | 1.88 / 2 |
| Reasoning consistency | 1.75 / 2 |
| Uncertainty handling | 1.75 / 2 |
| Clarity | 2.00 / 2 |

Both low-scoring responses concerned claims that could not be resolved using the supplied evidence. In each case, the model selected `false` and treated missing proof as disproof instead of selecting `unknowable`. This matched the two classification errors identified in the earlier LangSmith experiment.

The evaluation indicates that `gpt-4o-mini` generally produced clear and well-grounded explanations, but its handling of unresolved evidence gaps remains a weakness. Because the evaluation used one reviewer, the results do not establish inter-annotator agreement.

## Argilla Deployment

Argilla was deployed locally at:

```text
http://localhost:6900
```

The lab brief recommended a free Hugging Face Space. However, Hugging Face required a paid Pro subscription for the Docker Space needed by Argilla at the time of implementation. The project therefore uses Argilla’s documented local Docker deployment.

The Docker configuration uses named volumes, so data persists when the containers are stopped normally.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a `.env` file containing:

```text
ARGILLA_API_URL=http://localhost:6900
ARGILLA_API_KEY=your_argilla_api_key
ARGILLA_USERNAME=your_argilla_username
ARGILLA_PASSWORD=your_argilla_password
```

The real `.env` file is excluded from Git.

Start Argilla:

```powershell
docker compose up -d
```

Verify the connection:

```powershell
python src\verify_argilla_connection.py
```

Create the dataset and upload the records:

```powershell
python src\create_argilla_dataset.py
```

After completing the annotations in Argilla, export and analyse them:

```powershell
python src\export_annotations.py
python src\analyse_annotations.py
```

To stop Argilla without deleting its stored data:

```powershell
docker compose down
```

Do not add the `-v` option unless the Argilla volumes and their data are intended to be deleted.

## Project Files

| Path | Purpose |
|---|---|
| `annotator_guidelines.md` | Human scoring instructions and edge-case guidance |
| `dataset_config.md` | Dataset fields, metadata and annotation-question design |
| `lab_summary.md` | Concise summary of the method, findings and limitation |
| `docker-compose.yaml` | Local Argilla deployment |
| `source_data/langsmith_v2_traced_results.csv` | Model outputs imported from the LangSmith experiment |
| `exports/annotated_dataset.csv` | Exported human annotations |
| `exports/annotation_analysis.json` | Calculated scores and low-scoring records |
| `src/create_argilla_dataset.py` | Creates the workspace, dataset and 16 records |
| `src/update_argilla_guidelines.py` | Synchronises the Markdown guidelines with Argilla |
| `src/export_annotations.py` | Exports completed Argilla records to CSV |
| `src/analyse_annotations.py` | Calculates criterion and topic-level results |
| `src/verify_argilla_connection.py` | Confirms local Argilla authentication |
| `requirements.txt` | Python dependencies |

## Related Evaluation

The source responses came from the earlier [DRAGNET LangSmith Claim Evaluation](https://github.com/DavidGillAI/DRAGNET_LangSmith_Claim_Evaluation).