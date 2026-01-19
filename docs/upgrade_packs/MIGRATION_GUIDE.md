# 📦 MIGRATION_GUIDE.md
## Universal Orchestration System v2.1 → v2.2 → v2.3 업그레이드 가이드

본 문서는 기존 v2.1 자동화 시스템을 안정적으로 v2.2, v2.3까지 단계적으로 업그레이드하기 위한 실행 중심(Migration-first) 가이드입니다.

원칙:
- 기존 구조를 깨지 않는다
- 문서 → 규칙(게이트) → 자동화(scripts) 순으로 진화시킨다
- 언제든 중간 단계에서 멈춰도 시스템은 정상 동작해야 한다

------------------------------------------------------------
0) 전체 로드맵 요약
------------------------------------------------------------

단계별 핵심:
- v2.1: Gap-driven Q&A (설계 품질 보강)
- v2.2: Decision / Plan / Impact / Snapshot (실행 통제)
- v2.3: Scripts + Policy Engine (자동 강제)

------------------------------------------------------------
PART 1) v2.1 → v2.2 Migration (문서 기반 실행 통제)
------------------------------------------------------------

1.1 새로 추가해야 할 문서 (필수)
- 아래 파일들을 PROJECT_ROOT에 생성한다.

TEXT BLOCK: Files to add
- DECISION_LOG.md
- PLAN_OUTPUT.md
- CHANGE_IMPACT_REPORT.md
- SNAPSHOT_LOG.md

주의:
- 이 단계에서는 scripts가 없어도 된다.
- 사람 + LLM + SKILL 규칙으로도 “통제된 실행”을 구현 가능하다.

1.2 spec_analyst 업데이트 체크 (v2.2 요구사항 반영)

필수 확인 사항:
- spec_analyst/SKILL.md에 “Gap-driven Q&A” 섹션이 존재하는가?
- Q&A 결과가 최소 1곳 이상에 기록되는가?
  - MASTER_PLAN.md 또는 DECISION_LOG.md의 Evidence/Defaults 섹션

권장 Phase 0 종료 조건(명시):
- Gap-driven Q&A 완료
- MASTER_PLAN.md 생성/갱신 완료
- DECISION_LOG.md에 핵심 결정(Platform/Language/Backend 등) 기록 완료

1.3 orchestrator 업데이트 체크 (v2.2-A: Plan Mode Gate)

반드시 포함되어야 하는 규칙(게이트):
- Phase 1 진입 전, PLAN_OUTPUT.md가 반드시 존재해야 한다. 없으면 Phase 1 진입 금지.
- PLAN_OUTPUT.md의 Approval.Status가 APPROVED가 아니면 Execute Mode 전환 금지.

검증 방법:
- PLAN_OUTPUT.md 없이 Phase 1을 시도하면 반드시 차단되어야 한다.
- Approval이 PENDING/REJECTED인 상태에서 Execute로 넘어가면 반드시 차단되어야 한다.

1.4 orchestrator 업데이트 체크 (v2.2-B: Change Impact + Snapshot/Rollback)

반드시 포함되어야 하는 규칙:
- docs/* 또는 MASTER_PLAN/DECISION_LOG/PLAN_OUTPUT 변경 발생 시 CHANGE_IMPACT_REPORT.md 생성 전까지 진행 금지.
- 각 Phase 종료 시 SNAPSHOT_LOG.md에 스냅샷 기록 생성.
- Audit FAIL 발생 시 마지막 PASS 스냅샷으로 롤백 후 재시도(최소 재실행 시작점은 Impact Report 기반).

검증 방법:
- PRD 문장 1줄 수정 후, Impact Report 없이 진행 시도 → 반드시 차단
- Phase 1 완료 후 Snapshot 기록 존재 확인
- Audit FAIL 발생 시 RESTORED 기록 + 롤백 사유 기록 확인

1.5 auditor 업데이트 체크 (v2.2 감사 항목)

Auditor는 최소 아래 항목을 검사해야 한다:
- Decision Ledger 정합성
  - MASTER_PLAN 핵심 필드(PLATFORM_MODE, BACKEND_REQUIRED, PRIMARY_TYPE 등)가 DECISION_LOG에 대응 entry를 갖는가?
- Plan Gate 정합성
  - PLAN_OUTPUT 존재 여부
  - Approval.Status=APPROVED 여부
- Impact 정합성
  - 변경이 있었는데 Impact Report가 없으면 FAIL
  - Impact Report의 Start From Phase와 실제 재실행 시작점이 일치하는가?
- Snapshot 정합성
  - Phase 종료 후 CREATED 기록 존재
  - FAIL 후 롤백 발생 시 RESTORED 기록 존재

FAIL 조건:
- 위 항목 중 하나라도 누락되면 FAIL

1.6 v2.2 완료 기준 (Definition of Done)

체크리스트:
- Plan 승인 없이 실행 불가(우회 불가)
- 변경 발생 시 Impact 분석 없으면 진행 불가
- Phase 종료 시 Snapshot 기록 생성됨
- Audit FAIL 시 롤백 기록 및 재시도 루프 존재
- 문서만으로 전체 실행 흐름 재현 가능

여기까지 완료되면 v2.2 완료.

------------------------------------------------------------
PART 2) v2.2 → v2.3 Migration (scripts 도입 + Policy Engine)
------------------------------------------------------------

2.1 새로 추가해야 할 파일/폴더 (필수)

PROJECT_ROOT에 아래를 추가한다:
- POLICY_RULES.md
- .orchestrator/ 디렉토리
  - state.json
  - fingerprints.json
  - plan_actions.json
  - policy_report.json
  - snapshots/ (디렉토리)

2.2 scripts 디렉토리 생성

아래 경로를 생성한다:
- .agent/skills/orchestrator/scripts/
- .agent/skills/spec_analyst/scripts/
- .agent/skills/auditor/scripts/

주의:
- v2.3에서 scripts는 “처음엔 Soft Mode(경고)”로 도입하는 것을 권장한다.

2.3 v2.3 Scripts 도입 순서 (권장)

Step 1: detect_changes
- 목적: 문서 변경 자동 감지
- 초기에는 차단하지 않고 보고/기록만 수행

Step 2: compute_impact
- 목적: 최소 재실행 Phase 계산
- CHANGE_IMPACT_REPORT.md 및 impact.json(또는 유사)을 자동 생성

Step 3: generate_plan_actions
- 목적: 실행 계획을 기계가 처리 가능한 plan_actions.json으로 생성
- LLM은 이를 바탕으로 PLAN_OUTPUT.md(설명용)를 작성

Step 4: run_policy_checks (Soft Mode)
- 목적: POLICY_RULES.md 기반 정책 위반 탐지
- 초기에는 FAIL이어도 “기록/경고” 중심

Step 5: enforce_gates (Hard Mode 전환 핵심)
- 목적: 승인/정책/영향 분석 게이트를 실제로 차단
- allowed=false면 Phase 진행 불가

Step 6: snapshot create/restore 자동화
- 목적: 스냅샷 생성/복구를 기계가 수행
- FAIL 시 자동 롤백을 현실화

2.4 Soft Mode → Hard Mode 전환 기준

Soft Mode(초기 안정화):
- scripts 결과가 FAIL이어도 “중단”이 아닌 “경고/리포트”
- 사람이 override 가능(운영자 판단)

Hard Mode(운영 안정화 후):
- policy_report.status=FAIL이면 Execute 차단
- Approval 누락이면 Execute 차단
- Snapshot 자동 복구 활성화(FAIL → restore → 재시도)

2.5 Policy Rules 도입 체크

초기 MVP 권장 규칙(최소):
- BACKEND_REQUIRED=NO → DB/ORM 금지 (CRITICAL)
- PLATFORM_MODE=WEB → 모바일 권한/센서/푸시 API 금지 (MAJOR)
- Plan 승인 없이 Execute 시도 금지 (CRITICAL)
- REPO_LAYOUT=APPS_SPLIT이면 apps/* 밖에 앱 코드 난립 금지 (MAJOR)

운영 팁:
- 처음부터 규칙을 너무 많이 넣지 말 것(오탐 증가)
- CRITICAL 3~5개로 시작 후 점진 확장

2.6 v2.3 완료 기준 (Definition of Done)

체크리스트:
- 문서 변경 자동 감지(detect_changes) 동작
- 영향 분석(compute_impact)으로 최소 재실행 시작점 산출
- plan_actions 생성(generate_plan_actions) 동작
- 정책 검사(run_policy_checks)로 위반 탐지 및 기록
- 승인/정책/영향 분석 게이트(enforce_gates) 우회 불가
- 스냅샷 생성/복구(snapshot) 자동 동작
- Hard Mode에서 위반 시 실행 전 차단 + 롤백

여기까지 완료되면 v2.3 완료.

------------------------------------------------------------
PART 3) 운영 가이드 (실전 팁)
------------------------------------------------------------

3.1 절대 지켜야 할 순서
1) 문서 계약(템플릿) 고정
2) Gate 규칙 적용(Plan/Impact/Approval)
3) scripts 도입(Soft Mode)
4) scripts 강제(Hard Mode)
5) Policy 점진 확대

3.2 흔한 실패 패턴
- scripts부터 구현해서 문서 포맷이 흔들리는 상태(파싱/정합성 붕괴)
- Policy 과다 도입으로 생산성 급락(오탐/과차단)
- 승인 없는 자동 실행 허용(사고 발생)

3.3 추천 운영 전략
- 초기엔 느슨하게(Soft Mode)
- 안정화되면 강제로(Hard Mode)
- Policy는 작은 CRITICAL부터

------------------------------------------------------------
PART 4) 최종 한 줄 요약
------------------------------------------------------------

v2.1은 “똑똑한 설계”
v2.2는 “통제된 실행”
v2.3는 “사고가 구조적으로 불가능한 자동화”

END OF MIGRATION_GUIDE.md
