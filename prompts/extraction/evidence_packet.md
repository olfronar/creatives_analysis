# Evidence Packet Prompt

## Input

- Video manifest JSON.
- Transcript JSON or SRT when available.
- OCR JSON from sampled keyframes.
- Keyframe paths.
- Scene or audio notes when available.

## Task

Create an evidence packet for future deconstruction. Do not score the creative and do not brainstorm adaptations.

The evidence packet is the source of truth for every later claim. It must be valid against `schemas/evidence_packet.schema.json`.

## Required Sections

1. `analysis_run`: run ID, source hash, extractor name, schema version.
2. `manifest`: video metadata.
3. `timeline_evidence`: timestamped events sorted by time.
4. `artifacts`: manifest, keyframes, OCR, transcript status, scene status.
5. `reports_generated`: empty array in extraction-only mode.

## Evidence Event Contract

Every event must include:

- `evidence_id`: stable ID such as `ev_keyframe_001`.
- `timestamp`: timestamp or timestamp range.
- `source`: metadata, transcript, OCR, keyframe, scene, audio, or manual.
- `observation`: literal visible/audible fact, not interpretation.
- `confidence`: low, medium, or high.
- `artifact`: path to the supporting artifact when available.

## Validation Checklist

- Every observation has a source.
- Every observation has an evidence ID.
- No inferred score is included.
- No deconstruct or adapt report is generated.
- Missing transcript or OCR is labeled as missing evidence.
- Dense early-hook evidence should be preferred over uniform sampling when available.
