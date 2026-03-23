"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const navItems = [
    { href: "/", label: "Dashboard", icon: "🏠", desc: "Overview" },
    { href: "/dogs", label: "Dog Profiles", icon: "🐕", desc: "Manage profiles" },
    { href: "/vaccinations", label: "Vaccinations", icon: "💉", desc: "Safety report" },
    { href: "/diet", label: "Diet Planner", icon: "🍖", desc: "AI meal plans" },
    { href: "/environment", label: "Environment", icon: "🌿", desc: "Risk check" },
    { href: "/fir", label: "FIR Generator", icon: "📋", desc: "Health report" },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-border/50 bg-card/80 backdrop-blur-xl flex flex-col">
            {/* Logo */}
            <div className="p-6 border-b border-border/50">
                <Link href="/" className="flex items-center gap-3 group">
                    <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center text-xl group-hover:scale-110 transition-transform">
                        🛡️
                    </div>
                    <div>
                        <h1 className="text-lg font-bold tracking-tight text-foreground">
                            Pawsitive Care<span className="text-primary"> AI</span>
                        </h1>
                        <p className="text-[10px] text-muted-foreground tracking-widest uppercase">
                            Allergy-Aware Platform
                        </p>
                    </div>
                </Link>
            </div>

            {/* Nav */}
            <nav className="flex-1 p-4 space-y-1">
                {navItems.map((item) => {
                    const isActive =
                        pathname === item.href ||
                        (item.href !== "/" && pathname.startsWith(item.href));
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 group",
                                isActive
                                    ? "bg-primary/15 text-primary font-medium glow-emerald"
                                    : "text-muted-foreground hover:text-foreground hover:bg-secondary/50"
                            )}
                        >
                            <span className="text-lg group-hover:scale-110 transition-transform">
                                {item.icon}
                            </span>
                            <div>
                                <div className="font-medium">{item.label}</div>
                                <div className="text-[10px] text-muted-foreground">{item.desc}</div>
                            </div>
                            {isActive && (
                                <div className="ml-auto w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-border/50">
                <div className="glass rounded-lg p-3 text-center">
                    <p className="text-[10px] text-muted-foreground">
                        ⚠️ Advisory system only
                    </p>
                    <p className="text-[10px] text-muted-foreground/60 mt-0.5">
                        Always consult a licensed vet
                    </p>
                </div>
            </div>
        </aside>
    );
}
