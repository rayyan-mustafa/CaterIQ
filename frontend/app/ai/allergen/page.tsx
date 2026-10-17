"use client";

import React, { useState } from "react";
import { api } from "@/lib/api";
import {
  ShieldAlert,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  RotateCcw,
} from "lucide-react";

export default function AllergenFinderPage() {
  const [selectedAllergens, setSelectedAllergens] = useState<string[]>(["peanut"]);
  const [selectedDish, setSelectedDish] = useState<string>("satay");
  const [solution, setSolution] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const predefinedRecipes: Record<string, { name: string; ingredients: string[] }> = {
    satay: {
      name: "Thai Chicken Satay with Satay Dip",
      ingredients: ["Peanut Butter", "Chicken Breast", "Soy Sauce", "Heavy Cream"],
    },
    bruschetta: {
      name: "Tuscan Artisan Bruschetta",
      ingredients: ["Wheat Flour", "Heirloom Tomatoes", "Extra Virgin Olive Oil", "Parmesan Cheese"],
    },
    cake: {
      name: "Classic Chocolate Almond Lava Cake",
      ingredients: ["Wheat Flour", "Almond Butter", "Heavy Cream", "Fresh Farm Eggs"],
    },
  };

  const availableAllergens = ["peanut", "gluten", "dairy", "tree_nut", "soy", "egg"];

  const toggleAllergen = (alg: string) => {
    setSelectedAllergens((prev) =>
      prev.includes(alg) ? prev.filter((a) => a !== alg) : [...prev, alg]
    );
  };

  const handleRunBFS = async () => {
    setLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const ingredients = predefinedRecipes[selectedDish].ingredients;
      const res = await api.solveAllergens(ingredients, selectedAllergens);
      setSolution(res);
    } catch (err: any) {
      alert(`Search error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-rose-400 font-bold text-xs uppercase tracking-wider mb-1">
          <ShieldAlert className="w-4 h-4" />
          <span>Module A &bull; Course Week 4</span>
        </div>
        <h1 className="text-2xl font-black text-white tracking-tight">Allergen Substitution Finder</h1>
        <p className="text-xs text-slate-400">
          Uses <strong>Breadth-First Search (BFS)</strong> over the ingredient substitution graph to discover the minimal number of ingredient modifications that make a dish safe.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration Panel */}
        <div className="glass-panel p-6 rounded-2xl space-y-6 lg:col-span-1">
          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              1. Select Dish Recipe
            </label>
            <div className="space-y-2">
              {Object.entries(predefinedRecipes).map(([key, item]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => {
                    setSelectedDish(key);
                    setSolution(null);
                  }}
                  className={`w-full text-left p-3 rounded-xl border text-xs transition-all ${
                    selectedDish === key
                      ? "bg-indigo-600/20 border-indigo-500 text-white font-semibold"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-white"
                  }`}
                >
                  <div className="font-bold text-slate-200">{item.name}</div>
                  <div className="text-[11px] text-slate-500 mt-1 truncate">
                    {item.ingredients.join(", ")}
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
              2. Guest Allergens to Eliminate
            </label>
            <div className="flex flex-wrap gap-2">
              {availableAllergens.map((alg) => {
                const active = selectedAllergens.includes(alg);
                return (
                  <button
                    key={alg}
                    type="button"
                    onClick={() => toggleAllergen(alg)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-bold uppercase tracking-wider transition-all ${
                      active
                        ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                        : "bg-slate-900 text-slate-500 border border-slate-800 hover:text-slate-300"
                    }`}
                  >
                    {alg}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            onClick={handleRunBFS}
            disabled={loading || selectedAllergens.length === 0}
            className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-indigo-600/20 transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? "Searching Layer-by-Layer..." : "Find Minimal Swaps (BFS)"}</span>
          </button>
        </div>

        {/* Results & Search Trace Panel */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-base font-bold text-white">BFS Search Solution</h2>
              <p className="text-xs text-slate-400">Guaranteed to find the shortest substitution path</p>
            </div>
            {solution && (
              <div className="flex items-center gap-4 text-xs font-semibold">
                <span className="text-slate-400">
                  Nodes Expanded: <strong className="text-white">{solution.nodes_expanded}</strong>
                </span>
                <span className="text-slate-400">
                  Runtime: <strong className="text-indigo-400">{solution.runtime_ms.toFixed(2)} ms</strong>
                </span>
              </div>
            )}
          </div>

          {!solution ? (
            <div className="py-16 text-center text-slate-500 text-sm">
              Select a dish and allergens, then click <strong>Find Minimal Swaps (BFS)</strong>.
            </div>
          ) : solution.found ? (
            <div className="space-y-6">
              {/* Swap Sequence */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>
                    {solution.swaps_required.length === 0
                      ? "Dish is already safe! No ingredient swaps needed."
                      : `Minimal Swaps Required (${solution.swaps_required.length} Step${
                          solution.swaps_required.length > 1 ? "s" : ""
                        })`}
                  </span>
                </h3>

                {solution.swaps_required.length > 0 && (
                  <div className="space-y-2">
                    {solution.swaps_required.map((swap: any, idx: number) => (
                      <div
                        key={idx}
                        className="bg-slate-900/90 border border-slate-800 p-3.5 rounded-xl flex items-center justify-between text-sm"
                      >
                        <div className="flex items-center gap-3">
                          <span className="h-6 w-6 rounded-full bg-indigo-600/30 text-indigo-400 flex items-center justify-center text-xs font-bold">
                            {idx + 1}
                          </span>
                          <span className="text-rose-400 font-semibold line-through">
                            {swap.from}
                          </span>
                          <ArrowRight className="w-4 h-4 text-slate-500" />
                          <span className="text-emerald-400 font-bold">
                            {swap.to}
                          </span>
                        </div>
                        <span className="text-[11px] font-bold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                          Unit Cost: 1.0
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Before and After Comparison */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 border-t border-slate-800 pt-4">
                <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800/80">
                  <div className="text-xs font-bold uppercase text-slate-400 mb-2">Original Ingredients</div>
                  <ul className="space-y-1 text-xs text-slate-300">
                    {solution.original_ingredients.map((ing: string) => (
                      <li key={ing} className="flex items-center gap-1.5">
                        <span className="w-1.5 h-1.5 rounded-full bg-slate-600"></span>
                        <span>{ing}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/20">
                  <div className="text-xs font-bold uppercase text-emerald-400 mb-2">Safe Safe Recipe Version</div>
                  <ul className="space-y-1 text-xs text-emerald-200">
                    {solution.safe_ingredients.map((ing: string) => (
                      <li key={ing} className="flex items-center gap-1.5 font-medium">
                        <CheckCircle2 className="w-3 h-3 text-emerald-400" />
                        <span>{ing}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Safety Disclaimer */}
              <div className="bg-amber-500/10 border border-amber-500/20 p-3.5 rounded-xl flex items-start gap-2.5 text-xs text-amber-300">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5 text-amber-400" />
                <span>{solution.safety_disclaimer}</span>
              </div>
            </div>
          ) : (
            <div className="py-8 text-center space-y-3">
              <div className="inline-flex p-3 rounded-full bg-rose-500/10 text-rose-400">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <h3 className="font-bold text-white text-base">No Safe Recipe Path Found</h3>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                BFS exhausted all allowed substitution branches within depth limit without finding a combination that completely eliminates the target allergen(s).
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
