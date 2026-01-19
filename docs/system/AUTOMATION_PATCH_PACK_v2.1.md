# ✅ AUTOMATION PATCH PACK v2.1
# spec_analyst Gap-driven Q&A + Priority Questions + End-to-End Simulation

본 문서는 기존 Universal Orchestration System v2에 대해,
1) `spec_analyst`에 **Gap-driven Q&A** 섹션을 추가하는 패치(삽입용 문서)
2) **질문 최소화(우선순위 질문 세트)** 정의
3) **PRD → 질문 → 응답 → MASTER_PLAN 생성** 시뮬레이션 예시

를 한 번에 제공합니다.

⚠️ 코드블럭 깨짐 방지:
- 이 문서는 단일 코드블럭로 저장 가능
- 내부 예시는 `~~~`만 사용합니다 (``` 사용 금지)

---

# 1) spec_analyst SKILL.md – Gap-driven Q&A 섹션 추가본 (v2.1)

아래 섹션을 `.agent/skills/spec_analyst/SKILL.md`에 **그대로 추가**하세요.
(권장 위치: Platform Detection Rule 다음, MASTER_PLAN Output 이전)

---

## ✅ INSERT: Gap-driven Q&A (Field Completion Protocol)

### 목적
`docs/` 문서가 불완전할 때(필수 정보 누락),
추측으로 진행하지 않고 **최소한의 문답(Q&A)** 을 통해
`MASTER_PLAN.md`를 **흔들림 없이** 생성하기 위함입니다.

이 프로토콜은 “대화”가 아니라 “필드 충족(Field Completion)” 절차입니다.

---

### A. 필수 필드 정의 (Required Fields)

spec_analyst는 `MASTER_PLAN.md` 생성을 위해 아래 필드를 반드시 확보해야 합니다.

#### A1) Project Identity (필수)
- PLATFORM_MODE: [WEB | APP | HYBRID]
- PRIMARY_TYPE: [NEXTJS | FLUTTER | ANDROID | IOS]
- LANGUAGE: [TypeScript | Dart | Kotlin | Swift]

#### A2) Platform & Repo Flags (필수)
- BACKEND_REQUIRED: [YES | NO]
- REPO_LAYOUT: [APPS_SPLIT]
- PACKAGE_MANAGER: [pnpm | yarn | bun | flutter]

#### A3) Tech Stack (Pinned Versions) (필수)
- Frontend (버전 포함)
- Backend (BACKEND_REQUIRED=YES 인 경우 버전 포함)
- Database (BACKEND_REQUIRED=YES 또는 데이터 영구저장 필요 시)
- Runtime (Node/Flutter/JDK 등)
- Tooling (lint/test/build)

#### A4) Platform Detection Evidence (필수)
- WEB_SCORE / APP_SCORE
- EVIDENCE: 키워드 근거(문서 문장 요약 형태)

---

### B. Gap Detection (누락 감지 규칙)

1) `docs/PRD.md`를 먼저 읽고,
2) 기존 Platform Scoring을 수행한 후,
3) Required Fields를 채울 수 있는 정보가 부족하면 “GAP”으로 판정합니다.

#### GAP 판정 조건(예)
- PLATFORM_MODE 판정 점수 부족:
  - WEB_SCORE < 4 and APP_SCORE < 4
- BACKEND_REQUIRED가 불명확:
  - “저장/계정/동기화/관리자” 등의 암시가 있으나 명시 없음
- 배포/실행환경 불명확:
  - “앱” 언급은 있으나 스토어 배포/권한/오프라인 여부가 없음
- DESIGN/TRD 부재로 핵심 토큰/제약이 비어 있음:
  - 최소 토큰/성능/보안 요구가 전혀 없음

---

### C. Question Generation Rule (질문 생성 규칙)

#### C1) 질문 수 제한
- 1회 질의 배치에서 **최대 5문항**
- 가능하면 3문항 이내로 수렴

#### C2) 질문 형태 강제(선택형)
- YES/NO 또는 ENUM 선택형만 허용
- “모르겠다” 옵션을 제공하고 **기본값을 적용**할 수 있어야 함

#### C3) 질문 우선순위
- PLATFORM_MODE 결정을 좌우하는 질문이 최우선
- BACKEND_REQUIRED 결정 질문이 2순위
- 기술스택 핀 고정은 3순위(정보 없으면 보수 기본값 + 기록)

---

### D. Defaulting Policy (응답 없을 때 기본값 규칙)

사용자가 응답을 제공하지 않거나 “모르겠다”를 선택하면,
아래 기본값을 적용하고 `MASTER_PLAN.md`의 Evidence에 기록합니다.

- PLATFORM_MODE:
  - 애매하면 HYBRID (보수적)
- BACKEND_REQUIRED:
  - 명시 없으면 NO (보수적, 비용/복잡도 최소)
  - 단, “로그인/결제/영구저장/관리자/권한”이 핵심이면 YES
- REPO_LAYOUT:
  - APPS_SPLIT 고정
- PACKAGE_MANAGER:
  - WEB: pnpm (기본)
  - FLUTTER: flutter (기본)
- Pinned Versions:
  - 최신 추정 금지. “안정적 LTS”로 고정하고 추후 변경 가능 표기

---

### E. Output Rule (산출 규칙)

GAP-driven Q&A가 실행되면, spec_analyst는 반드시 다음을 수행합니다.

1) `QNA_REQUEST.md` 생성(또는 사용자에게 동일 포맷으로 질문 출력)
2) 사용자 답변을 수집한 뒤 `QNA_ANSWERS.md`로 정리(또는 대화 기록을 요약)
3) 위 답변과 기본값 적용 내역을 **MASTER_PLAN.md의 Evidence 섹션에 포함**
4) 질문 배치(1회) → 답변 → MASTER_PLAN 생성까지 한 사이클로 종료

---

### F. Q&A Output Format (고정 포맷)

질문 출력은 아래 포맷을 반드시 사용합니다.

~~~text
[필수 정보 누락 - Gap-driven Q&A]

아래 질문은 MASTER_PLAN.md 생성을 위한 최소 정보입니다.
각 질문은 A/B/C 중 하나로 답해주세요. (모르면 C)

Q1. <질문>
A) <선택지>
B) <선택지>
C) 모르겠다 (기본값: <기본값>)

Q2. ...
~~~

---

### G. MCP Fallback Rule

- MCP(ChatGPT)는 Q&A를 대체하지 않습니다.
- MCP는 “대안/리스크/스택 추천” 보조 역할이며,
  **PLATFORM_MODE와 BACKEND_REQUIRED가 불명확하면 Q&A가 우선**입니다.

---

# (END INSERT)
---

# 2) 질문 최소화: Priority Question Set (최소 질문 세트)

목표: 대부분 프로젝트를 **3문항 이내**로 결정

## P0 (플랫폼 결정) — 1문항
Q1. 최종 사용자 경험 기준, 무엇이 1차 타겟인가요?
A) 브라우저(SEO/URL/대시보드 포함) 중심 → WEB
B) 앱 설치/권한/푸시/오프라인 중심 → APP
C) 둘 다 동일하게 필요 → HYBRID (기본값: HYBRID)

## P1 (백엔드 필요 여부) — 1문항
Q2. 서버(DB) 없이도 제품이 성립하나요?
A) YES (로컬/정적/단말 내 저장 정도) → BACKEND_REQUIRED=NO
B) NO (계정/동기화/공유/영구저장/관리자 필요) → BACKEND_REQUIRED=YES
C) 모르겠다 (기본값: NO, 단 PRD에 계정/관리자/공유/영구저장 있으면 YES)

## P2 (배포/운영) — 1문항
Q3. 배포 형태는 무엇인가요?
A) 웹 배포(Vercel/Netlify 등) → WEB 기본 설정
B) 앱 배포(Play/App Store/사내배포) → APP 기본 설정
C) 둘 다 → HYBRID 기본 설정

### (옵션) P3 (권한/오프라인이 핵심인 경우만)
Q4. 오프라인/권한이 핵심 요구사항인가요?
A) YES (권한 목록: Camera/GPS/BLE/Notif 등 명시 필요)
B) NO
C) 모르겠다 (기본값: NO)

> 원칙:
- Q1~Q3로 90% 결정
- Q4는 APP/HYBRID이면서 기능이 센서/촬영/푸시/오프라인 암시가 있을 때만

---

# 3) End-to-End Simulation
# PRD → 질문 → 응답 → MASTER_PLAN 생성 시뮬레이션

## 3.1 입력 예시 PRD (불완전한 상태)

~~~markdown
# PRD (Example)

## Overview
사용자가 콘텐츠를 빠르게 기록하고 공유할 수 있는 서비스.
팀 단위로 협업도 가능하면 좋다.

## Core Features
- 로그인
- 콘텐츠 생성/수정/삭제
- 팀 멤버 초대
- 관리자 화면에서 전체 콘텐츠 모니터링

## Notes
모바일에서도 쓰고 싶다.
~~~

### 3.1 분석(초기 Scoring)
- WEB 키워드(관리자 화면, 모니터링, 대시보드 암시): +2 정도
- APP 키워드(모바일에서도): +2 정도
=> WEB_SCORE=2, APP_SCORE=2 → **PLATFORM_MODE 판정 불충분(GAP)**

또한:
- 로그인/팀 초대/관리자 → BACKEND_REQUIRED 거의 확실(YES)
- 하지만 사용자는 “웹/앱/둘다” 확정이 없음

따라서 Q&A 배치 1회 수행(최대 3문항).

---

## 3.2 spec_analyst가 생성하는 질문(QNA_REQUEST)

~~~text
[필수 정보 누락 - Gap-driven Q&A]

아래 질문은 MASTER_PLAN.md 생성을 위한 최소 정보입니다.
각 질문은 A/B/C 중 하나로 답해주세요. (모르면 C)

Q1. 최종 사용자 경험 기준, 무엇이 1차 타겟인가요?
A) 브라우저(SEO/URL/관리자 대시보드 중심)
B) 앱 설치/권한/푸시/오프라인 중심
C) 둘 다 동일하게 필요 (기본값: HYBRID)

Q2. 서버(DB) 없이도 제품이 성립하나요?
A) YES (로컬/정적 중심)
B) NO (계정/동기화/공유/영구저장/관리자 필요)
C) 모르겠다 (기본값: NO, 단 계정/관리자/공유 있으면 YES)

Q3. 배포 형태는 무엇인가요?
A) 웹 배포(Vercel/Netlify 등)
B) 앱 배포(Play/App Store/사내배포)
C) 둘 다 (기본값: 둘 다)
~~~

---

## 3.3 사용자 응답(QNA_ANSWERS)

(가정 응답)
- Q1: C (둘 다)
- Q2: B (서버 필요)
- Q3: C (둘 다)

---

## 3.4 결과 MASTER_PLAN.md 생성(시뮬레이션)

아래는 위 응답 기반으로 생성된 예시 `MASTER_PLAN.md` 입니다.

~~~markdown
# MASTER PLAN

## 1. Project Identity
- PLATFORM_MODE: HYBRID
- PRIMARY_TYPE: NEXTJS
- LANGUAGE: TypeScript

## 2. Platform & Repo Flags
- BACKEND_REQUIRED: YES
- REPO_LAYOUT: APPS_SPLIT
- PACKAGE_MANAGER: pnpm

## 3. Tech Stack (Pinned Versions)
- Frontend:
  - Next.js (pinned: 14.x LTS line)
  - React (pinned: 18.x)
- Backend:
  - Next.js Route Handlers OR NestJS (pinned: stable LTS)
- Database:
  - PostgreSQL (pinned: 16.x)
- Runtime:
  - Node.js (pinned: 20 LTS)
- Tooling:
  - TypeScript, ESLint, Prettier, Vitest (pinned: stable)

## 4. Platform Detection Evidence
- WEB_SCORE: 2
- APP_SCORE: 2
- EVIDENCE:
  - PRD에 “관리자 화면에서 전체 콘텐츠 모니터링” → WEB 성격(+2)
  - PRD에 “모바일에서도 쓰고 싶다” → APP 성격(+2)
  - 점수 임계치 미달 → Gap-driven Q&A 수행
  - Q1=C, Q3=C → PLATFORM_MODE=HYBRID 확정
  - 로그인/팀 초대/관리자 → Q2=B → BACKEND_REQUIRED=YES 확정

## 5. Architecture
- Design Pattern:
  - Web: Component-based + (optional) Clean-ish layering
  - Backend: Layered (Controller/Service/Repo)
- Folder Structure Tree:
  - apps/web (Next.js)
  - apps/mobile (placeholder; 추후 Flutter/Native 확정 시 생성)
  - shared packages (optional)

## 6. Implementation Tasks
### Phase 1 – Setup
- apps/web Next.js scaffold
- lint/format/test tooling setup
- DB 연결/마이그레이션 도입
- 기본 Auth 스켈레톤

### Phase 2 – Core Logic
- 로그인/세션
- 콘텐츠 CRUD
- 팀 초대/권한
- 관리자 목록/필터

### Phase 3 – UI / UX
- 메인 리스트/상세/편집
- 관리자 대시보드
- 에러/로딩/빈상태 디자인

## 7. Risks & Fallback
- Risk: HYBRID 범위로 인해 일정 확대 가능
- Fallback Strategy:
  - 1차: WEB(Next.js) 우선 완성
  - 2차: Mobile은 PWA 또는 Flutter로 확장
~~~

---

# 4) 구현 관점: 오케스트레이션에 반영되는 자동화 규칙(요약)

## 4.1 Phase 0에서의 분기
- docs 분석
- 점수 충분 → 바로 MASTER_PLAN 생성
- 점수 부족 → QNA_REQUEST 출력 → 답변 수집 → MASTER_PLAN 생성

## 4.2 PM(orchestrator)의 운영 규칙
- Q&A가 완료되기 전에는 @Agent_Dev를 호출하지 않는다.
- Q&A 결과/기본값 적용 내역은 RUN_LOG에 기록한다.

RUN_LOG 예시:

~~~markdown
# RUN LOG
## Phase 0
- STATUS: DONE
- GAP_QNA: EXECUTED (3 questions)
- PLATFORM_MODE: HYBRID
- BACKEND_REQUIRED: YES
- MASTER_PLAN.md: GENERATED
~~~

---

# 5) 다음 구현 단계(권장)

- (A) orchestrator SKILL.md에 규칙 1줄 추가:
  - “Phase 0에서 Gap-driven Q&A가 끝나기 전엔 Phase 1로 넘어가지 않는다.”
- (B) auditor에 Q&A 증거 체크 항목 추가:
  - “Evidence 섹션에 Q&A 결과/기본값 기록이 존재하는가?”

---

# END OF AUTOMATION PATCH PACK v2.1
