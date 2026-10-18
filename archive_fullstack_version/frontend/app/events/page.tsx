"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import {
  CalendarDays,
  Users,
  AlertCircle,
  Sparkles,
  CheckCircle2,
  Clock,
  ArrowRight,
} from "lucide-react";

export default function EventsPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        await api.ensureDefaultDemoLogin();
        const data = await api.getEvents();
        setEvents(data);
      } catch (err) {
        console.error("Failed to load events:", err);
      } finally {
        setLoading(false);
      }
    };
    loadEvents();
  }, []);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Events & Catering Requests</h1>
          <p className="text-xs text-slate-400">
            Client events and dietary constraints that feed into the AI search solvers (BFS &amp; DFS).
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/ai/constraints"
            className="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white hover:bg-indigo-500 transition-all shadow-md shadow-indigo-600/20"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Open AI Menu Solver</span>
          </Link>
        </div>
      </div>

      {/* Events Table / List */}
      {loading ? (
        <div className="p-8 text-center text-xs text-slate-400">Loading events...</div>
      ) : events.length === 0 ? (
        <div className="glass-card p-8 text-center text-xs text-slate-400 rounded-2xl">
          No catering events recorded.
        </div>
      ) : (
        <div className="glass-card rounded-2xl overflow-hidden border border-slate-800">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                <tr>
                  <th className="py-3 px-4 font-semibold">Event &amp; Client</th>
                  <th className="py-3 px-4 font-semibold">Date &amp; Schedule</th>
                  <th className="py-3 px-4 font-semibold">Guests</th>
                  <th className="py-3 px-4 font-semibold">Dietary &amp; Allergen Notes</th>
                  <th className="py-3 px-4 font-semibold">Status</th>
                  <th className="py-3 px-4 font-semibold text-right">AI Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {events.map((ev) => (
                  <tr key={ev.id} className="hover:bg-slate-900/40 transition-colors">
                    <td className="py-3.5 px-4">
                      <div className="font-bold text-white text-sm">{ev.title}</div>
                      <div className="text-[11px] text-slate-400">{ev.client_name || "Standard Client"}</div>
                    </td>
                    <td className="py-3.5 px-4 text-slate-300">
                      <div className="flex items-center gap-1.5 font-medium">
                        <CalendarDays className="w-3.5 h-3.5 text-slate-400" />
                        <span>{ev.event_date}</span>
                      </div>
                      <div className="text-[11px] text-slate-500 flex items-center gap-1 mt-0.5">
                        <Clock className="w-3 h-3" />
                        <span>{ev.start_time || "12:00"} – {ev.end_time || "16:00"}</span>
                      </div>
                    </td>
                    <td className="py-3.5 px-4">
                      <span className="inline-flex items-center gap-1 text-slate-300 font-semibold bg-slate-900 border border-slate-800 px-2 py-0.5 rounded-md">
                        <Users className="w-3 h-3 text-indigo-400" />
                        {ev.headcount}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 max-w-xs">
                      {ev.notes ? (
                        <div className="flex items-start gap-1.5 text-amber-300/90 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-lg text-[11px]">
                          <AlertCircle className="w-3 h-3 mt-0.5 shrink-0 text-amber-400" />
                          <span>{ev.notes}</span>
                        </div>
                      ) : (
                        <span className="text-slate-500 text-[11px]">Standard menu (no restrictions)</span>
                      )}
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
                          ev.status === "confirmed"
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                            : "bg-indigo-500/10 text-indigo-400 border border-indigo-500/20"
                        }`}
                      >
                        <CheckCircle2 className="w-3 h-3" />
                        {ev.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href="/ai/constraints"
                        className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-indigo-600 text-slate-300 hover:text-white transition-all border border-slate-800 text-[11px] font-medium"
                      >
                        <span>Run AI Solver</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
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
