# 🐾 Pawsitive Care: Allergy-Aware Veterinary Decision Support System

Pawsitive Care is a professional, allergy-first platform designed to assist pet owners and veterinarians in making safe health, diet, and environmental decisions for dogs.

## 🚀 Key Features

- **🛡️ Allergy-First Architecture**: Every recommendation (vaccines, diet, environment) is filtered through the dog's unique allergy profile.
- **💉 Vaccination Safety Engine**: Rule-based screening for contraindications in common vaccines like Rabies, DHPP, and Bordetella.
- **🍖 AI Diet Planner**: Customized meal plans using Gemini AI, considering breed, age, weight, and food allergies.
- **🌍 Environmental Risk Dashboard**: Real-time risk scoring based on geolocation, weather (OpenWeather), and AQI data.
- **📋 Multimodal FIR (First Information Report)**: AI-powered symptom analysis using text descriptions and photo uploads (Gemini Vision).

## 🛠️ Technology Stack

- **Frontend**: Next.js 16 (App Router), Tailwind CSS v4, Radix UI / ShadCN, Lucide.
- **Backend**: FastAPI, SQLAlchemy (Async), Pydantic v2, SQLite (aiosqlite).
- **AI**: Google Gemini Pro & Vision via `google-generativeai`.
- **Deployment**: Docker & Docker Compose.

## 🏁 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- Gemini API Key ([Get one here](https://aistudio.google.com/))

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd Mini_Proj
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

3. **Frontend Setup**:
   ```bash
   cd ../frontend
   npm install
   # Create .env.local if needed
   npm run dev
   ```

## 🐳 Docker Setup

Run the entire stack with a single command:
```bash
docker-compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## ⚖️ Disclaimer

Pawsitive Care is an advisory tool and does not provide medical diagnoses or prescriptions. Always consult a licensed veterinarian for medical concerns.

---
Built with ❤️ by Antigravity AI.
