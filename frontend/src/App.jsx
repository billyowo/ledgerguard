import React, { useState, useEffect } from "react";
import {
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  FileText,
  DollarSign,
  TrendingUp,
  CheckCircle2,
  XCircle,
  AlertCircle,
  RefreshCw,
  Send,
  Eye,
  Building2,
  Lock,
  Layers,
  FileSpreadsheet,
  ArrowUpRight,
  UserCheck
} from "lucide-react";

const API_BASE = "http://127.0.0.1:8000/api";

export default function App() {
  const [metrics, setMetrics] = useState(null);
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [activeTab, setActiveTab] = useState("all");
  const [auditLog, setAuditLog] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reviewModal, setReviewModal] = useState(false);
  const [reviewAction, setReviewAction] = useState("");
  const [reviewNotes, setReviewNotes] = useState("");
  const [submittingReview, setSubmittingReview] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [mRes, rRes, aRes] = await Promise.all([
        fetch(`${API_BASE}/dashboard-metrics`).then((r) => r.json()),
        fetch(`${API_BASE}/reports`).then((r) => r.json()),
        fetch(`${API_BASE}/audit-log`).then((r) => r.json())
      ]);
      setMetrics(mRes);
      setReports(rRes);
      setAuditLog(aRes);
      if (rRes.length > 0 && !selectedReport) {
        setSelectedReport(rRes[0]);
      } else if (selectedReport) {
        const updated = rRes.find((x) => x.match_id === selectedReport.match_id);
        if (updated) setSelectedReport(updated);
      }
    } catch (err) {
      console.error("API Fetch Error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleResetDemo = async () => {
    try {
      await fetch(`${API_BASE}/reset-demo`, { method: "POST" });
      fetchData();
    } catch (err) {
      console.error(err);
    }
  };

  const handleOpenReview = (action) => {
    setReviewAction(action);
    setReviewNotes(
      action === "APPROVE"
        ? "Verified business justification and approved override."
        : action === "DISPUTE"
        ? "Holding payment pending supplier issuance of revised credit memo."
        : "Rejected due to critical compliance failure."
    );
    setReviewModal(true);
  };

  const submitReview = async () => {
    if (!selectedReport) return;
    setSubmittingReview(true);
    try {
      const res = await fetch(`${API_BASE}/reports/${selectedReport.match_id}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: reviewAction,
          notes: reviewNotes
        })
      });
      if (res.ok) {
        setReviewModal(false);
        fetchData();
      }
    } catch (err) {
      console.error(err);
    } finally {
      setSubmittingReview(false);
    }
  };

  const filteredReports = reports.filter((r) => {
    if (activeTab === "flagged") return r.match_status === "FLAGGED_FOR_REVIEW";
    if (activeTab === "approved") return r.match_status === "APPROVED";
    if (activeTab === "disputed") return r.match_status === "DISPUTED" || r.match_status === "REJECTED";
    return true;
  });

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Header Bar */}
      <header className="border-b border-slate-800/80 bg-slate-900/60 backdrop-blur-md sticky top-0 z-30 px-6 py-4 flex items-center justify-between shadow-xl">
        <div className="flex items-center space-x-3">
          <div className="p-2.5 bg-gradient-to-tr from-indigo-600 to-violet-500 rounded-xl shadow-lg shadow-indigo-500/20 ring-1 ring-white/20">
            <Lock className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
                LedgerGuard AI
              </h1>
              <span className="text-xs uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                Track 2: Office of the CFO
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Autonomous Accounts Payable Reconciliation, Fraud Sentinel & Human-in-the-Loop Review
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1.5 px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/20 rounded-lg text-emerald-400 text-xs font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Agent Controller Online</span>
          </div>
          <button
            onClick={handleResetDemo}
            className="flex items-center space-x-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 active:scale-95 transition-all text-xs font-medium rounded-lg text-slate-200 border border-slate-700 shadow-sm"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset Demo Scenarios</span>
          </button>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 p-6 space-y-6 max-w-[1600px] mx-auto w-full">
        {/* KPI Stats Strip */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-900/40 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Audited Spend</p>
                <h3 className="text-2xl font-bold text-white mt-1">
                  ${metrics ? metrics.total_spend_evaluated.toLocaleString(undefined, { minimumFractionDigits: 2 }) : "0.00"}
                </h3>
              </div>
              <div className="p-2.5 bg-blue-500/10 border border-blue-500/20 text-blue-400 rounded-xl">
                <DollarSign className="w-5 h-5" />
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-3 flex items-center">
              <span className="text-emerald-400 font-medium mr-1.5 flex items-center">
                <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> 100%
              </span>{" "}
              evaluated by 3-Way Engine
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-900/40 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Auto-Approval Rate</p>
                <h3 className="text-2xl font-bold text-emerald-400 mt-1">
                  {metrics ? `${metrics.auto_approval_rate_pct}%` : "0%"}
                </h3>
              </div>
              <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
                <ShieldCheck className="w-5 h-5" />
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-3">
              <span className="font-semibold text-slate-200">{metrics?.auto_approved_count || 0}</span> touchless approvals
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-900/40 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Discrepancy / Fraud Saved</p>
                <h3 className="text-2xl font-bold text-amber-400 mt-1">
                  ${metrics ? metrics.discrepancy_and_fraud_savings.toLocaleString(undefined, { minimumFractionDigits: 2 }) : "0.00"}
                </h3>
              </div>
              <div className="p-2.5 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-xl">
                <TrendingUp className="w-5 h-5" />
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-3">Prevented leakage & bank hijack</p>
          </div>

          <div className="p-5 rounded-2xl bg-gradient-to-b from-slate-900/90 to-slate-900/40 border border-slate-800 shadow-lg relative overflow-hidden group hover:border-slate-700 transition">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">HITL Exceptions Queue</p>
                <h3 className="text-2xl font-bold text-rose-400 mt-1">
                  {metrics ? metrics.flagged_for_review_count : 0}
                </h3>
              </div>
              <div className="p-2.5 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl">
                <AlertTriangle className="w-5 h-5" />
              </div>
            </div>
            <p className="text-xs text-slate-400 mt-3">Requires CFO / Controller review</p>
          </div>
        </div>

        {/* 2-Column Split: Invoices List vs Deep Detail Inspection */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Invoices & Exception Queue (5 cols) */}
          <div className="lg:col-span-5 space-y-4">
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-xl">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Layers className="w-4 h-4 text-indigo-400" />
                  <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200">Reconciliation Pipeline</h2>
                </div>
                <div className="flex space-x-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs">
                  <button
                    onClick={() => setActiveTab("all")}
                    className={`px-2.5 py-1 rounded-md transition font-medium ${
                      activeTab === "all" ? "bg-indigo-600 text-white shadow-sm" : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    All ({reports.length})
                  </button>
                  <button
                    onClick={() => setActiveTab("flagged")}
                    className={`px-2.5 py-1 rounded-md transition font-medium ${
                      activeTab === "flagged" ? "bg-indigo-600 text-white shadow-sm" : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    Flagged ({reports.filter((r) => r.match_status === "FLAGGED_FOR_REVIEW").length})
                  </button>
                  <button
                    onClick={() => setActiveTab("approved")}
                    className={`px-2.5 py-1 rounded-md transition font-medium ${
                      activeTab === "approved" ? "bg-indigo-600 text-white shadow-sm" : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    Approved
                  </button>
                </div>
              </div>

              <div className="space-y-3 max-h-[640px] overflow-y-auto pr-1">
                {filteredReports.map((report) => {
                  const isSelected = selectedReport?.match_id === report.match_id;
                  const isCritical = report.risk_level === "CRITICAL";
                  const isHigh = report.risk_level === "HIGH";
                  const isApproved = report.match_status === "APPROVED";

                  return (
                    <div
                      key={report.match_id}
                      onClick={() => setSelectedReport(report)}
                      className={`p-4 rounded-xl border transition cursor-pointer text-left ${
                        isSelected
                          ? "bg-slate-800/90 border-indigo-500/80 shadow-md ring-1 ring-indigo-500/30"
                          : "bg-slate-950/40 border-slate-800 hover:bg-slate-800/40 hover:border-slate-700"
                      }`}
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="flex items-center space-x-2">
                            <span className="font-bold text-slate-100 text-sm">{report.invoice_number}</span>
                            <span className="text-xs px-2 py-0.5 rounded-full font-mono bg-slate-800 text-slate-300 border border-slate-700">
                              {report.po_number}
                            </span>
                          </div>
                          <p className="text-xs text-slate-400 font-medium mt-1">{report.vendor_name}</p>
                        </div>

                        <div className="text-right">
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold ${
                              isApproved
                                ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                                : isCritical
                                ? "bg-rose-500/10 text-rose-400 border border-rose-500/20 animate-pulse"
                                : isHigh
                                ? "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                                : "bg-slate-800 text-slate-300"
                            }`}
                          >
                            {report.match_status}
                          </span>
                          <div className="text-xs text-slate-500 mt-1">Risk Score: {report.risk_score}/100</div>
                        </div>
                      </div>

                      {/* Anomaly Preview Tags */}
                      {report.risk_reasons.length > 0 && (
                        <div className="mt-3 pt-2.5 border-t border-slate-800/60 flex items-start space-x-2">
                          <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0 mt-0.5" />
                          <p className="text-xs text-slate-300 line-clamp-1">
                            {report.risk_reasons[0]}
                          </p>
                        </div>
                      )}

                      {report.human_decision && (
                        <div className="mt-2 text-xs flex items-center space-x-1.5 text-indigo-300 font-medium">
                          <UserCheck className="w-3.5 h-3.5" />
                          <span>Resolved by CFO: {report.human_decision}</span>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Audit Log Stream */}
            <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-4 shadow-xl">
              <div className="flex items-center space-x-2 mb-3">
                <FileSpreadsheet className="w-4 h-4 text-violet-400" />
                <h2 className="text-sm font-bold uppercase tracking-wider text-slate-200">Immutable Audit Trail</h2>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto pr-1 text-xs">
                {auditLog.slice(0, 8).map((log, idx) => (
                  <div key={idx} className="p-2 rounded bg-slate-950/60 border border-slate-800/80 flex justify-between items-center">
                    <div>
                      <span className="font-semibold text-slate-300">{log.event}</span>
                      <span className="text-slate-500 ml-1.5">({log.invoice_number})</span>
                      <div className="text-[10px] text-slate-500">{log.actor}</div>
                    </div>
                    <span className="text-[10px] text-slate-400 font-mono">
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Deep Inspection, 3-Way Match Diff & HITL Actions (7 cols) */}
          <div className="lg:col-span-7">
            {selectedReport ? (
              <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 shadow-2xl space-y-6">
                {/* Top Banner with Invoice & Risk status */}
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center pb-5 border-b border-slate-800 gap-4">
                  <div>
                    <div className="flex items-center space-x-3">
                      <h2 className="text-xl font-bold text-white tracking-tight">{selectedReport.invoice_number}</h2>
                      <span
                        className={`text-xs px-2.5 py-1 rounded-md font-bold tracking-wide ${
                          selectedReport.match_status === "APPROVED"
                            ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                            : selectedReport.risk_level === "CRITICAL"
                            ? "bg-rose-500/15 text-rose-400 border border-rose-500/30"
                            : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
                        }`}
                      >
                        {selectedReport.match_status}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-1 flex items-center space-x-1.5">
                      <Building2 className="w-3.5 h-3.5" />
                      <span>{selectedReport.vendor_name}</span>
                      <span>•</span>
                      <span>Ref PO: {selectedReport.po_number}</span>
                    </p>
                  </div>

                  {/* HITL Action Controls */}
                  <div className="flex items-center space-x-2 w-full md:w-auto">
                    {selectedReport.match_status === "FLAGGED_FOR_REVIEW" && (
                      <>
                        <button
                          onClick={() => handleOpenReview("APPROVE")}
                          className="flex-1 md:flex-initial px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white text-xs font-semibold rounded-xl shadow-lg shadow-emerald-600/20 transition flex items-center justify-center space-x-1.5"
                        >
                          <CheckCircle2 className="w-4 h-4" />
                          <span>Approve & Post</span>
                        </button>
                        <button
                          onClick={() => handleOpenReview("DISPUTE")}
                          className="flex-1 md:flex-initial px-3.5 py-2 bg-amber-600 hover:bg-amber-500 active:scale-95 text-white text-xs font-semibold rounded-xl shadow-lg shadow-amber-600/20 transition flex items-center justify-center space-x-1.5"
                        >
                          <AlertTriangle className="w-4 h-4" />
                          <span>Dispute Supplier</span>
                        </button>
                        <button
                          onClick={() => handleOpenReview("REJECT")}
                          className="flex-1 md:flex-initial px-3.5 py-2 bg-rose-600 hover:bg-rose-500 active:scale-95 text-white text-xs font-semibold rounded-xl shadow-lg shadow-rose-600/20 transition flex items-center justify-center space-x-1.5"
                        >
                          <XCircle className="w-4 h-4" />
                          <span>Reject</span>
                        </button>
                      </>
                    )}
                  </div>
                </div>

                {/* Autonomous Multi-Agent Reasoning Panel */}
                <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-500/20 space-y-2">
                  <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider">
                    <ShieldAlert className="w-4 h-4" />
                    <span>Agent Audit Summary & Reasoning</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">{selectedReport.ai_analysis_summary}</p>
                  <p className="text-xs font-medium text-indigo-300">
                    <strong className="text-slate-200">Recommendation:</strong> {selectedReport.recommended_action}
                  </p>
                </div>

                {/* Risk Reasons Callout */}
                {selectedReport.risk_reasons.length > 0 && (
                  <div className="space-y-2">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">Flagged Exceptions</h3>
                    <div className="space-y-1.5">
                      {selectedReport.risk_reasons.map((reason, i) => (
                        <div
                          key={i}
                          className="p-2.5 rounded-lg bg-rose-950/20 border border-rose-500/30 text-rose-300 text-xs flex items-start space-x-2"
                        >
                          <AlertTriangle className="w-4 h-4 shrink-0 text-rose-400 mt-0.5" />
                          <span className="leading-snug">{reason}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 3-Way Line Item Variance Reconciliation Table */}
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      3-Way Line Item Verification (PO vs Invoiced vs Warehouse GRN)
                    </h3>
                  </div>

                  <div className="overflow-x-auto rounded-xl border border-slate-800">
                    <table className="w-full text-left text-xs border-collapse">
                      <thead>
                        <tr className="bg-slate-950 text-slate-400 border-b border-slate-800">
                          <th className="p-3 font-semibold">SKU / Item</th>
                          <th className="p-3 font-semibold text-center">PO Qty</th>
                          <th className="p-3 font-semibold text-center">GRN Rcvd</th>
                          <th className="p-3 font-semibold text-center">Inv Qty</th>
                          <th className="p-3 font-semibold text-right">PO Price</th>
                          <th className="p-3 font-semibold text-right">Inv Price</th>
                          <th className="p-3 font-semibold text-center">Status</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-800/60 bg-slate-900/40">
                        {selectedReport.variances.map((v) => (
                          <tr key={v.item_id} className="hover:bg-slate-800/30 transition">
                            <td className="p-3">
                              <div className="font-semibold text-slate-200">{v.item_id}</div>
                              <div className="text-[11px] text-slate-400">{v.description}</div>
                            </td>
                            <td className="p-3 text-center text-slate-300">{v.po_qty}</td>
                            <td className="p-3 text-center font-semibold text-slate-200">
                              <span className={v.invoice_qty > v.grn_qty ? "text-rose-400 font-bold" : "text-emerald-400"}>
                                {v.grn_qty}
                              </span>
                            </td>
                            <td className="p-3 text-center font-semibold text-slate-200">{v.invoice_qty}</td>
                            <td className="p-3 text-right text-slate-300">${v.po_price.toFixed(2)}</td>
                            <td className="p-3 text-right">
                              <span className={v.price_variance_pct > 0 ? "text-rose-400 font-bold" : "text-slate-200"}>
                                ${v.invoice_price.toFixed(2)}
                              </span>
                              {v.price_variance_pct > 0 && (
                                <div className="text-[10px] text-rose-400">+{v.price_variance_pct}%</div>
                              )}
                            </td>
                            <td className="p-3 text-center">
                              <span
                                className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                                  v.status === "MATCH"
                                    ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                                    : "bg-rose-500/10 text-rose-400 border border-rose-500/20"
                                }`}
                              >
                                {v.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Dispute Email Draft (Generated by Agent) */}
                {selectedReport.dispute_email_draft && (
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                      <Send className="w-3.5 h-3.5" />
                      <span>Autonomous Supplier Dispute Notice Draft</span>
                    </div>
                    <pre className="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 whitespace-pre-wrap leading-relaxed">
                      {selectedReport.dispute_email_draft}
                    </pre>
                  </div>
                )}

                {/* ERP Journal Entry Preview */}
                {selectedReport.erp_journal_entry && (
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2 text-violet-400 text-xs font-bold uppercase tracking-wider">
                      <FileText className="w-3.5 h-3.5" />
                      <span>ERP Journal Posting (SAP / NetSuite / Workday Ready)</span>
                    </div>
                    <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 text-xs space-y-1.5 font-mono">
                      <div className="flex justify-between text-slate-400">
                        <span>Journal ID: {selectedReport.erp_journal_entry.journal_id}</span>
                        <span className="font-bold text-indigo-400">{selectedReport.erp_journal_entry.status}</span>
                      </div>
                      <div className="flex justify-between text-slate-300">
                        <span>DR: {selectedReport.erp_journal_entry.debit_account}</span>
                        <span>${selectedReport.erp_journal_entry.debit_amount.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between text-slate-300">
                        <span>DR: {selectedReport.erp_journal_entry.tax_account}</span>
                        <span>${selectedReport.erp_journal_entry.tax_amount.toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between text-slate-200 font-semibold pt-1 border-t border-slate-800">
                        <span>CR: {selectedReport.erp_journal_entry.credit_account}</span>
                        <span>${selectedReport.erp_journal_entry.credit_amount.toFixed(2)}</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-12 text-center text-slate-500">
                Select an invoice from the pipeline to inspect 3-way matching and risk Sentinel details.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Human-in-the-Loop Review Confirmation Modal */}
      {reviewModal && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center space-x-3 pb-3 border-b border-slate-800">
              <UserCheck className="w-5 h-5 text-indigo-400" />
              <h3 className="text-base font-bold text-white">
                CFO / Controller Review Decision: {reviewAction}
              </h3>
            </div>

            <p className="text-xs text-slate-400">
              You are resolving exception for <strong>{selectedReport?.invoice_number}</strong> ({selectedReport?.vendor_name}). Provide rationale for audit compliance:
            </p>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1.5 uppercase tracking-wider">
                Auditor Notes & Justification
              </label>
              <textarea
                rows={3}
                value={reviewNotes}
                onChange={(e) => setReviewNotes(e.target.value)}
                className="w-full p-3 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div className="flex justify-end space-x-3 pt-2">
              <button
                onClick={() => setReviewModal(false)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded-xl text-slate-300 transition"
              >
                Cancel
              </button>
              <button
                onClick={submitReview}
                disabled={submittingReview}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 active:scale-95 text-xs font-semibold rounded-xl text-white shadow-lg shadow-indigo-600/20 transition"
              >
                {submittingReview ? "Submitting..." : "Confirm & Sign Off"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
