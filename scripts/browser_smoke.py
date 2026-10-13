"""Chromium compatibility and CSP enforcement checks for the isolated lab."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

root = Path("evidence")
root.mkdir(exist_ok=True)
result = {"status": "pending", "scope": "Public catalogue/API and selected CSP controls"}
with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    page.add_init_script("""
        window.cspViolations = [];
        document.addEventListener('securitypolicyviolation', e => {
            window.cspViolations.push({
                directive: e.effectiveDirective,
                blockedURI: e.blockedURI,
                disposition: e.disposition
            });
        });
    """)
    try:
        response = page.goto("http://127.0.0.1:3001/#/search", wait_until="domcontentloaded")
        assert response and response.status == 200, "Gateway navigation failed"
        csp = response.headers.get("content-security-policy", "")
        assert "img-src 'self' data:;" in csp, "Image CSP still broad"
        page.wait_for_function("""() => {
            const root = document.querySelector('[ng-version]');
            return root && document.body.innerText.includes('All Products');
        }""", timeout=45000)
        page.wait_for_function("""() => [...document.images].some(img =>
            img.src.includes('/assets/public/images/products/') &&
            img.complete && img.naturalWidth > 0
        )""", timeout=30000)
        data = page.evaluate("""async () => {
            const r = await fetch('/rest/products/search?q=apple');
            return {httpStatus: r.status, body: await r.json()};
        }""")
        assert data["httpStatus"] == 200, "Same-origin API failed in browser"
        assert data["body"].get("status") == "success", "Search API regression"
        assert len(data["body"].get("data", [])) > 0, "Search returned no data"
        before = len(page.evaluate("window.cspViolations"))
        # An inert external image tests CSP denial; no exploit or external target scan.
        page.evaluate("""() => {
            const img = document.createElement('img');
            img.src = 'https://blocked-image.example.invalid/csp-probe.png';
            document.body.appendChild(img);
        }""")
        page.wait_for_function("""n => window.cspViolations.slice(n).some(v =>
            v.directive === 'img-src' &&
            v.blockedURI.includes('blocked-image.example.invalid') &&
            v.disposition === 'enforce'
        )""", arg=before, timeout=10000)
        result.update(status="pass", title=page.title(),
                      product_search_count=len(data["body"]["data"]),
                      image_probe_blocked=True,
                      violations=page.evaluate("window.cspViolations"))
        print("PASS: catalogue renders, product image loads, API works, external image is blocked.")
    except Exception as exc:
        result.update(status="fail", error=str(exc))
        raise
    finally:
        page.screenshot(path=str(root / "browser-catalogue.png"), full_page=True)
        (root / "browser-validation.json").write_text(json.dumps(result, indent=2))
        browser.close()

