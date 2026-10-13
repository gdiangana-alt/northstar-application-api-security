# Remediation and retest strategy

## Remediation patterns

| Category | Preferred control | Retest proof |
|---|---|---|
| Missing browser security headers | Set explicit response headers at the application/gateway and verify on target response | Header present on the same endpoint; regression scan |
| Broken access control / BOLA | Enforce server-side object authorization on every request | Authorized request succeeds; cross-user/object request is denied |
| Injection | Parameterized queries, validated input and least-privilege data access | Malformed payload treated as data; expected behavior remains |
| Weak authentication/session control | Strong credential policy, MFA where appropriate, secure session settings and revocation | Expired/revoked session cannot access protected endpoint |
| Sensitive data exposure | TLS, response minimization, protected storage/logging and redaction | No sensitive value in approved response/log test |
| Unsafe API configuration | Explicit allowlists, authentication, rate limits and schema validation | Disallowed method/field/principal rejected |

## Retest sequence

1. Record the original report and commit.
2. Implement one targeted control in a controlled branch.
3. Run unit/integration checks for the control.
4. Re-run the identical scan scope.
5. Manually test the original endpoint with allowed and denied cases.
6. Compare old and new evidence; record residual risk.
7. Change the CI policy only after the team agrees on severity thresholds and exceptions.

## CI policy progression

- **Stage 1 - evidence:** workflow collects artifacts and does not fail on Juice Shop alerts.
- **Stage 2 - triage:** known alerts have documented status and owners.
- **Stage 3 - policy:** critical/high alerts fail a build unless an approved expiry-bound exception exists.
- **Stage 4 - production:** scans run against authorized test environments, never production by default.

This repository completes Stage 1 only when the workflow succeeds. Stages 2-4 require reviewed evidence and approved target ownership.

