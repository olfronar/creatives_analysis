# Validation Judge Prompt

## Input

- Evidence packet.
- Deconstruction report or adaptation variant.
- Relevant schema.

## Task

Validate whether the output is usable.

## Checks

- Schema shape is complete.
- No required section is empty.
- Every interpretive claim has resolvable evidence IDs.
- Evidence IDs actually support the claim; reject decorative citations.
- Scores are not presented as performance facts.
- Drop-off points are labeled as hypotheses.
- Submagic feature claims are supported by product research.
- Adaptation does not directly copy competitor expression.
- Platform notes address mobile framing, captions, safe zones, sound, CTA timing, and native feel.
- Adaptation includes a proof scene, mechanism lineage, test hypothesis, and swappability check.
- Generic feature-list ideas fail unless they include a specific human tension and visible product transformation.

## Output

Return pass, fail, or warn for each check with concise notes.
