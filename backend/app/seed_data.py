# Vendor Master Database (Verified corporate banking details and terms)
VENDOR_MASTER = {
    "VEND-001": {
        "vendor_id": "VEND-001",
        "vendor_name": "Apex Cloud Systems Inc.",
        "category": "Cloud Infrastructure & SaaS",
        "verified_routing": "121000358",
        "verified_account": "9876543210",
        "tolerance_price_pct": 2.0,
        "payment_terms": "Net 30",
        "status": "ACTIVE"
    },
    "VEND-002": {
        "vendor_id": "VEND-002",
        "vendor_name": "Quantum Hardware Solutions",
        "category": "Data Center & Servers",
        "verified_routing": "021000021",
        "verified_account": "1122334455",
        "tolerance_price_pct": 1.5,
        "payment_terms": "Net 45",
        "status": "ACTIVE"
    },
    "VEND-003": {
        "vendor_id": "VEND-003",
        "vendor_name": "CyberShield Security Ltd.",
        "category": "Cybersecurity & Compliance",
        "verified_routing": "071000013",
        "verified_account": "5566778899",
        "tolerance_price_pct": 0.0,
        "payment_terms": "Net 15",
        "status": "ACTIVE"
    },
    "VEND-004": {
        "vendor_id": "VEND-004",
        "vendor_name": "OfficeTech Direct",
        "category": "Workplace IT & Equipment",
        "verified_routing": "322070381",
        "verified_account": "4433221100",
        "tolerance_price_pct": 3.0,
        "payment_terms": "Net 30",
        "status": "ACTIVE"
    }
}

# Purchase Orders in ERP
PURCHASE_ORDERS = {
    "PO-2026-101": {
        "po_number": "PO-2026-101",
        "vendor_id": "VEND-001",
        "vendor_name": "Apex Cloud Systems Inc.",
        "date": "2026-08-15",
        "currency": "USD",
        "items": [
            {"item_id": "SKU-CLOUD-01", "description": "High-Mem Cloud Compute Cluster (vCPU 128)", "quantity": 10.0, "unit_price": 1200.00, "total_price": 12000.00},
            {"item_id": "SKU-CLOUD-STORAGE", "description": "NVMe Block Storage Allocation (100TB)", "quantity": 5.0, "unit_price": 500.00, "total_price": 2500.00}
        ],
        "subtotal": 14500.00,
        "tax": 1160.00,
        "total_amount": 15660.00,
        "status": "OPEN",
        "delivery_status": "DELIVERED"
    },
    "PO-2026-102": {
        "po_number": "PO-2026-102",
        "vendor_id": "VEND-002",
        "vendor_name": "Quantum Hardware Solutions",
        "date": "2026-08-18",
        "currency": "USD",
        "items": [
            {"item_id": "SKU-SRV-9000", "description": "Rackmount AI Inference Server", "quantity": 4.0, "unit_price": 8500.00, "total_price": 34000.00},
            {"item_id": "SKU-NET-SFP", "description": "100GbE QSFP28 Fiber Transceiver", "quantity": 20.0, "unit_price": 150.00, "total_price": 3000.00}
        ],
        "subtotal": 37000.00,
        "tax": 2960.00,
        "total_amount": 39960.00,
        "status": "OPEN",
        "delivery_status": "PARTIAL"
    },
    "PO-2026-103": {
        "po_number": "PO-2026-103",
        "vendor_id": "VEND-003",
        "vendor_name": "CyberShield Security Ltd.",
        "date": "2026-08-20",
        "currency": "USD",
        "items": [
            {"item_id": "SKU-CYBER-SEIM", "description": "Annual Threat Intelligence Enterprise License", "quantity": 1.0, "unit_price": 45000.00, "total_price": 45000.00}
        ],
        "subtotal": 45000.00,
        "tax": 3600.00,
        "total_amount": 48600.00,
        "status": "OPEN",
        "delivery_status": "DELIVERED"
    },
    "PO-2026-104": {
        "po_number": "PO-2026-104",
        "vendor_id": "VEND-004",
        "vendor_name": "OfficeTech Direct",
        "date": "2026-08-25",
        "currency": "USD",
        "items": [
            {"item_id": "SKU-MON-4K", "description": "32-inch 4K UHD Developer Monitors", "quantity": 15.0, "unit_price": 420.00, "total_price": 6300.00},
            {"item_id": "SKU-CHAIR-ERG", "description": "Ergonomic Task Chairs", "quantity": 15.0, "unit_price": 380.00, "total_price": 5700.00}
        ],
        "subtotal": 12000.00,
        "tax": 960.00,
        "total_amount": 12960.00,
        "status": "OPEN",
        "delivery_status": "DELIVERED"
    }
}

# Goods Received Notes (Warehouse / Logistics confirmation)
GOODS_RECEIVED = {
    "PO-2026-101": {
        "grn_number": "GRN-9901",
        "po_number": "PO-2026-101",
        "vendor_name": "Apex Cloud Systems Inc.",
        "received_date": "2026-08-20",
        "items": [
            {"item_id": "SKU-CLOUD-01", "received_qty": 10.0, "condition": "VERIFIED_OPERATIONAL"},
            {"item_id": "SKU-CLOUD-STORAGE", "received_qty": 5.0, "condition": "VERIFIED_OPERATIONAL"}
        ]
    },
    "PO-2026-102": {
        "grn_number": "GRN-9902",
        "po_number": "PO-2026-102",
        "vendor_name": "Quantum Hardware Solutions",
        "received_date": "2026-08-28",
        "items": [
            {"item_id": "SKU-SRV-9000", "received_qty": 3.0, "condition": "VERIFIED_OPERATIONAL"}, # Only 3 received out of 4! Short shipment
            {"item_id": "SKU-NET-SFP", "received_qty": 20.0, "condition": "VERIFIED_OPERATIONAL"}
        ]
    },
    "PO-2026-103": {
        "grn_number": "GRN-9903",
        "po_number": "PO-2026-103",
        "vendor_name": "CyberShield Security Ltd.",
        "received_date": "2026-08-22",
        "items": [
            {"item_id": "SKU-CYBER-SEIM", "received_qty": 1.0, "condition": "LICENSE_KEY_ACTIVATED"}
        ]
    },
    "PO-2026-104": {
        "grn_number": "GRN-9904",
        "po_number": "PO-2026-104",
        "vendor_name": "OfficeTech Direct",
        "received_date": "2026-08-29",
        "items": [
            {"item_id": "SKU-MON-4K", "received_qty": 15.0, "condition": "VERIFIED_OPERATIONAL"},
            {"item_id": "SKU-CHAIR-ERG", "received_qty": 15.0, "condition": "VERIFIED_OPERATIONAL"}
        ]
    }
}

# Test incoming Invoices representing real-world CFO challenge scenarios
INITIAL_INVOICES = [
    {
        "invoice_number": "INV-APEX-8841",
        "po_number": "PO-2026-101",
        "vendor_id": "VEND-001",
        "vendor_name": "Apex Cloud Systems Inc.",
        "invoice_date": "2026-08-22",
        "due_date": "2026-09-21",
        "remit_to_bank_account": "9876543210", # Valid
        "remit_to_routing": "121000358",       # Valid
        "items": [
            {"item_id": "SKU-CLOUD-01", "description": "High-Mem Cloud Compute Cluster (vCPU 128)", "quantity": 10.0, "unit_price": 1200.00, "total_price": 12000.00},
            {"item_id": "SKU-CLOUD-STORAGE", "description": "NVMe Block Storage Allocation (100TB)", "quantity": 5.0, "unit_price": 500.00, "total_price": 2500.00}
        ],
        "subtotal": 14500.00,
        "tax": 1160.00,
        "total_amount": 15660.00,
        "currency": "USD",
        "scenario_type": "PERFECT_MATCH",
        "description": "Standard flawless 3-way match. Meets all tolerances and passes banking verification. Should auto-approve without manual review."
    },
    {
        "invoice_number": "INV-QUANTUM-5512",
        "po_number": "PO-2026-102",
        "vendor_id": "VEND-002",
        "vendor_name": "Quantum Hardware Solutions",
        "invoice_date": "2026-08-30",
        "due_date": "2026-10-14",
        "remit_to_bank_account": "1122334455", # Valid
        "remit_to_routing": "021000021",       # Valid
        "items": [
            {"item_id": "SKU-SRV-9000", "description": "Rackmount AI Inference Server", "quantity": 4.0, "unit_price": 8500.00, "total_price": 34000.00}, # Invoicing for 4, but GRN only received 3!
            {"item_id": "SKU-NET-SFP", "description": "100GbE QSFP28 Fiber Transceiver", "quantity": 20.0, "unit_price": 150.00, "total_price": 3000.00}
        ],
        "subtotal": 37000.00,
        "tax": 2960.00,
        "total_amount": 39960.00,
        "currency": "USD",
        "scenario_type": "QUANTITY_SHORTFALL",
        "description": "Quantity variance: Vendor billed for 4 AI servers ($34,000) but warehouse GRN only received 3 ($25,500). Potential overpayment risk of $9,180 (incl tax)."
    },
    {
        "invoice_number": "INV-CYBER-9921",
        "po_number": "PO-2026-103",
        "vendor_id": "VEND-003",
        "vendor_name": "CyberShield Security Ltd.",
        "invoice_date": "2026-08-25",
        "due_date": "2026-09-09",
        "remit_to_bank_account": "9998887771", # SUSPICIOUS! Unregistered offshore account!
        "remit_to_routing": "026009593",       # Mismatched routing!
        "items": [
            {"item_id": "SKU-CYBER-SEIM", "description": "Annual Threat Intelligence Enterprise License", "quantity": 1.0, "unit_price": 45000.00, "total_price": 45000.00}
        ],
        "subtotal": 45000.00,
        "tax": 3600.00,
        "total_amount": 48600.00,
        "currency": "USD",
        "scenario_type": "SUSPICIOUS_BANK_CHANGE",
        "description": "Critical Fraud Risk: Invoiced line items match PO, but remittance routing & bank account do NOT match verified Vendor Master. Potential Business Email Compromise (BEC) fraud ($48,600)."
    },
    {
        "invoice_number": "INV-OFFICE-3309",
        "po_number": "PO-2026-104",
        "vendor_id": "VEND-004",
        "vendor_name": "OfficeTech Direct",
        "invoice_date": "2026-08-30",
        "due_date": "2026-09-29",
        "remit_to_bank_account": "4433221100", # Valid
        "remit_to_routing": "322070381",       # Valid
        "items": [
            {"item_id": "SKU-MON-4K", "description": "32-inch 4K UHD Developer Monitors", "quantity": 15.0, "unit_price": 490.00, "total_price": 7350.00}, # PO was $420, price hiked +16.7%!
            {"item_id": "SKU-CHAIR-ERG", "description": "Ergonomic Task Chairs", "quantity": 15.0, "unit_price": 380.00, "total_price": 5700.00}
        ],
        "subtotal": 13050.00,
        "tax": 1044.00,
        "total_amount": 14094.00,
        "currency": "USD",
        "scenario_type": "PRICE_CREEP_VARIANCE",
        "description": "Price Variance: Monitor price increased from approved $420.00 to $490.00 (+16.7%), exceeding vendor tolerance limit of 3.0%. Total overrun: $1,134.00."
    }
]
