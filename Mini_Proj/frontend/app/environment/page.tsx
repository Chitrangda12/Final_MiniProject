"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import type { Dog, EnvironmentRisk } from "@/types";

const riskLevelColors: Record<string, { bg: string; text: string; icon: string }> = {
    low: { bg: "bg-emerald-500/15", text: "text-emerald-400", icon: "✅" },
    moderate: { bg: "bg-amber-500/15", text: "text-amber-400", icon: "⚠️" },
    high: { bg: "bg-orange-500/15", text: "text-orange-400", icon: "🔶" },
    critical: { bg: "bg-rose-500/15", text: "text-rose-400", icon: "🚨" },
};

export default function EnvironmentPage() {
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [selectedDog, setSelectedDog] = useState("");
    const [lat, setLat] = useState("28.6139");
    const [lng, setLng] = useState("77.2090");
    const [risk, setRisk] = useState<EnvironmentRisk | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        api.dogs.list(0, 100).then((data) => setDogs(data.dogs)).catch(() => { });
    }, []);

    const useCurrentLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    setLat(pos.coords.latitude.toFixed(4));
                    setLng(pos.coords.longitude.toFixed(4));
                },
                () => alert("Location access denied")
            );
        }
    };

    const assessRisk = async () => {
        if (!selectedDog) return;
        setLoading(true);
        setRisk(null);
        try {
            const result = await api.environment.risk(
                parseInt(selectedDog),
                parseFloat(lat),
                parseFloat(lng)
            );
            setRisk(result);
        } catch (err) {
            console.error("Risk assessment failed:", err);
        } finally {
            setLoading(false);
        }
    };

    const riskStyle = risk ? riskLevelColors[risk.risk_level] || riskLevelColors.moderate : null;

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h1 className="text-3xl font-bold">Environmental Risk Dashboard</h1>
                <p className="text-muted-foreground mt-1">
                    Location-based allergy risk scoring with activity guidance
                </p>
            </div>

            {/* Input */}
            <Card className="glass border-border/50">
                <CardContent className="p-6 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div>
                            <Select value={selectedDog} onValueChange={setSelectedDog}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select dog..." />
                                </SelectTrigger>
                                <SelectContent>
                                    {dogs.map((dog) => (
                                        <SelectItem key={dog.id} value={dog.id.toString()}>
                                            {dog.name}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div>
                            <Input
                                placeholder="Latitude"
                                value={lat}
                                onChange={(e) => setLat(e.target.value)}
                                type="number"
                                step="0.0001"
                            />
                        </div>
                        <div>
                            <Input
                                placeholder="Longitude"
                                value={lng}
                                onChange={(e) => setLng(e.target.value)}
                                type="number"
                                step="0.0001"
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button onClick={assessRisk} disabled={!selectedDog || loading} className="flex-1">
                                {loading ? "⏳" : "🌿"} Assess
                            </Button>
                            <Button variant="outline" onClick={useCurrentLocation} title="Use current location">
                                📍
                            </Button>
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Loading */}
            {loading && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 animate-pulse">
                    {[1, 2, 3, 4].map((i) => (
                        <Card key={i} className="glass border-border/50">
                            <CardContent className="p-6 h-32" />
                        </Card>
                    ))}
                </div>
            )}

            {/* Results */}
            {risk && !loading && (
                <div className="space-y-4 animate-fade-in">
                    {/* Risk Score Hero */}
                    <Card className={`glass border-border/50 ${riskStyle?.bg}`}>
                        <CardContent className="p-8 text-center">
                            <div className="text-5xl mb-3">{riskStyle?.icon}</div>
                            <div className="text-6xl font-bold mb-2" style={{
                                background: `linear-gradient(135deg, ${risk.risk_score < 30 ? '#10b981' : risk.risk_score < 60 ? '#f59e0b' : '#ef4444'}, ${risk.risk_score < 30 ? '#14b8a6' : risk.risk_score < 60 ? '#f97316' : '#f43f5e'})`,
                                WebkitBackgroundClip: 'text',
                                WebkitTextFillColor: 'transparent',
                            }}>
                                {risk.risk_score}
                            </div>
                            <p className={`text-sm font-semibold uppercase tracking-wider ${riskStyle?.text}`}>
                                {risk.risk_level} Risk
                            </p>
                            <p className="text-xs text-muted-foreground mt-2">
                                for {risk.dog_name} at {risk.location.latitude.toFixed(2)}, {risk.location.longitude.toFixed(2)}
                            </p>
                        </CardContent>
                    </Card>

                    {/* Environmental Data */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                        {Object.entries(risk.environmental_data).map(([key, val]) => (
                            <Card key={key} className="glass border-border/50">
                                <CardContent className="p-4 text-center">
                                    <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                                        {key.replace(/_/g, " ")}
                                    </p>
                                    <p className="text-lg font-bold mt-1">
                                        {typeof val === "number" ? val.toFixed(1) : String(val)}
                                    </p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                    {/* Allergy Alerts */}
                    {risk.allergy_alerts.length > 0 && (
                        <Card className="glass border-amber-500/20">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm text-amber-400">⚠️ Allergy Alerts</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2">
                                    {risk.allergy_alerts.map((alert, i) => (
                                        <div key={i} className="bg-amber-500/5 rounded-lg px-4 py-2.5 text-sm">
                                            {alert}
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Activity Guidance */}
                    {risk.activity_guidance.length > 0 && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                            {risk.activity_guidance.map((g, i) => (
                                <Card key={i} className="glass border-border/50">
                                    <CardContent className="p-5 flex items-start gap-4">
                                        <div className="text-2xl">{g.icon}</div>
                                        <div>
                                            <h4 className="font-medium text-sm">{g.activity}</h4>
                                            <p className="text-xs text-muted-foreground mt-1">{g.recommendation}</p>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))}
                        </div>
                    )}

                    {/* Disclaimer */}
                    <Card className="glass border-amber-500/10">
                        <CardContent className="p-4 text-center">
                            <p className="text-xs text-muted-foreground">⚠️ {risk.disclaimer}</p>
                        </CardContent>
                    </Card>
                </div>
            )}

            {/* Empty */}
            {!risk && !loading && (
                <Card className="glass border-border/50">
                    <CardContent className="p-12 text-center">
                        <div className="text-5xl mb-4">🌍</div>
                        <h3 className="text-lg font-medium mb-2">Check Environmental Risk</h3>
                        <p className="text-sm text-muted-foreground">
                            Select a dog and location to assess environmental allergy risks
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
