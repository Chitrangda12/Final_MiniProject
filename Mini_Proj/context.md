# Project Context
## Allergy-Aware Intelligent Veterinary Decision Support System

---

## 1. Vision

This system is designed as a safety-first, AI-assisted veterinary decision support platform for dogs.

It integrates:
- Structured allergy-aware logic
- Rule-based safety engines
- Multimodal LLM reasoning
- Environmental intelligence APIs

The system architecture is modular and scalable.

---

## 2. Design Philosophy

### Allergy-First Constraint Model

All modules must:
1. Query stored allergy data.
2. Apply filtering logic.
3. Prevent unsafe recommendations.
4. Log all constraint decisions.

No output is generated without allergy validation.

---

## 3. System Architecture Layers

1. Presentation Layer (Next.js / Streamlit)
2. API Layer (FastAPI)
3. Business Logic Layer
4. AI Orchestration Layer (LangChain + GPT-4o)
5. Database Layer (PostgreSQL)
6. External API Integration Layer

---

## 4. AI Engineering Principles

- Use structured prompts for FIR generation.
- Use function-calling format for structured output.
- Keep prompts centralized in a prompt manager.
- Avoid hallucinated diagnosis.
- Always include disclaimers.
- Apply breed-aware reasoning logic.

---

## 5. Data Model Overview

Entities:
- Dog Profile
- Allergy
- Vaccination
- FIR
- Environmental Logs

Relationships:
- One dog → many allergies
- One dog → many FIR records
- Allergy influences vaccine eligibility
- Environmental data influences risk score

---

## 6. Multimodal Pipeline Logic

Step 1: Accept image/video  
Step 2: Extract visual features  
Step 3: Merge with text observation  
Step 4: Inject breed metadata  
Step 5: Inject allergy constraints  
Step 6: Multimodal LLM reasoning  
Step 7: Generate structured FIR  

---

## 7. Engineering Constraints

- No direct diagnosis.
- No prescription.
- Must output urgency level.
- All outputs must be structured JSON-compatible.
- Error handling required for:
  - API failure
  - Vision failure
  - LLM timeout

---

## 8. Deployment Strategy

Development:
- Dockerized FastAPI backend
- Local PostgreSQL

Production:
- AWS ECS or Kubernetes
- Managed PostgreSQL
- Redis cluster
- CDN for frontend

CI/CD:
- GitHub Actions
- Docker image pipeline
- Automated testing

---

## 9. Cursor Development Guidelines

When generating code:

- Maintain separation of concerns.
- Use service-layer architecture.
- Create reusable allergy-filtering middleware.
- Centralize prompts in a single config file.
- Ensure environment variables for API keys.
- Validate all user inputs with Pydantic.

---

## 10. Long-Term Roadmap

- Veterinary-specific fine-tuned LLM
- Historical health trend prediction
- Explainable AI visualization dashboards
- Mobile app version
- Research publication datasets
