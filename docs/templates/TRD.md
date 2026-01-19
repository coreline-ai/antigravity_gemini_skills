# 🛠️ Technical Requirement Document (TRD) v2

본 문서는 **구현을 위한 기술적 요구사항의 최종 기준**입니다.  
PRD / DESIGN을 해석하여 **개발자가 바로 코딩 가능한 수준**으로 명확히 기술합니다.

⚠️ 모호한 표현 금지  
⚠️ 라이브러리/버전/구조 명시 필수  
⚠️ MASTER_PLAN.md 생성의 핵심 입력

---

## 0) Document Metadata (REQUIRED)

- Project Name:
- Version:
- Author:
- Date:
- Status: [DRAFT | FINAL]

---

## 1) System Overview (REQUIRED)

### 1.1 Architecture Summary
- 전체 시스템 구조 요약

예시:
- Client(Web/App)
- Backend API
- Database
- External Services

---

### 1.2 Platform Mode
- PLATFORM_MODE: [WEB | APP | HYBRID]
- PRIMARY_TYPE: [NEXTJS | FLUTTER | ANDROID | IOS]

---

## 2) Tech Stack (CRITICAL)

⚠️ Auditor / Analyst는 이 섹션을 기준으로 기술 위반을 판단합니다.

### 2.1 Frontend
- Framework:
- Language:
- State Management:
- Build Tool:

---

### 2.2 Backend
- Framework:
- Language:
- API Style (REST / GraphQL):
- Auth Strategy:

---

### 2.3 Database
- Type (SQL / NoSQL):
- Engine:
- Migration Strategy:

---

### 2.4 Runtime & Tooling
- Node / Flutter / JDK Version:
- Package Manager:
- CI / Build Tool:

---

## 3) Repository & Folder Structure (REQUIRED)

### 3.1 Repo Layout
- SINGLE_ROOT or APPS_SPLIT

---

### 3.2 Folder Tree

~~~text
apps/
  web/
    src/
      ui/
      services/
      store/
  mobile/
    lib/
      screens/
      widgets/
~~~

---

## 4) Data Model (IMPORTANT)

### 4.1 Entities
- Entity Name:
- Fields:
- Relations:

---

### 4.2 API Contracts
각 API의 입력/출력을 정의하세요.

~~~json
{
  "request": {},
  "response": {}
}
~~~

---

## 5) Core Logic & Flows (REQUIRED)

PRD의 각 Feature에 대응하는 기술 흐름을 기술하세요.

### Feature A – Technical Flow
- Trigger:
- Processing Steps:
- Output:

---

## 6) Error Handling & Edge Cases (IMPORTANT)

- 예상 오류 시나리오
- 재시도 / 폴백 전략

---

## 7) Performance Requirements (REQUIRED)

- Response Time SLA:
- Caching Strategy:
- Concurrency 고려사항:

---

## 8) Security Requirements (CRITICAL)

- Authentication
- Authorization
- Data Protection
- Secret Management

---

## 9) Testing Strategy (IMPORTANT)

- Unit Test 범위
- Integration Test 범위
- E2E Test 여부

---

## 10) Deployment & Build (REQUIRED)

- Build Command:
- Environment Variables:
- Release Strategy:

---

## 11) Technical Constraints & Assumptions

- 필수 기술
- 금지 기술
- 환경 제약

---

## 12) Audit Readiness Checklist

- [ ] PRD 기능 전부 기술적으로 매핑됨
- [ ] DESIGN 규칙 위반 없음
- [ ] 빌드/실행 재현 가능
- [ ] 버전 고정 완료

---

## END OF TRD
