"use client";

import React, { useState } from "react";
import { api } from "@/lib/api";
import {
  Sparkles,
  Navigation,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  TrendingUp,
  MapPin,
  Clock,
} from "lucide-react";

export default function OptimizerPage() {
  const [activeTab, setActiveTab] = useState<"menu" | "routing">("menu");

  // Menu Optimizer state
  const [budget, setBudget] = useState<number>(55);
  const [appealWeight, setAppealWeight] = useState<number>(10);
  const [optResult, setOptResult] = useState<any>(null);
  const [optLoading, setOptLoading] = useState(false);

  // Routing state
  const [startLoc, setStartLoc] = useState<string>("Central Kitchen");
  const [destLoc, setDestLoc] = useState<string>("Waterfront Grand Ballroom");
  const [routeResult, setRouteResult] = useState<any>(null);
  const [routeLoading, setRouteLoading] = useState(false);

  const handleOptimizeMenu = async () => {
    setOptLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const res = await api.optimizeMenu({
        slots: ["starter", "main", "dessert"],
        max_budget: Number(budget),
        appeal_weight: Number(appealWeight),
      });
      setOptResult(res);
    } catch (err: any) {
      alert(`Optimization error: ${err.message}`);
    } finally {
      setOptLoading(false);
    }
  };

  const handlePlanRoute = async () => {
    setRouteLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const res = await api.planRoute(startLoc, destLoc);
      setRouteResult(res);
    } catch (err: any) {
      alert(`Routing error: ${err.message}`);
    } finally {
      setRouteLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-emerald-400 font-bold text-xs uppercase tracking-wider mb-1">
          <Sparkles className="w-4 h-4" />
          <span>Module C &bull; Course Week 6</span>
        </div>
        <h1 className="text-2xl font-black text-white tracking-tight">
          A* Optimizer & Heuristic Routing
        </h1>
        <p className="text-xs text-slate-400">
          Uses <strong>A* Search with admissible heuristics</strong> to balance menu cost and guest appeal, and compares <strong>Greedy Best-First vs A*</strong> on delivery logistics.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-xl border border-slate-800 w-fit">
        <button
          onClick={() => setActiveTab("menu")}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
            activeTab === "menu" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
          }`}
        >
          C1: A* Menu Value Optimizer
        </button>
        <button
          onClick={() => setActiveTab("routing")}
          className={`px-4 py-2 rounded-lg text-xs font-bold transition-all ${
            activeTab === "routing" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
          }`}
        >
          C2: Greedy vs A* Delivery Routing
        </button>
      </div>

      {activeTab === "menu" ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="glass-panel p-6 rounded-2xl space-y-6 lg:col-span-1">
            <div>
              <label className="block text-xs font-bold uppercase text-slate-400 mb-2">
                Budget Cap ($ / Head)
              </label>
              <input
                type="number"
                value={budget}
                onChange={(e) => setBudget(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-lg px-4 py-2.5 rounded-xl outline-none"
              />
            </div>

            <div>
              <label className="block text-xs font-bold uppercase text-slate-400 mb-1">
                Guest Appeal Weight (&lambda; = {appealWeight})
              </label>
              <input
                type="range"
                min="0"
                max="25"
                value={appealWeight}
                onChange={(e) => setAppealWeight(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Higher &lambda; prioritizes 5-star popular dishes even if slightly more expensive.
              </p>
            </div>

            <div className="bg-slate-900/60 p-3.5 rounded-xl border border-slate-800 text-[11px] text-slate-400 space-y-1">
              <strong className="text-slate-200">Admissibility Proof:</strong>
              <p>
                Heuristic <code className="text-indigo-400 font-mono">h(n)</code> sums the single cheapest step cost for each remaining course slot. The real future cost can never be lower than this minimum, guaranteeing A* finds the optimal package.
              </p>
            </div>

            <button
              onClick={handleOptimizeMenu}
              disabled={optLoading}
              className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
            >
              <Sparkles className="w-4 h-4" />
              <span>{optLoading ? "Running A* Search..." : "Find Best-Value Menu (A*)"}</span>
            </button>
          </div>

          <div className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h2 className="text-base font-bold text-white">Optimal Menu Combination</h2>
                <p className="text-xs text-slate-400">Guaranteed lowest f(n) = cost + &lambda;(1 - popularity)</p>
              </div>
              {optResult && (
                <div className="flex items-center gap-4 text-xs font-semibold">
                  <span className="text-slate-400">
                    Nodes Expanded: <strong className="text-white">{optResult.nodes_expanded}</strong>
                  </span>
                  <span className="text-slate-400">
                    Runtime: <strong className="text-indigo-400">{optResult.runtime_ms.toFixed(2)} ms</strong>
                  </span>
                </div>
              )}
            </div>

            {!optResult ? (
              <div className="py-16 text-center text-slate-500 text-sm">
                Set target budget and appeal weight, then click <strong>Find Best-Value Menu (A*)</strong>.
              </div>
            ) : optResult.found ? (
              <div className="space-y-4">
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-500">Total Price</div>
                    <div className="text-xl font-bold text-emerald-400">${optResult.total_price_per_head.toFixed(2)}</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-500">Avg Popularity</div>
                    <div className="text-xl font-bold text-indigo-400">{(optResult.average_popularity * 100).toFixed(0)}%</div>
                  </div>
                  <div>
                    <div className="text-[10px] uppercase font-bold text-slate-500">A* f(n) Score</div>
                    <div className="text-xl font-bold text-white">{optResult.evaluation_score}</div>
                  </div>
                </div>

                <div className="space-y-2">
                  {optResult.dishes.map((dish: any, idx: number) => (
                    <div
                      key={dish.id}
                      className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center justify-between"
                    >
                      <div>
                        <div className="text-[10px] font-bold uppercase text-indigo-400">Course {idx + 1}: {dish.category}</div>
                        <div className="font-bold text-white text-sm mt-0.5">{dish.name}</div>
                        <div className="text-xs text-slate-400 mt-1">Popularity Rating: {(dish.popularity_score * 100).toFixed(0)}%</div>
                      </div>
                      <div className="text-right">
                        <div className="text-sm font-bold text-white">${dish.price_per_head.toFixed(2)}</div>
                        <div className="text-[10px] text-slate-500">per head</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              <div className="py-8 text-center text-slate-400 text-sm">{optResult.message}</div>
            )}
          </div>
        </div>
      ) : (
        /* Routing Tab: Greedy vs A* */
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex flex-wrap items-center gap-4 w-full md:w-auto">
              <div>
                <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Kitchen Depot</label>
                <select
                  value={startLoc}
                  onChange={(e) => setStartLoc(e.target.value)}
                  className="bg-slate-900 border border-slate-700 text-xs text-white px-3 py-2 rounded-xl outline-none"
                >
                  <option value="Central Kitchen">Central Kitchen</option>
                  <option value="North Kitchen Hub">North Kitchen Hub</option>
                </select>
              </div>

              <ArrowRight className="w-4 h-4 text-slate-500 hidden md:block" />

              <div>
                <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Event Venue Destination</label>
                <select
                  value={destLoc}
                  onChange={(e) => setDestLoc(e.target.value)}
                  className="bg-slate-900 border border-slate-700 text-xs text-white px-3 py-2 rounded-xl outline-none"
                >
                  <option value="Waterfront Grand Ballroom">Waterfront Grand Ballroom</option>
                  <option value="City Convention Center">City Convention Center</option>
                </select>
              </div>
            </div>

            <button
              onClick={handlePlanRoute}
              disabled={routeLoading}
              className="w-full md:w-auto px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold text-xs shadow-lg shadow-indigo-600/20 transition-all"
            >
              {routeLoading ? "Comparing Algorithms..." : "Compare Greedy vs A*"}
            </button>
          </div>

          {routeResult && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Greedy Box */}
              <div className="glass-panel p-6 rounded-2xl space-y-4 border-amber-500/20">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                    Greedy Best-First Search
                  </span>
                  <span className="text-xs text-slate-400">Heuristic h(n) only</span>
                </div>

                <div>
                  <div className="text-2xl font-black text-white">{routeResult.greedy.total_minutes} Minutes</div>
                  <div className="text-xs text-slate-400 mt-1">
                    Nodes Expanded: <strong>{routeResult.greedy.nodes_expanded}</strong> &bull; Runtime:{" "}
                    <strong>{routeResult.greedy.runtime_ms.toFixed(2)} ms</strong>
                  </div>
                </div>

                <div className="border-t border-slate-800 pt-3">
                  <div className="text-xs font-semibold text-slate-400 mb-2">Navigated Route</div>
                  <div className="space-y-1 text-xs">
                    {routeResult.greedy.path?.map((step: string, i: number) => (
                      <div key={i} className="flex items-center gap-2 text-slate-300">
                        <MapPin className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* A* Box */}
              <div className="glass-panel p-6 rounded-2xl space-y-4 border-emerald-500/30">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold uppercase text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    A* Search (Guaranteed Optimal)
                  </span>
                  <span className="text-xs text-emerald-400 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Optimal
                  </span>
                </div>

                <div>
                  <div className="text-2xl font-black text-emerald-400">{routeResult.astar.total_minutes} Minutes</div>
                  <div className="text-xs text-slate-400 mt-1">
                    Nodes Expanded: <strong>{routeResult.astar.nodes_expanded}</strong> &bull; Runtime:{" "}
                    <strong>{routeResult.astar.runtime_ms.toFixed(2)} ms</strong>
                  </div>
                </div>

                <div className="border-t border-slate-800 pt-3">
                  <div className="text-xs font-semibold text-slate-400 mb-2">Optimal Route Path</div>
                  <div className="space-y-1 text-xs">
                    {routeResult.astar.path?.map((step: string, i: number) => (
                      <div key={i} className="flex items-center gap-2 text-emerald-200">
                        <MapPin className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
