# Submagic Report Brand Kit

## Status

This is an inferred report kit for internal creative-analysis HTML reports. It is not an official Submagic brand guideline. It is derived from Submagic's public product surface and should be replaced if an official brand guide becomes available.

## Product Signals To Preserve

Submagic presents itself as a fast AI video editor for short-form creators, teams, agencies, and businesses. Public product pages emphasize captions, B-roll, fonts, music, zooms, transitions, silence removal, export formats, and rapid repurposing of long-form content into shorts. The API documentation frames Submagic as a programmable way to generate AI-powered captions and short-form clips, with templates, webhooks, and export workflows.

For reports, this means the visual language should feel like a creator-operator tool, not an academic paper:

- Fast to scan.
- Built around visible proof.
- Strong hierarchy around likely campaign intent, hook, mechanism, and next action.
- Concrete enough for a creative director, strategist, and editor to discuss together.

## Visual Direction

Use a light, clean product surface with orange action accents. Submagic's current public site presents a white and warm off-white SaaS interface with black headline typography, Inter, rounded upload/product cards, orange CTA accents, and muted gray support copy. The report should feel like an internal creative-intelligence companion to that product surface, not a dark generic analytics dashboard.

Recommended tokens:

| Role | Token | Usage |
| --- | --- | --- |
| Shell | `#FFFCF7` | Warm report background |
| Paper | `#FFFFFF` | Analysis cards and readable body sections |
| Soft surface | `#F7F7F8` | Mini cards, empty states, side notes |
| Ink | `#0B0B0D` | Primary text and headlines |
| Muted | `#5F5F6D` | Timestamps, confidence labels, secondary text |
| Accent | `#FF4F01` | Primary brand accent, score bars, key emphasis |
| Accent soft | `#FFF2EA` | Evidence chips and highlighted core-read cards |
| Line | `#ECECEF` | Card borders and separators |
| Deep | `#26211F` | Phone frames and media wells only |

Typography:

- Use Inter or a system sans-serif fallback for portability.
- Keep report text compact: 15-16px body, 20px section headings, larger type only in the report hero.
- Use no negative letter spacing. Use uppercase only for tiny evidence labels.

Shape and layout:

- Use cards for individual evidence units, not for whole page sections nested inside other cards.
- Report cards should have moderate radius, roughly 12-18px.
- Pair each major timeline interpretation with a shot when a keyframe or scene image exists.
- Keep first-order sections sparse. Put full score tables, platform notes, contact sheets, raw evidence IDs, and exhaustive timelines inside collapsible details.
- Use source counts or short source labels in the visible review flow. Put evidence-ID strings inside collapsible details.

## Report Brand Application

Reports should borrow Submagic's public-site discipline rather than only its colors:

- Light warm background.
- White rounded cards.
- Black headline text.
- Orange accent for primary emphasis.
- Short confident copy.
- Sparse first screen.
- Visual proof before dense explanation.

Avoid dark neon shells, purple/lime accents, excessive card grids, and long visible evidence strings.

## Voice And Labels

Tone should be direct, practical, and evidence-bound:

- Prefer "why it catches attention" over vague "works well".
- Prefer "likely drop-off point" over "audience will leave".
- Prefer "creative signal only" over "performance".
- Avoid hype unless it is quoting the creative itself.

The report should not use generic sections like "Overview" when a sharper label exists. Preferred section labels:

- Core Read
- Core thesis
- Why this creative exists
- Creative mechanism
- Belief shift
- Submagic transfer
- What to steal
- What not to copy
- Top diagnostics
- Details

## Report Components

1. Hero
   - Contextual creative label.
   - Product context label: `Submagic creative intelligence`.
   - Core thesis only; keep metadata and metrics out of the header.

2. Why this creative exists
   - Likely hypothesis as the only larger card.
   - Audience, funnel stage, likely KPI, awareness stage, and confidence as compact facts.

3. Creative mechanism
   - Combine the selected visual arc and mechanism steps in one shot-backed section.
   - Keep annotations below the shot.
   - Color-code cards by narrative function: hook, pain, proof, CTA, risk.

4. Cold watch
   - Source data remains in JSON; do not render all cold-watch fields as equal first-order cards unless needed.

5. Core Read
   - Core thesis.
   - Belief shift.
   - Submagic transfer.

6. What to steal / what not to copy / what to test
   - Render the action implications before the full evidence.

7. Top diagnostics
   - Show only top strengths, top weaknesses, and proof gap before details.

8. Key shots
   - Keep this under a details block by default.
   - Left side: keyframe or scene image inside a 9:16 phone frame.
   - Right side: what happens, why it works, Submagic lesson.
   - If no image exists, show a clear "No shot available" state rather than hiding the absence.

9. Details
   - Key shots, creative intent evidence, contact sheet, full evidence timeline, proof ladder, score matrix, platform fit, drop-off points, and risk notes.

## Sources

- [Submagic AI video editor](https://www.submagic.co/ai-video-editor)
- [Submagic API introduction](https://docs.submagic.co/introduction)
- [Submagic AI Auto Edit help article](https://care.submagic.co/en/article/how-to-use-ai-auto-edit-in-submagic-gaxw7t/)
- [Submagic step-by-step guide](https://care.submagic.co/en/article/how-to-use-submagic-step-by-step-guide-pafx7o/)
