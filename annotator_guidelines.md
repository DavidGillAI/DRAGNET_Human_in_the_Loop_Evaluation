# DRAGNET Human Evaluation Guidelines

## Task Overview

Evaluate the quality of an LLM's justification for a claim classification. Each record contains a claim, supplied evidence, the model's classification and its justification.

Use only the supplied evidence. Do not use outside knowledge or attempt to discover the hidden reference answer.

## Scoring

Score each criterion from 0 to 2. The maximum total is 8.

### Evidence Grounding

- **0:** The justification contradicts the evidence or relies mainly on unsupported statements.
- **1:** It is partly supported but contains an unsupported assumption, exaggeration or material omission.
- **2:** Every material statement is supported by the supplied evidence.

### Reasoning Consistency

- **0:** The reasoning is contradictory or does not logically support the model's classification.
- **1:** The main reasoning is plausible but contains a logical gap or minor inconsistency.
- **2:** The reasoning is coherent and fully supports the classification.

### Uncertainty Handling

- **0:** The justification ignores or misrepresents material uncertainty, such as treating missing evidence as disproof or confusing conflicting evidence with an evidence gap.
- **1:** It recognises uncertainty but oversimplifies it or misses an important caveat.
- **2:** It accurately explains the relevant uncertainty and avoids unjustified certainty.

### Clarity

- **0:** The justification is confusing, incoherent or does not clearly explain its reasoning.
- **1:** It is understandable but vague, awkward or unnecessarily wordy.
- **2:** It is clear, concise and easy to follow.

## Edge Cases

- A correct classification does not automatically deserve high justification scores.
- A clear explanation may score highly for clarity while scoring poorly for evidence grounding.
- Missing evidence is not automatically evidence that a claim is false.
- Conflicting credible evidence may support `disputed`; incomplete evidence may support `unknowable`.
- Future outcomes should not be presented as certain when the evidence cannot establish them.
- If any criterion receives 0, briefly explain the problem in the reviewer comment.
- When no material uncertainty exists, score uncertainty handling as 2 if the justification expresses only the confidence warranted by the evidence.

## Quality Check

Before submitting, confirm that all four scores assess separate criteria and that your judgement uses only the evidence displayed in the record.