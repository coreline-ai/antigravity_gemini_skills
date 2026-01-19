# 🎨 Design Specification (DESIGN) v2

본 문서는 **UI / UX / Design System**에 대한 단일 기준 문서입니다.  
Universal Orchestration System v2에서 **감사(Audit) 대상 문서**로 사용됩니다.

⚠️ 구현 방식이 아니라 **사용자 경험과 시각 규칙**을 정의합니다.  
⚠️ “알아서 예쁘게” 금지, **규칙/토큰/근거 명시**

---

## 0) Document Metadata (REQUIRED)

- Project Name:
- Version:
- Author:
- Date:
- Status: [DRAFT | FINAL]

---

## 1) Design Goals (REQUIRED)

### 1.1 Experience Goals
- 사용자가 느껴야 하는 핵심 감정/인상

예시:
- 빠르고 신뢰감 있음
- 복잡하지만 정돈됨
- 가볍고 친근함

---

### 1.2 Design Principles
디자인 전반에 적용되는 원칙을 나열하세요.

예시:
- Clarity over Decoration
- Fewer Choices, Clear Actions
- Mobile First

---

## 2) Target Platforms & Form Factors (CRITICAL)

⚠️ 이 섹션은 **WEB / APP / HYBRID 디자인 분기 근거**로 사용됩니다.

- Desktop Web
- Mobile Web
- Android App
- iOS App
- Tablet 지원 여부

---

## 3) Information Architecture (IMPORTANT)

### 3.1 Screen / Page List
모든 화면을 나열하세요.

예시:
- Login
- Home
- Detail
- Settings
- Admin Dashboard

---

### 3.2 Navigation Structure
화면 간 이동 구조를 설명하세요.

예시:

~~~text
Login
 └─ Home
     ├─ List
     │   └─ Detail
     └─ Settings
~~~

---

## 4) Layout System (REQUIRED)

### 4.1 Grid & Spacing
- Grid 시스템 (예: 8px, 4dp)
- 최대 컨테이너 폭
- Breakpoint 기준

---

### 4.2 Responsive Rules (WEB)
- Desktop / Tablet / Mobile 전환 규칙
- 숨김/재배치 요소

---

## 5) Design Tokens (CRITICAL)

⚠️ Auditor는 이 섹션을 기준으로 **디자인 일관성**을 검사합니다.

### 5.1 Color Palette
- Primary:
- Secondary:
- Background:
- Text Primary / Secondary:
- Error / Warning / Success:

---

### 5.2 Typography
- Font Family:
- Base Font Size:
- Heading Scale (H1~H6):
- Line Height Rules:

---

### 5.3 Iconography
- Icon Style (Filled / Outline)
- Size 규칙
- 사용 금지 케이스

---

## 6) Component Guidelines (REQUIRED)

주요 UI 컴포넌트별 규칙을 정의하세요.

### Button
- Variants:
- Disabled Rules:
- Loading State:

---

### Input / Form
- Validation 표현 방식
- Error 메시지 규칙

---

### Modal / Dialog
- 사용 조건
- 닫기 규칙

---

## 7) Interaction & Motion (RECOMMENDED)

- 애니메이션 사용 여부
- Transition Duration
- Motion 원칙

---

## 8) Accessibility (IMPORTANT)

- Color Contrast 기준
- 키보드 접근성
- Screen Reader 고려사항

---

## 9) Design Validation Checklist (AUDIT BASE)

Auditor 검사용 체크리스트:

- [ ] 모든 화면이 정의되어 있음
- [ ] 색상/폰트 토큰이 일관됨
- [ ] 플랫폼 가이드 위반 없음
- [ ] 접근성 고려됨

---

## 10) References (OPTIONAL)

- Figma 링크
- 디자인 시안
- 레퍼런스 서비스

---

## END OF DESIGN SPEC
