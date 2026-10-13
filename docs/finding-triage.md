# Finding triage template

## Evidence intake

Download the `zap-juice-shop-baseline` artifact from a successful GitHub Actions run. Record the run URL, ZAP version/image tag, target URL, workflow commit, report SHA-256, and timestamp in a private working note. Publish only sanitized summaries.

## Triage rules

1. Treat scanner output as a lead, not proof.
2. Confirm the affected endpoint and response context inside the isolated training lab.
3. Distinguish missing security headers/configuration from an exploitable application weakness.
4. Map a confirmed issue to the relevant OWASP Top 10 or API Security category.
5. State the impacted asset, preconditions, business effect, likelihood, severity rationale, owner and remediation.
6. Retest the exact control after remediation. A different scan run alone is not proof of a fix.
7. Do not add exploitation steps or secrets to this public repository.

## Finding record

| Field | Record |
|---|---|
| Finding ID | `NS-APP-001` |
| Scan evidence | Workflow run and sanitized report reference |
| Endpoint / API operation |  |
| Scanner alert and confidence |  |
| Manual validation status | Unvalidated / confirmed / false positive |
| OWASP mapping |  |
| Risk and rationale |  |
| Root cause |  |
| Remediation |  |
| Retest procedure and evidence |  |
| Decision | Fix / accepted exception / false positive |
| Owner and review date |  |

## Initial expected lab outcomes

Juice Shop is intentionally vulnerable, so findings are expected. Do not pre-label a specific scanner alert as confirmed before a completed run and manual validation. The purpose is to practise disciplined triage, not produce a dramatic list of unverified vulnerabilities.

