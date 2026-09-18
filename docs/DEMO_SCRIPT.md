# 🎬 Citizen Assistance AI — Live Demo & Presentation Script

This script provides a step-by-step 5 to 10-minute live demonstration flow for project evaluations, viva presentations, and client demos.

---

## 🕒 Live Demo Sequence (7 Minutes)

### Phase 1: Introduction & Welcome Screen (1 Minute)
1. **Presenter Statement**:
   > *"Good morning/afternoon. Today I am presenting **Citizen Assistance AI**, a grounded multilingual RAG assistant built to help citizens navigate official Indian government services, procedures, police complaints, pensions, Aadhaar, vehicle procedures, PAN cards, driving licences, and government schemes."*
2. **Show UI**:
   - Open `http://localhost:3000`.
   - Point out the clean **ChatGPT-style interface**, the 🇮🇳 emblem header, RAG badge, and interactive English & Telugu example prompts.
   - Explain: *"Notice there is no forced category sidebar. Citizens simply type or speak their question naturally."*

---

### Phase 2: Core English RAG Retrieval & Source Verification (1.5 Minutes)
1. **Action**: Click or type:
   `"My Aadhaar card is lost. What should I do?"`
2. **Observe Output**:
   - Show typing indicator: *"Searching official information... ● ● ●"*
   - AI response lists direct procedural steps (myAadhaar portal, EID/UID retrieval, PVC card ordering).
3. **Inspect Sources**:
   - Click **`📄 Sources (1)`** accordion button.
   - Show source metadata card:
     - Document: `aadhaar_official_guide.txt`
     - Category: `aadhaar`
     - Page: `2`
     - Section: `Section 1: Procedure for Lost Aadhaar Card`
   - Explain: *"Unlike standard ChatGPT, our response is grounded in an actual uploaded official document with exact page and section citations."*

---

### Phase 3: Follow-Up Questions & Conversation Context (1 Minute)
1. **Action**: Type follow-up:
   `"What documents do I need?"`
2. **Observe Output**:
   - Show contextual understanding: AI understands *"documents needed"* refers to the lost Aadhaar process mentioned in the previous turn.
   - Point out that source cards update dynamically for the follow-up turn.

---

### Phase 4: Multilingual Support (Telugu & Telugu-English) (1.5 Minutes)
1. **Action (Telugu Script)**: Click **+ New Chat**, then type:
   `"నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?"`
2. **Observe Output**:
   - AI responds in Telugu with official grounded steps retrieved from the English knowledge base.
3. **Action (Telugu-English Mixed)**: Type:
   `"Ma amma pension ki em documents kavali?"`
4. **Observe Output**:
   - System automatically detects pension intent, clears Aadhaar context, retrieves `pension_schemes_guide.txt`, and lists required documents (Aadhaar, income certificate, bank passbook, age proof).

---

### Phase 5: Voice Input Demonstration (1 Minute)
1. **Action**: Click the Microphone icon 🎤 inside the input box.
2. **Observe Output**:
   - Badge changes to `🔴 Listening (తెలుగు)...`
   - Speak: *"Police naa bike teesukunnaru. Ela release cheyinchukovali?"*
   - Show that recognized speech appears as text in the input box.
   - Click **Send**.
   - Show grounded response listing police complaint steps and court superdari release procedures.

---

### Phase 6: Anti-Hallucination Guardrail Demo (0.5 Minutes)
1. **Action**: Type an out-of-domain query:
   `"Who won the FIFA World Cup final in 2026?"`
2. **Observe Output**:
   - RAG relevance threshold triggers:
     `"I could not find sufficient information in the available official documents to answer this question."`
   - Explain: *"Because this information is absent from our official document knowledge base, the AI refuses to fabricate or hallucinate an answer."*

---

### Phase 7: Admin Document Management & RBAC Security (1 Minute)
1. **Action**: Click **Admin Login** in header -> navigate to `/login`.
2. **Authenticate**:
   - Email: `admin@citizen.gov.in`
   - Password: `Admin@123456`
3. **Demonstrate Admin Hub**:
   - Show document table listing indexed files, categories, chunk counts, and upload dates.
   - Drag & drop a new PDF/TXT file into the upload dropzone.
   - Click **Upload & Index Document**.
   - Show real-time indexing success status and updated chunk count.
   - Explain: *"New official documents become retrievable instantly without rebuilding or restarting the application."*
   - Click **Logout**.

---

## 📋 Recommended Demo Questions Summary Table

| Category | Demo Question | Expected Source Document |
| :--- | :--- | :--- |
| **Aadhaar** | *"My Aadhaar card is lost. What should I do?"* | `aadhaar_official_guide.txt` (Page 2) |
| **Follow-up** | *"What documents do I need?"* | `aadhaar_official_guide.txt` (Page 2) |
| **Telugu Script** | *"నా ఆధార్ కార్డు పోయింది. నేను ఏం చేయాలి?"* | `aadhaar_official_guide.txt` (Page 2) |
| **Telugu-English** | *"Ma amma pension ki em documents kavali?"* | `pension_schemes_guide.txt` (Page 3) |
| **Vehicle / Police** | *"Police naa bike teesukunnaru. Ela release cheyinchukovali?"* | `police_complaint_and_fir_guide.txt` (Page 2) |
| **Driving Licence** | *"My driving licence is lost. What is the procedure?"* | `driving_licence_official_guide.txt` (Page 2) |
| **Out-of-Domain** | *"Who won the FIFA World Cup final in 2026?"* | Zero Sources (No-Information Trigger) |
