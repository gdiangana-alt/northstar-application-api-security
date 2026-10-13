# Application & API Security — Verified Results

## Scope
Self-directed OWASP Juice Shop training lab running on ephemeral GitHub Actions runners. No production application or public target was tested.

## Verified evidence
- Initial scan: run 38398962056.
- Gateway mitigation/retest: run 38401287485.
- Browser compatibility and CSP refinement: run 38406007357.
- Both raw and gateway scans covered 95 URLs in the final run.
- Direct HTTP tests reproduced missing CSP and wildcard CORS.
- Gateway responses enforced CSP and removed cross-origin permissions.
- Missing-CSP and wildcard-CORS alerts were absent from gateway scan results.
- Broad HTTPS image allowance was removed.
- Chromium confirmed catalogue rendering, product-image loading, same-origin API access and blocking of an external-image probe.
- JSON/HTML reports, browser screenshot, validation results and image digests were retained as workflow artifacts.
- CI fails if the selected response controls regress or validation fails.

Final validation run:
https://github.com/gdiangana-alt/northstar-application-api-security/actions/runs/38406007357

## Remaining risks and limitations
- Angular 20.3.12 remains flagged by dependency advisories. It has not been upgraded or retested as patched.
- Inline styles remain allowed for application compatibility. Nonce-based style handling is not implemented.
- CSP/CORS gateway controls do not fix all underlying Juice Shop vulnerabilities.
- Authenticated authorization, BOLA, full API coverage and exploitation were not tested.
- The passing gate covers selected controls, not every High-severity finding.
- Browser checks cover the public catalogue and product-search API, not every user journey.
- Artifact retention is 30 days; evidence must be exported if longer retention is required.

## Outcome
Completed a bounded scan → triage → gateway mitigation → retest → browser validation → CI regression-gate case study. Residual findings remain explicitly documented.
