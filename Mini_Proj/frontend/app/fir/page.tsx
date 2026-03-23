"use client";

import { useEffect, useState, useRef } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";
import { UrgencyLevel } from "@/types";
import type { Dog, FIRReport } from "@/types";

const urgencyStyles: Record<UrgencyLevel, { bg: string; text: string; label: string; icon: string }> = {
    [UrgencyLevel.LOW]: { bg: "bg-emerald-500/15", text: "text-emerald-400", label: "LOW", icon: "🟢" },
    [UrgencyLevel.MODERATE]: { bg: "bg-amber-500/15", text: "text-amber-400", label: "MODERATE", icon: "🟡" },
    [UrgencyLevel.HIGH]: { bg: "bg-orange-500/15", text: "text-orange-400", label: "HIGH", icon: "🟠" },
    [UrgencyLevel.CRITICAL]: { bg: "bg-rose-500/15", text: "text-rose-400", label: "CRITICAL", icon: "🔴" },
};

export default function FIRPage() {
    const [dogs, setDogs] = useState<Dog[]>([]);
    const [selectedDog, setSelectedDog] = useState("");
    const [description, setDescription] = useState("");
    const [image, setImage] = useState<File | null>(null);
    const [imagePreview, setImagePreview] = useState<string | null>(null);
    const [report, setReport] = useState<FIRReport | null>(null);
    const [loading, setLoading] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);

    useEffect(() => {
        api.dogs.list(0, 100).then((data) => setDogs(data.dogs)).catch(() => { });
    }, []);

    const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            setImage(file);
            const reader = new FileReader();
            reader.onload = () => setImagePreview(reader.result as string);
            reader.readAsDataURL(file);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        const file = e.dataTransfer.files?.[0];
        if (file && file.type.startsWith("image/")) {
            setImage(file);
            const reader = new FileReader();
            reader.onload = () => setImagePreview(reader.result as string);
            reader.readAsDataURL(file);
        }
    };

    const generateFIR = async () => {
        if (!selectedDog || !description) return;
        setLoading(true);
        setReport(null);
        try {
            const result = await api.fir.generate(
                parseInt(selectedDog),
                description,
                image || undefined
            );
            setReport(result);
        } catch (err) {
            console.error("FIR generation failed:", err);
        } finally {
            setLoading(false);
        }
    };

    const urgStyle = report ? urgencyStyles[report.urgency] || urgencyStyles[UrgencyLevel.MODERATE] : null;

    return (
        <div className="space-y-6 animate-fade-in">
            <div>
                <h1 className="text-3xl font-bold">First Information Report (FIR)</h1>
                <p className="text-muted-foreground mt-1">
                    Multimodal AI health assessment with allergy-aware analysis
                </p>
            </div>

            {/* Input Form */}
            <Card className="glass border-border/50">
                <CardContent className="p-6 space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-4">
                            <div>
                                <Label>Select Dog</Label>
                                <Select value={selectedDog} onValueChange={setSelectedDog}>
                                    <SelectTrigger className="mt-1">
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
                            <div>
                                <Label>Describe Symptoms</Label>
                                <Textarea
                                    className="mt-1 bg-secondary/30 border-border/50 min-h-[120px]"
                                    placeholder="Describe what you're observing... (e.g. 'Red patches on belly, excessive scratching for 2 days, loss of appetite')"
                                    value={description}
                                    onChange={(e) => setDescription(e.target.value)}
                                />
                            </div>
                        </div>

                        {/* Image Upload */}
                        <div>
                            <Label>Upload Photo (optional)</Label>
                            <div
                                className="mt-1 border-2 border-dashed border-border/50 rounded-xl h-[180px] flex items-center justify-center cursor-pointer hover:border-primary/30 transition-colors relative overflow-hidden"
                                onClick={() => fileInputRef.current?.click()}
                                onDrop={handleDrop}
                                onDragOver={(e) => e.preventDefault()}
                            >
                                {imagePreview ? (
                                    <div className="relative w-full h-full">
                                        {/* eslint-disable-next-line @next/next/no-img-element */}
                                        <img
                                            src={imagePreview}
                                            alt="Uploaded"
                                            className="w-full h-full object-cover rounded-xl"
                                        />
                                        <button
                                            className="absolute top-2 right-2 w-6 h-6 bg-background/80 rounded-full flex items-center justify-center text-xs hover:bg-destructive transition-colors"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                setImage(null);
                                                setImagePreview(null);
                                            }}
                                        >
                                            ✕
                                        </button>
                                    </div>
                                ) : (
                                    <div className="text-center">
                                        <div className="text-3xl mb-2">📸</div>
                                        <p className="text-xs text-muted-foreground">
                                            Drag & drop or click to upload
                                        </p>
                                    </div>
                                )}
                                <input
                                    ref={fileInputRef}
                                    type="file"
                                    accept="image/*"
                                    className="hidden"
                                    onChange={handleImageChange}
                                />
                            </div>
                        </div>
                    </div>

                    <Button
                        onClick={generateFIR}
                        disabled={!selectedDog || description.length < 10 || loading}
                        className="gap-2 w-full md:w-auto"
                    >
                        {loading ? "⏳ Analyzing..." : "📋 Generate FIR Report"}
                    </Button>
                </CardContent>
            </Card>

            {/* Loading */}
            {loading && (
                <Card className="glass border-primary/20 animate-pulse">
                    <CardContent className="p-8 text-center">
                        <div className="text-4xl mb-4 animate-bounce">🔬</div>
                        <p className="text-sm text-muted-foreground">Analyzing with AI...</p>
                        <p className="text-xs text-muted-foreground/60 mt-1">
                            Running allergy-aware health assessment
                        </p>
                    </CardContent>
                </Card>
            )}

            {/* FIR Report */}
            {report && !loading && (
                <div className="space-y-4 animate-fade-in">
                    {/* Urgency Banner */}
                    <Card className={`glass ${urgStyle?.bg} border-border/50`}>
                        <CardContent className="p-6 text-center">
                            <div className="text-4xl mb-2">{urgStyle?.icon}</div>
                            <Badge className={`${urgStyle?.bg} ${urgStyle?.text} border-0 text-lg px-4 py-1 font-bold`}>
                                {urgStyle?.label} URGENCY
                            </Badge>
                            {report.risk_score !== null && report.risk_score !== undefined && (
                                <p className="text-sm text-muted-foreground mt-2">
                                    Risk Score: <span className="font-bold">{report.risk_score}/100</span>
                                </p>
                            )}
                        </CardContent>
                    </Card>

                    {/* Visual Summary */}
                    {report.visual_summary && (
                        <Card className="glass border-border/50">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm flex items-center gap-2">👁️ Visual Assessment</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground">{report.visual_summary}</p>
                            </CardContent>
                        </Card>
                    )}

                    {/* Affected Systems */}
                    {report.affected_systems.length > 0 && (
                        <Card className="glass border-border/50">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm flex items-center gap-2">🏥 Affected Systems</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="flex flex-wrap gap-2">
                                    {report.affected_systems.map((s, i) => (
                                        <Badge key={i} variant="secondary">{s}</Badge>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Allergy Warnings */}
                    {report.allergy_warnings.length > 0 && (
                        <Card className="glass border-rose-500/20">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm text-rose-400 flex items-center gap-2">
                                    ⚠️ Allergy Warnings
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <div className="space-y-2">
                                    {report.allergy_warnings.map((w, i) => (
                                        <div key={i} className="bg-rose-500/5 rounded-lg px-4 py-2.5 text-sm">
                                            {w}
                                        </div>
                                    ))}
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Immediate Care */}
                    {report.immediate_care && (
                        <Card className="glass border-sky-500/20">
                            <CardHeader className="pb-2">
                                <CardTitle className="text-sm text-sky-400 flex items-center gap-2">
                                    🩹 Immediate Care Advice
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">{report.immediate_care}</p>
                            </CardContent>
                        </Card>
                    )}

                    {/* Disclaimer */}
                    <Card className="glass border-amber-500/10">
                        <CardContent className="p-4 text-center">
                            <p className="text-xs text-muted-foreground">⚠️ {report.disclaimer}</p>
                        </CardContent>
                    </Card>
                </div>
            )}

            {/* Empty */}
            {!report && !loading && (
                <Card className="glass border-border/50">
                    <CardContent className="p-12 text-center">
                        <div className="text-5xl mb-4">📋</div>
                        <h3 className="text-lg font-medium mb-2">Generate a Health Report</h3>
                        <p className="text-sm text-muted-foreground">
                            Select a dog, describe symptoms, and optionally upload a photo for AI analysis
                        </p>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
