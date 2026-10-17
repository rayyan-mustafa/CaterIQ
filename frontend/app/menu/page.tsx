"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  UtensilsCrossed,
  Leaf,
  WheatOff,
  Flame,
  CheckCircle,
  Plus,
  ShieldAlert,
} from "lucide-react";

export default function MenuPage() {
  const [items, setItems] = useState<any[]>([]);
  const [ingredients, setIngredients] = useState<any[]>([]);
  const [activeTab, setActiveTab] = useState<"dishes" | "ingredients">("dishes");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadMenu() {
      try {
        await api.ensureDefaultDemoLogin();
        const [mItems, ings] = await Promise.all([
          api.getMenuItems(),
          api.getIngredients(),
        ]);
        setItems(mItems);
        setIngredients(ings);
      } catch (err) {
        console.error("Failed to load menu:", err);
      } finally {
        setLoading(false);
      }
    }
    loadMenu();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Menu & Inventory Catalog</h1>
          <p className="text-xs text-slate-400">Library of dishes, raw ingredients, dietary classifications, and allergen profiles</p>
        </div>

        <div className="flex items-center gap-2 bg-slate-900 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab("dishes")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === "dishes" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Dishes ({items.length})
          </button>
          <button
            onClick={() => setActiveTab("ingredients")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
              activeTab === "ingredients" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Ingredients ({ingredients.length})
          </button>
        </div>
      </div>

      {activeTab === "dishes" ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((dish) => (
            <div key={dish.id} className="glass-card p-5 rounded-2xl flex flex-col justify-between space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-300 border border-slate-700 px-2 py-0.5 rounded-full">
                    {dish.category}
                  </span>
                  <div className="flex items-center gap-1.5">
                    {dish.is_vegetarian && (
                      <span className="text-[10px] font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded flex items-center gap-1">
                        <Leaf className="w-2.5 h-2.5" />
                        <span>VEG</span>
                      </span>
                    )}
                    {dish.is_gluten_free && (
                      <span className="text-[10px] font-bold text-amber-400 bg-amber-500/10 border border-amber-500/20 px-1.5 py-0.5 rounded flex items-center gap-1">
                        <WheatOff className="w-2.5 h-2.5" />
                        <span>GF</span>
                      </span>
                    )}
                  </div>
                </div>

                <h3 className="font-bold text-white text-base leading-snug">{dish.name}</h3>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{dish.description || "Freshly prepared by kitchen staff."}</p>
              </div>

              <div className="border-t border-slate-800/80 pt-3 flex items-center justify-between text-xs">
                <div>
                  <div className="text-[10px] uppercase text-slate-500 font-semibold">Price / Head</div>
                  <div className="text-base font-bold text-emerald-400">${dish.price_per_head.toFixed(2)}</div>
                </div>
                <div className="text-right">
                  <div className="text-[10px] uppercase text-slate-500 font-semibold">Popularity</div>
                  <div className="text-sm font-semibold text-slate-200">{(dish.popularity_score * 100).toFixed(0)}% Score</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-panel p-6 rounded-2xl">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                  <th className="pb-3 font-semibold">Ingredient</th>
                  <th className="pb-3 font-semibold">Unit</th>
                  <th className="pb-3 font-semibold text-right">Cost / Unit</th>
                  <th className="pb-3 font-semibold text-right">Associated Allergens</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {ingredients.map((ing) => (
                  <tr key={ing.id} className="hover:bg-slate-900/40">
                    <td className="py-3 font-semibold text-white">{ing.name}</td>
                    <td className="py-3 text-slate-400">{ing.unit}</td>
                    <td className="py-3 text-right font-bold text-slate-200">${ing.cost_per_unit.toFixed(2)}</td>
                    <td className="py-3 text-right">
                      {ing.allergens && ing.allergens.length > 0 ? (
                        <div className="flex flex-wrap justify-end gap-1">
                          {ing.allergens.map((a: any) => (
                            <span
                              key={a.id}
                              className="text-[10px] font-bold uppercase bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 rounded-full"
                            >
                              {a.name}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <span className="text-xs text-emerald-400 font-medium">None</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
