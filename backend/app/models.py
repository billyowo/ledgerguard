from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class MatchStatus(str, Enum):
    APPROVED = "APPROVED"
    FLAGGED_FOR_REVIEW = "FLAGGED_FOR_REVIEW"
    REJECTED = "REJECTED"
    DISPUTED = "DISPUTED"
    PENDING_MATCH = "PENDING_MATCH"

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class LineItem(BaseModel):
    item_id: str
    description: str
    quantity: float
    unit_price: float
    total_price: float

class PurchaseOrder(BaseModel):
    po_number: str
    vendor_id: str
    vendor_name: str
    date: str
    currency: str = "USD"
    items: List[LineItem]
    subtotal: float
    tax: float
    total_amount: float
    status: str = "OPEN"
    delivery_status: str = "DELIVERED"

class GoodsReceivedNote(BaseModel):
    grn_number: str
    po_number: str
    vendor_name: str
    received_date: str
    items: List[Dict[str, Any]]

class Invoice(BaseModel):
    invoice_number: str
    po_number: str
    vendor_id: str
    vendor_name: str
    invoice_date: str
    due_date: str
    remit_to_bank_account: str
    remit_to_routing: str
    items: List[LineItem]
    subtotal: float
    tax: float
    total_amount: float
    currency: str = "USD"

class LineItemVariance(BaseModel):
    item_id: str
    description: str
    po_qty: float
    invoice_qty: float
    grn_qty: float
    po_price: float
    invoice_price: float
    price_variance_pct: float
    qty_variance_pct: float
    status: str

class MatchReport(BaseModel):
    match_id: str
    invoice_number: str
    po_number: str
    vendor_name: str
    timestamp: str
    match_status: MatchStatus
    risk_level: RiskLevel
    risk_score: int
    risk_reasons: List[str]
    variances: List[LineItemVariance]
    ai_analysis_summary: str
    recommended_action: str
    dispute_email_draft: Optional[str] = None
    erp_journal_entry: Optional[Dict[str, Any]] = None
    human_decision: Optional[str] = None
    human_notes: Optional[str] = None
    resolved_at: Optional[str] = None

class HumanReviewAction(BaseModel):
    action: str
    notes: Optional[str] = ""
