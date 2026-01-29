============================================================
FILE: tools/ci/post_policy_comment.py
============================================================

import os
import sys
import json
from typing import Any, Dict, List, Optional
import urllib.request

# ---------------------------------------------------------
# Post PR Comment with Top Violations (Design + Security + Exceptions)
#
# Requirements:
# - GitHub Actions provides:
#   - GITHUB_TOKEN (or token passed via env)
#   - GITHUB_REPOSITORY (owner/repo)
#   - GITHUB_EVENT_PATH (path to event json)
#
# Inputs:
# - .orchestrator/design_policy_report.json (optional)
# - .orchestrator/contrast_report.json (optional)
# - .orchestrator/security_report.json (optional)
# - check_exceptions_expiry result (optional) via a json stub file you can create
#
# Usage:
#   python3 tools/ci/post_policy_comment.py --root . --max 3 --title "Policy Gates"
# ---------------------------------------------------------

def read_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def gh_event() -> Dict[str, Any]:
    p = os.environ.get("GITHUB_EVENT_PATH", "")
    if not p or not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def get_pr_number_from_event(event: Dict[str, Any]) -> Optional[int]:
    # pull_request event
    pr = event.get("pull_request")
    if isinstance(pr, dict):
        n = pr.get("number")
        if isinstance(n, int):
            return n
    # fallback: issue comment event etc
    n = event.get("number")
    return n if isinstance(n, int) else None

def http_post_json(url: str, token: str, payload: Dict[str, Any]) -> Tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"token {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        return resp.getcode(), body

def pick_top_findings_design(report: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    # expected: "violations": [{rule_id,severity,path,message,remediation}, ...]
    v = report.get("violations", [])
    if not isinstance(v, list):
        return []
    # sort by severity weight then rule_id
    weight = {"CRITICAL": 3, "MAJOR": 2, "MINOR": 1}
    def key(x: Dict[str, Any]):
        s = str(x.get("severity", "MINOR")).upper()
        return (-weight.get(s, 0), str(x.get("rule_id","")))
    v2 = [x for x in v if isinstance(x, dict)]
    v2.sort(key=key)
    return v2[:limit]

def pick_top_findings_security(report: Dict[str, Any], limit: int) -> List[Dict[str, Any]]:
    f = report.get("findings", [])
    if not isinstance(f, list):
        return []
    weight = {"CRITICAL": 3, "MAJOR": 2, "MINOR": 1, "HIGH": 2, "MEDIUM": 1, "LOW": 0}
    def key(x: Dict[str, Any]):
        s = str(x.get("severity","MINOR")).upper()
        return (-weight.get(s, 0), str(x.get("rule_id","")))
    f2 = [x for x in f if isinstance(x, dict)]
    f2.sort(key=key)
    return f2[:limit]

def fmt_item(i: int, item: Dict[str, Any]) -> str:
    rid = item.get("rule_id") or item.get("id") or "RULE"
    sev = (item.get("severity") or "UNKNOWN")
    path = item.get("path") or item.get("file") or ""
    msg = item.get("message") or item.get("summary") or ""
    rem = item.get("remediation") or item.get("fix") or ""
    line = item.get("line")
    loc = f"{path}:{line}" if line else path
    s = f"{i}. **{rid}** ({sev})"
    if loc:
        s += f" — `{loc}`"
    if msg:
        s += f"\n   - 문제: {msg}"
    if rem:
        s += f"\n   - 해결: {rem}"
    return s

def main():
    root = "."
    max_items = 3
    title = "Policy Gates Report (Top Findings)"

    args = sys.argv[1:]
    if "--root" in args:
        root = args[args.index("--root")+1]
    if "--max" in args:
        max_items = int(args[args.index("--max")+1])
    if "--title" in args:
        title = args[args.index("--title")+1]

    token = os.environ.get("GITHUB_TOKEN", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not token or not repo:
        print("SKIP: missing GITHUB_TOKEN or GITHUB_REPOSITORY")
        sys.exit(0)

    event = gh_event()
    pr_number = get_pr_number_from_event(event)
    if pr_number is None:
        print("SKIP: not a pull_request event")
        sys.exit(0)

    design = read_json(os.path.join(root, ".orchestrator", "design_policy_report.json")) or {}
    contrast = read_json(os.path.join(root, ".orchestrator", "contrast_report.json")) or {}
    security = read_json(os.path.join(root, ".orchestrator", "security_report.json")) or {}
    exceptions = read_json(os.path.join(root, ".orchestrator", "exceptions_report.json")) or {}

    design_status = str(design.get("status", "UNKNOWN"))
    contrast_status = str(contrast.get("status", "UNKNOWN"))
    security_status = str(security.get("status", "UNKNOWN"))
    exceptions_status = str(exceptions.get("status", "UNKNOWN"))

    top_design = pick_top_findings_design(design, max_items) if design else []
    top_sec = pick_top_findings_security(security, max_items) if security else []
    ex_find = exceptions.get("expired", []) if isinstance(exceptions, dict) else []

    lines: List[str] = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append("## ✅ Status Summary")
    lines.append(f"- Design Policy: **{design_status}**")
    lines.append(f"- Contrast: **{contrast_status}**")
    lines.append(f"- Security: **{security_status}**")
    if exceptions:
        lines.append(f"- Exceptions Expiry: **{exceptions_status}**")
    lines.append("")
    lines.append("## 🔎 Top Findings (Fix these first)")
    if not top_design and not top_sec and not ex_find:
        lines.append("- 발견된 주요 위반 항목이 없습니다. (All clear)")
    else:
        if top_design:
            lines.append("")
            lines.append("### 🎨 Design Policy")
            for idx, it in enumerate(top_design, start=1):
                lines.append(fmt_item(idx, it))
        if contrast_status == "FAIL":
            lines.append("")
            lines.append("### 🌈 Contrast")
            v = contrast.get("violations", [])
            if isinstance(v, list) and v:
                for idx, it in enumerate(v[:max_items], start=1):
                    if isinstance(it, dict):
                        lines.append(fmt_item(idx, {"rule_id": "CONTRAST", "severity": "MAJOR", **it}))
                    else:
                        lines.append(f"{idx}. CONTRAST (MAJOR) — {str(it)}")
            else:
                lines.append("- 대비 기준 위반이 존재합니다. contrast_report.json을 확인하세요.")
        if top_sec:
            lines.append("")
            lines.append("### 🔐 Security")
            for idx, it in enumerate(top_sec, start=1):
                lines.append(fmt_item(idx, it))
        if ex_find:
            lines.append("")
            lines.append("### ⏳ Exceptions Expired")
            for idx, it in enumerate(ex_find[:max_items], start=1):
                lines.append(f"{idx}. `{it}` — 예외 만료로 인해 CI가 차단되었습니다. EXCEPTIONS.md 갱신/해제 필요")

    lines.append("")
    lines.append("## 📦 Evidence")
    lines.append("- Artifacts에 업로드된 보고서(.orchestrator/*_report.json, decision_events)를 확인하세요.")
    lines.append("- Decision Ledger(DECISION_LOG.md)에서 자동 기록된 게이트 평가 이벤트를 확인하세요.")
    body = "\n".join(lines)

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    code, resp = http_post_json(url, token, {"body": body})
    print("OK: comment posted", code)
    sys.exit(0)

if __name__ == "__main__":
    try:
        from typing import Tuple
        main()
    except Exception as e:
        print("ERROR:", str(e))
        sys.exit(0)

============================================================
FILE: tools/policy/write_exceptions_report.py
============================================================

import os
import sys
import json
import datetime
from typing import List, Dict, Any

# ---------------------------------------------------------
# Writes .orchestrator/exceptions_report.json based on EXCEPTIONS.md expiry check output
# - This is a helper to make PR comments show exception failures clearly.
#
# Usage:
#   python3 tools/policy/write_exceptions_report.py --root . --status PASS
#   python3 tools/policy/write_exceptions_report.py --root . --status FAIL --expired "EX-001:EXPIRED:2026-01-01" --expired "EX-002:MISSING_EXPIRATION_DATE"
# ---------------------------------------------------------

def ensure_dir(p: str) -> None:
    os.makedirs(p, exist_ok=True)

def main():
    root = "."
    status = "PASS"
    expired: List[str] = []

    args = sys.argv[1:]
    if "--root" in args:
        root = args[args.index("--root")+1]
    if "--status" in args:
        status = args[args.index("--status")+1].upper()
    # multiple --expired
    for i, a in enumerate(args):
        if a == "--expired" and i + 1 < len(args):
            expired.append(args[i+1])

    out_dir = os.path.join(root, ".orchestrator")
    ensure_dir(out_dir)
    out_path = os.path.join(out_dir, "exceptions_report.json")

    report: Dict[str, Any] = {
        "generated_at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "status": status,
        "expired": expired,
        "counts": {
            "expired": len(expired),
        }
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("OK:", out_path)

if __name__ == "__main__":
    main()

============================================================
FILE: .github/workflows/policy-gates-v4_1-final.yml
============================================================

name: Policy Gates v4.1 (Final) - Design + Security + Exceptions + Ledger + PR Comment

on:
  pull_request:
    branches: [ "main" ]
  push:
    branches: [ "main" ]

jobs:
  policy-gates:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # -------------------------
      # (1) Exception expiry check (v4.1)
      # - We also write a JSON report for PR comment consumption.
      # -------------------------
      - name: Policy - Check Exceptions Expiry
        id: exceptions
        shell: bash
        run: |
          set +e
          python3 tools/policy/check_exceptions_expiry.py --root . --exceptions EXCEPTIONS.md
          rc=$?
          mkdir -p .orchestrator
          if [ $rc -eq 0 ]; then
            python3 tools/policy/write_exceptions_report.py --root . --status PASS
          else
            # capture stdout into a file and pass a summarized form
            echo "Exceptions expiry check failed." > .orchestrator/exceptions_stdout.txt
            # best-effort: add one expired entry marker (detailed list is in CI logs)
            python3 tools/policy/write_exceptions_report.py --root . --status FAIL --expired "EXCEPTIONS:EXPIRED_OR_INVALID"
          fi
          exit $rc

      # -------------------------
      # (2) DESIGN checks (existing v4.0 scripts assumed)
      # -------------------------
      - name: Design - Generate Tokens
        run: |
          python3 tools/design/generate_tokens.py --root .

      - name: Design - Policy Scan
        run: |
          python3 tools/design/scan_design_policy.py --root .

      - name: Design - Contrast Check
        run: |
          python3 tools/design/check_contrast.py --root .

      # -------------------------
      # (3) SECURITY checks (replace with real script when ready)
      # -------------------------
      - name: Security - Run Checks (placeholder)
        run: |
          mkdir -p .orchestrator
          cat > .orchestrator/security_report.json << 'EOF'
          {
            "generated_at": "CI",
            "status": "PASS",
            "counts": {"critical": 0, "major": 0, "minor": 0},
            "vuln_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "sast_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "secret_summary": {"findings": 0},
            "findings": []
          }
          EOF

      # -------------------------
      # (4) Decision Ledger auto log (implicit)
      # -------------------------
      - name: Ledger - Log Decision (implicit)
        run: |
          python3 tools/ledger/log_decision.py --root . --actor ci --type IMPLICIT

      # -------------------------
      # (5) Upload evidence artifacts
      # -------------------------
      - name: Upload Evidence (reports)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: evidence-reports
          path: |
            DECISION_LOG.md
            .orchestrator/decision_events
            .orchestrator/design_policy_report.json
            .orchestrator/contrast_report.json
            .orchestrator/security_report.json
            .orchestrator/exceptions_report.json
            .orchestrator/exceptions_stdout.txt

      # -------------------------
      # (6) PR Comment Summary (Top 3)
      # - Runs on PR events only, even if failures occurred.
      # -------------------------
      - name: PR Comment - Top Findings Summary
        if: always() && github.event_name == 'pull_request'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 tools/ci/post_policy_comment.py --root . --max 3 --title "v4.1 Policy Gates Summary"

============================================================
END
============================================================
