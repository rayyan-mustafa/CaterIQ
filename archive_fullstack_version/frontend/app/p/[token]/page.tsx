"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { api } from "@/lib/api";
import {
  FileText,
  CheckCircle2,
  Calendar,
  MapPin,
  Users,
  CreditCard,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

export default function PublicProposalPage() {
  const params = useParams();
  const token = params?.token as string;

  const [proposal, setProposal] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [paymentSuccess, setPaymentSuccess] = useState(false);

  useEffect(() => {
    async function loadProposal() {
      if (!token) return;
      try {
        const data = await api.getPublicProposal(token);
        setProposal(data);
      } catch (err: any) {
        console.error("Failed to load proposal:", err);
      } finally {
        setLoading(false);
      }
    }
    loadProposal();
  }, [token]);

  const handleApproveAndPay = async () => {
    setProcessing(true);
    try {
      // 1. Approve proposal & create deposit invoice
      const appRes = await api.approvePublicProposal(token);

      // 2. Complete simulated Stripe test payment
      const checkoutRes = await api.checkoutInvoice(appRes.invoice_id);

      setPaymentSuccess(true);
      setProposal((prev: any) => ({
        ...prev,
        status: "approved",
      }));
    } catch (err: any) {
      alert(`Approval failed: ${err.message}`);
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-slate-400 text-sm">
        Loading catering proposal...
      </div>
    );
  }

  if (!proposal) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
        <div className="glass-panel p-8 rounded-3xl max-w-md text-center space-y-3">
          <FileText className="w-12 h-12 text-slate-600 mx-auto" />
          <h2 className="text-xl font-bold text-white">Proposal Not Found</h2>
          <p className="text-xs text-slate-400">
            This proposal link is invalid or has expired. Please contact your caterer for a revised link.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 py-12 px-4 sm:px-6">
      <div className="max-w-3xl mx-auto space-y-6">
        {/* Header */}
        <div className="glass-panel p-8 rounded-3xl border-indigo-500/20 bg-gradient-to-b from-slate-900 to-slate-950">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6 mb-6">
            <div>
              <div className="flex items-center gap-2 text-indigo-400 font-bold text-xs uppercase tracking-wider mb-1">
                <Sparkles className="w-4 h-4" />
                <span>Apex Artisan Catering &bull; Official Proposal</span>
              </div>
              <h1 className="text-2xl sm:text-3xl font-black text-white">{proposal.event_title}</h1>
            </div>

            <div>
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                  proposal.status === "approved" || paymentSuccess
                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                    : "bg-amber-500/10 text-amber-400 border border-amber-500/30"
                }`}
              >
                {paymentSuccess ? "APPROVED & PAID" : proposal.status.toUpperCase()}
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs text-slate-300">
            <div className="flex items-center gap-2.5">
              <Calendar className="w-4 h-4 text-indigo-400" />
              <span>Event Date: <strong>{proposal.event_date}</strong></span>
            </div>
            <div className="flex items-center gap-2.5">
              <Users className="w-4 h-4 text-indigo-400" />
              <span>Headcount: <strong>{proposal.headcount} Guests</strong></span>
            </div>
            <div className="flex items-center gap-2.5">
              <MapPin className="w-4 h-4 text-indigo-400" />
              <span>Venue: <strong>{proposal.venue || "On Location"}</strong></span>
            </div>
          </div>
        </div>

        {/* Menu Items Table */}
        <div className="glass-panel p-8 rounded-3xl space-y-6">
          <h2 className="text-base font-bold text-white">Curated Event Menu</h2>
          <div className="divide-y divide-slate-800/80">
            {proposal.items?.map((item: any, idx: number) => (
              <div key={idx} className="py-3 flex items-center justify-between text-sm">
                <div>
                  <div className="font-semibold text-white">{item.name}</div>
                  <div className="text-xs text-slate-400 capitalize">{item.category}</div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-white">${item.line_total.toLocaleString()}</div>
                  <div className="text-[11px] text-slate-500">${item.unit_price} &times; {proposal.headcount}</div>
                </div>
              </div>
            ))}
          </div>

          {/* Pricing Summary */}
          <div className="border-t border-slate-800 pt-6 space-y-2">
            <div className="flex justify-between text-sm text-slate-400">
              <span>Total Catering Package:</span>
              <span className="font-bold text-white">${proposal.total_amount.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm text-indigo-400 font-semibold">
              <span>Required Deposit ({proposal.deposit_percent}%):</span>
              <span>${proposal.deposit_amount.toLocaleString()}</span>
            </div>
            <div className="flex justify-between text-sm text-slate-500">
              <span>Balance Remaining (Due 7 days before event):</span>
              <span>${(proposal.total_amount - proposal.deposit_amount).toLocaleString()}</span>
            </div>
          </div>

          {/* Action Box */}
          <div className="border-t border-slate-800 pt-6">
            {paymentSuccess || proposal.status === "approved" ? (
              <div className="bg-emerald-950/20 border border-emerald-500/30 p-6 rounded-2xl text-center space-y-2">
                <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
                <h3 className="font-bold text-white text-base">Booking Confirmed!</h3>
                <p className="text-xs text-emerald-300">
                  Thank you! Your 30% deposit has been processed in Stripe test mode. Your catering date is now officially locked in our calendar.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Secure 256-bit encrypted checkout via Stripe Test Mode</span>
                </div>
                <button
                  onClick={handleApproveAndPay}
                  disabled={processing}
                  className="w-full py-4 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-extrabold text-base shadow-xl shadow-indigo-600/30 transition-all flex items-center justify-center gap-2"
                >
                  <CreditCard className="w-5 h-5" />
                  <span>
                    {processing ? "Processing Test Checkout..." : `Approve & Pay Deposit ($${proposal.deposit_amount.toLocaleString()})`}
                  </span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
