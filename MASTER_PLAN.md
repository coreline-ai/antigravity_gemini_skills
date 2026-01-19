# MASTER PLAN

## 1. Project Identity
- PLATFORM_MODE: WEB
- PRIMARY_TYPE: NEXTJS
- LANGUAGE: TypeScript

## 2. Platform & Repo Flags
- BACKEND_REQUIRED: NO
- REPO_LAYOUT: APPS_SPLIT
- PACKAGE_MANAGER: pnpm

## 3. Tech Stack (Pinned Versions)
- Frontend:
  - Framework: Next.js 14.2 (App Router)
  - UI Library: React 18.3
  - Styling: Tailwind CSS 3.4
  - State Management: Zustand 4.5 (Lightweight for local state)
- Backend:
  - None (Client-side functionality only)
- Database:
  - None (Browser LocalStorage / IndexedDB only)
- Runtime:
  - Node.js 20.x (LTS)
- Tooling:
  - Biome 1.8 (Fast Lint/Format) or ESLint/Prettier
  - TypeScript 5.5

## 4. Platform Detection Evidence
- WEB_SCORE: 0 (Initial PRD)
- APP_SCORE: 2 (Initial PRD)
- EVIDENCE:
  - Initial PRD score was insufficient (Gap Detected).
  - **Gap-driven Q&A Executed:**
    - Q1 (Target): A (Browser/Web focus) -> **Determines WEB Mode**
    - Q2 (Server): A (Local storage only) -> **Determines BACKEND_REQUIRED = NO**
    - Q3 (Deploy): A (Web deployment)
  - Result: Pure Web Application using Local Storage.

## 5. Architecture
- Design Pattern:
  - Atomic Design (components/atoms, molecules, organisms)
  - Service Layer Pattern (even for LocalStorage, to abstract data access)
- Folder Structure Tree:
  ```
  apps/
    web/
      src/
        components/  # UI Components
        lib/         # Utilities
        services/    # Storage Services (LocalStorage wrapper)
        store/       # State Management (Zustand)
        app/         # Next.js App Router
  ```

## 6. Implementation Tasks
### Phase 1 – Setup
- Initialize `apps/web` with Next.js 14
- Setup Tailwind CSS
- Setup generic Layout (Header, Main)

### Phase 2 – Core Logic
- Implement `MemoService` (CRUD with LocalStorage)
- Implement `useMemoStore` (Zustand)
- Feature: Create Memo
- Feature: Delete Memo
- Feature: Edit Memo

### Phase 3 – UI / UX
- Memo List View (Grid/List)
- Memo Detail/Edit Modal or Page
- Responsive Design (Mobile/Desktop friendly)

## 7. Risks & Fallback
- Risk: Data loss if browser cache is cleared.
- Fallback Strategy: None required as per Q2-A (Local only accepted), but consider generating a JSON export feature as a future bonus.
