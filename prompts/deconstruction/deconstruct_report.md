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

The deconstruction task returns JSON only. Human-readable HTML is generated later by `uv run creatives-render-report` from the validated JSON plus the evidence packet.

Required sections:

1. `cold_watch`: immediate felt reaction, curiosity, confusion/boredom, most memorable image.
2. `evidence_timeline`: observation, viewer perception, mechanism, narrative function, evidence IDs, confidence.
3. `core_mechanism`: mechanism name, why it catches attention, why it might persuade, what cannot be copied.
4. `creative_intent`: why the creative was likely made: hypothesis, audience, funnel stage, KPI, offer strategy, and confidence.
5. `distilled_core`: compact first-order strategic read for the HTML report.
6. `core_understanding`: the deeper persuasion model behind the surface execution.
7. `scores`: required creative dimensions scored `0-3`, with evidence IDs and confidence.
8. `platform_fit`: TikTok, Reels, Shorts, Meta paid, LinkedIn.
9. `drop_off_hypotheses`: framed as hypotheses, not facts.
10. `risks_and_unknowns`: missing metrics, weak evidence, copycat risk, platform uncertainty.

## Creative Intent Requirement

Before the core read, infer why this creative was likely made. This is an evidence-bound marketing hypothesis, not a performance claim.

`creative_intent` must include:

- `creative_label`: a short contextual name such as `Gruns symptom-ladder UGC ad`, not only `ad1`.
- `creative_type`: UGC, demo, founder read, testimonial, social proof, offer ad, retargeting ad, etc.
- `likely_hypothesis`: the testable advertiser hypothesis.
- `target_audience`: who the ad appears to be built for.
- `awareness_stage`: unaware, problem-aware, solution-aware, product-aware, or most-aware, with nuance if needed.
- `funnel_stage`: cold prospecting, warm consideration, retargeting, activation, upsell, renewal, or inferred equivalent.
- `likely_kpi`: the likely KPI, such as CTR, landing-page visits, signups, trial activation, first purchase, CAC, or ROAS.
- `offer_strategy`: how the ad turns attention into action.
- `marketer_job_to_be_done`: the business problem the creative is trying to solve.
- `evidence_ids`: evidence supporting the inference.
- `confidence`: low, medium, or high.
- `unknowns`: missing data that would change the intent read.

Do not imply access to media-buy, targeting, or performance data unless it is provided.

## Distilled Core Requirement

Before writing detailed analysis, produce `distilled_core`. This is the first-order strategic read that the HTML report shows by default.

Rules:

- `core_thesis` must explain the creative's central persuasion idea in one sentence.
- `mechanism_formula` must use `->` to show the causal path, for example `pain trigger -> diagnostic escalation -> product proof -> urgency`.
- Each `evidence_timeline` item should include `narrative_function` as one of `hook`, `pain`, `proof`, `cta`, or `risk`. Use the dominant role of that beat in the persuasion sequence.
- `belief_shift_summary` must describe the before/after belief change, not just summarize scenes.
- `why_it_works` must name the viewer psychology.
- `where_it_breaks` must name the main proof, trust, pacing, or audience-fit weakness.
- `submagic_transfer` must translate the mechanism to Submagic without copying competitor surface details.
- `steal`, `avoid`, and `test_next` must be action-oriented and short.
- Do not include raw evidence IDs in `distilled_core` prose. Evidence belongs in detailed fields.

## Core Understanding Contract

`core_understanding` must include:

- `human_truth`: the emotional, social, or operational truth the creative exploits.
- `belief_shift`: before, after, and bridge.
- `tension_stack`: ordered fears, desires, objections, proof needs, and urgency pressures.
- `proof_ladder`: ordered claim/proof/weakness stages with evidence IDs.
- `viewer_state_timeline`: beat-level viewer psychology with timestamp, state, trigger, and evidence IDs.
- `skeptic_read`: what a skeptical viewer may reject.
- `transfer_principle_for_submagic`: the reusable mechanism translated away from competitor surface details.
- `counterfactuals`: likely improvements or degradations if key beats changed.

## Constraints

- Do not claim the creative performed well without metrics.
- Every score needs evidence IDs and confidence.
- Separate observation from viewer perception and strategic interpretation.
- Do not invent unseen product features, results, or platform data.
- Keep Submagic ideas at the opportunity level; full scripts belong in the adaptation prompt.
- Reject "evidence theater": do not cite an evidence ID unless it actually supports the claim.
- Write observations and viewer perceptions so they can sit beside a keyframe in the HTML report. If a claim depends on a visual moment, cite the keyframe or scene evidence ID.
- Do not stop at beat summaries. Move each major insight through `observation -> viewer perception -> mechanism -> human truth -> transferable principle`.
