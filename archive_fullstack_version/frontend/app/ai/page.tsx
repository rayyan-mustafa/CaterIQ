"use client";

import React from "react";
import Link from "next/link";
import {
  ShieldAlert,
  Sliders,
  Sparkles,
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Lock,
} from "lucide-react";

export default function AIStudioHubPage() {
  return (
    <div className="space-y-8">
      {/* Header Banner */}
      <div className="relative overflow-hidden rounded-3xl p-8 bg-gradient-to-r from-indigo-950 via-slate-900 to-slate-950 border border-indigo-500/20 shadow-2xl">
        <div className="relative z-10 max-w-3xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-4">
            <BookOpen className="w-3.5 h-3.5" />
            <span>Active Syllabus Focus: Week 1 &ndash; Week 5</span>
          </div>
          <h1 className="text-3xl font-black text-white tracking-tight mb-2">
            AI Search Studio
          </h1>
          <p className="text-slate-300 text-sm leading-relaxed mb-4">
            Focused implementation of foundational state-space search algorithms covered in 
            <strong> Weeks 1&ndash;5 (Labs 04 and 05)</strong>: Uninformed Breadth-First Search (BFS) for minimal allergen swaps and Depth-First Search (DFS) with constraint-based backtracking pruning.
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-400 font-medium">
            <CheckCircle2 className="w-4 h-4" />
            <span>100% Pure Python Search Engine &bull; Zero external heuristics or black-box solvers</span>
          </div>
        </div>
      </div>

      {/* Active Modules (Weeks 1 - 5) */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white">Active Curriculum Modules</h2>
            <p className="text-xs text-slate-400">Taught algorithms actively verified in this project</p>
          </div>
          <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-2.5 py-1 rounded-full">
            2 Active Labs
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Module A */}
          <Link
            href="/ai/allergen"
            className="glass-card p-6 rounded-2xl group border border-slate-800 hover:border-rose-500/40 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-rose-400 bg-rose-500/10 border border-rose-500/20 px-2.5 py-1 rounded-lg">
                  Module A &bull; Week 4 (Lab 04)
                </span>
                <span className="text-xs font-mono font-bold text-slate-400 group-hover:text-rose-400 transition-colors">
                  BFS Search
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-rose-300 transition-colors flex items-center gap-2">
                <ShieldAlert className="w-5 h-5 text-rose-400" />
                Allergen Substitution Finder
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-6">
                Applies <strong>Breadth-First Search (FIFO queue)</strong> across the ingredient replacement graph to discover the provably shortest chain of safe ingredient swaps for guests with peanut, gluten, dairy, or nut allergies.
              </p>
            </div>
            <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs font-semibold text-rose-400">
              <span>Launch Allergen Solver</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform" />
            </div>
          </Link>

          {/* Module B */}
          <Link
            href="/ai/constraints"
            className="glass-card p-6 rounded-2xl group border border-slate-800 hover:border-amber-500/40 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-lg">
                  Module B &bull; Week 5 (Lab 05)
                </span>
                <span className="text-xs font-mono font-bold text-slate-400 group-hover:text-amber-400 transition-colors">
                  Pruned DFS
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mb-2 group-hover:text-amber-300 transition-colors flex items-center gap-2">
                <Sliders className="w-5 h-5 text-amber-400" />
                Menu Constraint Solver
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed mb-6">
                Uses <strong>Depth-First Search (DFS) with backtracking</strong> and early constraint violation pruning to synthesize 3-course packages under strict client budget and dietary constraints (vegetarian, gluten-free).
              </p>
            </div>
            <div className="pt-4 border-t border-slate-800/80 flex items-center justify-between text-xs font-semibold text-amber-400">
              <span>Launch Constraint Solver</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1.5 transition-transform" />
            </div>
          </Link>
        </div>
      </div>

      {/* Upcoming / Deferred Modules */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800/80 bg-slate-950/40">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Lock className="w-4 h-4 text-slate-500" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
              Deferred Modules (Pending Subsequent Lectures)
            </h3>
          </div>
          <span className="text-[11px] font-semibold text-slate-500 bg-slate-900 px-2 py-0.5 rounded">
            Weeks 6 &ndash; 7
          </span>
        </div>
        <p className="text-xs text-slate-500 leading-relaxed">
          <strong>Module C (A* Search & Greedy Best-First)</strong> and <strong>Module D (Adversarial Minimax Game Theory)</strong> are deferred from active evaluation per class syllabus progression.
        </p>
      </div>
    </div>
  );
}
