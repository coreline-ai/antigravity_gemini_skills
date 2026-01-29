# MIGRATION_GUIDE_v4_0_to_v4_1.md

## 1. 개요

이 문서는 v4.0 시스템을 유지한 상태에서
v4.1 운영 자동화 레이어를 추가하는 방법을 설명한다.

중요:
- v4.1은 v4.0을 대체하지 않는다
- v4.1은 v4.0 위에 얹는 운영 레이어다
- 기존 정책, 디자인, 보안 기준은 변경하지 않는다

요약:
- v4.0 = 기준(Policy / Design / Security)
- v4.1 = 운영(Operation / Change / Incident / Exception)

---

## 2. 사전 점검 (필수는 아님, 권장)

다음 파일이 존재하면 바로 v4.1 적용 가능하다.

v4.0 기준 파일:
- DESIGN_SYSTEM.md
- POLICY_RULES.md
- SECURITY_POLICY_RULES.md
- DESIGN_TOKENS.json
- tools/ledger/log_decision.py
- .orchestrator/ 디렉토리
- .github/workflows 내 policy 관련 yml

※ 일부만 있어도 진행 가능
※ 2.x 문서는 필요 없음

---

## 3. v4.0에서 유지되는 것 (삭제 금지)

다음 파일은 그대로 둔다.

- DESIGN_SYSTEM.md
- DESIGN_TOKENS.json
- POLICY_RULES.md
- SECURITY_POLICY_RULES.md
- 기존 정책 검사 스크립트
- Decision Ledger 포맷

주의:
- 내용 수정 금지
- 경로 변경 금지
- 파일명 변경 금지

---

## 4. v4.1에서 새로 추가되는 구성요소

운영 문서:
- RUNBOOK.md
- CHANGE_REQUEST.md
- INCIDENT.md
- EXCEPTIONS.md

운영 스크립트:
- tools/setup/install_v4_1.py
- tools/ledger/log_explicit_from_change.py
- tools/ledger/log_implicit_from_incident.py
- tools/policy/check_exceptions_expiry.py
- tools/policy/write_exceptions_report.py
- tools/ci/post_policy_comment.py

CI 워크플로우:
- .github/workflows/policy-gates-v4_1-final.yml

---

## 5. 마이그레이션 절차

### Step 1. v4.1 설치 (1회)

프로젝트 루트에서 실행:

  python3 tools/setup/install_v4_1.py --root .

동작 설명:
- 없는 파일만 생성
- 기존 파일은 덮어쓰지 않음
- 누락된 필수 스크립트는 경고 출력

---

### Step 2. CI 워크플로우 정리

아래 중 하나만 선택한다.

옵션 A (권장):
- policy-gates-v4_1-final.yml 만 사용
- 기존 v4.0 workflow 삭제 또는 비활성화

옵션 B (과도기):
- v4.0 + v4.1 유지
- 단, PR 트리거 중복 금지

권장:
- 혼란 방지를 위해 옵션 A

---

## 6. 운영 방식 변화

v4.0:
- PR → 정책/보안 검사 → PASS/FAIL

v4.1:
- PR → 정책/보안/예외 검사
- PR 코멘트 자동 요약
- Decision Ledger 자동 기록
- Evidence Pack 자동 업로드
- 예외 만료 시 자동 FAIL

---

## 7. 운영 시나리오

### 7.1 새 기능

- Phase 0 문서 작성
- 승인 후 구현
- PR 생성 → CI 자동 실행

### 7.2 기능 변경

1. CHANGE_REQUEST.md 작성
2. Decision을 APPROVED로 설정
3. 선택적으로 명시적 로그 실행:

   python3 tools/ledger/log_explicit_from_change.py --root . --change CHANGE_REQUEST.md --actor lead

4. 구현 PR → CI

### 7.3 버그 수정

1. INCIDENT.md 작성
2. 수정 PR → CI
3. 선택적으로 암묵적 로그 실행:

   python3 tools/ledger/log_implicit_from_incident.py --root . --incident INCIDENT.md --actor ci

### 7.4 정책 예외

- EXCEPTIONS.md에 기록
- 만료일 필수
- 만료 시 CI 자동 FAIL

---

## 8. 롤백 방법

v4.1 롤백은 안전하다.

절차:
1. policy-gates-v4_1-final.yml 제거
2. v4.0 workflow 복구
3. v4.1 문서/스크립트는 남겨도 무방

---

## 9. 마이그레이션 완료 체크리스트

- PR에 자동 코멘트 생성됨
- evidence-reports artifact 업로드됨
- DECISION_LOG.md append-only 증가 확인
- 예외 만료 시 CI 실패 확인

---

## 10. 최종 결론

v4.1은 업그레이드가 아니라
v4.0 위에 얹는 운영 레이어다.

기존 시스템을 깨지 않고
운영 안정성과 추적성을 추가한다.
