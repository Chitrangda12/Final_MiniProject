"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";
import type { Dog } from "@/types";

const modules = [
  {
    href: "/dogs",
    title: "Dog Profiles",
    icon: "🐕",
    desc: "Manage profiles and allergy records",
    color: "from-emerald-500/20 to-teal-500/10",
  },
  {
    href: "/vaccinations",
    title: "Vaccination Safety",
    icon: "💉",
    desc: "Allergy-aware vaccine screening",
    color: "from-sky-500/20 to-cyan-500/10",
  },
  {
    href: "/diet",
    title: "AI Diet Planner",
    icon: "🍖",
    desc: "Breed-aware, allergy-filtered meals",
    color: "from-amber-500/20 to-orange-500/10",
  },
  {
    href: "/environment",
    title: "Environment Risk",
    icon: "🌿",
    desc: "Location-based allergy risk scoring",
    color: "from-green-500/20 to-lime-500/10",
  },
  {
    href: "/fir",
    title: "FIR Generator",
    icon: "📋",
    desc: "Multimodal health report generation",
    color: "from-rose-500/20 to-pink-500/10",
  },
];

export default function DashboardPage() {
  const [dogs, setDogs] = useState<Dog[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.dogs
      .list(0, 5)
      .then((data) => {
        setDogs(data.dogs);
        setTotal(data.total);
      })
      .catch(() => { })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero */}
      <div className="relative overflow-hidden rounded-2xl glass p-8 gradient-border">
        <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-3xl" />
        <div className="relative">
          <Badge variant="secondary" className="mb-4 text-xs tracking-wider uppercase">
            Allergy-First Platform
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight mb-2">
            Welcome to <span className="text-primary">Pawsitive Care</span>
          </h1>
          <p className="text-muted-foreground max-w-lg">
            Intelligent veterinary decision support with allergy-aware safety
            constraints. Every recommendation is filtered through your pet&apos;s
            allergy profile.
          </p>
          <div className="flex gap-3 mt-6">
            <Link href="/dogs">
              <Button className="gap-2">
                🐕 Manage Dogs
              </Button>
            </Link>
            <Link href="/fir">
              <Button variant="outline" className="gap-2">
                📋 Generate Report
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="glass border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Registered Dogs</p>
                <p className="text-3xl font-bold text-primary mt-1">
                  {loading ? "—" : total}
                </p>
              </div>
              <div className="text-4xl">🐾</div>
            </div>
          </CardContent>
        </Card>
        <Card className="glass border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Total Allergies Tracked</p>
                <p className="text-3xl font-bold text-amber-400 mt-1">
                  {loading ? "—" : dogs.reduce((sum, d) => sum + d.allergies.length, 0)}
                </p>
              </div>
              <div className="text-4xl">⚠️</div>
            </div>
          </CardContent>
        </Card>
        <Card className="glass border-border/50">
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-muted-foreground">Safety Modules</p>
                <p className="text-3xl font-bold text-sky-400 mt-1">5</p>
              </div>
              <div className="text-4xl">🛡️</div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Module Cards */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Modules</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {modules.map((mod) => (
            <Link key={mod.href} href={mod.href}>
              <Card className="glass border-border/50 hover:border-primary/30 transition-all duration-300 group cursor-pointer h-full">
                <CardContent className="p-6">
                  <div
                    className={`w-12 h-12 rounded-xl bg-gradient-to-br ${mod.color} flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform`}
                  >
                    {mod.icon}
                  </div>
                  <h3 className="font-semibold text-foreground group-hover:text-primary transition-colors">
                    {mod.title}
                  </h3>
                  <p className="text-sm text-muted-foreground mt-1">{mod.desc}</p>
                </CardContent>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Dogs */}
      {dogs.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Recent Profiles</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {dogs.map((dog) => (
              <Link key={dog.id} href={`/dogs/${dog.id}`}>
                <Card className="glass border-border/50 hover:border-primary/30 transition-all cursor-pointer">
                  <CardContent className="p-5">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-lg">
                        🐕
                      </div>
                      <div>
                        <h4 className="font-medium">{dog.name}</h4>
                        <p className="text-xs text-muted-foreground">{dog.breed}</p>
                      </div>
                    </div>
                    {dog.allergies.length > 0 && (
                      <div className="flex flex-wrap gap-1 mt-3">
                        {dog.allergies.slice(0, 3).map((a) => (
                          <Badge key={a.id} variant="destructive" className="text-[10px]">
                            {a.allergen_name}
                          </Badge>
                        ))}
                        {dog.allergies.length > 3 && (
                          <Badge variant="secondary" className="text-[10px]">
                            +{dog.allergies.length - 3} more
                          </Badge>
                        )}
                      </div>
                    )}
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
