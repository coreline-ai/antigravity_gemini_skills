# 🎨 DESIGN SYSTEM v3.0
## Design-as-Policy · Design-as-Contract · Design-as-Automation

본 문서는 Universal Orchestration v3.0의 **디자인 특화 핵심 헌장**이다.
디자인을 “감각”이나 “산출물”이 아니라, **정책·결정·검증 가능한 계약**으로 다룬다.

============================================================
PART 1. DESIGN_SYSTEM.md v3.0 (헌법)
============================================================

## 1.1 목적 (Purpose)
- 디자인 일관성을 자동으로 유지한다
- 프로젝트 성격에 맞는 미감을 시스템적으로 고정한다
- 사람/AI/코드가 디자인을 임의로 훼손하지 못하게 한다

디자인은 결과물이 아니라 **시스템 자산**이다.

---

## 1.2 Design Identity (필수 선언)

이 섹션은 프로젝트마다 반드시 채워야 한다.

- DESIGN_MODE: 
  - 선택값: B2B_DENSE | B2B_MINIMAL | CONSUMER_FRIENDLY | MARKETING_EXPRESSIVE | DEVELOPER_TOOL
- DESIGN_TONE:
  - 예: professional, neutral, calm, energetic, playful
- PRIMARY_CONTEXT:
  - admin | dashboard | content | marketing | utility
- ACCESSIBILITY_LEVEL:
  - WCAG_AA | WCAG_AAA

---

## 1.3 Design Principles (핵심 원칙)

아래 원칙은 모든 디자인 판단의 상위 규칙이다.

1. Consistency over Creativity  
   - 새로움보다 일관성을 우선한다.
2. Density follows Purpose  
   - 정보 밀도는 사용 목적에 따라 결정한다.
3. Tokens over Hardcode  
   - 모든 시각적 결정은 토큰을 통해서만 이뤄진다.
4. Auditability  
   - 모든 디자인은 검증 가능해야 한다.

---

## 1.4 Forbidden Practices (절대 금지)

- 임의 색상/폰트/간격 하드코딩
- 디자인 토큰 우회 사용
- 승인되지 않은 애니메이션 추가
- 디자인 모드와 불일치하는 컴포넌트 도입

---

## 1.5 Design Decision Ledger 연동

모든 주요 디자인 결정은 DESIGN_DECISIONS.md에 기록되어야 한다.

예:
- 왜 Dense UI를 선택했는가
- 왜 그림자 depth를 낮췄는가
- 왜 primary color 사용을 제한했는가

============================================================
PART 2. DESIGN POLICY RULES (OPA-style 초안)
============================================================

정책은 “허용/금지”만 결정한다.
미적 판단이나 대안 제시는 하지 않는다.

---

## POLICY RULE FORMAT

각 정책은 아래 구조를 따른다.

- RULE_ID
- SEVERITY: CRITICAL | MAJOR | MINOR
- WHEN: (조건)
- MUST / MUST_NOT: (강제/금지)
- RATIONALE: (이유)

---

## POLICY SET v3.0 (MVP)

### RULE: DESIGN_TOKEN_ONLY_USAGE
- SEVERITY: CRITICAL
- WHEN:
  - ALWAYS
- MUST_NOT:
  - Hard-coded color, font, spacing values
- RATIONALE:
  - 토큰 우회는 디자인 시스템 붕괴의 시작이다.

---

### RULE: B2B_DENSE_SHADOW_LIMIT
- SEVERITY: MAJOR
- WHEN:
  - DESIGN_MODE == B2B_DENSE
- MUST_NOT:
  - Shadow depth greater than level 2
- RATIONALE:
  - Dense UI에서 과한 그림자는 가독성을 해친다.

---

### RULE: MINIMAL_COLOR_LIMIT
- SEVERITY: MAJOR
- WHEN:
  - DESIGN_MODE == B2B_MINIMAL
- MUST_NOT:
  - More than 3 distinct UI colors
- RATIONALE:
  - Minimal UI는 색상 절제가 핵심이다.

---

### RULE: ACCESSIBILITY_CONTRAST_REQUIRED
- SEVERITY: CRITICAL
- WHEN:
  - ACCESSIBILITY_LEVEL >= WCAG_AA
- MUST:
  - Text contrast ratio >= 4.5:1
- RATIONALE:
  - 접근성은 선택이 아니라 기본 요건이다.

---

### RULE: UNAPPROVED_ANIMATION_FORBIDDEN
- SEVERITY: MINOR
- WHEN:
  - ALWAYS
- MUST_NOT:
  - Animation not defined in DESIGN_SYSTEM.md
- RATIONALE:
  - 무분별한 모션은 UX 일관성을 깨뜨린다.

============================================================
PART 3. DESIGN TOKEN SCHEMA (Web + Flutter 공용)
============================================================

토큰은 **디자인의 단일 진실원(Source of Truth)** 이다.

---

## 3.1 Token Categories

- color.*
- typography.*
- spacing.*
- radius.*
- elevation.*
- motion.*

---

## 3.2 Canonical Token Schema (JSON 개념)

color.primary
color.secondary
color.background
color.surface
color.text.primary
color.text.secondary

typography.font.family
typography.font.size.sm
typography.font.size.md
typography.font.size.lg
typography.font.weight.regular
typography.font.weight.bold

spacing.xs
spacing.sm
spacing.md
spacing.lg
spacing.xl

radius.sm
radius.md
radius.lg

elevation.level1
elevation.level2
elevation.level3

motion.duration.fast
motion.duration.normal
motion.easing.standard

---

## 3.3 Web Mapping Rules

- CSS Variables:
  - --color-primary
  - --spacing-md
- Tailwind:
  - theme.colors.primary
  - theme.spacing.md
- Direct hex/px/em 사용 금지

---

## 3.4 Flutter Mapping Rules

- ThemeData.colorScheme
- TextTheme
- EdgeInsets via spacing tokens
- BorderRadius via radius tokens
- 직접 숫자 사용 금지 (예: EdgeInsets.all(16) 금지)

============================================================
PART 4. DESIGN AUDITOR (Checklist + Scoring)
============================================================

Design Auditor는 디자인 품질을 **정량화**한다.

---

## 4.1 Design Audit Checklist

### Token Integrity
- 모든 색상이 토큰을 통해 정의되었는가?
- 폰트/간격/라운드 값 하드코딩이 없는가?

### Visual Consistency
- 동일 컴포넌트가 동일 스타일을 유지하는가?
- 그림자/테두리 규칙이 일관적인가?

### Density & Hierarchy
- 정보 밀도가 DESIGN_MODE에 부합하는가?
- 시각적 우선순위가 명확한가?

### Accessibility
- 텍스트 대비 충족 여부
- 터치 타겟 최소 크기 충족 여부

### Motion Discipline
- 애니메이션이 정책에 정의된 범위 내인가?
- 불필요한 모션이 없는가?

---

## 4.2 Design Quality Score Model (100점 만점)

- Token Compliance: 30점
- Visual Consistency: 20점
- Density Fitness: 20점
- Accessibility: 20점
- Motion Discipline: 10점

총점 = 100점

---

## 4.3 Score Interpretation

- 90 ~ 100: EXCELLENT (시스템 준수)
- 75 ~ 89: GOOD (경미한 개선 필요)
- 60 ~ 74: WARNING (디자인 부채 누적)
- < 60: FAIL (시스템 위반)

---

## 4.4 Audit Result Output (DESIGN_AUDIT.md)

반드시 다음을 포함해야 한다:
- 총점
- FAIL 항목 목록
- 위반 Policy ID
- 개선 권고 (설명용, 강제 아님)

============================================================
FINAL STATEMENT
============================================================

Design v3.0은 “잘 만든 디자인”이 아니라  
“**망가지지 않는 디자인 시스템**”을 만든다.

END OF DESIGN v3.0 SYSTEM
