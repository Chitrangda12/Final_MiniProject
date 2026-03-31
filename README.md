# Pawsitive Care: Allergy-Aware Veterinary Decision Support System

Pawsitive Care is an allergy-focused decision support platform designed to assist pet owners and veterinarians in making informed health, dietary, and environmental decisions for dogs.

## Overview

The system prioritizes allergy safety by filtering all recommendations—such as vaccinations, diet plans, and environmental considerations—based on the individual dog's allergy profile. It aims to reduce health risks and improve overall pet care through intelligent, data-driven insights.

## Key Features

- **Allergy-Centric Recommendation System**  
  Filters all health, diet, and environmental suggestions based on the dog’s specific allergies.

- **Vaccination Safety Engine**  
  Implements rule-based checks to identify potential contraindications for common vaccines such as Rabies, DHPP, and Bordetella.

- **AI-Based Diet Planner**  
  Generates personalized diet plans using AI, taking into account breed, age, weight, and food allergies.

- **Environmental Risk Assessment**  
  Provides real-time risk evaluation based on geolocation, weather conditions, and air quality index (AQI).

- **Multimodal Symptom Analysis**  
  Supports analysis of pet health conditions using both text inputs and image-based data.

## Technology Stack

- **Frontend**: Next.js (App Router), Tailwind CSS, Radix UI / ShadCN  
- **Backend**: FastAPI, SQLAlchemy (Async), Pydantic, SQLite  
- **AI Integration**: Google Gemini Pro and Vision APIs  
- **Deployment**: Docker and Docker Compose  

## Getting Started

### Prerequisites

- Python 3.10 or higher  
- Node.js 18 or higher  
- Docker and Docker Compose (optional)  
- Gemini API Key (available via Google AI Studio)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Mini_Proj

2. Backend setup:
   ```bash
      cd backend
      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate
      pip install -r requirements.txt
      cp .env.example .env
      # Add your GEMINI_API_KEY in the .env file
   
3. Frontend setup:
   ```bash
      cd ../frontend
      npm install
      npm run dev

4. Docker Setup
   To run the full application using Docker:
   ```bash
      docker-compose up --build

Disclaimer:
Pawsitive Care is intended for advisory purposes only and does not replace professional veterinary consultation. Users are encouraged to consult licensed veterinarians for medical advice.
