import os
import json
from typing import Optional, Dict, Any
import httpx

TENSORMUX_BASE_URL = os.getenv("TENSORMUX_BASE_URL", "https://api.tensormux.com/v1")
TENSORMUX_API_KEY = os.getenv("TENSORMUX_API_KEY", "")
TENSORMUX_MODEL = os.getenv("TENSORMUX_MODEL", "glm-4-7-flash")

class TensorMuxClient:
    """
    Client for TensorMux OpenAI-compatible endpoint hosting GLM-4.7-Flash.
    Provides intelligent CFO reasoning, fraud threat profiling, and natural language dispute generation.
    Falls back gracefully to high-precision rule engine if API key is not yet supplied.
    """
    def __init__(self, base_url: str = TENSORMUX_BASE_URL, api_key: str = TENSORMUX_API_KEY, model: str = TENSORMUX_MODEL):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model

    def generate_cfo_assessment(self, invoice_data: Dict[str, Any], variances: list, risk_findings: list) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            return None

        prompt = f"""
You are an autonomous Senior Forensic Accountant and AP Controller in the Autonomous Office of the CFO.
Analyze this invoice reconciliation event:

Vendor: {invoice_data.get('vendor_name')} (ID: {invoice_data.get('vendor_id')})
Invoice #{invoice_data.get('invoice_number')} | PO #{invoice_data.get('po_number')}
Total Amount: ${invoice_data.get('total_amount')}
Line-Item Variances: {json.dumps(variances, default=str)}
Risk Findings / Flags: {json.dumps(risk_findings)}

Respond strictly in valid JSON with these keys:
- "executive_summary": (string, concise forensic synthesis of the situation)
- "cfo_recommendation": (string, specific tactical next step: HOLD, OVERRIDE, DEMAND_CREDIT_MEMO, etc.)
- "dispute_letter": (string, formal correspondence to supplier accounts receivable detailing line discrepancies or bank validation issues)
"""
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "You are LedgerGuard AI, an autonomous financial controller for the Office of the CFO. Return only valid JSON."},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.1,
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.endswith("```"):
                        content = content[:-3]
                    return json.loads(content.strip())
        except Exception as e:
            print(f"[TensorMux Warning] Could not reach GLM-4.7-Flash: {e}")
        return None
