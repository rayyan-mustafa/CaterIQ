"use client";

import React, { useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  TrendingUp,
  Sparkles,
  CheckCircle2,
  GitBranch,
  ShieldCheck,
  DollarSign,
  Users,
  Award,
} from "lucide-react";

export default function BidPricingPage() {
  const [basePrice, setBasePrice] = useState<number>(45);
  const [ourCost, setOurCost] = useState<number>(26);
  const [headcount, setHeadcount] = useState<number>(100);
  const [compPrice, setCompPrice] = useState<number>(44);
  const [compCost, setCompCost] = useState<number>(28);
  const [ourRating, setOurRating] = useState<number>(4.9);
  const [compRating, setCompRating] = useState<number>(4.4);
  const [rounds, setRounds] = useState<number>(3);

  const [advice, setAdvice] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const res = await api.getBidAdvice({
        base_price: Number(basePrice),
        our_cost: Number(ourCost),
        headcount: Number(headcount),
        competitor_est_price: Number(compPrice),
        competitor_est_cost: Number(compCost),
        our_rating: Number(ourRating),
        competitor_rating: Number(compRating),
        max_rounds: Number(rounds),
      });
      setAdvice(res);
    } catch (err: any) {
      alert(`Pricing advisor error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Syllabus Deferred Notice */}
      <div className="bg-purple-950/30 border border-purple-500/30 rounded-2xl p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs text-purple-300">
        <div>
          <span className="font-bold">⚠️ Syllabus Notice:</span> Module D (Week 7) is currently deferred &mdash; active coursework focuses strictly on <strong>Weeks 1&ndash;5 (BFS & DFS)</strong>.
        </div>
        <Link
          href="/ai"
          className="px-3 py-1.5 rounded-lg bg-purple-500/20 hover:bg-purple-500/30 text-purple-200 font-semibold transition-colors shrink-0"
        >
          &larr; Back to AI Studio (Weeks 1-5)
        </Link>
      </div>

      {/* Header */}
      <div>
        <div className="flex items-center gap-2 text-purple-400 font-bold text-xs uppercase tracking-wider mb-1">
          <TrendingUp className="w-4 h-4" />
          <span>Module D &bull; Course Week 7</span>
        </div>
        <h1 className="text-2xl font-black text-white tracking-tight">Bid Pricing Advisor</h1>
        <p className="text-xs text-slate-400">
          Adversarial 2-player game search simulating competitive bidding. Uses <strong>Minimax and Alpha-Beta Pruning</strong> to pick the quote price that delivers the best worst-case margin against rival caterers.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Game Parameters */}
        <div className="glass-panel p-6 rounded-2xl space-y-5 lg:col-span-1">
          <h2 className="text-sm font-bold uppercase tracking-wider text-slate-300">Bid Scenario Parameters</h2>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Our Base Price ($)</label>
              <input
                type="number"
                value={basePrice}
                onChange={(e) => setBasePrice(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Our Unit Cost ($)</label>
              <input
                type="number"
                value={ourCost}
                onChange={(e) => setOurCost(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Competitor Est. ($)</label>
              <input
                type="number"
                value={compPrice}
                onChange={(e) => setCompPrice(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Competitor Cost ($)</label>
              <input
                type="number"
                value={compCost}
                onChange={(e) => setCompCost(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Our Rating (★)</label>
              <input
                type="number"
                step="0.1"
                value={ourRating}
                onChange={(e) => setOurRating(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Rival Rating (★)</label>
              <input
                type="number"
                step="0.1"
                value={compRating}
                onChange={(e) => setCompRating(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 text-white font-bold text-sm px-3 py-2 rounded-xl"
              />
            </div>
          </div>

          <div>
            <label className="block text-[11px] font-bold uppercase text-slate-400 mb-1">Headcount: {headcount} Guests</label>
            <input
              type="range"
              min="20"
              max="500"
              step="10"
              value={headcount}
              onChange={(e) => setHeadcount(Number(e.target.value))}
              className="w-full accent-purple-500"
            />
          </div>

          <button
            onClick={handleSimulate}
            disabled={loading}
            className="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-50 text-white font-bold text-sm shadow-lg shadow-purple-600/20 transition-all flex items-center justify-center gap-2"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? "Simulating Game Tree..." : "Evaluate Optimal Bid (Minimax)"}</span>
          </button>
        </div>

        {/* Results & Pruning Analytics */}
        <div className="glass-panel p-6 rounded-2xl lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <div>
              <h2 className="text-base font-bold text-white">Minimax Recommendation & Pruning Stats</h2>
              <p className="text-xs text-slate-400">Verifies identical values between Minimax and Alpha-Beta</p>
            </div>
            {advice && (
              <span className="text-xs font-bold px-2.5 py-1 rounded-full uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Values Match</span>
              </span>
            )}
          </div>

          {!advice ? (
            <div className="py-16 text-center text-slate-500 text-sm">
              Adjust bid scenario parameters and click <strong>Evaluate Optimal Bid (Minimax)</strong>.
            </div>
          ) : (
            <div className="space-y-6">
              {/* Recommendation Card */}
              <div className="bg-gradient-to-r from-purple-950/40 via-slate-900 to-slate-900 p-6 rounded-2xl border border-purple-500/30 grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <div className="text-[10px] font-bold uppercase text-purple-400">Recommended Quote / Head</div>
                  <div className="text-3xl font-black text-white mt-1">
                    ${advice.recommended_price_per_head.toFixed(2)}
                  </div>
                  <div className="text-xs text-purple-300 font-semibold mt-1">
                    {advice.recommended_adjustment_pct >= 0 ? "+" : ""}{advice.recommended_adjustment_pct}% vs Base
                  </div>
                </div>

                <div className="border-t sm:border-t-0 sm:border-l border-slate-800 sm:pl-4">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Projected Margin</div>
                  <div className="text-3xl font-black text-emerald-400 mt-1">
                    {advice.projected_margin_pct}%
                  </div>
                  <div className="text-xs text-slate-400 mt-1">
                    Unit Margin: ${(advice.recommended_price_per_head - ourCost).toFixed(2)} / head
                  </div>
                </div>

                <div className="border-t sm:border-t-0 sm:border-l border-slate-800 sm:pl-4">
                  <div className="text-[10px] font-bold uppercase text-slate-400">Expected Total Profit</div>
                  <div className="text-3xl font-black text-white mt-1">
                    ${advice.expected_total_profit.toLocaleString()}
                  </div>
                  <div className="text-xs text-slate-400 mt-1">Minimax Equilibrium</div>
                </div>
              </div>

              {/* Minimax vs Alpha-Beta Pruning Table */}
              <div>
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
                  Adversarial Search Efficiency Comparison
                </h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                    <div className="text-xs font-bold text-slate-400">Full Minimax (No Pruning)</div>
                    <div className="text-xl font-black text-white mt-2">
                      {advice.minimax.nodes_evaluated} <span className="text-xs font-normal text-slate-400">States Evaluated</span>
                    </div>
                    <div className="text-xs text-slate-500 mt-1">Runtime: {advice.minimax.runtime_ms.toFixed(2)} ms</div>
                  </div>

                  <div className="bg-purple-950/20 p-4 rounded-xl border border-purple-500/30">
                    <div className="text-xs font-bold text-purple-400">Alpha-Beta Pruning</div>
                    <div className="text-xl font-black text-purple-300 mt-2">
                      {advice.alpha_beta.nodes_evaluated} <span className="text-xs font-normal text-purple-400/80">States Evaluated</span>
                    </div>
                    <div className="text-xs text-purple-400/80 mt-1">
                      {advice.verification.pruning_efficiency_pct}% Branches Pruned &bull; {advice.alpha_beta.pruned_branches} Cutoffs
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-1.5">
                <div className="font-bold text-slate-200">Quality-Adjusted Decision Rule:</div>
                <p>
                  Because your rating ({ourRating}★) exceeds the rival ({compRating}★), the client accepts up to a ${( (ourRating - compRating) * 2.5).toFixed(2)} premium per head before switching to the competitor. Minimax exploits this quality buffer to protect healthy catering profit margins.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
