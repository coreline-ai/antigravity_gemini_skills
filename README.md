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

## 📂 테스트 산출물: 간단한 메모 앱 (Sample)

> **참고:** 이 기능은 시스템의 성능을 증명하기 위해 **100% 자율적으로 생성**되었습니다.

### 📝 개요
**Web (Next.js) + LocalStorage** 스택 결정 로직을 보여주기 위해 만들어진 가볍고 빠른 오프라인 메모 앱입니다.

### 🏗️ 기술 스택 (에이전트가 결정함)
- **Framework:** Next.js 14.2 (App Router)
- **Language:** TypeScript
- **State:** Zustand
- **Storage:** Browser LocalStorage (서버 없음)
- **Styling:** Tailwind CSS

### 📸 기능
- **Zero-Config:** DB 설정 불필요. 열자마자 바로 사용 가능.
- **CRUD:** 메모 생성, 조회, 수정, 삭제 즉시 반영.
- **반응형 UI:** 데스크탑, 모바일 완벽 지원.
- **다크 모드:** Tailwind 기반 자동 지원.

### 💻 실행 방법
```bash
cd apps/web
npm run dev
# http://localhost:3000 접속
```

---

## � 향후 로드맵 (Future Roadmap)

시스템의 안정성과 확장성을 위해 다음과 같은 핵심 업그레이드가 계획되어 있습니다. 상시 분석을 완료했으며, 순차적으로 적용될 예정입니다.

### v2.2: 설명 가능하고 결정적인 자동화 (Deterministic Automation) 🗺️
- **의사결정 원장 (Decision Ledger):** 모든 결정(`BACKEND_REQUIRED` 등)의 근거를 기록하여 블랙박스를 해소합니다.
- **드라이런 모드 (Dry-run):** 실제 코드를 수정하기 전, 실행 계획을 미리 출력하고 사용자 승인을 받습니다.
- **변경 영향 분석 (Change Impact):** PRD/Design 변경 시 영향 받는 범위를 자동으로 계산하여 불필요한 재작업을 방지합니다.
- **작업 의존성 DAG:** 작업 간의 관계를 그래프로 관리하여 실패 시 필요한 부분만 골라 재시도합니다.
- **자동 롤백 스냅샷:** 감사(Audit) 실패 시 즉시 마지막 정상 상태로 스냅샷 기반 복구를 수행합니다.

### v2.3: 정책 기반 거버넌스 (Policy-driven Governance) ✅
- **OPA 스타일 정책 엔진:** `POLICY_RULES.md`를 통해 "하면 안 되는 것"을 명시적으로 관리합니다.
- **자동 정책 검사 (Policy Gate):** 실행 직전 기술 스택 준수, 폴더 구조 무결성 등을 강제로 검사합니다.
- **규정 준수 자동화:** 기획-개발-감사 전 과정에 걸쳐 프로젝트 고유의 정책을 일관되게 적용합니다.

---

## �📁 저장소 구조

```
.
├── .agent/              # 🧠 두뇌 (The Brain)
│   ├── skills/          # 에이전트 스킬 정의 (PM, Analyst, Dev, Auditor)
│   └── workflows/       # 자동화 스크립트 (/new 커맨드 등)
├── apps/                # 🏭 공장 (산출물)
│   └── web/             # (Artifact) 메모 앱 소스코드
├── docs/                # 📄 입력 문서
│   ├── templates/       # 표준 템플릿 (PRD, TRD, DESIGN)
│   └── PRD.md           # 현재 프로젝트 요구사항
├── MASTER_PLAN.md       # 📜 계약서 (Analyst 작성)
├── AUDIT_REPORT.md      # ✅ 합격증 (Auditor 작성)
└── README.md            # 이 파일
```
