# 🗺️ Universal Orchestration System v2.2 – Roadmap

본 문서는 v2.1까지 완성된 Universal Orchestration System을  
**실제 장기 운용 / 팀 단위 사용 / 재현 가능 자동화** 수준으로 끌어올리기 위한  
**v2.2 단계적 업그레이드 로드맵**입니다.

---

## 0) v2.2 목표 요약

v2.2의 핵심 목표는 다음 한 문장으로 요약됩니다.

> “자동으로 돌아간다”에서  
> **“왜 그렇게 결정됐는지 설명 가능하고, 실패해도 안전하며, 다시 실행 가능한 자동화”**로 진화

---

## 1) v2.2 핵심 설계 원칙

1. **설명 가능성 (Explainability)**
   - 모든 중요한 결정은 기록된다.
2. **사전 검증 (Preflight)**
   - 실행 전에 무엇을 할지 예측 가능해야 한다.
3. **부분 재실행 가능성 (Partial Re-run)**
   - 실패 시 전체 재시작을 강요하지 않는다.
4. **정책 기반 품질 보장**
   - 규칙 위반은 즉시 차단된다.
5. **기존 에이전트 확장**
   - 새로운 에이전트는 추가하지 않는다.

---

## 2) v2.2 구성 요소 맵

v2.2는 아래 8개 컴포넌트로 구성됩니다.

| ID | Component | 담당 에이전트 |
|---|---|---|
| C1 | Decision Ledger | spec_analyst |
| C2 | Plan / Dry-run Mode | orchestrator |
| C3 | Change Impact Analysis | orchestrator |
| C4 | Task Dependency DAG | orchestrator |
| C5 | Auto-Rollback Snapshot | orchestrator |
| C6 | Policy Rule Engine | auditor |
| C7 | LLM Call Budgeting | spec_analyst |
| C8 | Blueprint / Recipe System | spec_analyst |

---

## 3) Phase-based Roadmap

### Phase 2.2-A (Foundational Reliability)

**목표:**  
“왜 이 결정을 했는지”를 언제든지 재현 가능하게 만든다.

#### 포함 기능
- C1. Decision Ledger
- C2. Plan / Dry-run Mode

#### 산출물
- `DECISION_LOG.md`
- `PLAN_OUTPUT.md`

#### 성공 기준
- MASTER_PLAN.md의 모든 핵심 필드에 결정 근거가 연결됨
- Plan Mode 실행 결과가 실제 실행과 90% 이상 일치

---

### Phase 2.2-B (Safe Execution)

**목표:**  
변경과 실패가 발생해도 자동화가 무너지지 않게 만든다.

#### 포함 기능
- C3. Change Impact Analysis
- C5. Auto-Rollback Snapshot

#### 산출물
- `CHANGE_IMPACT_REPORT.md`
- `SNAPSHOT_LOG.md`

#### 성공 기준
- PRD/Design/TRD 변경 시 영향 범위 자동 계산
- Audit FAIL 시 마지막 정상 스냅샷으로 복구 가능

---

### Phase 2.2-C (Deterministic Automation)

**목표:**  
자동화 실행 경로를 명확한 그래프로 고정한다.

#### 포함 기능
- C4. Task Dependency DAG

#### 산출물
- `TASK_GRAPH.md`

#### 성공 기준
- Phase 0~3의 모든 단계가 DAG로 표현됨
- 특정 노드 실패 시 관련 노드만 재실행 가능

---

### Phase 2.2-D (Governance & Cost Control)

**목표:**  
품질과 비용을 동시에 제어한다.

#### 포함 기능
- C6. Policy Rule Engine
- C7. LLM Call Budgeting

#### 산출물
- `POLICY_RULES.md`
- `LLM_USAGE_LOG.md`

#### 성공 기준
- 정책 위반 시 Dev 단계 진입 차단
- Phase별 LLM 호출 상한 준수

---

### Phase 2.2-E (Acceleration & Reuse)

**목표:**  
반복 프로젝트의 초기 비용을 최소화한다.

#### 포함 기능
- C8. Blueprint / Recipe System

#### 산출물
- `blueprints/`
  - web_admin_dashboard.md
  - mobile_only_app.md
  - hybrid_saas.md

#### 성공 기준
- Blueprint 적용 시 Gap-driven Q&A 질문 수 50% 이상 감소
- MASTER_PLAN 생성 시간 단축

---

## 4) 컴포넌트별 상세 설명

### C1. Decision Ledger
- 모든 주요 결정 기록
- 사람이 읽을 수 있고 기계가 파싱 가능

~~~markdown
## Decision: BACKEND_REQUIRED
- Options: YES / NO
- Evidence:
  - PRD: 로그인, 팀 초대
- Final: YES
- Decided By: spec_analyst
~~~

---

### C2. Plan / Dry-run Mode
- 실제 파일 생성 전 실행 계획 출력
- 사용자 승인 포인트 제공 가능

---

### C3. Change Impact Analysis
- 변경된 문서 → 영향 받는 Phase 자동 산출
- 불필요한 전체 재실행 방지

---

### C4. Task Dependency DAG
- 순서 기반이 아닌 의존성 기반 실행
- 실패 시 최소 단위 재시도

---

### C5. Auto-Rollback Snapshot
- Phase 종료 시 스냅샷 생성
- FAIL 발생 시 자동 복구

---

### C6. Policy Rule Engine
- “하면 안 되는 것”을 명시적 정책으로 관리
- Auditor는 정책 위반 즉시 FAIL

---

### C7. LLM Call Budgeting
- Phase별 MCP 호출 상한 설정
- 비용/속도 예측 가능

---

### C8. Blueprint / Recipe System
- 자주 쓰는 프로젝트 유형을 템플릿화
- spec_analyst가 우선 적용 후 부족분만 Q&A

---

## 5) 권장 구현 순서 (현실적인 접근)

1. Phase 2.2-A (Decision Ledger + Plan Mode)
2. Phase 2.2-B (Change Impact + Rollback)
3. Phase 2.2-D (Policy + Budget)
4. Phase 2.2-C (Task DAG)
5. Phase 2.2-E (Blueprint)

---

## 6) v2.2 완료 정의 (Definition of Done)

v2.2는 아래 조건을 모두 만족할 때 완료로 간주합니다.

- 모든 자동화 결정에 근거 문서 존재
- 실행 전 결과 예측 가능
- 실패 후 자동 복구 가능
- 정책 위반 사전 차단
- 반복 프로젝트 초기 설정 시간 대폭 감소

---

## 7) v2.2 이후(v2.3+) 확장 방향 (Preview)

- Multi-project Orchestration
- Team Role-based Policy
- Metrics 기반 자동 품질 조정
- Human-in-the-loop 승인 단계

---

## END OF v2.2 ROADMAP
