# CSP and CORS gateway control case study
Status: remediation configuration prepared; retest pending.

## Evidence baseline
Successful initial run: https://github.com/gdiangana-alt/northstar-application-api-security/actions/runs/38398962056
95 URLs crawled. The report contains multiple alert records within some plugin IDs; the ten warning-rule count is not ten distinct exploitable vulnerabilities.

- 10038: CSP header absent on observed responses; scanner Medium/High confidence.
- 10098: wildcard Access-Control-Allow-Origin observed; scanner Medium/Medium confidence.
- 10003: dependency advisory candidate in vendor.js, ng-version 20.3.12; scanner High/Medium confidence. Advisory identity, affected range and fix version still need review.
- Dangerous JS functions and timestamps require context; neither alone proves exploitation.
- Informational cache/modern-app alerts are not automatically defects.

## Risk decisions
Missing CSP is a missing browser defence, not proof of XSS. Wildcard CORS on a public unauthenticated response is not proof of sensitive-data exposure; classify the data, authentication and browser behaviour before deciding business severity.
The lab adopts same-origin-only API consumption. Cross-origin clients are unsupported by this selected policy. CORS controls browser access to responses; it is not authentication, a server-side authorization mechanism or protection from non-browser requests.

## Remediation
A local Nginx gateway inserts enforced CSP, removes upstream CORS permissions and replaces deprecated Feature-Policy with Permissions-Policy. Upstream Juice Shop remains deliberately vulnerable and reachable only on runner loopback.
CSP keeps cdnjs as an explicit script source and inline styles for compatibility. These are residual trust choices; vendoring dependencies and nonce/hash styles would narrow them. No unsafe-inline script or unsafe-eval allowance is added. Browser rendering and CSP violation checks are required before using this policy for a real application.

## Validation
The workflow scans raw and gateway targets in the same run, using the same ZAP image digest. Direct HTTP tests reproduce missing CSP/wildcard CORS on HTML and the public product-search API, then verify headers and healthy responses through the gateway. The selected gate requires plugin IDs 10038/10098 in baseline and absent after control insertion.
This demonstrates a gateway mitigation on selected responses. It does not modify/fix the Angular dependency or prove BOLA, authentication, XSS or complete application security. Application browser testing and dependency remediation remain open.

## Operational lesson
The first scan (38398586825) failed to save reports because the ZAP container user could not write the mount. Ownership was aligned to the image's UID/GID and explicit JSON/HTML existence checks added. Never equate scanner exit success with retained evidence.

## Evidence to retain after retest
Both JSON/HTML reports, control-validation.json, image-digests.txt, retest-summary.json and workflow commit/run URL. Do not claim success until this new workflow passes.

