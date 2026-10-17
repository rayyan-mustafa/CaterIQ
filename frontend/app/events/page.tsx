"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  Calendar,
  Users,
  DollarSign,
  Plus,
  FileText,
  CheckCircle,
  Clock,
  ExternalLink,
  ChevronRight,
  TrendingUp,
} from "lucide-react";

export default function EventsPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [selectedStatus, setSelectedStatus] = useState<string>("all");
  const [loading, setLoading] = useState(true);
  const [proposalMsg, setProposalMsg] = useState<{ [key: string]: string }>({});

  const loadEvents = async () => {
    try {
      await api.ensureDefaultDemoLogin();
      const data = await api.getEvents(selectedStatus === "all" ? undefined : selectedStatus);
      setEvents(data);
    } catch (err) {
      console.error("Failed to load events:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, [selectedStatus]);

  const handleGenerateProposal = async (eventId: string) => {
    try {
      const prop = await api.createProposal(eventId, 30);
      setProposalMsg((prev) => ({
        ...prev,
        [eventId]: `Proposal #${prop.version} created! Public token: ${prop.public_token}`,
      }));
      loadEvents();
    } catch (err: any) {
      alert(`Error creating proposal: ${err.message}`);
    }
  };

  const handleAdvanceStatus = async (eventId: string, nextStatus: string) => {
    try {
      await api.updateEventStatus(eventId, nextStatus);
      loadEvents();
    } catch (err: any) {
      alert(`Error updating status: ${err.message}`);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Events & Orders</h1>
          <p className="text-xs text-slate-400">Manage client catering events, menus, pricing, and proposals</p>
        </div>
        <div className="flex items-center gap-2">
          {["all", "confirmed", "proposed", "lead", "completed"].map((st) => (
            <button
              key={st}
              onClick={() => setSelectedStatus(st)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold capitalize transition-all ${
                selectedStatus === st
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {/* Events Grid */}
      <div className="grid grid-cols-1 gap-4">
        {events.map((ev) => (
          <div key={ev.id} className="glass-panel p-6 rounded-2xl space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
              <div>
                <div className="flex items-center gap-3">
                  <h3 className="text-lg font-bold text-white">{ev.title}</h3>
                  <span
                    className={`px-2.5 py-0.5 rounded-full text-xs font-semibold uppercase tracking-wider ${
                      ev.status === "confirmed"
                        ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                        : ev.status === "proposed"
                        ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        : ev.status === "completed"
                        ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                        : "bg-slate-700 text-slate-300"
                    }`}
                  >
                    {ev.status}
                  </span>
                </div>
                <div className="text-xs text-slate-400 mt-1 flex flex-wrap items-center gap-4">
                  <span>Client: <strong className="text-slate-200">{ev.client_name}</strong></span>
                  <span>Date: <strong className="text-slate-200">{ev.event_date}</strong> ({ev.start_time || "11:00"} - {ev.end_time || "15:00"})</span>
                  <span>Venue: <strong className="text-slate-200">{ev.venue_address || "Commissary Kitchen"}</strong></span>
                </div>
              </div>

              {/* Financial Box */}
              <div className="flex items-center gap-6 bg-slate-900/80 px-4 py-2.5 rounded-xl border border-slate-800">
                <div>
                  <div className="text-[10px] uppercase font-semibold text-slate-500">Headcount</div>
                  <div className="text-base font-bold text-slate-200">{ev.headcount} Guests</div>
                </div>
                <div className="border-l border-slate-800 pl-4">
                  <div className="text-[10px] uppercase font-semibold text-slate-500">Revenue</div>
                  <div className="text-base font-bold text-emerald-400">${ev.total_revenue.toLocaleString()}</div>
                </div>
                <div className="border-l border-slate-800 pl-4">
                  <div className="text-[10px] uppercase font-semibold text-slate-500">Est. Profit</div>
                  <div className="text-base font-bold text-indigo-400">
                    ${ev.projected_profit.toLocaleString()} ({ev.profit_margin_pct}%)
                  </div>
                </div>
              </div>
            </div>

            {/* Menu Items Table */}
            {ev.items && ev.items.length > 0 && (
              <div className="border-t border-slate-800/80 pt-3">
                <div className="text-xs font-semibold text-slate-400 mb-2">Attached Menu Items</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2">
                  {ev.items.map((it: any) => (
                    <div key={it.id} className="bg-slate-900/60 p-2.5 rounded-xl border border-slate-800/60 flex items-center justify-between text-xs">
                      <div>
                        <div className="font-semibold text-slate-200">{it.menu_item_name}</div>
                        <div className="text-[10px] text-slate-400 capitalize">{it.category} &bull; ${it.unit_price}/head</div>
                      </div>
                      <div className="font-bold text-slate-300">
                        ${it.line_total?.toLocaleString()}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Actions Bar */}
            <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-800/60">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleGenerateProposal(ev.id)}
                  className="px-3 py-1.5 rounded-lg bg-indigo-600/90 hover:bg-indigo-600 text-white font-medium text-xs flex items-center gap-1.5 transition-colors"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Generate Proposal</span>
                </button>
                {ev.status === "lead" && (
                  <button
                    onClick={() => handleAdvanceStatus(ev.id, "proposed")}
                    className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-medium text-xs"
                  >
                    Mark as Proposed
                  </button>
                )}
                {ev.status === "proposed" && (
                  <button
                    onClick={() => handleAdvanceStatus(ev.id, "confirmed")}
                    className="px-3 py-1.5 rounded-lg bg-emerald-600/90 hover:bg-emerald-600 text-white font-medium text-xs"
                  >
                    Confirm Event
                  </button>
                )}
                {ev.status === "confirmed" && (
                  <button
                    onClick={() => handleAdvanceStatus(ev.id, "completed")}
                    className="px-3 py-1.5 rounded-lg bg-blue-600/90 hover:bg-blue-600 text-white font-medium text-xs"
                  >
                    Mark as Completed
                  </button>
                )}
              </div>

              {proposalMsg[ev.id] && (
                <div className="text-xs text-indigo-400 font-semibold flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" />
                  <span>{proposalMsg[ev.id]}</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
