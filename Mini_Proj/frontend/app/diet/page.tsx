"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import type { Dog, MealPlan } from "@/types";

function DietContent() {
    const searchParams = useSearchParams();
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [selectedDog, setSelectedDog] = useState<string>(searchParams.get("dog") || "");
    const [preferences, setPreferences] = useState("");
    const [plan, setPlan] = useState<MealPlan | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        api.dogs.list(0, 100).then((data) => setDogs(data.dogs)).catch(() => { });
    }, []);

    const generatePlan = async () => {
        if (!selectedDog) return;
        setLoading(true);
        setPlan(null);
        try {
            const result = await api.diet.plan(parseInt(selectedDog), preferences || undefined);
            setPlan(result);
        } catch (err) {
            console.error("Diet plan failed:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h1 className="text-3xl font-bold">AI Diet Planner</h1>
                <p className="text-muted-foreground mt-1">
                    Breed-aware, allergy-filtered meal planning powered by AI
                </p>
            </div>

            {/* Input */}
            <Card className="glass border-border/50">
                <CardContent className="p-6 space-y-4">
                    <div className="flex gap-4">
                        <div className="flex-1 max-w-sm">
                            <Select value={selectedDog} onValueChange={setSelectedDog}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select a dog..." />
                                </SelectTrigger>
                                <SelectContent>
                                    {dogs.map((dog) => (
                                        <SelectItem key={dog.id} value={dog.id.toString()}>
                                            {dog.name} — {dog.breed}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>
                    <Textarea
                        placeholder="Any dietary preferences? (optional, e.g. 'prefers wet food', 'home-cooked meals')"
                        value={preferences}
                        onChange={(e) => setPreferences(e.target.value)}
                        className="bg-secondary/30 border-border/50"
                        rows={2}
                    />
                    <Button onClick={generatePlan} disabled={!selectedDog || loading} className="gap-2">
                        {loading ? "⏳ Generating..." : "🍖 Generate Meal Plan"}
                    </Button>
                </CardContent>
            </Card>

            {/* Loading */}
            {loading && (
                <div className="space-y-4 animate-pulse">
                    {[1, 2, 3].map((i) => (
                        <Card key={i} className="glass border-border/50">
                            <CardContent className="p-6 h-24" />
                        </Card>
                    ))}
                </div>
            )}

            {/* Meal Plan Result */}
            {plan && !loading && (
                <div className="space-y-4 animate-fade-in">
                    {/* Dog Info */}
                    <Card className="glass border-primary/20 glow-emerald">
                        <CardContent className="p-5">
                            <div className="flex items-center gap-4">
                                <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-2xl">
                                    🐕
                                </div>
                                <div>
                                    <h3 className="font-semibold">{plan.dog_name}</h3>
                                    <p className="text-xs text-muted-foreground">
                                        {plan.breed} · {plan.age_years} yrs · {plan.weight_kg} kg
                                    </p>
                                </div>
                                {plan.allergies.length > 0 && (
                                    <div className="ml-auto flex gap-1">
                                        {plan.allergies.map((a) => (
                                            <Badge key={a} variant="destructive" className="text-[10px]">
                                                🚫 {a}
                                            </Badge>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Meal Plan */}
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {Object.entries(plan.meal_plan).map(([meal, desc]) => (
                            <Card key={meal} className="glass border-border/50">
                                <CardHeader className="pb-2">
                                    <CardTitle className="text-sm capitalize flex items-center gap-2">
                                        {meal === "morning" ? "🌅" : meal === "evening" ? "🌙" : "🍬"}{" "}
                                        {meal}
                                    </CardTitle>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm text-muted-foreground">{desc}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {/* Avoid List */}
                    {plan.avoid_list.length > 0 && (
                        <Card className="glass border-rose-500/20">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm text-rose-400 flex items-center gap-2">
                                    🚫 Avoid These Ingredients
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex flex-wrap gap-2">
                                    {plan.avoid_list.map((item) => (
                                        <Badge key={item} variant="destructive" className="text-xs">
                                            {item}
                                        </Badge>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Supplements */}
                    {plan.supplements.length > 0 && (
                        <Card className="glass border-sky-500/20">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm text-sky-400 flex items-center gap-2">
                                    💊 Recommended Supplements
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex flex-wrap gap-2">
                                    {plan.supplements.map((s) => (
                                        <Badge key={s} variant="secondary" className="text-xs">
                                            {s}
                                        </Badge>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Schedule */}
                    <Card className="glass border-border/50">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm flex items-center gap-2">
                                🕐 Feeding Schedule
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                                {Object.entries(plan.feeding_schedule).map(([key, val]) => (
                                    <div key={key} className="bg-secondary/30 rounded-lg px-3 py-2">
                                        <p className="text-[10px] text-muted-foreground capitalize">
                                            {key.replace(/_/g, " ")}
                                        </p>
                                        <p className="text-sm font-medium">{String(val)}</p>
                                    </div>
                                ))}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Disclaimer */}
                    <Card className="glass border-amber-500/10">
                        <CardContent className="p-4 text-center">
                            <p className="text-xs text-muted-foreground">⚠️ {plan.disclaimer}</p>
                        </CardContent>
                    </Card>
                </div>
            )}

            {/* Empty State */}
            {!plan && !loading && (
                <Card className="glass border-border/50">
                    <CardContent className="p-12 text-center">
                        <div className="text-5xl mb-4">🍖</div>
                        <h3 className="text-lg font-medium mb-2">Generate a Diet Plan</h3>
                        <p className="text-sm text-muted-foreground">
                            Select a dog and let AI create a personalized, allergy-safe meal plan
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}

export default function DietPage() {
    return (
        <Suspense fallback={<div className="p-8 text-center text-muted-foreground animate-pulse">Loading diet planner...</div>}>
            <DietContent />
        </Suspense>
    );
}
