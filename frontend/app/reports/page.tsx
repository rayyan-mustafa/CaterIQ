"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  FileBarChart,
  Download,
  DollarSign,
  TrendingUp,
  AlertCircle,
  FileSpreadsheet,
} from "lucide-react";

export default function ReportsPage() {
  const [profitData, setProfitData] = useState<any>(null);
  const [agingData, setAgingData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadReports() {
      try {
        await api.ensureDefaultDemoLogin();
        const [pData, aData] = await Promise.all([
          api.getProfitReport(),
          api.getOutstandingInvoices(),
        ]);
        setProfitData(pData);
        setAgingData(aData);
      } catch (err) {
        console.error("Failed to load reports:", err);
      } finally {
        setLoading(false);
      }
    }
    loadReports();
  }, []);

  const handleDownloadCSV = () => {
    window.open("http://127.0.0.1:8000/api/v1/reports/profit?format=csv", "_blank");
  };

  const summary = profitData?.summary;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Financial Reports & Profitability</h1>
          <p className="text-xs text-slate-400">
            Realized event margins, food cost breakdowns, and receivables aging (answering user complaints from market research)
          </p>
        </div>

        <button
          onClick={handleDownloadCSV}
          className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/20 transition-all flex items-center gap-2"
        >
          <Download className="w-3.5 h-3.5" />
          <span>Export Profit CSV</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Total Billed Revenue</div>
          <div className="text-2xl font-black text-white">
            ${summary?.total_revenue ? summary.total_revenue.toLocaleString() : "0.00"}
          </div>
          <div className="text-xs text-slate-500 mt-1">{summary?.events_analyzed || 0} Events Analyzed</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Total Food Cost</div>
          <div className="text-2xl font-black text-slate-300">
            ${summary?.total_food_cost ? summary.total_food_cost.toLocaleString() : "0.00"}
          </div>
          <div className="text-xs text-slate-500 mt-1">Raw Ingredient Expenses</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Net Event Profit</div>
          <div className="text-2xl font-black text-emerald-400">
            ${summary?.net_profit ? summary.net_profit.toLocaleString() : "0.00"}
          </div>
          <div className="text-xs text-emerald-400/80 mt-1">Realized Gross Margin</div>
        </div>

        <div className="glass-panel p-5 rounded-2xl">
          <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Average Profit Margin</div>
          <div className="text-2xl font-black text-indigo-400">
            {summary?.overall_margin_pct || "0.0"}%
          </div>
          <div className="text-xs text-indigo-400/80 mt-1">Target: &gt; 60%</div>
        </div>
      </div>

      {/* Profit by Event Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-white">Profit & Margin Per Event</h2>
            <p className="text-xs text-slate-400">Calculated as: (Menu Price &times; Headcount) &minus; (Cost &times; Headcount)</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                <th className="pb-3 font-semibold">Event Title</th>
                <th className="pb-3 font-semibold">Client</th>
                <th className="pb-3 font-semibold text-center">Headcount</th>
                <th className="pb-3 font-semibold text-right">Revenue</th>
                <th className="pb-3 font-semibold text-right">Food Cost</th>
                <th className="pb-3 font-semibold text-right">Profit</th>
                <th className="pb-3 font-semibold text-right">Margin %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {profitData?.events?.map((ev: any) => (
                <tr key={ev.event_id} className="hover:bg-slate-900/40">
                  <td className="py-3.5 font-semibold text-white">
                    <div>{ev.title}</div>
                    <div className="text-xs text-slate-500">{ev.event_date}</div>
                  </td>
                  <td className="py-3.5 text-slate-300">{ev.client_name}</td>
                  <td className="py-3.5 text-center text-slate-300">{ev.headcount}</td>
                  <td className="py-3.5 text-right font-bold text-white">${ev.revenue.toLocaleString()}</td>
                  <td className="py-3.5 text-right text-slate-400">${ev.food_cost.toLocaleString()}</td>
                  <td className="py-3.5 text-right font-bold text-emerald-400">${ev.profit.toLocaleString()}</td>
                  <td className="py-3.5 text-right font-bold text-indigo-400">{ev.margin_pct}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Receivables Aging Buckets */}
      {agingData && (
        <div className="glass-panel p-6 rounded-2xl space-y-4">
          <div>
            <h2 className="text-base font-bold text-white">Outstanding Invoices Aging Analysis</h2>
            <p className="text-xs text-slate-400">Total Unpaid Balance: ${agingData.total_outstanding.toLocaleString()}</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="text-xs font-bold text-emerald-400 uppercase">Current (0 - 30 Days)</div>
              <div className="text-xl font-bold text-white mt-1">
                ${agingData.buckets?.current_to_30_days?.toLocaleString()}
              </div>
            </div>

            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="text-xs font-bold text-amber-400 uppercase">31 - 60 Days Overdue</div>
              <div className="text-xl font-bold text-white mt-1">
                ${agingData.buckets?.["31_to_60_days"]?.toLocaleString()}
              </div>
            </div>

            <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800">
              <div className="text-xs font-bold text-rose-400 uppercase">60+ Days Delinquent</div>
              <div className="text-xl font-bold text-white mt-1">
                ${agingData.buckets?.["60_plus_days"]?.toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
