from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os

from app.models import (
    Invoice, PurchaseOrder, MatchReport, HumanReviewAction, MatchStatus
)
from app.seed_data import (
    VENDOR_MASTER, PURCHASE_ORDERS, GOODS_RECEIVED, INITIAL_INVOICES
)
from app.engine import MultiAgentReconciliationEngine

app = FastAPI(
    title="LedgerGuard AI — Autonomous Office of the CFO",
    description="End-to-End Autonomous Accounts Payable & Fraud Anomaly Detection Multi-Agent System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = MultiAgentReconciliationEngine()

REPORTS_DB: Dict[str, MatchReport] = {}
INVOICES_DB: Dict[str, Dict[str, Any]] = {}
AUDIT_LOG: List[Dict[str, Any]] = []

def init_system_data():
    for inv_data in INITIAL_INVOICES:
        INVOICES_DB[inv_data["invoice_number"]] = inv_data
        report = engine.process_invoice(inv_data)
        REPORTS_DB[report.match_id] = report
        AUDIT_LOG.append({
            "timestamp": datetime.now().isoformat(),
            "event": "INVOICE_PROCESSED_BY_AGENT",
            "invoice_number": report.invoice_number,
            "status": report.match_status,
            "risk_score": report.risk_score,
            "actor": "Autonomous Agents (Matching + Fraud Sentinel + GLM-4.7-Flash)"
        })

init_system_data()

@app.get("/api/dashboard-metrics")
def get_dashboard_metrics():
    reports = list(REPORTS_DB.values())
    total_invoices = len(reports)
    auto_approved = sum(1 for r in reports if r.match_status == MatchStatus.APPROVED and not r.human_decision)
    flagged = sum(1 for r in reports if r.match_status == MatchStatus.FLAGGED_FOR_REVIEW)
    disputed_or_rejected = sum(1 for r in reports if r.match_status in [MatchStatus.REJECTED, MatchStatus.DISPUTED] or r.human_decision in ["REJECT", "DISPUTE"])
    human_resolved = sum(1 for r in reports if r.human_decision is not None)

    total_spend_evaluated = sum(INVOICES_DB[r.invoice_number]["total_amount"] for r in reports if r.invoice_number in INVOICES_DB)
    discrepancy_amount_saved = 0.0
    for r in reports:
        for v in r.variances:
            if v.status in ["PRICE_DISCREPANCY", "QTY_DISCREPANCY"]:
                expected = v.grn_qty * v.po_price
                invoiced = v.invoice_qty * v.invoice_price
                discrepancy_amount_saved += max(0.0, invoiced - expected)

    for r in reports:
        if r.risk_score >= 80 and r.invoice_number in INVOICES_DB:
            discrepancy_amount_saved += INVOICES_DB[r.invoice_number]["total_amount"]

    auto_approval_rate = round((auto_approved / max(1, total_invoices)) * 100, 1)

    return {
        "total_invoices": total_invoices,
        "auto_approved_count": auto_approved,
        "flagged_for_review_count": flagged,
        "disputed_or_rejected_count": disputed_or_rejected,
        "human_resolved_count": human_resolved,
        "auto_approval_rate_pct": auto_approval_rate,
        "total_spend_evaluated": round(total_spend_evaluated, 2),
        "discrepancy_and_fraud_savings": round(discrepancy_amount_saved, 2)
    }

@app.get("/api/reports", response_model=List[MatchReport])
def list_reports():
    return list(REPORTS_DB.values())

@app.get("/api/reports/{match_id}", response_model=MatchReport)
def get_report(match_id: str):
    if match_id not in REPORTS_DB:
        raise HTTPException(status_code=404, detail="Report not found")
    return REPORTS_DB[match_id]

@app.post("/api/reports/{match_id}/review")
def review_report(match_id: str, payload: HumanReviewAction):
    if match_id not in REPORTS_DB:
        raise HTTPException(status_code=404, detail="Report not found")

    report = REPORTS_DB[match_id]
    report.human_decision = payload.action
    report.human_notes = payload.notes
    report.resolved_at = datetime.now().isoformat()

    if payload.action in ["APPROVE", "OVERRIDE"]:
        report.match_status = MatchStatus.APPROVED
        if report.erp_journal_entry:
            report.erp_journal_entry["status"] = "POSTED_TO_ERP"
    elif payload.action == "REJECT":
        report.match_status = MatchStatus.REJECTED
        if report.erp_journal_entry:
            report.erp_journal_entry["status"] = "VOIDED"
    elif payload.action == "DISPUTE":
        report.match_status = MatchStatus.DISPUTED
        if report.erp_journal_entry:
            report.erp_journal_entry["status"] = "HELD_FOR_SUPPLIER_CREDIT"

    AUDIT_LOG.append({
        "timestamp": datetime.now().isoformat(),
        "event": f"HUMAN_RESOLUTION_{payload.action}",
        "invoice_number": report.invoice_number,
        "match_id": match_id,
        "status": report.match_status,
        "actor": "CFO / AP Finance Lead",
        "notes": payload.notes
    })

    return {"message": f"Successfully processed review action: {payload.action}", "report": report}

@app.get("/api/audit-log")
def get_audit_log():
    return list(reversed(AUDIT_LOG))

@app.post("/api/reset-demo")
def reset_demo():
    REPORTS_DB.clear()
    INVOICES_DB.clear()
    AUDIT_LOG.clear()
    init_system_data()
    return {"message": "Demo state successfully reset to initial scenarios"}

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return f.read()
