# ✅ Design v3.0 Extension Pack (All-in-One)
# 1) DESIGN_TOKENS.json 실제 예시(Web + Flutter 공용)
# 2) design_policy_check.ts 의사코드(구현 가이드)
# 3) Figma Tokens ↔ v3.0 자동 동기화 전략
# 4) Design Drift(버전 간 변화) 추적 시스템

주의:
- 코드블럭 깨짐 방지를 위해 이 문서 전체는 “단 하나의 코드블럭”입니다.
- 내부에 ``` / ~~~ 같은 중첩 코드펜스는 사용하지 않습니다.
- 각 “FILE:” 섹션을 그대로 파일로 저장하면 됩니다.

============================================================
1) DESIGN_TOKENS.json 실제 예시 (Web + Flutter 공용)
============================================================

FILE: DESIGN_TOKENS.json

설명:
- 이 JSON은 “토큰 단일 진실원(Source of Truth)”입니다.
- Web은 CSS Variables / Tailwind 매핑으로 사용
- Flutter는 ThemeData / Wrapper 클래스 생성으로 사용
- 값은 MVP 예시이며 프로젝트 모드(B2B_DENSE 등)에 맞게 조정하세요.

{
  "meta": {
    "version": "3.0.0",
    "updated_at": "2026-01-21T08:00:00+09:00",
    "design_mode": "B2B_DENSE",
    "accessibility_level": "WCAG_AA",
    "source_of_truth": "DESIGN_TOKENS.json"
  },
  "color": {
    "primary": { "value": "#2563EB" },
    "secondary": { "value": "#0EA5E9" },
    "background": { "value": "#0B1220" },
    "surface": { "value": "#111A2E" },
    "surfaceAlt": { "value": "#0F172A" },
    "border": { "value": "#1F2A44" },
    "text": {
      "primary": { "value": "#E5E7EB" },
      "secondary": { "value": "#9CA3AF" },
      "muted": { "value": "#6B7280" },
      "inverse": { "value": "#0B1220" }
    },
    "status": {
      "success": { "value": "#22C55E" },
      "warning": { "value": "#F59E0B" },
      "danger": { "value": "#EF4444" },
      "info": { "value": "#38BDF8" }
    },
    "overlay": {
      "scrim": { "value": "rgba(0,0,0,0.55)" },
      "focusRing": { "value": "rgba(37,99,235,0.45)" }
    }
  },
  "typography": {
    "fontFamily": {
      "sans": { "value": "Inter, Pretendard, system-ui, -apple-system, Segoe UI, Roboto, Arial" },
      "mono": { "value": "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, Liberation Mono, monospace" }
    },
    "fontSize": {
      "xs": { "value": 12 },
      "sm": { "value": 14 },
      "md": { "value": 16 },
      "lg": { "value": 18 },
      "xl": { "value": 20 },
      "2xl": { "value": 24 }
    },
    "fontWeight": {
      "regular": { "value": 400 },
      "medium": { "value": 500 },
      "semibold": { "value": 600 },
      "bold": { "value": 700 }
    },
    "lineHeight": {
      "tight": { "value": 1.25 },
      "normal": { "value": 1.5 },
      "relaxed": { "value": 1.65 }
    },
    "letterSpacing": {
      "normal": { "value": 0.0 },
      "tight": { "value": -0.2 },
      "wide": { "value": 0.2 }
    }
  },
  "spacing": {
    "0": { "value": 0 },
    "xs": { "value": 4 },
    "sm": { "value": 8 },
    "md": { "value": 12 },
    "lg": { "value": 16 },
    "xl": { "value": 24 },
    "2xl": { "value": 32 },
    "3xl": { "value": 40 }
  },
  "radius": {
    "none": { "value": 0 },
    "sm": { "value": 6 },
    "md": { "value": 10 },
    "lg": { "value": 16 },
    "xl": { "value": 24 }
  },
  "elevation": {
    "level0": {
      "web": { "value": "none" },
      "flutter": { "value": { "blur": 0, "y": 0, "opacity": 0 } }
    },
    "level1": {
      "web": { "value": "0 1px 2px rgba(0,0,0,0.35)" },
      "flutter": { "value": { "blur": 8, "y": 2, "opacity": 0.22 } }
    },
    "level2": {
      "web": { "value": "0 8px 18px rgba(0,0,0,0.35)" },
      "flutter": { "value": { "blur": 16, "y": 6, "opacity": 0.24 } }
    }
  },
  "motion": {
    "durationMs": {
      "fast": { "value": 120 },
      "normal": { "value": 180 },
      "slow": { "value": 240 }
    },
    "easing": {
      "standard": { "value": "cubic-bezier(0.2, 0, 0, 1)" },
      "emphasized": { "value": "cubic-bezier(0.2, 0.8, 0.2, 1)" }
    },
    "reduceMotion": { "value": true }
  },
  "component": {
    "button": {
      "height": { "value": 44 },
      "radius": { "ref": "radius.md" },
      "paddingX": { "ref": "spacing.lg" },
      "paddingY": { "ref": "spacing.sm" }
    },
    "card": {
      "radius": { "ref": "radius.lg" },
      "padding": { "ref": "spacing.lg" },
      "elevation": { "ref": "elevation.level1" }
    },
    "input": {
      "height": { "value": 44 },
      "radius": { "ref": "radius.md" },
      "paddingX": { "ref": "spacing.md" }
    }
  },
  "rulesHints": {
    "noHardcodedColor": true,
    "noArbitraryTailwind": true,
    "noHardcodedSpacing": true,
    "b2bDenseMaxElevationLevel": 2,
    "minTapTarget": 44
  }
}

============================================================
2) design_policy_check.ts 의사코드 (실제 구현 가이드)
============================================================

FILE: .agent/skills/orchestrator/scripts/design_policy_check.ts

목표:
- DESIGN_SYSTEM.md / POLICY_RULES.md / DESIGN_TOKENS.json / state.json 읽기
- Context 구성
- 코드베이스 스캔(웹/플러터)
- 위반 탐지(토큰 우회, 디자인 모드 위반, a11y 휴리스틱, 모션 규율)
- 점수 계산 + JSON 리포트 + (선택) DESIGN_AUDIT.md 생성

의사코드(타입스크립트 스타일):

1) Entry + CLI Options
- args:
  - --root <PROJECT_ROOT> (default ".")
  - --writeAuditMd true|false (default true)
  - --hardMode true|false (default false)
  - --maxFiles <n> (default 20000)
  - --maxFileBytes <n> (default 2000000)

2) Load Inputs
- readFile(root + "/DESIGN_SYSTEM.md")
- readFile(root + "/POLICY_RULES.md")
- readFile(root + "/DESIGN_TOKENS.json")
- readFile(root + "/.orchestrator/state.json")

3) Parse DESIGN_SYSTEM.md
- simple "KEY: VALUE" parser
- extract:
  - DESIGN_MODE
  - ACCESSIBILITY_LEVEL
  - (optional) PRIMARY_CONTEXT
  - (optional) DESIGN_TONE
- if missing critical keys → ERROR exit=2

4) Parse POLICY_RULES.md (Design rules subset)
- parse blocks starting with "RULE:" OR "## RULE:" (둘 다 지원 권장)
- fields:
  - SEVERITY
  - WHEN (list of "KEY == VALUE")
  - MUST / MUST_NOT (free text but mapped to detectors)
- store as rule objects

5) Parse DESIGN_TOKENS.json
- tokens = JSON.parse
- build indices:
  - tokenKeys list (e.g., color.primary, spacing.md)
  - tokenValue maps (for allowlist checks)
  - allowlists:
    - allowed CSS vars prefix: --color-, --spacing-, --radius-
    - allowed tailwind classes: from config if available (optional future)

6) Build Context
- from design system + state:
  - DESIGN_MODE
  - ACCESSIBILITY_LEVEL
  - MODE (DRY_RUN/EXECUTE)
  - CURRENT_PHASE
- keep context in object

7) Build Scan Plan
- scan paths:
  - apps/web (if exists)
  - apps/mobile (if exists)
  - shared (if exists)
- exclude dirs:
  - node_modules, .next, dist, build, coverage
  - .dart_tool, ios/Pods, android/.gradle
  - .git, .orchestrator/snapshots
- include extensions:
  - web: ts, tsx, js, jsx, css, scss
  - flutter: dart
  - shared: md, json, yml, yaml, toml
- file size cap and count cap

8) Define Detectors (MVP)
- Detector A: Hardcoded Color
  - patterns:
    - /#[0-9a-fA-F]{3,8}\b/
    - /\brgba?\([^)]*\)/
    - /\bhsla?\([^)]*\)/
    - Flutter: /\bColor\(\s*0x[0-9A-Fa-f]{8}\s*\)/
    - Flutter: /\bColor\.fromARGB\b|\bColor\.fromRGBO\b/
  - allowlist cases:
    - "var(--" present (web)
    - token wrapper usage patterns (flutter): AppTheme.colors., Tokens.color.
    - NOTE: allowlist는 프로젝트 규칙에 맞게 확장

- Detector B: Hardcoded Spacing/Radius
  - patterns:
    - web css: /\b(padding|margin|gap|border-radius)\s*:\s*\d+(px|rem)\b/
    - tailwind arbitrary: /\b(p|m|gap|rounded)-\[[^\]]+\]\b/
    - inline style numeric: /padding\s*:\s*\d+/
    - Flutter: /\bEdgeInsets\.(all|only|symmetric)\s*\(\s*\d+/
    - Flutter: /\bSizedBox\(\s*(height|width)\s*:\s*\d+/
    - Flutter: /\bBorderRadius\.circular\(\s*\d+/
  - allowlist:
    - references to Tokens/Theme wrapper (AppSpacing., AppRadius.)

- Detector C: Dense Mode Shadow Limit (DESIGN_MODE == B2B_DENSE)
  - web:
    - /shadow-(2xl|3xl|4xl)\b/
    - /box-shadow\s*:\s*[^;]*\b(30px|40px)\b/ (heuristic)
  - flutter:
    - /BoxShadow\([^)]*blurRadius\s*:\s*(2[4-9]|[3-9]\d)\b/
    - multiple BoxShadow entries count > 1 (heuristic)
  - allowlist:
    - elevation.level1/2 references only

- Detector D: Motion Discipline
  - web:
    - /transition-all\b/ (flag as minor)
    - /duration-(3\d\d|4\d\d|5\d\d)\b/ (>=300ms)
    - /@keyframes\s+\w+/ (new keyframes)
  - flutter:
    - /AnimationController\([^)]*duration\s*:\s*Duration\(milliseconds:\s*(3\d\d|4\d\d|5\d\d)/
  - allowlist:
    - Tokens.motion.durationMs.* / AppMotion.*

- Detector E: Accessibility MVP (heuristics)
  - if ACCESSIBILITY_LEVEL >= WCAG_AA:
    - flag if both text and bg are hardcoded in same file
    - flag tiny tap targets:
      - web: /h-6\b|py-1\b/
      - flutter: /height\s*:\s*(3\d|[12]\d)\b/ (less than 40)
    - allowlist:
      - components that are not interactive (hard to know; treat as minor unless "button/link" nearby)

9) Evaluate Policy Rules
- for each rule:
  - check WHEN conditions against context
  - if active:
    - map rule to detectors and/or path existence checks
    - run relevant detectors
    - record violations with:
      - rule_id, severity, path, evidence snippet, category, context

10) Scoring
- start score_total=100
- for each violation:
  - CRITICAL: -15 (cap cumulative -45)
  - MAJOR: -6
  - MINOR: -2
- compute breakdown:
  - token_compliance: 30 baseline, subtract based on token-related violations
  - density_fitness: based on density rules
  - accessibility: based on a11y flags
  - motion: based on motion flags
  - consistency: (MVP) inferred from repeated violations across same component types
- verdict:
  - FAIL if any CRITICAL OR score_total < 60
  - WARNING if 60..74
  - PASS if score_total >= 75 and CRITICAL=0

11) Write Outputs
- write .orchestrator/design_policy_report.json
- if writeAuditMd:
  - write DESIGN_AUDIT.md (overwrite recommended; append optional)

12) Exit Code
- PASS: 0
- FAIL: 1
- ERROR: 2

============================================================
3) Figma Tokens ↔ v3.0 자동 동기화 전략
============================================================

목표:
- Figma가 “시각적 편집 도구”라면
- v3.0 토큰 시스템은 “실행 가능한 단일 진실원”이다.
- 두 세계를 충돌 없이 연결한다.

권장 아키텍처(현실적/안정적):
A) Source of Truth를 코드(DESIGN_TOKENS.json)로 둔다 (권장)
- 장점: CI에서 강제 가능, 롤백 쉬움, 리뷰/버전 관리 쉬움
- 단점: 디자이너가 Figma에서 직접 수정하면 반영 흐름 필요

동기화 방향:
- CODE → FIGMA: 자동 푸시(주기/릴리즈)
- FIGMA → CODE: PR 기반 반영(리뷰 필수)

B) Source of Truth를 Figma로 두는 방식은 MVP에서는 비추천
- 이유: CI 강제가 어렵고, 변경 감지/롤백/리뷰 흐름이 약해짐

3.1 운영 플로우(권장)
1) 디자이너가 Figma에서 변경 제안
2) 변경 내용은 “토큰 변경 요청”으로 정리
3) 개발자가 DESIGN_TOKENS.json을 수정하여 PR 생성
4) CI에서:
   - design_policy_check.ts 실행
   - token schema validation 실행
5) 머지 후, CODE → FIGMA 자동 푸시로 Figma 토큰 업데이트

3.2 동기화 구현 옵션(선택지)
- 옵션 1: Figma Tokens 플러그인 + JSON Import/Export
  - 운영 난이도 낮음
  - “수동 Export/Import + CI 검증”으로도 충분히 강력

- 옵션 2: Figma API 기반 자동화(고급)
  - 토큰을 변수(Variables)로 관리
  - 릴리즈 시 API로 Figma Variables 업데이트
  - 단, 인증/권한/레이트리밋 고려 필요

3.3 동기화 산출물(권장)
- tools/figma/
  - export_figma_tokens.(js/ts)
  - push_tokens_to_figma.(js/ts)
- 그리고 반드시 남겨야 할 기록:
  - DESIGN_DECISIONS.md에 “토큰 변경 이유/영향” 기록
  - CHANGE_IMPACT_REPORT.md에 “토큰 변경 영향 범위” 기록

3.4 안전장치(필수)
- FIGMA → CODE 변경은 무조건 PR + 리뷰
- CODE → FIGMA는 릴리즈 태그 기준으로만(예: v3.0.1)
- 토큰 충돌 시 우선순위:
  - CODE wins (v3.0 권장)

============================================================
4) Design Drift(버전 간 디자인 변화) 추적 시스템
============================================================

목표:
- “디자인이 언제/왜/얼마나 바뀌었는지”를 자동으로 추적한다.
- 디자인 부채(조용한 붕괴)를 조기에 발견한다.

핵심 아이디어:
- Drift는 주로 3가지에서 발생:
  1) 토큰 변경(합법적 변화)
  2) 토큰 우회(불법/위험 변화)
  3) 컴포넌트 스타일 분기(서서히 붕괴)

4.1 Drift 입력 데이터(권장)
- DESIGN_TOKENS.json (정식 변화)
- .orchestrator/design_policy_report.json (정책 위반)
- UI Snapshot(optional) (시각 비교, v3.1+)
- Git commit metadata

4.2 Drift 산출물(권장 파일)
- DESIGN_DRIFT_LOG.md
- .orchestrator/design_drift.json

4.3 Drift 계산(MVP: 수치 기반)
- Token Diff Score:
  - color.* 변경 개수 / 총 color 토큰 수
  - typography.* 변경 개수 / 총 typography 토큰 수
  - spacing/radius/motion 변경 개수 비율
- Violation Drift:
  - 이전 대비 위반 수 증감
  - CRITICAL 위반 발생 여부
- Score Drift:
  - design_policy_report.score_total의 변화량

Drift 등급 예시:
- STABLE: score 변화 < 5, 위반 증가 없음, 토큰 변경 적음
- WARNING: score -10 이상 또는 MAJOR 위반 급증
- CRITICAL: CRITICAL 위반 발생 또는 score < 60

4.4 Drift 워크플로우(권장)
1) PR 또는 릴리즈 시점에:
   - 이전 기준점(마지막 release tag)의 토큰/리포트와 비교
2) DESIGN_DRIFT_LOG.md 업데이트
3) CRITICAL Drift면:
   - orchestrator가 자동으로 “Design Review Required” 상태로 Gate

4.5 Drift를 Gate로 연결하는 규칙(권장)
- 새 릴리즈에서:
  - CRITICAL 위반이 1개라도 있으면 차단
  - score_total이 10점 이상 하락하면 “승인 필요”로 전환
  - token diff가 특정 임계치 초과(예: color 30% 변경)면 “Design Decision 기록 필수”

4.6 v3.1+ 확장(선택)
- 시각적 회귀(Visual Regression):
  - Playwright(웹) 또는 Golden tests(Flutter)로 스크린샷 생성
  - 픽셀 diff/SSIM 등으로 drift 정량화
- 컴포넌트 카탈로그(Storybook/Widgetbook)와 연동

============================================================
END OF Design v3.0 Extension Pack
============================================================
