# Deconstruct Report Prompt

## Input

- Evidence packet.
- Short-form creative rubric.
- Platform fit rubric.
- Creative deconstruction best practices research.

## Task

Produce a complete competitor creative deconstruction for one video.

## Required Output

Return a report compatible with `schemas/deconstruct_report.schema.json`.

Required sections:

1. `cold_watch`: immediate felt reaction, curiosity, confusion/boredom, most memorable image.
2. `evidence_timeline`: observation, viewer perception, mechanism, evidence IDs, confidence.
3. `core_mechanism`: mechanism name, why it catches attention, why it might persuade, what cannot be copied.
4. `scores`: required creative dimensions scored `0-3`, with evidence IDs and confidence.
5. `platform_fit`: TikTok, Reels, Shorts, Meta paid, LinkedIn.
6. `drop_off_hypotheses`: framed as hypotheses, not facts.
7. `risks_and_unknowns`: missing metrics, weak evidence, copycat risk, platform uncertainty.

## Constraints

- Do not claim the creative performed well without metrics.
- Every score needs evidence IDs and confidence.
- Separate observation from viewer perception and strategic interpretation.
- Do not invent unseen product features, results, or platform data.
- Keep Submagic ideas at the opportunity level; full scripts belong in the adaptation prompt.
- Reject "evidence theater": do not cite an evidence ID unless it actually supports the claim.
