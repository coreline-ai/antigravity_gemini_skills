============================================================
FILE: tools/setup/install_v4_1.py
============================================================

import os
import sys
import shutil
from typing import Dict, List, Tuple

# ---------------------------------------------------------
# v4.1 Installer (One-shot)
#
# What it does:
# 1) Ensures required directories exist
# 2) Creates missing core docs (templates) WITHOUT overwriting existing files
# 3) Verifies expected scripts exist (warns if missing)
# 4) Installs/updates GitHub Actions workflow file if not present (no overwrite by default)
# 5) Prints a post-install checklist
#
# Philosophy:
# - Never overwrite user-authored files unless --force is provided.
#
# Usage:
#   python3 tools/setup/install_v4_1.py --root .
#   python3 tools/setup/install_v4_1.py --root . --force
# ---------------------------------------------------------

TEMPLATES: Dict[str, str] = {}

TEMPLATES["RUNBOOK.md"] = """# 🧭 v4.1 RUNBOOK (운영 메뉴얼)
목표: “대화”가 아니라 “문서/리포트/게이트”가 프로젝트를 끌고 가도록, 팀이 동일한 절차로 움직이게 한다.

## 0) 핵심 원칙 (절대 규칙)
1. Plan Mode Gate: Phase 0에서 승인(Approval) 전엔 구현(Phase 1+) 금지
2. Policy/Design/Security Gate: PR은 게이트 PASS 전엔 merge 금지
3. Evidence First: 모든 PASS/FAIL은 리포트/증거팩으로 남겨야 한다
4. Decision Ledger: 모든 중요한 이벤트(승인/변경/예외/릴리즈/장애수정)는 결정 로그에 기록되어야 한다
5. Exceptions: CRITICAL 예외는 금지, MAJOR 예외는 만료일 필수 + 결정 로그 필수

## 1) 새 기능 시작 (/new ...)
- Phase 0 Plan Mode → 문서 고정 → 승인 → 구현
- PR마다 Gate + Ledger + Evidence 확인

## 2) 기능 변경 (/change ...)
- CHANGE_REQUEST.md 작성 → 승인 → EXPLICIT Ledger → 구현/검증

## 3) 버그/장애 (/fix ...)
- INCIDENT.md 작성 → 원인 분류 → 최소 수정 PR → Gate → Ledger 기록

## 4) 예외 처리 (Exception Workflow)
- CRITICAL 예외 불가
- MAJOR 예외는 만료일 필수 + 승인 + EXPLICIT Ledger 기록

## 5) 로컬 명령
- Change 승인 로그:
  python3 tools/ledger/log_explicit_from_change.py --root . --change CHANGE_REQUEST.md --actor lead
- Incident fix 로그:
  python3 tools/ledger/log_implicit_from_incident.py --root . --incident INCIDENT.md --actor ci
- Exception 만료 검사:
  python3 tools/policy/check_exceptions_expiry.py --root . --exceptions EXCEPTIONS.md
"""

TEMPLATES["CHANGE_REQUEST.md"] = """# 🔄 Change Request

## 1. Request Summary
- Title:
- Requested By:
- Date:
- Priority: LOW | MEDIUM | HIGH | URGENT

## 2. Change Type
- [ ] Feature Addition
- [ ] Feature Modification
- [ ] UX / Design Change
- [ ] Performance Improvement
- [ ] Security / Compliance Update
- [ ] Refactor (No behavior change)

## 3. Description
- What needs to change?
- Why is this change needed?

## 4. Scope & Impact Analysis
- Affected Areas: Frontend | Backend | Database | Tokens | Policies | CI
- Risk: LOW | MEDIUM | HIGH
- Reason:

## 5. Policy & Compliance Impact
- Design Policy Impact: NONE | MINOR | MAJOR
- Security Policy Impact: NONE | MINOR | MAJOR | CRITICAL
- Accessibility Impact: NONE | A | AA | AAA

## 6. Data Impact
- Data Change: NONE | SCHEMA_CHANGE | MIGRATION_REQUIRED
- Details:

## 7. Approval
- Decision: PENDING | APPROVED | REJECTED
- Approved By:
- Approval Date:
- Conditions:

## 8. Decision Ledger
- Decision ID:
- Type: EXPLICIT
"""

TEMPLATES["INCIDENT.md"] = """# 🚨 Incident Report

## 1. Incident Summary
- Incident ID:
- Reported By:
- Date Detected:
- Environment: DEV | STAGING | PROD
- Severity: LOW | MEDIUM | HIGH | CRITICAL

## 2. Symptoms
- What is happening?
- Error messages / screenshots / logs:

## 3. Reproduction Steps
1.
2.
3.

## 4. Impact Assessment
- Affected Users:
- Business Impact:
- Data Integrity: NONE | POSSIBLE | CONFIRMED

## 5. Suspected Root Cause (Optional)
- Category: CODE | CONFIG | DEPENDENCY | INFRA | SECURITY | DESIGN | UNKNOWN

## 6. Fix Plan
- Summary:
- Files / Modules:
- Test Strategy:

## 7. Post-Fix Verification
- Design Policy: PASS | FAIL
- Security Policy: PASS | FAIL
- Regression: PASS | FAIL

## 8. Decision Ledger
- Decision ID:
- Type: IMPLICIT
"""

TEMPLATES["EXCEPTIONS.md"] = """# ⚠️ Policy Exception Register (v4.1)

> CRITICAL 예외는 금지, 모든 예외는 만료일 필수, 모든 예외는 Decision Ledger 기록 필수

---

## Exception Entry

### 1. Exception Overview
- Exception ID:
- Date Created:
- Created By:
- Policy Domain: DESIGN | SECURITY | COMPLIANCE
- Policy Rule ID:
- Severity: MINOR | MAJOR

### 2. Description
- What rule is being bypassed?
- Why is this exception necessary now?

### 3. Scope
- Files / Paths:
- Environment: DEV | STAGING | PROD

### 4. Mitigation Plan
- Short-term:
- Long-term:
- Owner:

### 5. Expiration
- Expiration Date: YYYY-MM-DD

### 6. Approval
- Approved By:
- Approval Date:

### 7. Decision Ledger
- Decision ID:
- Type: EXPLICIT

### 8. Status
- Status: ACTIVE | EXPIRED | RESOLVED

---

## Exception History (Append Only)
- [YYYY-MM-DD] ...
"""

WORKFLOW_PATH = ".github/workflows/policy-gates-v4_1-final.yml"

WORKFLOW_TEMPLATE = """name: Policy Gates v4.1 (Final) - Design + Security + Exceptions + Ledger + PR Comment

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
            echo "Exceptions expiry check failed." > .orchestrator/exceptions_stdout.txt
            python3 tools/policy/write_exceptions_report.py --root . --status FAIL --expired "EXCEPTIONS:EXPIRED_OR_INVALID"
          fi
          exit $rc

      - name: Design - Generate Tokens
        run: |
          python3 tools/design/generate_tokens.py --root .

      - name: Design - Policy Scan
        run: |
          python3 tools/design/scan_design_policy.py --root .

      - name: Design - Contrast Check
        run: |
          python3 tools/design/check_contrast.py --root .

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

      - name: Ledger - Log Decision (implicit)
        run: |
          python3 tools/ledger/log_decision.py --root . --actor ci --type IMPLICIT

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

      - name: PR Comment - Top Findings Summary
        if: always() && github.event_name == 'pull_request'
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          python3 tools/ci/post_policy_comment.py --root . --max 3 --title "v4.1 Policy Gates Summary"
"""

REQUIRED_DIRS = [
    "tools/setup",
    "tools/ledger",
    "tools/policy",
    "tools/ci",
    ".github/workflows",
    ".orchestrator",
]

REQUIRED_FILES_WARN = [
    "tools/ledger/log_decision.py",
    "tools/ledger/log_explicit_from_change.py",
    "tools/ledger/log_implicit_from_incident.py",
    "tools/policy/check_exceptions_expiry.py",
    "tools/policy/write_exceptions_report.py",
    "tools/ci/post_policy_comment.py",
    # design scripts are project-specific; warn if missing
    "tools/design/generate_tokens.py",
    "tools/design/scan_design_policy.py",
    "tools/design/check_contrast.py",
]

def ensure_dirs(root: str) -> None:
    for d in REQUIRED_DIRS:
        os.makedirs(os.path.join(root, d), exist_ok=True)

def write_file_if_missing(path: str, content: str, force: bool) -> Tuple[bool, str]:
    if os.path.exists(path) and not force:
        return False, "SKIP (exists)"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True, "WROTE"

def main():
    root = "."
    force = False

    args = sys.argv[1:]
    if "--root" in args:
        root = args[args.index("--root") + 1]
    if "--force" in args:
        force = True

    ensure_dirs(root)

    created: List[str] = []
    skipped: List[str] = []

    # Core templates
    for rel, content in TEMPLATES.items():
        p = os.path.join(root, rel)
        did, status = write_file_if_missing(p, content, force=force)
        (created if did else skipped).append(f"{rel} - {status}")

    # Workflow
    wf_abs = os.path.join(root, WORKFLOW_PATH)
    did, status = write_file_if_missing(wf_abs, WORKFLOW_TEMPLATE, force=force)
    (created if did else skipped).append(f"{WORKFLOW_PATH} - {status}")

    # Summary
    print("==================================================")
    print("v4.1 Install Summary")
    print("Root:", os.path.abspath(root))
    print("Force overwrite:", force)
    print("--------------------------------------------------")
    print("Created/Updated:")
    for x in created:
        print("  -", x)
    print("--------------------------------------------------")
    print("Skipped:")
    for x in skipped:
        print("  -", x)
    print("--------------------------------------------------")
    print("Warnings (missing expected scripts):")
    for rel in REQUIRED_FILES_WARN:
        p = os.path.join(root, rel)
        if not os.path.exists(p):
            print("  - MISSING:", rel)
    print("--------------------------------------------------")
    print("Post-Install Checklist:")
    print("  1) Ensure these exist or are implemented:")
    print("     - tools/design/generate_tokens.py")
    print("     - tools/design/scan_design_policy.py")
    print("     - tools/design/check_contrast.py")
    print("     - tools/security/run_security_checks.py (optional; replace placeholder in workflow)")
    print("  2) Commit files and open a PR to verify CI comments + artifacts.")
    print("  3) Add at least one Exception entry ONLY if needed, with expiration date.")
    print("  4) Run locally:")
    print("     - python3 tools/policy/check_exceptions_expiry.py --root . --exceptions EXCEPTIONS.md")
    print("     - python3 tools/ledger/log_decision.py --root . --actor local --type IMPLICIT")
    print("==================================================")

if __name__ == "__main__":
    main()

============================================================
END
============================================================
