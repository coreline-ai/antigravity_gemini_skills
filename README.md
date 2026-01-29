# 🌌 Anti-Agents Skills: 유니버설 오케스트레이션 시스템 (v2.1)

> **"코드는 직접 짜는 게 아니라, 조율(Orchestration)하는 것입니다."**
> 
> 요구사항 분석부터 구현, 그리고 엄격한 감사까지 소프트웨어 개발 수명 주기(SDLC) 전체를 관리하는 완전 자율 에이전틱 DevOps 프레임워크입니다.

![Version](https://img.shields.io/badge/Version-v2.1-blueviolet) ![Status](https://img.shields.io/badge/Status-Operational-success) ![License](https://img.shields.io/badge/License-ISC-blue)

---

## 🧠 핵심 아키텍처 (Core Architecture)

이 시스템은 단일 AI가 아닌, 엄격한 프로토콜 하에 협업하는 **전문 에이전트 팀**으로 운영됩니다.

### 🎭 에이전트 명단 (Roster)
| 에이전트 | 역할(Role) | 책임(Responsibility) |
|-------|------|----------------|
| **@Agent_PM** | `orchestrator` | 프로젝트 매니저. 워크플로우 통제, 단계(Phase) 관리, 안전 게이트 담당. |
| **@Agent_Analyst** | `spec_analyst` | 아키텍트. `docs/PRD.md`를 분석하고, 누락된 정보를 감지하여 `MASTER_PLAN.md`를 설계. |
| **@Agent_Dev** | `universal_dev` | 개발자. 마스터 플랜과 페르소나에 따라 오차 없이 코드를 구현. |
| **@Agent_Auditor** | `auditor` | QA & 감사. **100% PASS**가 나올 때까지 개발자를 무한 루프로 검증. |

---

## ✨ 주요 기능 (v2.1)

### 1. Gap-driven Q&A (빈칸 채우기 프로토콜) 🛡️
사용자의 입력(`PRD.md`)이 모호하거나 미완성일 경우, 시스템은 추측하지 않고 **멈춥니다.**
- 자동으로 Q&A 세션을 시작하여 필요한 정보를 수집합니다.
- **예시:** "웹 앱이라고 하셨는데, 서버가 필요한가요? 로컬 저장소만 쓸까요?"

### 2. Phase 0 게이트 & 무한 감사 루프 ♾️
- **Phase 0 게이트:** `MASTER_PLAN.md`가 완벽하게 합의되지 않으면 개발 단계로 넘어가지 않습니다.
- **무한 감사 루프 (Infinite Audit Loop):** Phase 3에서는 `AUDIT_REPORT.md`가 **ALL PASS**를 기록할 때까지 끝나지 않습니다. 감사관(Auditor)이 개발자를 끈질기게 괴롭혀 완벽한 코드를 만들어냅니다.

### 3. 워크플로우 자동화 ⚡
- **슬래시 커맨드:** `/new <아이디어>` — 복잡한 설정 없이 명령어 한 줄로 시작.
- **자동 스캐폴딩:** 프로젝트 타입(Web/App/Hybrid)과 기술 스택(Next.js/Flutter 등)을 상황에 맞춰 동적으로 결정.

---

## 🚀 빠른 시작 (Quick Start)

### 방법 A: "한 줄 시작" (추천)
채팅창에 슬래시 커맨드를 입력하세요:
```bash
/new 간단한 투두리스트 앱 만들어줘
```

### 방법 B: 수동 실행
1. `docs/PRD.md` 파일에 요구사항을 작성합니다.
2. 아래 명령어를 실행합니다:
```bash
@Agent_PM, orchestrator 스킬을 실행해.
```

---

## 📂 테스트 산출물: 간단한 메모 앱 (Sample Artifact)

> **참고:** 이 앱은 시스템의 성능을 증명하기 위해 **100% 자율적으로 생성**된 실제 산출물 예시입니다.

### 🏗️ 기술 스택 (에이전트 자율 결정)
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **State Management:** Zustand
- **Storage:** Browser LocalStorage
- **Styling:** Tailwind CSS (Modern Aesthetics)

### 📸 주요 기능
- **Zero-Config Deployment:** 데이터베이스 설정 없이 즉시 실행 가능.
- **Persistent Data:** 로컬 스토리지를 통한 데이터 영속성 유지.
- **Responsive & Dark Mode:** 모든 디바이스에서 최적화된 테마 지원.

---

## 🚀 향후 로드맵 (Detailed Upgrade Roadmap)

시스템의 안정성, 확장성, 그리고 엔터프라이즈급 거버넌스를 확보하기 위한 단계적 업그레이드 계획의 상세 기술 사양입니다.

### Phase 2: 실행 통제 및 정책 자동화 (Governance & Reliability)
- **v2.1 (Current): Smart Design** 🛡️
    - **목표:** Gap-driven Q&A를 통해 설계 단계의 모호성을 제거하고 정교한 `MASTER_PLAN.md` 구축.
- **v2.2: Controlled Execution** 🗺️
    - **목표:** 설명 가능하고 재현 가능한 자동화 프로세스 정립.
    - **주요 기능:** 의사결정 원장(`DECISION_LOG.md`), 드라이런(`PLAN_OUTPUT.md`) 모드, 변경 영향 분석(`CHANGE_IMPACT_REPORT.md`), 자동 롤백 스냅샷(`SNAPSHOT_LOG.md`).
- **v2.3: Policy-based Automation** ✅
    - **목표:** 아키텍처 및 보안 규칙의 알고리즘적 강제.
    - **핵심 도구:** `run_policy_checks.ts`, `POLICY_RULES.md`, `.orchestrator/state.json`. LLM 호출 예산 관리(`LLM_USAGE_LOG.md`) 도입.

### Phase 3: 디자인 시스템 자동화 (Design Automation)
- **v3.0: Design System Charter** 🎨
    - **목표:** 디자인을 심미적 요소가 아닌 검증 가능한 '계약(Contract)'으로 관리.
    - **핵심 사양:** `DESIGN_SYSTEM.md` v3.0, 토큰 기반 설계(`DESIGN_TOKENS.json`), WCAG AA 접근성 강제.
- **v3.1: Operational Design Skill** 🚀
    - **목표:** 실시간 디자인 품질 유지 및 자동 교정.
    - **핵심 도구:** `autofix_tokens.py`, `compute_design_drift.py`, `generate_tokens.py`.

### Phase 4: 엔터프라이즈 거버넌스 및 운영 (Enterprise Security & Ops)
- **v4.0: Enterprise Governance** 🔐
    - **목표:** 전사적 보안 정책 수립 및 CI 파이프라인 통합 게이트 구축.
    - **핵심 기능:** `SECURITY_POLICY_RULES.md` (Secrets/Vulnerability/SAST), GitHub Actions 통합 정책 게이트(`policy-gates.yml`).
- **v4.1: Change & Incident Management** 🔄
    - **목표:** 공식적인 운영 프로세스 및 규정 준수 자동화.
    - **표준 템플릿:** `CHANGE_REQUEST.md` (변경 요청), `INCIDENT.md` (사고 리포트), `EXCEPTIONS.md` (정책 예외 관리).

---

## 📁 저장소 구조 (Repository Structure)

```text
.
├── .agent/              # 🧠 에이전트 브레인 (Skills & Workflows)
├── .orchestrator/       # ⚙️ 오케스트레이션 엔진 상태 및 리포트 (v2.2+)
├── apps/                # 🏭 프로젝트 산출물 (web, mobile, shared)
├── docs/                # 📄 가이드, 템플릿 및 업그레이드 팩
│   └── upgrade_packs/   # 버전별 업그레이드 상세 기술 문서
├── tools/               # 🛠️ 정책 검사, 토큰 생성 등 자동화 스크립트
├── MASTER_PLAN.md       # 📜 프로젝트 설계 계약서
├── AUDIT_REPORT.md      # ✅ 최종 품질 감사 레포트
└── README.md            # 메인 가이드
```
