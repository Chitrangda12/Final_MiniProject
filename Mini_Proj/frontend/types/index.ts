// Shared TypeScript types for Pawsitive Care

export enum BreedEnum {
  LABRADOR = "Labrador Retriever",
  SHIH_TZU = "Shih-Tzu",
  GOLDEN = "Golden Retriever",
  BEAGLE = "Beagle",
  GERMAN_SHEPHERD = "German Shepherd",
}

export enum AllergyCategory {
  FOOD = "food",
  ENVIRONMENTAL = "environmental",
  MEDICATION = "medication",
  CONTACT = "contact",
}

export enum AllergySeverity {
  MILD = "mild",
  MODERATE = "moderate",
  SEVERE = "severe",
}

export enum VaccineStatus {
  SAFE = "safe",
  CONDITIONAL = "conditional",
  UNSAFE = "unsafe",
}

export enum UrgencyLevel {
  LOW = "low",
  MODERATE = "moderate",
  HIGH = "high",
  CRITICAL = "critical",
}

// Dog
export interface Allergy {
  id: number;
  dog_id: number;
  allergen_name: string;
  category: AllergyCategory;
  severity: AllergySeverity;
  notes?: string;
}

export interface Dog {
  id: number;
  name: string;
  breed: BreedEnum;
  age_years: number;
  weight_kg: number;
  owner_name: string;
  image_url?: string;
  created_at?: string;
  allergies: Allergy[];
}

export interface DogCreate {
  name: string;
  breed: BreedEnum;
  age_years: number;
  weight_kg: number;
  owner_name: string;
  image_url?: string;
}

export interface AllergyCreate {
  allergen_name: string;
  category: AllergyCategory;
  severity: AllergySeverity;
  notes?: string;
}

// Vaccination
export interface VaccineEvaluation {
  vaccine_name: string;
  status: VaccineStatus;
  contraindications: string[];
  reason: string;
}

export interface VaccinationReport {
  dog_id: number;
  dog_name: string;
  breed: string;
  allergies: string[];
  evaluations: VaccineEvaluation[];
  disclaimer: string;
}

// Diet
export interface MealPlan {
  dog_name: string;
  breed: string;
  age_years: number;
  weight_kg: number;
  allergies: string[];
  meal_plan: Record<string, string>;
  avoid_list: string[];
  supplements: string[];
  feeding_schedule: Record<string, string | number>;
  disclaimer: string;
}

// Environment
export interface EnvironmentRisk {
  dog_name: string;
  location: { latitude: number; longitude: number };
  risk_score: number;
  risk_level: string;
  environmental_data: Record<string, string | number>;
  allergy_alerts: string[];
  activity_guidance: { activity: string; recommendation: string; icon: string }[];
  disclaimer: string;
}

// FIR
export interface FIRReport {
  id: number;
  dog_id: number;
  visual_summary?: string;
  affected_systems: string[];
  allergy_warnings: string[];
  immediate_care?: string;
  urgency: UrgencyLevel;
  risk_score?: number;
  disclaimer: string;
  full_report?: Record<string, unknown>;
}
