# Argilla Dataset Configuration

## Dataset

- **Name:** `dragnet-justification-quality`
- **Workspace:** `default`
- **Records:** 16
- **Argilla URL:** `http://localhost:6900`
- **Deployment:** Local Docker deployment

The dataset uses model outputs from the final traced LangSmith experiment. Reference answers were deliberately excluded from the Argilla interface so that the human reviewer assessed each response using only the claim, supplied evidence and model output.

## Fields

Each record displays:

- `claim`: the factual proposition being assessed
- `evidence`: the evidence supplied to the model
- `model_classification`: the model’s selected label
- `model_justification`: the model’s explanation

## Metadata

Each record also contains:

- `example_id`
- `topic`
- `difficulty`

## Annotation Questions

The reviewer scores four required criteria from 0 to 2:

1. **Evidence grounding:** whether material statements are supported by the supplied evidence
2. **Reasoning consistency:** whether the reasoning logically supports the classification
3. **Uncertainty handling:** whether evidence gaps and conflicting evidence are represented accurately
4. **Clarity:** whether the explanation is concise and understandable

An optional reviewer comment records specific problems. The annotation guidelines require a comment whenever any criterion receives a score of 0.

## Score Interpretation

Each record can receive a maximum total score of 8. The four criteria are evaluated independently, so a clear response can still score poorly for reasoning or uncertainty handling.

## Deployment Note

The lab brief recommended deploying Argilla through a free Hugging Face Space. At the time of implementation, Hugging Face required a Pro subscription for the Docker Space needed by Argilla. The project therefore uses Argilla’s documented local Docker deployment instead. Named Docker volumes preserve the local data between container restarts.