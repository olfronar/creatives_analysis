# HTML Templates

`deconstruction_report.template.html` is a structural guide for the distilled report shape. The production renderer is `src/creatives_analysis/html_report.py`, which uses the same first-order / second-order hierarchy but keeps escaping, asset-path resolution, and styling in Python so reports are deterministic and safe to generate from validated JSON.

Do not paste model-authored HTML into `outputs/`. Generate reports with:

```bash
uv run creatives-render-report --deconstruct <deconstruct.json> --evidence <evidence_packet.json> --output <report.html>
```
