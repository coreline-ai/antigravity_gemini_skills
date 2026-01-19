# 📄 Product Requirement Document (PRD) v2

본 문서는 Universal Orchestration System v2의 **유일한 입력 문서**입니다.  
이 문서를 기준으로 플랫폼 판별, 아키텍처 설계, 개발, 감사가 자동 수행됩니다.

⚠️ 모호한 표현 금지  
⚠️ “알아서”, “적절히” 사용 금지  
⚠️ 사용자 관점 + 시스템 관점 모두 기술

---

## 0) Document Metadata (REQUIRED)

- Project Name:
- Version:
- Author:
- Date:
- Status: [DRAFT | FINAL]

---

## 1) Project Overview (REQUIRED)

### 1.1 Problem Statement
- 사용자가 겪고 있는 **구체적인 문제**를 서술하세요.
- 왜 기존 방식이 불편한지 명확히 기술하세요.

예시:
- 관리자가 여러 툴을 오가며 데이터를 확인해야 한다.
- 모바일에서 특정 기능을 사용할 수 없다.

---

### 1.2 Solution Summary
- 이 프로젝트가 문제를 **어떻게 해결하는지**를 요약하세요.
- 기술이 아니라 **행동/경험 중심**으로 작성하세요.

---

### 1.3 Target Users
- 주요 사용자 유형을 나열하세요.

예시:
- 일반 사용자
- 관리자
- 내부 운영자

---

## 2) Platform & Usage Context (CRITICAL)

⚠️ 이 섹션은 **플랫폼 판별(Web/App/Hybrid)**의 핵심 근거가 됩니다.

### 2.1 Expected Platforms
아래 항목 중 **해당되는 것을 모두 상세히 서술**하세요.

- 웹 브라우저에서 사용해야 하는가?
- 모바일 앱으로 설치되어야 하는가?
- 앱스토어 / 플레이스토어 배포가 필요한가?
- SEO, 검색 노출이 중요한가?
- 관리자 전용 대시보드가 필요한가?

---

### 2.2 Device & OS Requirements
- 사용 디바이스와 OS 요구사항을 명시하세요.

예시:
- Desktop Web (Chrome, Safari)
- Mobile Web
- Android / iOS
- 태블릿 지원 여부

---

### 2.3 Offline / Background / Permission Needs
해당되는 항목을 구체적으로 작성하세요.

- 오프라인에서도 동작해야 하는가?
- 백그라운드 실행이 필요한가?
- 권한이 필요한가?
  - Camera
  - Location
  - Storage
  - Bluetooth
  - Notification

---

## 3) Core Features (REQUIRED)

⚠️ 감사(Audit)는 이 섹션을 기준으로 PASS / FAIL을 판정합니다.

각 기능은 **반드시 독립적으로 검증 가능**해야 합니다.

---

### Feature 1
- Name:
- Description:
- User Flow:
  - Step 1:
  - Step 2:
- Success Criteria:
  - 어떤 상태가 되면 “완료”인가?

---

### Feature 2
(동일 형식으로 반복)

---

## 4) User Flows (RECOMMENDED)

대표적인 사용자 흐름을 **순서대로** 기술하세요.

예시:

~~~text
1. 사용자가 앱/웹에 접속한다
2. 로그인한다
3. 메인 화면에서 데이터를 조회한다
4. 특정 항목을 클릭한다
5. 결과를 저장하거나 공유한다
~~~

---

## 5) Data & Backend Requirements (IMPORTANT)

### 5.1 Data Types
- 어떤 데이터가 저장되어야 하는지 기술하세요.

예시:
- 사용자 정보
- 설정 값
- 로그 / 이력 데이터

---

### 5.2 Backend Logic
- 서버가 필요한지 여부를 명확히 하세요.

예시 질문:
- 인증이 필요한가?
- 데이터는 영구 저장되는가?
- 외부 API 연동이 있는가?

---

### 5.3 Performance / Scale Expectations
- 예상 사용자 수
- 트래픽 패턴
- 실시간성 요구 여부

---

## 6) Non-Functional Requirements (REQUIRED)

### 6.1 Performance
- 응답 시간 요구사항
- 초기 로딩 시간

---

### 6.2 Security
- 인증/인가 필요 여부
- 민감 정보 처리 여부

---

### 6.3 Accessibility / UX
- 접근성 요구사항
- 반응형 필요 여부

---

## 7) Constraints & Assumptions (IMPORTANT)

- 예산 제한
- 일정 제한
- 기술적 제약
- 반드시 사용해야 하는 기술이 있다면 명시

---

## 8) Out of Scope (RECOMMENDED)

이번 프로젝트에서 **하지 않을 것**을 명확히 적으세요.

예시:
- 결제 기능은 포함하지 않는다
- 관리자 페이지는 1차 범위에서 제외

---

## 9) Acceptance Criteria (CRITICAL)

이 프로젝트가 **성공적으로 완료되었다고 판단할 기준**을 명시하세요.

예시:
- 모든 Core Feature가 구현됨
- 감사(Audit) 결과 STATUS = PASS
- 빌드 및 실행 재현 가능

---

## 10) Notes / References (OPTIONAL)

- 참고 링크
- 유사 서비스
- 디자인 시안 링크
- 기타 특이사항

---

## END OF PRD
