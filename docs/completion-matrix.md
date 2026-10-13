# Completion matrix

| Capability | Status | Evidence |
|---|---|---|
| Deliberately vulnerable authorized target selected | Ready | Juice Shop image pinned in workflow |
| Isolated ephemeral lab workflow | Ready | GitHub Actions configuration |
| ZAP baseline scan | Pending execution | Workflow artifact expected |
| JSON / HTML evidence | Pending execution | Workflow artifact expected |
| Finding triage | Template ready | `finding-triage.md` |
| Manual validation | Pending | Requires successful run and controlled lab review |
| Remediation | Pending | Requires selected confirmed finding |
| Retest | Pending | Requires remediation evidence |
| CI security gate | Initial evidence mode ready | `-I` enables non-blocking discovery |
| Strict severity policy | Pending | Requires reviewed thresholds/exceptions |

## Integrity note

"Ready" means the repository contains the configuration. "Pending" means no result has been observed. The project must not claim scan success, confirmed findings, remediation, retesting or production security coverage until corresponding evidence exists.

