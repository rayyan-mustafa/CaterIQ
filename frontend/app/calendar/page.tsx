"use client";

import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import {
  CalendarDays,
  Copy,
  Check,
  RefreshCw,
  ExternalLink,
  MapPin,
  Clock,
  Users,
} from "lucide-react";

export default function CalendarPage() {
  const [events, setEvents] = useState<any[]>([]);
  const [calTokenInfo, setCalTokenInfo] = useState<{ token: string; feed_url: string } | null>(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadCalendar() {
      try {
        await api.ensureDefaultDemoLogin();
        const [evList, tok] = await Promise.all([
          api.getCalendarEvents(),
          api.getCalendarToken(),
        ]);
        setEvents(evList);
        setCalTokenInfo(tok);
      } catch (err) {
        console.error("Failed to load calendar:", err);
      } finally {
        setLoading(false);
      }
    }
    loadCalendar();
  }, []);

  const fullFeedUrl = calTokenInfo
    ? `${window?.location?.origin || "http://localhost:8000"}${calTokenInfo.feed_url}`
    : "";

  const handleCopy = () => {
    navigator.clipboard.writeText(fullFeedUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight">Calendar & Schedule</h1>
        <p className="text-xs text-slate-400">Sync with Apple Calendar, Google Calendar, or Outlook via private RFC 5545 iCal feed</p>
      </div>

      {/* iCal Subscription Banner */}
      <div className="glass-panel p-5 rounded-2xl border-indigo-500/20 bg-gradient-to-r from-indigo-950/40 to-slate-900/60">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm mb-1">
              <CalendarDays className="w-4 h-4" />
              <span>Live Calendar Subscription Feed</span>
            </div>
            <p className="text-xs text-slate-300">
              Subscribe once in your phone calendar and all confirmed catering bookings will sync automatically.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <input
              type="text"
              readOnly
              value={fullFeedUrl}
              className="bg-slate-900 border border-slate-700 text-slate-300 text-xs px-3 py-2 rounded-xl w-64 md:w-80 select-all"
            />
            <button
              onClick={handleCopy}
              className="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all"
            >
              {copied ? <Check className="w-4 h-4 text-emerald-300" /> : <Copy className="w-4 h-4" />}
              <span>{copied ? "Copied!" : "Copy Feed URL"}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Events Timeline */}
      <div className="space-y-3">
        <h2 className="text-sm font-bold uppercase tracking-wider text-slate-400">Scheduled Bookings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {events.map((ev) => (
            <div key={ev.id} className="glass-card p-5 rounded-2xl space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/20">
                  {ev.start.split("T")[0]}
                </span>
                <span
                  className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                    ev.status === "confirmed"
                      ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                      : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                  }`}
                >
                  {ev.status}
                </span>
              </div>

              <div>
                <h3 className="font-bold text-white text-base leading-snug">{ev.title}</h3>
                <div className="text-xs text-slate-400 mt-1">Client: {ev.client_name}</div>
              </div>

              <div className="space-y-1.5 text-xs text-slate-400 border-t border-slate-800/80 pt-3">
                <div className="flex items-center gap-2">
                  <Clock className="w-3.5 h-3.5 text-slate-500" />
                  <span>{ev.start.split("T")[1]?.slice(0, 5)} - {ev.end.split("T")[1]?.slice(0, 5)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-3.5 h-3.5 text-slate-500" />
                  <span>{ev.headcount} Guests</span>
                </div>
                <div className="flex items-center gap-2">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" />
                  <span className="truncate">{ev.venue}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
