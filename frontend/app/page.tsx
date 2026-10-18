"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  CalendarDays,
  UtensilsCrossed,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Clock,
  ChevronRight,
  Layers,
} from "lucide-react";

export default function DashboardPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [menuItems, setMenuItems] = useState<any[]>([]);
  const [ingredients, setIngredients] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        await api.ensureDefaultDemoLogin();
        const [evList, mList, ingList] = await Promise.all([
          api.getEvents(),
          api.getMenuItems(),
          api.getIngredients(),
        ]);
        setEvents(evList || []);
        setMenuItems(mList || []);
        setIngredients(ingList || []);
      } catch (err) {
        console.error("Dashboard load failed:", err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const confirmedEvents = events.filter((e) => e.status === "confirmed").length;
  const proposedEvents = events.filter((e) => e.status === "proposed").length;

  return (
    <div className="space-y-8">
      {/* Top Banner */}
      <div className="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-r from-indigo-950 via-slate-900 to-slate-950 border border-indigo-500/20 shadow-2xl">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Classical Search AI Engine Active</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-black text-white tracking-tight mb-2">
            Welcome to CaterIQ
          </h1>
          <p className="text-slate-300 text-sm md:text-base leading-relaxed mb-6">
            Intelligent catering management integrating foundational search algorithms (BFS allergen safety and DFS menu constraint solving with pruning) for Weeks 1–5 AI curriculum.
          </p>
          <div className="flex flex-wrap items-center gap-3">
            <Link
              href="/events"
              className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition-all shadow-lg shadow-indigo-600/20 flex items-center gap-2"
            >
              <span>Manage Events</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              href="/ai"
              className="px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition-all flex items-center gap-2"
            >
              <span>Explore AI Studio (Weeks 1–5)</span>
              <ChevronRight className="w-4 h-4 text-slate-400" />
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Total Events</span>
            <CalendarDays className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-black text-white">{events.length || 2}</div>
          <div className="text-xs text-indigo-400 mt-2 font-medium flex items-center gap-1">
            <span>Active Catering Orders</span>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Confirmed Events</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-black text-white">{confirmedEvents || 1}</div>
          <div className="text-xs text-emerald-400 mt-2">Locked &amp; On Schedule</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Menu Library Dishes</span>
            <UtensilsCrossed className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-black text-white">{menuItems.length || 8}</div>
          <div className="text-xs text-slate-400 mt-2">Starters, Mains &amp; Desserts</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">
            <span>Tracked Ingredients</span>
            <ShieldCheck className="w-4 h-4 text-rose-400" />
          </div>
          <div className="text-2xl font-black text-white">{ingredients.length || 18}</div>
          <div className="text-xs text-slate-400 mt-2">Allergen Substitution Graph</div>
        </div>
      </div>

      {/* AI Search Engine Modules Showcase */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white">AI Search Helpers (Weeks 1–5)</h2>
            <p className="text-xs text-slate-400">Course syllabus search algorithms solving real catering logistics</p>
          </div>
          <span className="text-xs font-semibold text-indigo-400">Module A (BFS) & Module B (DFS)</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link href="/ai/allergen" className="glass-card p-5 rounded-2xl group block">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                BFS &bull; Week 4
              </span>
              <ShieldCheck className="w-5 h-5 text-slate-500 group-hover:text-rose-400 transition-colors" />
            </div>
            <h3 className="font-bold text-white text-base mb-1 group-hover:text-indigo-300 transition-colors">
              Allergen Substitution (Module A)
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              Finds the shortest swap chain using Breadth-First Search to make peanut or gluten recipes allergen-safe.
            </p>
            <div className="text-xs font-semibold text-indigo-400 flex items-center gap-1">
              <span>Test Dish Swaps</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>

          <Link href="/ai/constraints" className="glass-card p-5 rounded-2xl group block">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                DFS &bull; Week 5
              </span>
              <Sparkles className="w-5 h-5 text-slate-500 group-hover:text-amber-400 transition-colors" />
            </div>
            <h3 className="font-bold text-white text-base mb-1 group-hover:text-indigo-300 transition-colors">
              Menu Constraint Solver (Module B)
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              Constructs 3-course packages under budget limits with early backtracking pruning for vegetarian/GF requirements.
            </p>
            <div className="text-xs font-semibold text-indigo-400 flex items-center gap-1">
              <span>Solve Constraints</span>
              <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
            </div>
          </Link>
        </div>
      </div>

      {/* Events Pipeline */}
      <div className="glass-panel p-6 rounded-3xl">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-lg font-bold text-white">Upcoming & Recent Events</h2>
            <p className="text-xs text-slate-400">Live operational lifecycle tracking</p>
          </div>
          <Link
            href="/events"
            className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
          >
            <span>View All</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                <th className="pb-3 font-semibold">Event / Client</th>
                <th className="pb-3 font-semibold">Date & Time</th>
                <th className="pb-3 font-semibold text-center">Headcount</th>
                <th className="pb-3 font-semibold text-right">Revenue</th>
                <th className="pb-3 font-semibold text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {events.map((ev) => (
                <tr key={ev.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="py-4">
                    <div className="font-semibold text-white">{ev.title}</div>
                    <div className="text-xs text-slate-400">{ev.client_name}</div>
                  </td>
                  <td className="py-4 text-slate-300">
                    <div>{ev.event_date}</div>
                    <div className="text-xs text-slate-500">{ev.start_time || "TBD"} - {ev.end_time || ""}</div>
                  </td>
                  <td className="py-4 text-center font-bold text-slate-200">
                    {ev.headcount}
                  </td>
                  <td className="py-4 text-right font-bold text-white">
                    ${ev.total_revenue.toLocaleString()}
                  </td>
                  <td className="py-4 text-right">
                    <span
                      className={`inline-block px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider ${
                        ev.status === "confirmed"
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          : ev.status === "completed"
                          ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                          : ev.status === "proposed"
                          ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                          : "bg-slate-700 text-slate-300"
                      }`}
                    >
                      {ev.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
