"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { getStoredSession, UserSession } from "@/lib/api";
import { Sparkles, Utensils, Calendar, ShieldCheck } from "lucide-react";

export default function Navbar() {
  const [session, setSession] = useState<UserSession | null>(null);

  useEffect(() => {
    setSession(getStoredSession());
  }, []);

  return (
    <header className="sticky top-0 z-40 border-b border-slate-800 bg-slate-950/80 backdrop-blur-md px-6 py-3.5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <Link href="/" className="flex items-center gap-2.5">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 text-white font-black text-lg">
            C
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg text-white tracking-tight">CaterIQ</span>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-2 py-0.5 rounded-full">
                AI Project 1
              </span>
            </div>
            <p className="text-xs text-slate-400">Search-Based Catering Intelligence</p>
          </div>
        </Link>
      </div>

      <div className="flex items-center gap-4">
        {session ? (
          <div className="flex items-center gap-3 bg-slate-900/90 border border-slate-800 rounded-full py-1.5 px-3.5">
            <div className="h-6 w-6 rounded-full bg-indigo-600 flex items-center justify-center text-xs font-bold text-white">
              {session.fullName.charAt(0)}
            </div>
            <div className="text-left hidden sm:block">
              <div className="text-xs font-semibold text-slate-200">{session.fullName}</div>
              <div className="text-[10px] text-slate-400">{session.organizationName}</div>
            </div>
            <span className="text-[10px] font-bold uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded-full ml-1">
              {session.role}
            </span>
          </div>
        ) : (
          <div className="text-xs text-slate-400">Demo Mode Active</div>
        )}
      </div>
    </header>
  );
}
