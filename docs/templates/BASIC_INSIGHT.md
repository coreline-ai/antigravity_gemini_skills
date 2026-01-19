# 🧠 Universal Orchestration System v2 (FINAL SPEC)

Web(React/Next.js) / App(Flutter/Native) / Hybrid 프로젝트를 자동 판별하고  
분석 → 구현 → 감사(루프)까지 **기계적으로 자동 수행**하는  
에이전트 기반 오케스트레이션 규격 문서입니다.

---

## 0) Code Block Integrity Policy (중요)

이 문서는 “단일 코드블럭로 저장”을 전제로 배포됩니다.

- 본 문서 바깥은 ```markdown 으로 감싸며,
- 문서 내부의 예시 코드펜스는 **절대 ```를 쓰지 않고 `~~~`만 사용**합니다.
- 따라서, 복사/저장 시 코드블럭이 깨질 가능성이 매우 낮습니다.

---

## 1) Agent Naming Convention (STRICT)

아래 네이밍은 모든 문서/프롬프트에서 **절대 변경 금지**입니다.

| Role | Agent Name | Skill |
|---|---|---|
| PM | @Agent_PM | orchestrator |
| Architect / Analyst | @Agent_Analyst | spec_analyst |
| Developer | @Agent_Dev | universal_dev |
| Auditor | @Agent_Auditor | auditor |

---

## 2) Project Directory Structure (v2)

최종 디렉토리 구조(권장):

PROJECT_ROOT/  
├── docs/                       # PRD / DESIGN / TRD (유일한 입력 소스)  
│   ├── PRD.md                  # 없으면 오케스트레이터가 템플릿 생성 요청  
│   ├── DESIGN.md               # 선택(없으면 진행 가능)  
│   └── TRD.md                  # 선택(없으면 Analyst가 생성 가능)  
├── .agent/  
│   ├── mcp_config.json         # MCP 설정 (수정 금지)  
│   └── skills/  
│       ├── orchestrator/  
│       │   └── SKILL.md  
│       ├── spec_analyst/  
│       │   └── SKILL.md  
│       ├── universal_dev/  
│       │   └── SKILL.md  
│       └── auditor/  
│           └── SKILL.md  
├── apps/  
│   ├── web/                    # WEB 프로젝트 생성 위치  
│   └── mobile/                 # APP 프로젝트 생성 위치  
├── MASTER_PLAN.md              # 프로젝트 계약서 (자동 생성)  
├── RUN_LOG.md                  # Phase별 체크포인트 로그 (자동 기록)  
└── AUDIT_REPORT.md             # 감사 결과 보고서 (자동 생성)  

---

## 3) MCP Configuration (ORIGINAL – DO NOT MODIFY)

⚠️ MCP 설정은 시스템 외부 의존성입니다.  
에이전트는 이를 **생성/수정/추론/자동변경하지 않습니다.**  
(“경로만 사용자가 로컬에 맞게 수정”)

파일: `.agent/mcp_config.json`

~~~json
{
  "mcpServers": {
    "chatgpt": {
      "command": "bun",
      "args": ["run", "/Users/YOUR_USER/path/to/claude-chatgpt-mcp/index.ts"],
      "env": {}
    }
  }
}
~~~

---

## 4) spec_analyst Skill (v2 강화)

### 4.1 Role
- `docs/` 폴더를 **유일한 입력 소스**로 읽고,
- 프로젝트 플랫폼(Web/App/Hybrid)과 기술스택/아키텍처를
- **규칙 기반으로 확정**하여,
- 루트에 `MASTER_PLAN.md`(단일 계약서)를 생성합니다.

출력은 반드시 `MASTER_PLAN.md` 하나로 수렴합니다.

---

### 4.2 Platform Detection Rule (MANDATORY)

#### 4.2.1 Keyword Scoring (점수화)
- WEB 키워드 발견 시 +2
  - SEO, SSR, CMS, Admin, Dashboard, URL, Webhook, Browser, Landing, Marketing Site
- APP 키워드 발견 시 +2
  - App Store, Play Store, Push, Permission, Offline, Camera, Sensor, BLE, GPS, Background Service

#### 4.2.2 Decision Rule (판정)
- WEB ≥ 4 and APP < 4 → PLATFORM_MODE = WEB
- APP ≥ 4 and WEB < 4 → PLATFORM_MODE = APP
- WEB ≥ 4 and APP ≥ 4 → PLATFORM_MODE = HYBRID
- 애매한 경우(둘 다 0~2점대):
  - MCP(ChatGPT) 질의 후
  - 여전히 불명확하면 **보수적으로 HYBRID**

#### 4.2.3 Hard Constraints
- “감으로 판단” 금지
- 반드시:
  - 점수 합산 결과
  - 근거 키워드(문서 내 위치/문장)
  를 `MASTER_PLAN.md`에 기록

---

### 4.3 MCP(ChatGPT) Usage (Optional Brain)

#### 4.3.1 When to Call
1) PRD에 기술스택이 명시되지 않은 경우  
2) DB/ERD 초안이 필요한 경우  
3) 복잡한 비즈니스 로직의 엣지케이스가 필요한 경우  

#### 4.3.2 Prompt Contract (출력 강제)
- 버전 포함(Pinned)
- 폴더 트리 포함
- 대안 1개 포함
- 리스크/폴백 포함
- JSON + Markdown 병행

예시 프롬프트(참고):

~~~text
너는 2025~2026 기준 프로덕션 설계에 강한 시니어 아키텍트야.

[입력]
- 아래 PRD 요약을 바탕으로, 가장 안정적이고 생산성 높은 Tech Stack 추천.
- WEB vs APP vs HYBRID 판단 근거 포함.

[출력 포맷(반드시 준수)]
1) JSON:
{
  "platform_mode": "WEB|APP|HYBRID",
  "primary_type": "NEXTJS|FLUTTER|ANDROID|IOS",
  "language": "TypeScript|Dart|Kotlin|Swift",
  "pinned_versions": {...},
  "repo_layout": "APPS_SPLIT",
  "backend_required": true|false,
  "folder_tree": "string",
  "risks": [...],
  "fallback": "string"
}

2) Markdown:
- 추천 이유
- 대안 1개와 트레이드오프
- 최소 폴더트리
~~~

---

### 4.4 Output: MASTER_PLAN.md (Strict Contract)

spec_analyst는 아래 “고정 템플릿”을 기반으로 `MASTER_PLAN.md`를 생성합니다.

(템플릿)

~~~markdown
# MASTER PLAN

## 1. Project Identity
- PLATFORM_MODE: [WEB | APP | HYBRID]
- PRIMARY_TYPE: [NEXTJS | FLUTTER | ANDROID | IOS]
- LANGUAGE: [TypeScript | Dart | Kotlin | Swift]

## 2. Platform & Repo Flags
- BACKEND_REQUIRED: [YES | NO]
- REPO_LAYOUT: [APPS_SPLIT]
- PACKAGE_MANAGER: [pnpm | yarn | bun | flutter]

## 3. Tech Stack (Pinned Versions)
- Frontend:
- Backend:
- Database:
- Runtime:
- Tooling:

## 4. Platform Detection Evidence
- WEB_SCORE: <number>
- APP_SCORE: <number>
- EVIDENCE:
  - (문서 인용/요약)

## 5. Architecture
- Design Pattern:
- Folder Structure Tree:

## 6. Implementation Tasks
### Phase 1 – Setup
### Phase 2 – Core Logic
### Phase 3 – UI / UX

## 7. Risks & Fallback
- Risk:
- Fallback Strategy:
~~~

---

### 4.5 Constraints
- “적절히”, “알아서” 같은 모호 표현 금지
- 라이브러리/프레임워크는 **버전 고정(Pinned)**
- Backend 필요 여부는 반드시 YES/NO로 명시

---

## 5) orchestrator Skill (PM v2)

### 5.1 Role
- PM은 직접 코딩하지 않습니다.
- 모든 지시는 `MASTER_PLAN.md`를 기준으로만 이뤄집니다.
- Phase 체크포인트를 `RUN_LOG.md`에 기록합니다.

---

### 5.2 Phase 0 – Blueprinting (설계)
1) `docs/` 검사  
   - `docs/PRD.md` 없으면: PRD 템플릿 생성 요청(자동 중단하지 말고 “생성 요청”으로 진행)
2) `@Agent_Analyst` 호출  
   - docs 분석
   - `MASTER_PLAN.md` 생성
3) MCP 연결 확인  
   - 성공/실패를 `RUN_LOG.md`에 기록  
   - 실패 시: “MCP 없이 자체 판단 + 보수적 스택” 지시

Checkpoint 기록 예시:

~~~markdown
# RUN LOG
## Phase 0
- STATUS: DONE
- MCP: OK | FAIL
- MASTER_PLAN.md: GENERATED
~~~

---

### 5.3 Phase 1 – Context Injection (환경/정체성 주입)
`@Agent_Dev`를 호출하고, 아래를 **반드시 주입**합니다.

- PLATFORM_MODE
- PRIMARY_TYPE
- LANGUAGE
- ROOT_WORK_DIR
  - WEB: `apps/web`
  - APP: `apps/mobile`
  - HYBRID: `apps/web` + `apps/mobile` (순차/소유권 규칙 필수)
- BACKEND_REQUIRED
- CODING RULES (빌드 가능 기준, 파일 생성 규칙)

Injection 예시:

~~~text
너는 이제 [PRIMARY_TYPE] 전문가야.
언어는 [LANGUAGE]를 사용해.
작업 루트는 [ROOT_WORK_DIR]야.
MASTER_PLAN.md의 Tech Stack/Architecture를 100% 준수해.
Phase1 종료 시 반드시 빌드 가능한 상태를 만들어.
~~~

Checkpoint:

~~~markdown
## Phase 1
- STATUS: DONE
- ROOT_WORK_DIR: apps/web
- BUILD_STATUS: OK
~~~

---

### 5.4 Phase 2 – Implementation (구현)
기본값: **순차 실행**

병렬 실행은 아래 조건을 만족할 때만 허용:
- 폴더 소유권(Owner) 명시
- 충돌 감지 시 즉시 중단 후 순차로 전환

Owner 규칙 예시:
- UI Owner: `apps/web/src/ui/**`
- Server Owner: `apps/web/src/server/**`

Checkpoint:
- 기능 단위로 `RUN_LOG.md`에 기록

---

### 5.5 Phase 3 – Audit Loop (감사 루프)
1) `@Agent_Auditor` 호출하여 `AUDIT_REPORT.md` 생성  
2) FAIL이면:
   - 실패 원인 요약
   - `@Agent_Dev`에게 수정 지시
   - 최대 3회 반복
3) PASS면 종료

---

### 5.6 Safety Protocol
- PLATFORM_MODE 변경 감지 시 즉시 중단
- 중단 보고에는 반드시 포함:
  - 변경 사유
  - 근거
  - 대안(최소 1개)

---

## 6) universal_dev Skill (v2)

### 6.1 Role
- Dev의 정체성은 PM이 주입한 컨텍스트로만 결정됩니다.
- Context 밖의 코드 작성/제안 금지

---

### 6.2 Golden Rules
1) MASTER_PLAN.md 100% 준수  
2) 작업 루트(ROOT_WORK_DIR) 밖 수정 금지  
3) 각 Phase 종료 시 **빌드 가능한 상태** 유지  
4) 파일 생성 시 경로/파일명 정확성 우선  
5) 막히면 TODO 프로토콜 사용 후 진행

---

### 6.3 Web Project Rules
- Component 기반 개발(Atomic Design 권장)
- Responsive 필수
- SEO 고려(Next.js면 메타/라우팅/서버 렌더 포인트 준수)

---

### 6.4 App Project Rules
- 플랫폼 가이드(Material/Cupertino) 준수
- Permission/Offline 처리 필수
- 백그라운드/센서 등 OS 제약 고려

---

### 6.5 TODO Protocol
막히는 구간은 아래 주석을 남기고 진행합니다.

~~~text
// TODO: Need Architect Review
~~~

PM은 TODO를 수집하여 Analyst에게 전달하고 해결책을 반영합니다.

---

## 7) auditor Skill (QA v2)

### 7.1 Role
- Auditor는 **증거 기반** 판정자입니다.
- PASS/FAIL은 기계적으로 결정합니다.

---

### 7.2 Audit Rules (증거 제출 강제)
PRD의 각 요구사항마다 반드시 포함:
- 파일 경로
- 함수/컴포넌트명
- 실행 방법(빌드/런 커맨드 등)
- (가능하면) 테스트/스크린샷/로그

---

### 7.3 AUDIT_REPORT.md Format (고정)

~~~markdown
# Audit Report

- [x] Feature A
  - Evidence:
    - File: apps/web/src/...
    - Symbol: ComponentOrFunctionName
    - How to Verify: <command or steps>

- [ ] Feature B (Missing)
  - Evidence:
    - Not found

## Critical Issues
- NONE

## Final Verdict
STATUS: [PASS | FAIL]
~~~

---

### 7.4 PASS 조건 (고정)
- 필수 기능 100% 체크
- Critical Issues 0
- 빌드/실행 재현 가능(검증 커맨드 존재)

---

## 8) Execution Prompt (FINAL)

안티그레비티 IDE Agent Manager에 아래 프롬프트를 1회 입력:

~~~text
@Agent_PM, orchestrator 스킬을 로드해.

[지시사항]
1. docs/ 폴더 문서들을 읽고 Phase 0부터 시작해.
2. Phase 0에서 @Agent_Analyst를 통해 플랫폼을 확정하고 MASTER_PLAN.md를 만들어.
3. Phase 1에서 @Agent_Dev에게 플랫폼 전문가 페르소나를 주입하고 스캐폴딩을 진행해.
4. Phase 2 구현을 진행하고, Phase 3 감사 루프를 PASS가 나올 때까지 반복해. (Max Loop: 3)
5. 모든 과정은 RUN_LOG.md에 체크포인트로 기록해.
~~~

---

## 9) System Guarantees (v2)
- 플랫폼 자동 판별(규칙 기반 + 근거 기록)
- 계약서(MASTER_PLAN.md) 기반 개발
- 컨텍스트 주입을 통한 Dev 역할 고정
- 증거 기반 QA 및 PASS/FAIL 기계적 판정
- 실패 시 자동 수정 루프(최대 3회)
- MCP 설정은 외부 의존성으로 고정(수정 금지)

---

## END OF SPEC
