"use client";

import React, { useState } from "react";
import { api } from "@/lib/api";
import {
  Sliders,
  Sparkles,
  CheckCircle2,
  DollarSign,
  TrendingDown,
  Layers,
  ArrowRight,
} from "lucide-react";

export default function MenuConstraintPage() {
  const [maxBudget, setMaxBudget] = useState<number>(45);
  const [minVeg, setMinVeg] = useState<number>(1);
  const [minGf, setMinGf] = useState<number>(1);
  const [usePruning, setUsePruning] = useState<boolean>(true);
  const [result, setResult] = useState<any>(null);
  const [comparison, setComparison] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSolve = async () => {
    setLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const payload = {
        slots: ["starter", "main", "dessert"],
        max_budget: Number(maxBudget),
        min_vegetarian: Number(minVeg),
        min_gluten_free: Number(minGf),
      };

      // Run both pruned and plain to illustrate search tree pruning!
      const [prunedRes, plainRes] = await Promise.all([
        api.solveMenuConstraints({ ...payload, use_pruning: true }),
        api.solveMenuConstraints({ ...payload, use_pruning: false }),
      ]);

      setResult(usePruning ? prunedRes : plainRes);
      setComparison({
        pruned: prunedRes,
        plain: plainRes,
      });
    } catch (err: any) {
      alert(`Solver failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-amber-400 font-bold text-xs uppercase tracking-wider mb-1">
          <Sliders className="w-4 h-4" />
          <span>Module B &bull; Course Week 5</span>
        </div>
        <h1 className="text-2xl font-black text-white tracking-tight">Menu Constraint Solver</h1>
        <p className="text-xs text-slate-400">
          Uses <strong>Depth-First Search (DFS) with backtracking</strong> to assemble a multi-course package meeting hard budget and dietary constraints.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Controls */}
        <div className="glass-panel p-6 rounded-2xl space-y-6 lg:col-span-1">
          <div>
            <label className="block text-xs font-bold uppercase text-slate-400 mb-2">
              Maximum Budget / Head ($)
            </label>
            <div className="relative">
              <input
                type="number"
                value={maxBudget}
                onChange={(e) => setMaxBudget(Number(e.target.value))}
                min={20}
                max={100}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-lg px-4 py-2.5 rounded-xl focus:border-indigo-500 outline-none"
              />
              <span className="absolute right-4 top-3 text-slate-500 font-bold">$ USD</span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">Try $42 for tight constraint testing</p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-bold uppercase text-slate-400 mb-1">
                Min. Vegetarian Courses
              </label>
              <input
                type="range"
                min="0"
                max="3"
                value={minVeg}
                onChange={(e) => setMinVeg(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <div className="text-xs text-right text-slate-300 font-bold">{minVeg} Required</div>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase text-slate-400 mb-1">
                Min. Gluten-Free Courses
              </label>
              <input
                type="range"
                min="0"
                max="3"
                value={minGf}
                onChange={(e) => setMinGf(Number(e.target.value))}
                className="w-full accent-indigo-500"
              />
              <div className="text-xs text-right text-slate-300 font-bold">{minGf} Required</div>
            </div>
          </div>

          <div className="border-t border-slate-800 pt-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={usePruning}
                onChange={(e) => setUsePruning(e.target.checked)}
                className="rounded accent-indigo-600 h-4 w-4"
              />
              <span className="text-xs font-semibold text-slate-300">
                Enable Early Constraint Pruning
              </span>
            </label>
            <p className="text-[11px] text-slate-500 mt-1">
              Prunes partial paths immediately when running price exceeds budget.
            </p>
          </div>

          <button
            onClick={handleSolve}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? "Backtracking..." : "Solve Package (DFS)"}</span>
          </button>
        </div>

        {/* Output Panel */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-base font-bold text-white">DFS Solution & Exploration Stats</h2>
              <p className="text-xs text-slate-400">Compares plain backtracking against early constraint pruning</p>
            </div>
            {result && (
              <span
                className={`text-xs font-bold px-2.5 py-1 rounded-full uppercase ${
                  result.found
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                    : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                }`}
              >
                {result.found ? "Valid Package Found" : "Unsolvable"}
              </span>
            )}
          </div>

          {comparison && (
            <div className="grid grid-cols-2 gap-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
              <div>
                <div className="text-[10px] font-bold uppercase text-slate-500">Plain DFS Search</div>
                <div className="text-lg font-black text-white mt-1">
                  {comparison.plain.nodes_expanded} <span className="text-xs font-normal text-slate-400">Nodes Expanded</span>
                </div>
                <div className="text-xs text-slate-400 mt-0.5">{comparison.plain.runtime_ms.toFixed(2)} ms</div>
              </div>

              <div className="border-l border-slate-800 pl-4">
                <div className="text-[10px] font-bold uppercase text-emerald-400">Pruned DFS Search</div>
                <div className="text-lg font-black text-emerald-400 mt-1">
                  {comparison.pruned.nodes_expanded} <span className="text-xs font-normal text-slate-400">Nodes Expanded</span>
                </div>
                <div className="text-xs text-emerald-400/80 mt-0.5">
                  {comparison.plain.nodes_expanded > 0
                    ? `${(
                        (1 - comparison.pruned.nodes_expanded / comparison.plain.nodes_expanded) *
                        100
                      ).toFixed(1)}% Tree Cutoff`
                    : "Optimized"}
                </div>
              </div>
            </div>
          )}

          {!result ? (
            <div className="py-16 text-center text-slate-500 text-sm">
              Configure parameters and click <strong>Solve Package (DFS)</strong>.
            </div>
          ) : result.found && result.packages?.length > 0 ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold uppercase text-slate-400">Constructed Course Package</h3>
                <div className="text-sm font-bold text-white">
                  Total: <span className="text-emerald-400">${result.packages[0].total_price_per_head.toFixed(2)}</span> / Head
                </div>
              </div>

              <div className="space-y-2">
                {result.packages[0].dishes.map((dish: any, idx: number) => (
                  <div
                    key={dish.id || idx}
                    className="bg-slate-900/80 border border-slate-800 p-4 rounded-xl flex items-center justify-between"
                  >
                    <div>
                      <div className="text-[10px] font-bold uppercase text-indigo-400 tracking-wider">
                        Course {idx + 1}: {dish.category}
                      </div>
                      <div className="font-bold text-white text-sm mt-0.5">{dish.name}</div>
                      <div className="flex items-center gap-2 mt-1">
                        {dish.is_vegetarian && (
                          <span className="text-[9px] font-bold text-emerald-400 bg-emerald-500/10 px-1.5 py-0.5 rounded">
                            Vegetarian
                          </span>
                        )}
                        {dish.is_gluten_free && (
                          <span className="text-[9px] font-bold text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded">
                            Gluten-Free
                          </span>
                        )}
                      </div>
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
            <div className="py-8 text-center text-slate-400 text-sm">
              {result.message || "No valid menu combination found."}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
