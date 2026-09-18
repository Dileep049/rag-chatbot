# 📷 Screenshot Checklist — Citizen Assistance AI

This checklist outlines the recommended UI screenshots to capture for project reports, documentation, presentation slides, and portfolio showcases.

---

## 🖼️ User Interface Screenshots

- [ ] **1. Welcome Screen**:
  - **URL**: `http://localhost:3000`
  - **Description**: Main screen showing 🇮🇳 emblem logo, Citizen Assistance AI header, RAG badge, search input box with 🎤 microphone icon, and English/Telugu prompt suggestions.

- [ ] **2. English RAG Response & Source Card**:
  - **Action**: Ask *"My Aadhaar card is lost. What should I do?"*
  - **Description**: Show structured grounded steps and expanded `📄 Sources (1)` accordion card detailing document name (`aadhaar_official_guide.txt`), category (`aadhaar`), page (`2`), and section (`Section 1: Procedure for Lost Aadhaar Card`).

- [ ] **3. Multilingual Telugu Response (Native Script)**:
  - **Action**: Ask *"నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?"*
  - **Description**: Show grounded AI response rendered in Native Telugu script with Telugu source header.

- [ ] **4. Multilingual Telugu-English Phonetic Response**:
  - **Action**: Ask *"Ma amma pension ki em documents kavali?"*
  - **Description**: Show answer listing pension required documents retrieved from `pension_schemes_guide.txt`.

- [ ] **5. Voice Input Active State**:
  - **Action**: Click microphone 🎤 button.
  - **Description**: Show active `🔴 Listening (తెలుగు)...` badge and voice-to-text string populated inside the input box.

- [ ] **6. Follow-Up Question Sequence**:
  - **Action**: Ask *"What documents do I need?"* after lost Aadhaar question.
  - **Description**: Show contextual follow-up thread displaying conversation history and updated source citations.

- [ ] **7. Anti-Hallucination Guardrail (No-Information Response)**:
  - **Action**: Ask *"Who won the FIFA World Cup final in 2026?"*
  - **Description**: Show safe no-information refusal message: *"I could not find sufficient information in the available official documents to answer this question."*

---

## 🔐 Admin Dashboard Screenshots

- [ ] **8. Admin Login Page**:
  - **URL**: `http://localhost:3000` (click Admin Login -> `/login`)
  - **Description**: Admin authentication form showing Email (`admin@citizen.gov.in`), Password fields, submit button, and `Back to Citizen Assistant` link.

- [ ] **9. Admin Dashboard Hub**:
  - **URL**: `/admin` (Authenticated)
  - **Description**: Admin overview displaying indexed document list, chunk counts, upload timestamps, search filter, and document action buttons (Re-index, Delete).

- [ ] **10. Admin Document Upload**:
  - **Description**: Document upload modal / dropzone showing file selection, category selector dropdown (`Aadhaar`, `Pension`, `Police`, `Vehicle`, `PAN`, `Driving Licence`, `Government Schemes`), and upload button.

---

## 🛠️ System & Code Artifacts Screenshots

- [ ] **11. Full Test Suite Execution**:
  - **Command**: `python test_full_suite.py`
  - **Description**: Terminal output showing 21/21 passed tests (100% pass rate).

- [ ] **12. Swagger API Documentation**:
  - **URL**: `http://localhost:8000/docs`
  - **Description**: FastAPI interactive Swagger docs listing `/api/chat`, `/api/documents/*`, `/api/auth/*`, and `/health` endpoints.
