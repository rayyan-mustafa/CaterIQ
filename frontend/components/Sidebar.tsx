"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  CalendarDays,
  UtensilsCrossed,
  Sparkles,
  TrendingUp,
  FileBarChart,
  Navigation,
  ShieldAlert,
  GitBranch,
  Gauge,
  Sliders,
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { label: "Dashboard", href: "/", icon: LayoutDashboard },
    { label: "Events & Requests", href: "/events", icon: CalendarDays },
    { label: "Menu & Inventory", href: "/menu", icon: UtensilsCrossed },
  ];

  const aiLinks = [
    { label: "BFS: Allergen Finder", href: "/ai/allergen", icon: ShieldAlert, badge: "BFS" },
    { label: "DFS: Menu Constraints", href: "/ai/constraints", icon: Sliders, badge: "DFS" },
  ];

  const isLinkActive = (href: string) => {
    if (href === "/" && pathname !== "/") return false;
    return pathname.startsWith(href);
  };

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/60 p-4 flex flex-col gap-6 select-none shrink-0 min-h-[calc(100vh-61px)]">
      <div>
        <div className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2 px-3">
          Catering Operations
        </div>
        <nav className="flex flex-col gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            const active = isLinkActive(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center gap-3 px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                  active
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`}
              >
                <Icon className={`w-4 h-4 ${active ? "text-white" : "text-slate-400"}`} />
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>

      <div>
        <div className="flex items-center justify-between text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-2 px-3">
          <span>AI Search Studio</span>
          <span className="text-[10px] bg-indigo-500/10 text-indigo-400 px-1.5 py-0.2 rounded border border-indigo-500/20">
            Labs 04-05
          </span>
        </div>
        <nav className="flex flex-col gap-1">
          {aiLinks.map((link) => {
            const Icon = link.icon;
            const active = isLinkActive(link.href);
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`flex items-center justify-between px-3 py-2 rounded-xl text-sm font-medium transition-all ${
                  active
                    ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${active ? "text-white" : "text-slate-400"}`} />
                  <span className="truncate">{link.label}</span>
                </div>
                {link.badge && (
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700/60">
                    {link.badge}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="mt-auto pt-4 border-t border-slate-900 text-xs text-slate-500 px-3">
        <p className="font-semibold text-slate-400">Rayyan Mustafa</p>
        <p>Reg: 2312335 &bull; AI Lab</p>
      </div>
    </aside>
  );
}
