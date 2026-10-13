"""Fail closed on missing coverage or selected control regressions."""
import json
from pathlib import Path

def alerts(name):
    report = json.loads(Path(f"evidence/{name}.json").read_text())
    sites = report.get("site", [])
    if not sites:
        raise RuntimeError(f"{name}: no scanned site")
    return [a for s in sites for a in s.get("alerts", [])]

baseline = alerts("baseline")
hardened = alerts("hardened")
required = {"10038", "10098"}
seen_before = {str(a.get("pluginid")) for a in baseline}
seen_after = {str(a.get("pluginid")) for a in hardened}
if not required.issubset(seen_before):
    raise RuntimeError("Selected baseline findings absent; investigate scan scope")
if required & seen_after:
    raise RuntimeError(f"Selected gateway controls regressed: {sorted(required & seen_after)}")
summary = {
    "selected_controls": sorted(required),
    "baseline_alert_records": len(baseline),
    "gateway_alert_records": len(hardened),
    "selected_gate_result": "pass",
    "remaining_alerts": [
        {"id": a.get("pluginid"), "name": a.get("name"), "risk": a.get("riskdesc")}
        for a in hardened
    ],
    "scope": "Selected response controls only; no global high-severity gate or auth testing."
}
Path("evidence/retest-summary.json").write_text(json.dumps(summary, indent=2))
print(json.dumps(summary, indent=2))

