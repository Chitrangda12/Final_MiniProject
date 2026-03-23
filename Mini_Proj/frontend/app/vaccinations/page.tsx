"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import { VaccineStatus } from "@/types";
import type { Dog, VaccinationReport } from "@/types";

const statusStyles: Record<VaccineStatus, { bg: string; text: string; label: string; icon: string }> = {
    [VaccineStatus.SAFE]: { bg: "bg-emerald-500/15", text: "text-emerald-400", label: "SAFE", icon: "✅" },
    [VaccineStatus.CONDITIONAL]: { bg: "bg-amber-500/15", text: "text-amber-400", label: "CONDITIONAL", icon: "⚠️" },
    [VaccineStatus.UNSAFE]: { bg: "bg-rose-500/15", text: "text-rose-400", label: "UNSAFE", icon: "🚫" },
};

function VaccinationsContent() {
    const searchParams = useSearchParams();
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [selectedDog, setSelectedDog] = useState<string>(searchParams.get("dog") || "");
    const [report, setReport] = useState<VaccinationReport | null>(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        api.dogs.list(0, 100).then((data) => setDogs(data.dogs)).catch(() => { });
    }, []);

    useEffect(() => {
        if (!selectedDog) return;
        let cancelled = false;

        async function fetchReport() {
            setLoading(true);
            try {
                const data = await api.vaccinations.report(parseInt(selectedDog));
                if (!cancelled) setReport(data);
            } catch {
                if (!cancelled) setReport(null);
            } finally {
                if (!cancelled) setLoading(false);
            }
        }

        fetchReport();
        return () => { cancelled = true; };
    }, [selectedDog]);

    const safeCount = report?.evaluations.filter((e) => e.status === VaccineStatus.SAFE).length || 0;
    const conditionalCount = report?.evaluations.filter((e) => e.status === VaccineStatus.CONDITIONAL).length || 0;
    const unsafeCount = report?.evaluations.filter((e) => e.status === VaccineStatus.UNSAFE).length || 0;

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h1 className="text-3xl font-bold">Vaccination Safety Report</h1>
                <p className="text-muted-foreground mt-1">
                    Allergy-aware vaccine contraindication screening
                </p>
            </div>

            {/* Dog Selector */}
            <Card className="glass border-border/50">
                <CardContent className="p-6">
                    <div className="flex items-center gap-4">
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
                        {report && (
                            <div className="flex gap-2">
                                <Badge className="bg-emerald-500/15 text-emerald-400 border-0">
                                    ✅ {safeCount} Safe
                                </Badge>
                                <Badge className="bg-amber-500/15 text-amber-400 border-0">
                                    ⚠️ {conditionalCount} Conditional
                                </Badge>
                                <Badge className="bg-rose-500/15 text-rose-400 border-0">
                                    🚫 {unsafeCount} Unsafe
                                </Badge>
                            </div>
                        )}
                    </div>
                </CardContent>
            </Card>

            {/* Report */}
            {loading ? (
                <div className="space-y-3">
                    {[1, 2, 3, 4].map((i) => (
                        <Card key={i} className="glass border-border/50 animate-pulse">
                            <CardContent className="p-6 h-20" />
                        </Card>
                    ))}
                </div>
            ) : report ? (
                <div className="space-y-3">
                    {report.allergies.length > 0 && (
                        <Card className="glass border-amber-500/20">
                            <CardContent className="p-4 flex items-center gap-3">
                                <span className="text-lg">⚠️</span>
                                <div>
                                    <p className="text-sm font-medium">Known Allergies</p>
                                    <div className="flex gap-1 mt-1">
                                        {report.allergies.map((a) => (
                                            <Badge key={a} variant="destructive" className="text-[10px]">
                                                {a}
                                            </Badge>
                                        ))}
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {report.evaluations.map((evaluation, i) => {
                        const style = statusStyles[evaluation.status];
                        return (
                            <Card
                                key={evaluation.vaccine_name}
                                className={`glass border-border/50 animate-fade-in`}
                                style={{ animationDelay: `${i * 0.05}s` }}
                            >
                                <CardContent className="p-5">
                                    <div className="flex items-center justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className={`w-10 h-10 rounded-lg ${style.bg} flex items-center justify-center text-lg`}>
                                                {style.icon}
                                            </div>
                                            <div>
                                                <h3 className="font-medium">{evaluation.vaccine_name}</h3>
                                                <p className="text-xs text-muted-foreground mt-0.5">
                                                    {evaluation.reason}
                                                </p>
                                            </div>
                                        </div>
                                        <Badge className={`${style.bg} ${style.text} border-0 font-semibold`}>
                                            {style.label}
                                        </Badge>
                                    </div>
                                    {evaluation.contraindications.length > 0 && (
                                        <div className="mt-3 flex gap-1">
                                            {evaluation.contraindications.map((c) => (
                                                <Badge key={c} variant="outline" className="text-[10px] border-destructive/30 text-destructive">
                                                    ↳ {c}
                                                </Badge>
                                            ))}
                                        </div>
                                    )}
                                </CardContent>
                            </Card>
                        );
                    })}

                    {/* Disclaimer */}
                    <Card className="glass border-amber-500/10">
                        <CardContent className="p-4 text-center">
                            <p className="text-xs text-muted-foreground">
                                ⚠️ {report.disclaimer}
                            </p>
                        </CardContent>
                    </Card>
                </div>
            ) : selectedDog ? (
                <Card className="glass border-border/50">
                    <CardContent className="p-12 text-center">
                        <p className="text-muted-foreground">Failed to load vaccination report.</p>
                    </CardContent>
                </Card>
            ) : (
                <Card className="glass border-border/50">
                    <CardContent className="p-12 text-center">
                        <div className="text-5xl mb-4">💉</div>
                        <h3 className="text-lg font-medium mb-2">Select a dog</h3>
                        <p className="text-sm text-muted-foreground">
                            Choose a dog profile to view their personalized vaccination safety report
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}

export default function VaccinationsPage() {
    return (
        <Suspense fallback={<div className="p-8 text-center text-muted-foreground animate-pulse">Loading vaccinations...</div>}>
            <VaccinationsContent />
        </Suspense>
    );
}
