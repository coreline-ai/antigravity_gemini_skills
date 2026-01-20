# ✅ Design v3.0 Automation Pack (v3.0-A)
# 1) design_policy_check.ts 계약서 (File-based Contract)
# 2) 구현 전략(검사 규칙/패턴/스코어링/리포트)
# 3) Web(Tailwind) / Flutter 토큰 주입(Injection) 템플릿 전략

중요:
- 코드블럭 깨짐 방지를 위해 “이 문서 전체가 하나의 코드블럭”이며,
  내부에 ``` 또는 ~~~ 같은 중첩 펜스는 사용하지 않습니다.
- 아래 “FILE:” 섹션을 그대로 파일로 저장하면 됩니다.

============================================================
0) 추천 파일 배치
============================================================

PROJECT_ROOT/
- DESIGN_SYSTEM.md
- POLICY_RULES.md
- DESIGN_TOKENS.json
- DESIGN_AUDIT.md                 (자동 생성/갱신)
- .orchestrator/
  - state.json
  - design_policy_report.json     (자동 생성)
- .agent/skills/orchestrator/scripts/
  - design_policy_check.ts        (이번 문서의 대상)
- apps/
  - web/...
  - mobile/...

============================================================
1) design_policy_check.ts 계약서 (File-based Contract)
============================================================

FILE: .agent/skills/orchestrator/scripts/design_policy_check.ts

1.1 목적
- DESIGN_SYSTEM.md + POLICY_RULES.md + DESIGN_TOKENS.json을 “정책/토큰 계약”으로 해석한다.
- 코드베이스(apps/web, apps/mobile 등)를 스캔해서:
  - 토큰 우회(하드코딩 색상/간격/라운드/폰트)
  - 디자인 모드 위반(예: B2B_DENSE에서 과한 shadow)
  - 접근성 기본 체크(대비/터치 타겟은 MVP에서 부분)
  를 탐지한다.
- 결과를 “기계용 JSON 리포트”와 “사람용 DESIGN_AUDIT.md”로 기록한다.
- enforce_gates.ts가 이 결과를 읽어 실행을 차단할 수 있게 한다.

1.2 Inputs (읽기)
- Required
  - DESIGN_SYSTEM.md
  - POLICY_RULES.md
  - DESIGN_TOKENS.json
  - .orchestrator/state.json
- Optional (존재 시 스캔)
  - apps/web
  - apps/mobile
  - shared

1.3 Outputs (쓰기)
- Required
  - .orchestrator/design_policy_report.json
- Optional (사람용)
  - DESIGN_AUDIT.md (append 또는 overwrite; 운영 정책에 따라 선택)

1.4 Context(정책 평가 입력) 구성 규칙
- DESIGN_SYSTEM.md에서:
  - DESIGN_MODE
  - DESIGN_TONE
  - ACCESSIBILITY_LEVEL
- state.json에서:
  - MODE (DRY_RUN/EXECUTE)
  - CURRENT_PHASE
- DESIGN_TOKENS.json에서:
  - token key 목록
  - color/spacing/radius/typography/motion 카테고리별 값 목록

Context Example (in-memory):
- DESIGN_MODE=B2B_DENSE
- ACCESSIBILITY_LEVEL=WCAG_AA
- MODE=EXECUTE
- CURRENT_PHASE=2

1.5 Parsing 규칙 (MVP)
- DESIGN_SYSTEM.md:
  - “KEY: VALUE” 라인만 파싱 (대문자/언더스코어 key 권장)
- POLICY_RULES.md:
  - “RULE:” 블록 기반 파싱
  - WHEN / MUST / MUST_NOT / SEVERITY / RATIONALE 파싱
  - MVP에서는 MUST/MUST_NOT을 “검사 타입”으로 매핑(아래 구현 전략 참고)
- DESIGN_TOKENS.json:
  - JSON 파싱 후 token key 및 실제 값 인덱싱

1.6 스캔 대상 파일 타입(MVP)
- Web:
  - .ts .tsx .js .jsx .css .scss .md .json .yml .yaml .toml
- Flutter:
  - .dart .yaml .md .json
- 공통:
  - 2MB 초과 파일은 스킵(성능/오탐 방지)
  - node_modules, build, dist, .next, .dart_tool 등은 기본 제외

1.7 Exit Codes (고정)
- 0: PASS (위반 없음)
- 1: FAIL (위반 존재; 정상 동작)
- 2: ERROR (입력 누락/파싱 실패/권한 문제)

============================================================
2) 리포트 스키마 (design_policy_report.json)
============================================================

FILE: .orchestrator/design_policy_report.json

Schema (MVP):
- generated_at: ISO string
- status: PASS|FAIL
- score_total: 0..100
- score_breakdown:
  - token_compliance
  - visual_consistency
  - density_fitness
  - accessibility
  - motion_discipline
- rules_checked: number
- violations: array
  - rule_id
  - severity: CRITICAL|MAJOR|MINOR
  - category: TOKEN|DENSITY|A11Y|MOTION|CONSISTENCY
  - path
  - line (optional)
  - evidence (short snippet <= 160 chars)
  - suggestion (optional, 짧게; “강제”가 아니라 “힌트”)
  - context (DESIGN_MODE, MODE, PHASE)

============================================================
3) 정책-검사 매핑 (OPA-style → 정규식/휴리스틱) 구현 전략
============================================================

핵심 원칙:
- “정책 문서”는 사람이 합의하는 헌법
- “스크립트”는 그 정책을 기계적으로 집행하는 집행관

아래는 v3.0 MVP에 필요한 최소 검사기(Detector) 목록이다.

------------------------------------------------------------
3.1 Detector A: Token-Only Usage (가장 중요 / CRITICAL)
------------------------------------------------------------

목표:
- 하드코딩 색상/간격/라운드/폰트/모션 값이 코드에 존재하면 위반.

A-1) 색상 하드코딩 탐지(공통)
- 탐지 패턴(예시):
  - HEX: #RGB / #RRGGBB / #RRGGBBAA
  - rgb(), rgba(), hsl(), hsla()
  - Flutter: Color(0xFFxxxxxx), Color.fromARGB, Color.fromRGBO
- 허용 예외(Allowlist):
  - CSS var(--color-xxx), var(--token)
  - Tailwind 토큰 클래스(예: text-primary, bg-surface) — 단, arbitrary 값(bg-[#...])은 금지
  - Flutter: AppTheme.colors.primary 같은 토큰 참조(프로젝트에서 정한 래퍼)
- 대응 정책 RULE_ID:
  - DESIGN_TOKEN_ONLY_USAGE (CRITICAL)

A-2) 간격/크기 하드코딩 탐지(공통)
- 탐지 패턴(예시):
  - CSS: padding: 16px, margin: 12px, gap: 24px, border-radius: 12px
  - JS/TS style 객체: padding: 16, marginTop: 12
  - Tailwind arbitrary: p-[18px], m-[14px], rounded-[20px]
  - Flutter: EdgeInsets.all(16), EdgeInsets.only(left: 12), SizedBox(height: 24), BorderRadius.circular(12)
- 허용 예외:
  - spacing token 사용:
    - Web: var(--spacing-md) / theme spacing class(p-md 같은 프로젝트 규칙) / Tailwind config spacing
    - Flutter: AppTheme.spacing.md 같은 참조
- 대응 정책 RULE_ID:
  - DESIGN_TOKEN_ONLY_USAGE (CRITICAL)

A-3) 폰트 하드코딩 탐지
- 탐지 패턴:
  - CSS font-family: "Inter", "Pretendard" 등 문자열 직접 삽입
  - Flutter: TextStyle(fontFamily: 'Inter'), GoogleFonts.xxx 직접 사용
- 허용 예외:
  - typography token 참조만 허용
- 대응 정책 RULE_ID:
  - DESIGN_TOKEN_ONLY_USAGE (CRITICAL)

------------------------------------------------------------
3.2 Detector B: Mode-specific Density Rules (MAJOR)
------------------------------------------------------------

B-1) B2B_DENSE에서 Shadow 제한
- 탐지 패턴(예시):
  - Web: shadow-3xl, shadow-[...] , drop-shadow-...
  - CSS: box-shadow가 3개 이상 레이어, blur 과다(heuristic)
  - Flutter: BoxShadow blurRadius 큰 값(예: >= 24) 또는 여러 shadows
- 허용 범위(예시):
  - elevation.level1, level2만 허용
- 대응 RULE_ID:
  - B2B_DENSE_SHADOW_LIMIT (MAJOR)

B-2) B2B_MINIMAL에서 색상 수 제한
- 스캔 결과로 “서로 다른 색상 값”의 개수를 집계
  - (토큰 기반이면 token key 기준으로 집계)
- 제한(예시):
  - 3개 초과면 위반
- 대응 RULE_ID:
  - MINIMAL_COLOR_LIMIT (MAJOR)

------------------------------------------------------------
3.3 Detector C: Accessibility MVP (CRITICAL/MAJOR)
------------------------------------------------------------

MVP에서는 “완전한 대비 계산”은 어렵고,
다음 2단계를 권장한다.

C-1) Hard-coded text color + hard-coded bg color 조합 탐지
- 같은 파일/컴포넌트 내에서
  - text color와 bg color가 둘 다 하드코딩이면 “위험 플래그”
- Severity:
  - WCAG_AA 이상이면 MAJOR 또는 CRITICAL(정책에 따라)
- 대응 RULE_ID:
  - ACCESSIBILITY_CONTRAST_REQUIRED

C-2) 터치 타겟 최소 크기(휴리스틱)
- Web: 버튼 height/py 너무 작은 값 탐지(예: h-6, py-1 등)
- Flutter: SizedBox(height: < 40), constraints 작은 값 탐지
- Severity:
  - WCAG_AA면 MAJOR

------------------------------------------------------------
3.4 Detector D: Motion Discipline (MINOR)
------------------------------------------------------------

D-1) 승인되지 않은 애니메이션 탐지
- Web: transition-all 과다, duration 과다, keyframes 신규 정의 난립
- Flutter: AnimationController duration 과다, curve 난립
- 허용 예외:
  - DESIGN_SYSTEM.md에 명시된 duration/easing token만 사용
- 대응 RULE_ID:
  - UNAPPROVED_ANIMATION_FORBIDDEN (MINOR)

============================================================
4) 스코어링 모델 (자동 점수 계산)
============================================================

기본:
- score_total = 100에서 시작해서 위반에 따라 감점
- 카테고리별 부분 점수도 같이 계산

권장 가중치(MVP):
- CRITICAL 위반: -15점 (최대 -45점까지 누적; 이후는 FAIL로만 처리)
- MAJOR 위반: -6점
- MINOR 위반: -2점

카테고리 배분(100점 만점):
- Token Compliance: 30
- Visual Consistency: 20
- Density Fitness: 20
- Accessibility: 20
- Motion Discipline: 10

계산 예:
- Token 관련 CRITICAL 1개 발견 → Token Compliance에서 큰 감점, 총점 -15
- Density 관련 MAJOR 2개 → 총점 -12
- 총점 73이면 WARNING

판정:
- PASS: score_total >= 75 AND CRITICAL 위반 0
- FAIL: score_total < 60 OR CRITICAL 위반 >= 1
(이 기준은 DESIGN_SYSTEM.md에서 조절 가능하도록 해도 좋다)

============================================================
5) DESIGN_AUDIT.md 생성 규칙(사람용 리포트)
============================================================

FILE: DESIGN_AUDIT.md

권장 포맷:
- Timestamp
- Overall Score / Verdict
- Top Violations (최대 10개)
- Policy IDs
- Fix Suggestions (짧게)
- Evidence (path + snippet)

예시 섹션:
- STATUS: FAIL
- SCORE: 58
- CRITICAL:
  - DESIGN_TOKEN_ONLY_USAGE: apps/web/src/components/Button.tsx (hard-coded #2563EB)
- MAJOR:
  - B2B_DENSE_SHADOW_LIMIT: shadow-2xl detected …

============================================================
6) Web(Tailwind) 토큰 주입(Injection) 템플릿 전략
============================================================

목표:
- “토큰을 쓰는 게 더 쉽고 편하게” 만들어서 우회를 막는다.

6.1 단일 진실원
- DESIGN_TOKENS.json을 원본으로 두고,
  빌드 시 아래로 변환한다:
  - CSS Variables 파일
  - Tailwind theme 확장
  - (선택) TS 상수

6.2 CSS Variables 생성(권장 파일)
- apps/web/src/styles/tokens.css
- 예:
  :root { --color-primary: ...; --spacing-md: ...; }

6.3 Tailwind config 매핑
- tailwind.config.ts에:
  - theme.colors.primary = "var(--color-primary)"
  - theme.spacing.md = "var(--spacing-md)"
  - theme.borderRadius.md = "var(--radius-md)"

6.4 금지 패턴(Policy로 차단)
- bg-[#...], text-[#...], p-[17px], rounded-[13px] 같은 arbitrary values
- inline style에서 숫자 직접 사용

============================================================
7) Flutter 토큰 주입(Injection) 템플릿 전략
============================================================

목표:
- ThemeData/Token wrapper를 만들어 하드코딩을 원천 차단.

7.1 권장 생성 파일
- apps/mobile/lib/theme/design_tokens.dart
  - class DesignTokens { static const ... } 형태 또는 JSON 로드
- apps/mobile/lib/theme/app_theme.dart
  - ThemeData, ColorScheme, TextTheme를 토큰으로 생성

7.2 권장 사용 규칙(개발자 UX)
- EdgeInsets는 AppSpacing.md 같은 래퍼 사용
- BorderRadius는 AppRadius.md 사용
- TextStyle은 AppTypography.bodyMd 사용

7.3 금지 패턴(Policy로 차단)
- Color(0xFFxxxxxx)
- EdgeInsets.all(16)
- BorderRadius.circular(12)
- TextStyle(fontSize: 16)

============================================================
8) Gate 연동 권장 (v3.0)
============================================================

- design_policy_check.ts 실행 결과(status=FAIL)가 나오면:
  - enforce_gates.ts는 Execute를 차단해야 한다.
- 스냅샷이 활성화되어 있다면:
  - FAIL 시 마지막 PASS 스냅샷으로 롤백을 권장한다.

============================================================
9) MVP 실행 순서 (Design v3.0)
============================================================

1) (분석) DESIGN_SYSTEM.md / POLICY_RULES.md / DESIGN_TOKENS.json 준비
2) (검사) design_policy_check.ts 실행 → design_policy_report.json 생성
3) (게이트) enforce_gates.ts가 PASS/FAIL 반영
4) (리포트) DESIGN_AUDIT.md 갱신
5) (수정) 위반 수정 후 재검사

============================================================
END OF Design v3.0 Automation Pack
============================================================
