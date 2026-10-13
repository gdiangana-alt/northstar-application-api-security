"""Compare raw and gateway responses; save observed evidence, not exploit claims."""
import json
from pathlib import Path
from urllib.request import Request, urlopen

results = []
for path in ["/", "/rest/products/search?q=apple"]:
    observations = {}
    for mode, port in [("raw", 3000), ("gateway", 3001)]:
        req = Request(f"http://127.0.0.1:{port}{path}",
                      headers={"Origin": "https://untrusted.example"})
        with urlopen(req, timeout=20) as response:
            body = response.read()
            csp = response.headers.get("Content-Security-Policy")
            cors = response.headers.get("Access-Control-Allow-Origin")
            if response.status != 200:
                raise RuntimeError(f"{mode} {path} is not healthy")
            if path.startswith("/rest/"):
                payload = json.loads(body)
                if payload.get("status") != "success" or not isinstance(payload.get("data"), list):
                    raise RuntimeError("Product search API regression")
            elif b"<html" not in body.lower():
                raise RuntimeError("HTML response regression")
            observations[mode] = {"status": response.status, "csp": csp, "cors": cors,
                                   "body_bytes": len(body)}
    results.append({"path": path, "observed": observations})
Path("evidence").mkdir(exist_ok=True)
Path("evidence/control-validation.json").write_text(json.dumps(results, indent=2))
for result in results:
    raw = result["observed"]["raw"]
    gateway = result["observed"]["gateway"]
    if raw["csp"] or raw["cors"] != "*":
        raise RuntimeError("Baseline differs from expected finding; review evidence")
    if not gateway["csp"] or "object-src 'none'" not in gateway["csp"]:
        raise RuntimeError("Gateway CSP missing or weakened")
    if gateway["cors"] is not None:
        raise RuntimeError("Unexpected cross-origin permission at gateway")
print("PASS: raw CSP/CORS findings reproduced; gateway controls and API responses checked.")
print("Browser rendering, authenticated APIs and exploitability remain untested.")

