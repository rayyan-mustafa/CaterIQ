"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  Gauge,
  RotateCcw,
  CheckCircle2,
  TrendingDown,
  Layers,
  Sparkles,
  MapPin,
  TrendingUp,
} from "lucide-react";

export default function BenchmarksPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [syllabusScope, setSyllabusScope] = useState<"week1-5" | "all">("week1-5");

  const fetchBenchmarks = async () => {
    setLoading(true);
    try {
      await api.ensureDefaultDemoLogin();
      const res = await api.getBenchmarks();
      setData(res);
    } catch (err: any) {
      alert(`Benchmark execution failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBenchmarks();
  }, []);

  const b = data?.benchmarks;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider mb-1">
            <Gauge className="w-4 h-4" />
            <span>Empirical Algorithmic Verification Lab</span>
          </div>
          <h1 className="text-2xl font-black text-white tracking-tight">AI Algorithm Benchmarks</h1>
          <p className="text-xs text-slate-400">
            Real empirical measurements proving that our search implementations strictly adhere to foundational AI theoretical properties.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setSyllabusScope("week1-5")}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                syllabusScope === "week1-5"
                  ? "bg-indigo-600 text-white shadow-md shadow-indigo-600/20"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              Weeks 1–5 Focus
            </button>
            <button
              onClick={() => setSyllabusScope("all")}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
                syllabusScope === "all"
                  ? "bg-slate-800 text-white"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              All Labs
            </button>
          </div>

          <button
            onClick={fetchBenchmarks}
            disabled={loading}
            className="px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-xs shadow-lg shadow-indigo-600/20 transition-all flex items-center gap-2"
          >
            <RotateCcw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>{loading ? "Benchmarking..." : "Re-Run"}</span>
          </button>
        </div>
      </div>

      {loading && !data ? (
        <div className="py-24 text-center text-slate-400 text-sm">
          Executing automated benchmark runs across BFS, DFS, Greedy, A*, and Minimax...
        </div>
      ) : (
        <div className="space-y-6">
          {/* Comparison 1: DFS Plain vs Pruned */}
          <div className="glass-panel p-6 rounded-2xl space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-amber-400">
                  Experiment 1 &bull; DFS Backtracking Search Space
                </span>
                <h3 className="text-lg font-bold text-white mt-1">Plain DFS vs Early Constraint Pruning</h3>
                <p className="text-xs text-slate-400">Combinatorial space: {b?.dfs_plain_vs_pruned?.combinations_space} dish combinations</p>
              </div>
              <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full">
                {b?.dfs_plain_vs_pruned?.reduction_percentage}% Tree Reduction
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                <div className="text-xs font-bold text-slate-400 uppercase">Plain DFS</div>
                <div className="text-2xl font-black text-white mt-1">
                  {b?.dfs_plain_vs_pruned?.plain_dfs?.nodes_expanded}
                  <span className="text-xs font-normal text-slate-500 ml-1">Nodes Expanded</span>
                </div>
                <div className="text-xs text-slate-400 mt-1">
                  Runtime: {b?.dfs_plain_vs_pruned?.plain_dfs?.runtime_ms?.toFixed(2)} ms
                </div>
              </div>

              <div className="bg-amber-950/20 p-4 rounded-xl border border-amber-500/20">
                <div className="text-xs font-bold text-amber-400 uppercase">Pruned DFS</div>
                <div className="text-2xl font-black text-amber-300 mt-1">
                  {b?.dfs_plain_vs_pruned?.pruned_dfs?.nodes_expanded}
                  <span className="text-xs font-normal text-amber-400/80 ml-1">Nodes Expanded</span>
                </div>
                <div className="text-xs text-amber-400/80 mt-1">
                  Runtime: {b?.dfs_plain_vs_pruned?.pruned_dfs?.runtime_ms?.toFixed(2)} ms
                </div>
              </div>
            </div>
          </div>

          {syllabusScope === "week1-5" ? (
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 bg-slate-950/40 text-center py-8">
              <div className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-1">
                Upcoming Coursework
              </div>
              <h4 className="text-sm font-bold text-slate-300">
                Module C (A* Routing) &amp; Module D (Minimax Game Search) Benchmarks Deferred
              </h4>
              <p className="text-xs text-slate-500 max-w-md mx-auto mt-1 mb-4">
                Per course syllabus guidelines, active focus is restricted to Weeks 1&ndash;5 (BFS &amp; DFS). Click &quot;All Labs&quot; above to preview upcoming modules.
              </p>
              <button
                onClick={() => setSyllabusScope("all")}
                className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 border border-slate-700 transition-colors"
              >
                Preview All Labs
              </button>
            </div>
          ) : (
            <>
              {/* Comparison 2: Greedy Best-First vs A* */}
              <div className="glass-panel p-6 rounded-2xl space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                      Experiment 2 &bull; Path Cost &amp; Optimality
                    </span>
                    <h3 className="text-lg font-bold text-white mt-1">Greedy Best-First vs A* Search</h3>
                    <p className="text-xs text-slate-400">
                      Route: {b?.greedy_vs_astar?.start} &rarr; {b?.greedy_vs_astar?.goal}
                    </p>
                  </div>
                  <span className="text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full flex items-center gap-1">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>A* Cost &le; Greedy Verified</span>
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                    <div className="text-xs font-bold text-amber-400 uppercase">Greedy Best-First (Heuristic Only)</div>
                    <div className="text-2xl font-black text-white mt-1">
                      {b?.greedy_vs_astar?.greedy?.total_minutes} <span className="text-xs font-normal text-slate-400">Minutes</span>
                    </div>
                    <div className="text-xs text-slate-400 mt-1">
                      Nodes Expanded: <strong>{b?.greedy_vs_astar?.greedy?.nodes_expanded}</strong> &bull; Runtime:{" "}
                      <strong>{b?.greedy_vs_astar?.greedy?.runtime_ms?.toFixed(2)} ms</strong>
                    </div>
                  </div>

                  <div className="bg-emerald-950/20 p-4 rounded-xl border border-emerald-500/20">
                    <div className="text-xs font-bold text-emerald-400 uppercase">A* Search (Cost + Admissible h)</div>
                    <div className="text-2xl font-black text-emerald-400 mt-1">
                      {b?.greedy_vs_astar?.astar?.total_minutes} <span className="text-xs font-normal text-emerald-300">Minutes</span>
                    </div>
                    <div className="text-xs text-emerald-400/80 mt-1">
                      Nodes Expanded: <strong>{b?.greedy_vs_astar?.astar?.nodes_expanded}</strong> &bull; Runtime:{" "}
                      <strong>{b?.greedy_vs_astar?.astar?.runtime_ms?.toFixed(2)} ms</strong>
                    </div>
                  </div>
                </div>
              </div>

              {/* Comparison 3: Minimax vs Alpha-Beta */}
              <div className="glass-panel p-6 rounded-2xl space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold uppercase tracking-wider text-purple-400">
                      Experiment 3 &bull; Game Tree Search
                    </span>
                    <h3 className="text-lg font-bold text-white mt-1">Full Minimax vs Alpha-Beta Pruning</h3>
                    <p className="text-xs text-slate-400">2-Player competitive pricing game</p>
                  </div>
                  <span className="text-xs font-bold text-purple-400 bg-purple-500/10 border border-purple-500/20 px-3 py-1 rounded-full">
                    {b?.minimax_vs_alphabeta?.verification?.pruning_efficiency_pct}% Pruning Cutoff
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                    <div className="text-xs font-bold text-slate-400 uppercase">Full Minimax</div>
                    <div className="text-2xl font-black text-white mt-1">
                      {b?.minimax_vs_alphabeta?.minimax?.nodes_evaluated}
                      <span className="text-xs font-normal text-slate-500 ml-1">States Evaluated</span>
                    </div>
                    <div className="text-xs text-slate-400 mt-1">
                      Runtime: {b?.minimax_vs_alphabeta?.minimax?.runtime_ms?.toFixed(2)} ms
                    </div>
                  </div>

                  <div className="bg-purple-950/20 p-4 rounded-xl border border-purple-500/20">
                    <div className="text-xs font-bold text-purple-400 uppercase">Alpha-Beta Pruning</div>
                    <div className="text-2xl font-black text-purple-300 mt-1">
                      {b?.minimax_vs_alphabeta?.alpha_beta?.nodes_evaluated}
                      <span className="text-xs font-normal text-purple-400/80 ml-1">States Evaluated</span>
                    </div>
                    <div className="text-xs text-purple-400/80 mt-1">
                      Pruned Branches: <strong>{b?.minimax_vs_alphabeta?.alpha_beta?.pruned_branches}</strong> &bull; Expected Profit:{" "}
                      <strong>${b?.minimax_vs_alphabeta?.expected_total_profit}</strong>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}

          {/* Recent AI Runs History Table */}
          {data?.recent_runs && data.recent_runs.length > 0 && (
            <div className="glass-panel p-6 rounded-2xl">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 mb-4">
                Recent AI Execution Logs (ai_runs Table)
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-500 uppercase">
                      <th className="pb-2">Algorithm Module</th>
                      <th className="pb-2">Nodes / States</th>
                      <th className="pb-2">Execution Latency</th>
                      <th className="pb-2 text-right">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    {data.recent_runs.map((run: any) => (
                      <tr key={run.id} className="hover:bg-slate-900/40">
                        <td className="py-2.5 font-bold text-white font-mono">{run.module}</td>
                        <td className="py-2.5">{run.nodes_expanded} nodes</td>
                        <td className="py-2.5 text-indigo-400 font-semibold">{run.runtime_ms.toFixed(2)} ms</td>
                        <td className="py-2.5 text-right text-slate-500">{run.created_at.slice(0, 19)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
