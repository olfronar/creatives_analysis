# Submagic Variant Prompt

## Input

- Deconstruction report.
- Submagic product research.
- Submagic adaptation rubric.
- Submagic capability catalog.

## Task

Generate Submagic-native creative briefs plus scripts inspired by competitor mechanisms.

## Required Output For Each Variant

Return each variant compatible with `schemas/adaptation_variant.schema.json`.

- Variant name.
- Target persona.
- Competitor mechanism being transformed: name, safe translation, what must change.
- Evidence lineage: evidence IDs that justify the source mechanism.
- Hook.
- Core promise.
- Proof scene: visual transformation and Submagic feature proof.
- Beat-by-beat script with timestamps.
- CTA.
- Platform adjustments.
- Submagic feature mapping using approved feature names only.
- Test hypothesis.
- Swappability check.
- Copycat/IP risk.

## Constraints

- Do not copy exact wording, shots, music, creator identity, or branded design.
- Do not use unsupported Submagic claims.
- Make the product proof visible or demonstrable.
- Prefer creator/agency pains: editing time, output volume, client consistency, platform variants, and publishing flow.
- Reject any idea where another AI editor can replace Submagic without changing the proof scene.
- Generate fewer, sharper variants: faithful mechanism/new expression, contrarian reversal, and quiet human version before expanding volume.
