# Allergy-Aware Intelligent Veterinary Decision Support System

## Goal

Build a full-stack, AI-powered veterinary decision support platform for dogs that integrates allergy-aware rule engines, multimodal LLM reasoning, environmental APIs, and structured medical records — all under an **Allergy-First Decision Pipeline**.

> [!IMPORTANT]
> **Project Type:** Full-Stack (WEB frontend + PYTHON backend)
> **Primary Agents:** `backend-specialist` (FastAPI) + `frontend-specialist` (Next.js)
> **Core Constraint:** No module generates output without querying allergy data first.

---

## Current State

| Component | Status | Details |
|-----------|--------|---------|
| **Backend** | 🟡 Bare skeleton | `main.py` (Hello World), `pyproject.toml` (Python 3.14, no deps) |
| **Frontend** | 🟡 Fresh scaffold | Next.js 16 + Tailwind v4 + ShadCN UI — default page only |
| **Database** | 🔴 Not started | No PostgreSQL, no models, no migrations |
| **AI/LLM** | 🔴 Not started | No Gemini, no LangChain, no prompt manager |
| **Infra** | 🔴 Not started | No Docker, no Redis, no Celery |

---

## Success Criteria

| # | Criteria | Measurable Outcome |
|---|----------|-------------------|
| 1 | Dog profiles with allergies | CRUD → 200 OK, allergies persist in PostgreSQL |
| 2 | Vaccination filtering | Given allergies → Safe / Conditional / Unsafe classification |
| 3 | AI Diet Chatbot | breed + age + weight + allergies → allergy-filtered meal plan via Gemini |
| 4 | Environmental Risk | location + allergies → risk score from external APIs |
| 5 | Multimodal FIR Engine | image + text + breed + allergies → structured FIR JSON with urgency |
| 6 | Allergy-First Pipeline | Every module queries allergy data before generating output |
| 7 | Response time < 3s | Excluding external API delays |

---

## Tech Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Frontend** | Next.js 16 (App Router) + TypeScript | Already scaffolded, modern SSR, PRD-specified |
| **Styling** | Tailwind CSS v4 + ShadCN UI | Already installed, rapid premium UI |
| **Forms** | React Hook Form + Zod | Type-safe validation, PRD-specified |
| **Backend** | FastAPI (Python 3.12+) | Async, Pydantic-native, PRD-specified |
| **ORM** | SQLAlchemy 2.0 + Alembic | Type-safe ORM, migration support |
| **Database** | PostgreSQL 16 | Relational, PRD-specified |
| **Cache/Queue** | Redis + Celery | Async tasks (LLM calls), caching |
| **AI/LLM** | Google Gemini + LangChain | Multimodal capable, PRD-specified |
| **Vision** | Gemini Vision (multimodal) | Image analysis, replacing CLIP/OpenCV complexity |
| **Env APIs** | OpenWeather API, AQI API, Pollen API | Environmental risk data |
| **Auth** | NextAuth.js (v5) | JWT-based sessions, open-source |
| **Infra** | Docker + Docker Compose | Local dev parity |

---

## File Structure

```
Mini_Proj/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry + CORS
│   │   ├── config.py                  # Settings via pydantic-settings
│   │   ├── database.py                # Async DB session & engine
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── dog.py
│   │   │   ├── allergy.py
│   │   │   ├── vaccination.py
│   │   │   └── fir.py
│   │   ├── schemas/                   # Pydantic I/O schemas
│   │   │   ├── dog.py
│   │   │   ├── allergy.py
│   │   │   ├── vaccination.py
│   │   │   └── fir.py
│   │   ├── routers/                   # API route handlers
│   │   │   ├── dogs.py
│   │   │   ├── allergies.py
│   │   │   ├── vaccinations.py
│   │   │   ├── diet.py
│   │   │   ├── environment.py
│   │   │   └── fir.py
│   │   ├── services/                  # Business logic
│   │   │   ├── allergy_filter.py      # Core allergy constraint engine
│   │   │   ├── vaccination_engine.py
│   │   │   ├── diet_planner.py
│   │   │   ├── environment_risk.py
│   │   │   └── fir_generator.py
│   │   ├── ai/                        # AI orchestration
│   │   │   ├── prompt_manager.py      # Centralized prompt templates
│   │   │   ├── llm_client.py          # Gemini wrapper
│   │   │   ├── vision_pipeline.py     # Image processing via Gemini Vision
│   │   │   └── chains.py             # LangChain chains
│   │   └── middleware/
│   │       └── allergy_middleware.py   # Allergy-first validation layer
│   ├── alembic/                       # DB migrations
│   ├── tests/
│   │   ├── test_dogs.py
│   │   ├── test_allergies.py
│   │   ├── test_vaccination_engine.py
│   │   ├── test_diet_planner.py
│   │   └── test_fir_generator.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── alembic.ini
├── frontend/
│   ├── app/
│   │   ├── layout.tsx                 # Root layout + global providers
│   │   ├── page.tsx                   # Dashboard landing
│   │   ├── dogs/
│   │   │   ├── page.tsx               # Dog list
│   │   │   └── [id]/page.tsx          # Dog profile detail
│   │   ├── vaccinations/
│   │   │   └── page.tsx               # Vaccination report
│   │   ├── diet/
│   │   │   └── page.tsx               # Diet chatbot
│   │   ├── environment/
│   │   │   └── page.tsx               # Environmental risk dashboard
│   │   └── fir/
│   │       └── page.tsx               # FIR generator
│   ├── components/
│   │   ├── ui/                        # ShadCN base components
│   │   ├── dog-profile-form.tsx
│   │   ├── allergy-selector.tsx
│   │   ├── vaccination-report.tsx
│   │   ├── diet-chat.tsx
│   │   ├── risk-dashboard.tsx
│   │   └── fir-form.tsx
│   ├── lib/
│   │   ├── api.ts                     # Backend API client (fetch wrapper)
│   │   └── utils.ts
│   ├── types/
│   │   └── index.ts                   # Shared TypeScript types
│   ├── package.json
│   └── tailwind.config.ts
├── docker-compose.yml
├── context.md
├── prd.md
└── PLAN-vet-allergy-system.md
```

---

## Task Breakdown

### Phase 1: Foundation (P0) — `backend-specialist`

> **Skills:** `database-design`, `api-patterns`, `python-patterns`

- [ ] **T1: FastAPI Project Scaffolding**
  - INPUT: Current bare `backend/main.py`
  - OUTPUT: FastAPI app with `requirements.txt`, `app/main.py` (CORS, health endpoint), `app/config.py` (pydantic-settings), `app/database.py` (async SQLAlchemy engine)
  - VERIFY: `pip install -r requirements.txt && uvicorn app.main:app` → `GET /health` returns `200`
  - AGENT: `backend-specialist`

- [ ] **T2: Database Models + Migrations**
  - INPUT: Data model from `context.md` — Dog, Allergy, Vaccination, FIR, EnvironmentalLog
  - OUTPUT: SQLAlchemy 2.0 models in `app/models/`, Alembic config + initial migration, Pydantic schemas in `app/schemas/`
  - VERIFY: `alembic upgrade head` → tables created in PostgreSQL, `alembic downgrade -1` → clean rollback
  - AGENT: `backend-specialist`
  - DEPENDS: T1

- [ ] **T3: Core Allergy Constraint Engine**
  - INPUT: Allergy model, allergy-first design philosophy
  - OUTPUT: `app/services/allergy_filter.py` — queries a dog's allergies, applies exclusion filtering, logs every constraint decision
  - VERIFY: Unit test → dog with "chicken" allergy → filter returns items excluding chicken
  - AGENT: `backend-specialist`
  - DEPENDS: T2

- [ ] **T4: Dog Profile CRUD API**
  - INPUT: Dog + Allergy models and schemas
  - OUTPUT: `app/routers/dogs.py`, `app/routers/allergies.py` — full CRUD endpoints with pagination
  - VERIFY: `POST /dogs` → 201, `GET /dogs/{id}` → 200 with allergies, `PUT /dogs/{id}/allergies` → 200
  - AGENT: `backend-specialist`
  - DEPENDS: T2, T3

---

### Phase 2: Core Modules (P1) — `backend-specialist`

> **Skills:** `api-patterns`, `python-patterns`

- [ ] **T5: Vaccination Filtering Module**
  - INPUT: Allergy data, vaccination rules (contraindication matrix)
  - OUTPUT: `app/services/vaccination_engine.py` (rule-based engine), `app/routers/vaccinations.py`
  - VERIFY: Dog with "egg" allergy → vaccine with egg excipient = "Unsafe", others = "Safe"
  - AGENT: `backend-specialist`
  - DEPENDS: T3, T4

- [ ] **T6: AI Diet Planner (LLM Integration)**
  - INPUT: Breed, age, weight, food allergies
  - OUTPUT: `app/ai/prompt_manager.py`, `app/ai/llm_client.py` (Gemini wrapper), `app/services/diet_planner.py`, `app/routers/diet.py`
  - VERIFY: `POST /diet/plan` with breed="Labrador", allergies=["chicken"] → structured JSON meal plan without chicken + disclaimer
  - AGENT: `backend-specialist`
  - DEPENDS: T3, T4

- [ ] **T7: Environmental Risk Module**
  - INPUT: Location coordinates, environmental allergies from dog profile
  - OUTPUT: `app/services/environment_risk.py` (API aggregation + risk scoring), `app/routers/environment.py`
  - VERIFY: `POST /environment/risk` with lat/lng → risk score + activity guidance JSON
  - AGENT: `backend-specialist`
  - DEPENDS: T3, T4

- [ ] **T8: Multimodal FIR Engine**
  - INPUT: Image upload, text description, breed metadata, allergy profile
  - OUTPUT: `app/ai/vision_pipeline.py` (Gemini Vision), `app/ai/chains.py` (LangChain), `app/services/fir_generator.py`, `app/routers/fir.py`
  - VERIFY: `POST /fir/generate` with image + breed + allergies → structured FIR JSON with urgency level + disclaimer
  - AGENT: `backend-specialist`
  - DEPENDS: T3, T4, T6 (shares prompt_manager + llm_client)

---

### Phase 3: Frontend (P2) — `frontend-specialist`

> **Skills:** `frontend-design`, `react-best-practices`, `tailwind-patterns`

- [ ] **T9: Frontend Architecture Setup**
  - INPUT: Existing Next.js 16 scaffold
  - OUTPUT: API client (`lib/api.ts`), shared types (`types/index.ts`), global layout with navigation sidebar, React Hook Form + Zod installed
  - VERIFY: `pnpm dev` → renders dashboard with working navigation at `localhost:3000`
  - AGENT: `frontend-specialist`
  - DEPENDS: T4 (needs API contract)

- [ ] **T10: Dashboard + Dog Profile UI**
  - INPUT: API from T4
  - OUTPUT: Dashboard landing page, Dog list page, Dog profile detail page with allergy checkbox selector
  - VERIFY: Create dog with allergies in UI → data persisted via API → visible on dashboard
  - AGENT: `frontend-specialist`
  - DEPENDS: T9

- [ ] **T11: Vaccination Report UI**
  - INPUT: API from T5
  - OUTPUT: Vaccination page showing Safe (green) / Conditional (amber) / Unsafe (red) classification per vaccine
  - VERIFY: Select dog with allergies → vaccination report renders with correct color-coded statuses
  - AGENT: `frontend-specialist`
  - DEPENDS: T9, T5

- [ ] **T12: Diet Chatbot UI**
  - INPUT: API from T6
  - OUTPUT: Chat-style interface for diet planning with streaming response display, structured meal plan card
  - VERIFY: Submit breed + weight + age → chat displays allergy-filtered meal plan
  - AGENT: `frontend-specialist`
  - DEPENDS: T9, T6

- [ ] **T13: Environmental Risk Dashboard**
  - INPUT: API from T7
  - OUTPUT: Risk score gauge visualization, activity guidance cards, location input (manual or geolocation)
  - VERIFY: Enter location → dashboard renders with AQI, pollen, humidity data + risk score
  - AGENT: `frontend-specialist`
  - DEPENDS: T9, T7

- [ ] **T14: FIR Generator UI**
  - INPUT: API from T8
  - OUTPUT: Image upload form with drag-drop, text description input, structured FIR report display with urgency badge
  - VERIFY: Upload image + describe symptoms → FIR report displays with urgency level + disclaimer
  - AGENT: `frontend-specialist`
  - DEPENDS: T9, T8

---

### Phase 4: Integration & Infrastructure (P3)

- [ ] **T15: Docker Compose Setup**
  - INPUT: Backend + Frontend + PostgreSQL + Redis
  - OUTPUT: `docker-compose.yml` with all services, `backend/Dockerfile`, health checks
  - VERIFY: `docker compose up` → all services healthy, frontend at `:3000` can reach backend at `:8000`
  - AGENT: `backend-specialist`
  - DEPENDS: T1–T14

- [ ] **T16: Backend Tests Suite**
  - INPUT: All backend routers + services
  - OUTPUT: `backend/tests/` — pytest tests for CRUD, allergy filtering, vaccination engine, diet planner input validation
  - VERIFY: `pytest backend/tests/ -v` → all pass, coverage > 60%
  - AGENT: `backend-specialist`
  - DEPENDS: T1–T8

---

### Phase X: Verification

- [ ] **VX1:** `pytest backend/tests/ -v` → all pass
- [ ] **VX2:** `pnpm run build` in frontend → no TypeScript or build errors
- [ ] **VX3:** `docker compose up` → all services healthy
- [ ] **VX4:** Manual E2E test flow through UI:
  1. Create dog profile with allergies (Labrador, chicken allergy)
  2. View vaccination report → "chicken" contraindicated vaccines marked Unsafe
  3. Request diet plan → meal plan excludes chicken
  4. Check environmental risk for a location → risk score renders
  5. Upload dog image + symptoms → FIR report with urgency
- [ ] **VX5:** `python .agent/skills/vulnerability-scanner/scripts/security_scan.py .`
- [ ] **VX6:** `python .agent/skills/frontend-design/scripts/ux_audit.py .`

---

## Dependency Graph

```
T1 (FastAPI scaffold)
 └→ T2 (DB models + migrations)
     └→ T3 (Allergy constraint engine)
         └→ T4 (Dog CRUD API)
             ├→ T5 (Vaccination engine)
             ├→ T6 (Diet planner + LLM)
             ├→ T7 (Environment risk)
             └→ T8 (FIR engine)  ← also depends on T6 (shared AI infra)
                 │
T9 (Frontend setup) ← depends on T4 API contract
 ├→ T10 (Dashboard + Dog profiles)
 ├→ T11 (Vaccination UI)     ← also depends on T5
 ├→ T12 (Diet chatbot UI)    ← also depends on T6
 ├→ T13 (Env risk dashboard) ← also depends on T7
 └→ T14 (FIR generator UI)   ← also depends on T8
        │
        ├→ T15 (Docker Compose)
        └→ T16 (Backend tests)
                │
            Phase X (Verify all)
```

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Gemini API rate limits | Diet/FIR modules blocked | Redis caching for repeated queries, graceful fallback message |
| External env API downtime | Environmental module fails | Cache last-known data, show staleness indicator in UI |
| Vision model latency | FIR generation > 3s | Async processing via Celery, show loading skeleton in UI |
| PostgreSQL schema changes | Breaking migrations | Alembic migrations with rollback scripts, tested in CI |
| LLM hallucination | Unsafe recommendations | Allergy filter runs AFTER LLM output as safety net, mandatory disclaimers |
| Python 3.14 compatibility | Some packages may not support 3.14 yet | Pin Python 3.12 in Dockerfile, test deps compatibility early |

---

## Supported Breeds (MVP)

| # | Breed | Common Allergies (Reference) |
|---|-------|------------------------------|
| 1 | Labrador Retriever | Chicken, beef, dairy, wheat |
| 2 | Shih-Tzu | Corn, soy, certain grasses |
| 3 | Golden Retriever | Chicken, beef, flea saliva |
| 4 | Beagle | Beef, dairy, wheat |
| 5 | German Shepherd | Chicken, dairy, eggs, wheat |

---

## Notes

- **Allergy-first** is the core architectural constraint — no module generates output without querying allergy data
- **No direct diagnosis or prescriptions** — all outputs are advisory with mandatory disclaimers
- All LLM prompts centralized in `prompt_manager.py` to avoid prompt drift
- Structured JSON output via Pydantic models on all endpoints
- API versioning via `/api/v1/` prefix for future-proofing
