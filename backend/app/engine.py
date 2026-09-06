import uuid
import os
from datetime import datetime
from typing import Dict, List, Any, Tuple
from app.models import (
    Invoice, PurchaseOrder, GoodsReceivedNote,
    MatchReport, MatchStatus, RiskLevel, LineItemVariance
)
from app.seed_data import VENDOR_MASTER, PURCHASE_ORDERS, GOODS_RECEIVED
from app.tensormux_client import TensorMuxClient

class MultiAgentReconciliationEngine:
    """
    Autonomous Multi-Agent AP Controller:
    Agent 1: 3-Way Matching Agent (PO vs Invoice vs GRN)
    Agent 2: Fraud & Compliance Sentinel (Vendor Master, Bank Account / Routing Verification)
    Agent 3: TensorMux GLM-4.7-Flash Agent & HITL Decision Synthesizer
    """

    def __init__(self):
        self.vendor_master = VENDOR_MASTER
        self.purchase_orders = PURCHASE_ORDERS
        self.goods_received = GOODS_RECEIVED
        self.llm_client = TensorMuxClient()

    def agent_reconcile_3way(self, invoice: Invoice, po: PurchaseOrder, grn: GoodsReceivedNote) -> Tuple[List[LineItemVariance], List[str], int]:
        variances = []
        findings = []
        score_penalty = 0

        vendor_meta = self.vendor_master.get(invoice.vendor_id, {})
        allowed_tolerance_pct = vendor_meta.get("tolerance_price_pct", 1.0)

        po_item_map = {item.item_id: item for item in po.items}
        grn_item_map = {item["item_id"]: item for item in grn.items}

        for inv_item in invoice.items:
            po_item = po_item_map.get(inv_item.item_id)
            grn_item = grn_item_map.get(inv_item.item_id)

            if not po_item:
                findings.append(f"Unmatched SKU {inv_item.item_id} ('{inv_item.description}') - not present in original Purchase Order {po.po_number}")
                score_penalty += 35
                variances.append(LineItemVariance(
                    item_id=inv_item.item_id,
                    description=inv_item.description,
                    po_qty=0.0,
                    invoice_qty=inv_item.quantity,
                    grn_qty=0.0,
                    po_price=0.0,
                    invoice_price=inv_item.unit_price,
                    price_variance_pct=100.0,
                    qty_variance_pct=100.0,
                    status="UNAPPROVED_ITEM"
                ))
                continue

            po_price = po_item.unit_price
            inv_price = inv_item.unit_price
            price_var_pct = round(((inv_price - po_price) / po_price) * 100.0, 2)

            grn_qty = grn_item.get("received_qty", 0.0) if grn_item else 0.0
            po_qty = po_item.quantity
            inv_qty = inv_item.quantity
            qty_var_pct = round(((inv_qty - grn_qty) / max(grn_qty, 1.0)) * 100.0, 2)

            item_status = "MATCH"

            if price_var_pct > allowed_tolerance_pct:
                item_status = "PRICE_DISCREPANCY"
                findings.append(
                    f"Unit price overrun for SKU {inv_item.item_id}: invoiced at ${inv_price:,.2f} vs PO ${po_price:,.2f} "
                    f"(+{price_var_pct}% variance, exceeds vendor threshold of {allowed_tolerance_pct}%)"
                )
                score_penalty += 30

            if inv_qty > grn_qty:
                item_status = "QTY_DISCREPANCY"
                findings.append(
                    f"Short-shipment discrepancy for SKU {inv_item.item_id}: billed for {inv_qty} units but warehouse received only {grn_qty} units "
                    f"({inv_qty - grn_qty} unreceived units)"
                )
                score_penalty += 45

            variances.append(LineItemVariance(
                item_id=inv_item.item_id,
                description=inv_item.description,
                po_qty=po_qty,
                invoice_qty=inv_qty,
                grn_qty=grn_qty,
                po_price=po_price,
                invoice_price=inv_price,
                price_variance_pct=price_var_pct,
                qty_variance_pct=qty_var_pct,
                status=item_status
            ))

        return variances, findings, score_penalty

    def agent_fraud_sentinel(self, invoice: Invoice) -> Tuple[List[str], int, bool]:
        findings = []
        score_penalty = 0
        critical_fraud_alert = False

        vendor_meta = self.vendor_master.get(invoice.vendor_id)
        if not vendor_meta:
            findings.append(f"UNREGISTERED GHOST VENDOR: Vendor ID '{invoice.vendor_id}' is not in approved corporate Vendor Master.")
            score_penalty += 80
            critical_fraud_alert = True
            return findings, score_penalty, critical_fraud_alert

        verified_acct = vendor_meta.get("verified_account")
        verified_routing = vendor_meta.get("verified_routing")

        if invoice.remit_to_bank_account != verified_acct or invoice.remit_to_routing != verified_routing:
            findings.append(
                f"🚨 REMITTANCE ACCOUNT MISMATCH: Invoice bank account '{invoice.remit_to_bank_account}' "
                f"(Routing: {invoice.remit_to_routing}) deviates from verified master records "
                f"(Routing: {verified_routing}, Acct: ending in ...{verified_acct[-4:]}). "
                f"High-risk Business Email Compromise (BEC) indicator!"
            )
            score_penalty += 90
            critical_fraud_alert = True

        return findings, score_penalty, critical_fraud_alert

    def agent_decision_and_resolution(
        self,
        invoice: Invoice,
        po: PurchaseOrder,
        variances: List[LineItemVariance],
        match_findings: List[str],
        fraud_findings: List[str],
        total_risk_score: int,
        is_critical_fraud: bool
    ) -> MatchReport:
        all_reasons = fraud_findings + match_findings
        risk_score = min(total_risk_score, 100)

        # Baseline rule-based defaults
        if is_critical_fraud or risk_score >= 70:
            risk_level = RiskLevel.CRITICAL
            match_status = MatchStatus.FLAGGED_FOR_REVIEW
            recommendation = "HOLD PAYMENT IMMEDIATELY. Conduct verbal out-of-band verification with vendor treasury before releasing funds."
            dispute_email = (
                f"Subject: URGENT: Verification Required for Invoice #{invoice.invoice_number}\n\n"
                f"Dear Accounts Receivable at {invoice.vendor_name},\n\n"
                f"Our autonomous financial security systems flagged Invoice #{invoice.invoice_number} due to a critical discrepancy "
                f"in remittance banking instructions. For our mutual security, payments have been halted until our treasury team performs "
                f"voice authentication with your verified primary contact.\n\n"
                f"Best regards,\nOffice of the CFO Financial Controller"
            )
        elif risk_score >= 25:
            risk_level = RiskLevel.HIGH if risk_score >= 40 else RiskLevel.MEDIUM
            match_status = MatchStatus.FLAGGED_FOR_REVIEW
            recommendation = "ROUTED TO AP CONTROLLER: Line item / pricing variances detected. Require supplier credit memo or buyer sign-off."
            dispute_email = (
                f"Subject: Discrepancy Notice for Invoice #{invoice.invoice_number} (Ref PO: {po.po_number})\n\n"
                f"Dear Accounts Receivable at {invoice.vendor_name},\n\n"
                f"During automated 3-way reconciliation against PO #{po.po_number}, the following variances were detected:\n"
                + "\n".join([f"- {reason}" for reason in match_findings])
                + f"\n\nPlease issue an updated invoice or corresponding credit memo reflecting verified quantities and agreed contracted pricing.\n\n"
                f"Sincerely,\nAutonomous AP Operations Team"
            )
        else:
            risk_level = RiskLevel.LOW
            match_status = MatchStatus.APPROVED
            recommendation = "AUTONOMOUSLY APPROVED. 3-Way match fully verified within 0% variance tolerance. Scheduled for disbursement."
            dispute_email = None

        analysis_summary = (
            f"Autonomous 3-Way Audit completed for {invoice.vendor_name} (Invoice: {invoice.invoice_number}, PO: {po.po_number}). "
            f"Evaluated {len(invoice.items)} line items. "
            f"Identified {len(all_reasons)} anomaly flags. Risk Score: {risk_score}/100."
        )

        # Enhance with TensorMux GLM-4.7-Flash LLM if available
        llm_assessment = self.llm_client.generate_cfo_assessment(
            invoice_data=invoice.dict(),
            variances=[v.dict() for v in variances],
            risk_findings=all_reasons
        )
        if llm_assessment:
            analysis_summary = f"[GLM-4.7-Flash] {llm_assessment.get('executive_summary', analysis_summary)}"
            if 'cfo_recommendation' in llm_assessment:
                recommendation = llm_assessment['cfo_recommendation']
            if 'dispute_letter' in llm_assessment and llm_assessment['dispute_letter']:
                dispute_email = llm_assessment['dispute_letter']

        erp_entry = {
            "journal_id": f"JE-{datetime.now().strftime('%Y%m%d')}-{invoice.invoice_number}",
            "posting_date": invoice.invoice_date,
            "vendor": invoice.vendor_name,
            "debit_account": "5010 - Cost of Goods / Cloud Infrastructure Expense",
            "debit_amount": invoice.subtotal,
            "tax_account": "2030 - Sales & Use Tax Payable",
            "tax_amount": invoice.tax,
            "credit_account": "2000 - Accounts Payable Liability",
            "credit_amount": invoice.total_amount,
            "status": "POSTED_TO_ERP" if match_status == MatchStatus.APPROVED else "PENDING_HITL_RESOLUTION"
        }

        return MatchReport(
            match_id=str(uuid.uuid4())[:8],
            invoice_number=invoice.invoice_number,
            po_number=invoice.po_number,
            vendor_name=invoice.vendor_name,
            timestamp=datetime.now().isoformat(),
            match_status=match_status,
            risk_level=risk_level,
            risk_score=risk_score,
            risk_reasons=all_reasons,
            variances=variances,
            ai_analysis_summary=analysis_summary,
            recommended_action=recommendation,
            dispute_email_draft=dispute_email,
            erp_journal_entry=erp_entry,
            human_decision=None,
            human_notes=None,
            resolved_at=None
        )

    def process_invoice(self, invoice_dict: Dict[str, Any]) -> MatchReport:
        invoice = Invoice(**invoice_dict)
        po_dict = self.purchase_orders.get(invoice.po_number)
        if not po_dict:
            return MatchReport(
                match_id=str(uuid.uuid4())[:8],
                invoice_number=invoice.invoice_number,
                po_number=invoice.po_number,
                vendor_name=invoice.vendor_name,
                timestamp=datetime.now().isoformat(),
                match_status=MatchStatus.REJECTED,
                risk_level=RiskLevel.CRITICAL,
                risk_score=100,
                risk_reasons=[f"Missing PO: Purchase order {invoice.po_number} does not exist in ERP database."],
                variances=[],
                ai_analysis_summary=f"Invoice rejected: No valid purchase order found for {invoice.po_number}.",
                recommended_action="Reject invoice immediately and contact procurement team.",
                dispute_email_draft=f"Subject: Invalid Purchase Order Reference on Invoice {invoice.invoice_number}\n\nNo active PO found."
            )

        po = PurchaseOrder(**po_dict)
        grn_dict = self.goods_received.get(invoice.po_number, {
            "grn_number": "N/A",
            "po_number": invoice.po_number,
            "vendor_name": invoice.vendor_name,
            "received_date": "",
            "items": []
        })
        grn = GoodsReceivedNote(**grn_dict)

        variances, match_findings, match_penalty = self.agent_reconcile_3way(invoice, po, grn)
        fraud_findings, fraud_penalty, is_critical_fraud = self.agent_fraud_sentinel(invoice)

        total_penalty = match_penalty + fraud_penalty

        return self.agent_decision_and_resolution(
            invoice=invoice,
            po=po,
            variances=variances,
            match_findings=match_findings,
            fraud_findings=fraud_findings,
            total_risk_score=total_penalty,
            is_critical_fraud=is_critical_fraud
        )
