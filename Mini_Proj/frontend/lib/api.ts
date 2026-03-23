// API Client for Pawsitive Care Backend

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

class ApiError extends Error {
    constructor(public status: number, message: string) {
        super(message);
    }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${API_BASE}${path}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options?.headers,
        },
    });

    if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: "Request failed" }));
        throw new ApiError(res.status, error.detail || "Request failed");
    }

    if (res.status === 204) return undefined as T;
    return res.json();
}

// Dogs
export const api = {
    dogs: {
        list: (skip = 0, limit = 20) =>
            request<{ dogs: import("@/types").Dog[]; total: number }>(`/dogs/?skip=${skip}&limit=${limit}`),
        get: (id: number) => request<import("@/types").Dog>(`/dogs/${id}`),
        create: (data: import("@/types").DogCreate) =>
            request<import("@/types").Dog>("/dogs/", { method: "POST", body: JSON.stringify(data) }),
        update: (id: number, data: Partial<import("@/types").DogCreate>) =>
            request<import("@/types").Dog>(`/dogs/${id}`, { method: "PUT", body: JSON.stringify(data) }),
        delete: (id: number) => request<void>(`/dogs/${id}`, { method: "DELETE" }),
    },
    allergies: {
        list: (dogId: number) =>
            request<import("@/types").Allergy[]>(`/dogs/${dogId}/allergies/`),
        add: (dogId: number, data: import("@/types").AllergyCreate) =>
            request<import("@/types").Allergy>(`/dogs/${dogId}/allergies/`, { method: "POST", body: JSON.stringify(data) }),
        bulkAdd: (dogId: number, allergies: import("@/types").AllergyCreate[]) =>
            request<import("@/types").Allergy[]>(`/dogs/${dogId}/allergies/bulk`, {
                method: "POST",
                body: JSON.stringify({ allergies }),
            }),
        delete: (dogId: number, allergyId: number) =>
            request<void>(`/dogs/${dogId}/allergies/${allergyId}`, { method: "DELETE" }),
    },
    vaccinations: {
        report: (dogId: number) =>
            request<import("@/types").VaccinationReport>(`/vaccinations/${dogId}/report`),
    },
    diet: {
        plan: (dogId: number, preferences?: string) =>
            request<import("@/types").MealPlan>("/diet/plan", {
                method: "POST",
                body: JSON.stringify({ dog_id: dogId, preferences }),
            }),
    },
    environment: {
        risk: (dogId: number, latitude: number, longitude: number) =>
            request<import("@/types").EnvironmentRisk>("/environment/risk", {
                method: "POST",
                body: JSON.stringify({ dog_id: dogId, latitude, longitude }),
            }),
    },
    fir: {
        generate: (dogId: number, description: string, image?: File) => {
            const formData = new FormData();
            formData.append("dog_id", dogId.toString());
            formData.append("description", description);
            if (image) formData.append("image", image);
            return fetch(`${API_BASE}/fir/generate`, { method: "POST", body: formData }).then(
                async (res) => {
                    if (!res.ok) throw new ApiError(res.status, "FIR generation failed");
                    return res.json() as Promise<import("@/types").FIRReport>;
                }
            );
        },
    },
};
