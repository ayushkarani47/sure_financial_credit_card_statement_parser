"""
American Express Credit Card Statement Parser
Extracts key information from American Express credit card statements
"""

import re
from typing import Dict, Optional


def parse_amex_statement(text: str) -> Dict[str, Optional[str]]:
    """Parse American Express credit card statement"""
    data = {
        "issuer": "American Express",
        "card_holder": None,
        "last_4_digits": None,
        "billing_cycle": None,
        "payment_due_date": None,
        "total_amount_due": None
    }
    
    # Extract Card Holder Name
    name_patterns = [
        r"Card\s+(?:Member|Holder)[:\s]+([A-Z\s]+?)(?:\n|Card)",
        r"Dear\s+([A-Z\s]+?)(?:,|\n)",
        r"Account\s+Holder[:\s]+([A-Z\s]+?)(?:\n)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["card_holder"] = match.group(1).strip()
            break
    
    # Extract Last 4 Digits
    card_patterns = [
        r"Card\s+(?:Number|No\.?)[:\s]+(?:X+\s*)*(\d{4})",
        r"[X\*]{11}(\d{4})",
        r"Account\s+ending[:\s]+(\d{4})"
    ]
    
    for pattern in card_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["last_4_digits"] = match.group(1)
            break
    
    # Extract Billing Cycle
    cycle_patterns = [
        r"Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–to]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})"
    ]
    
    for pattern in cycle_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["billing_cycle"] = match.group(1).strip()
            break
    
    # Extract Payment Due Date
    due_date_patterns = [
        r"Payment\s+Due[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})"
    ]
    
    for pattern in due_date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["payment_due_date"] = match.group(1).strip()
            break
    
    # Extract Total Amount Due
    amount_patterns = [
        r"Total\s+(?:Amount\s+)?Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
        r"Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)"
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["total_amount_due"] = f"₹{match.group(1).strip()}"
            break
    
    return data


def validate_amex_statement(text: str) -> bool:
    """Validate if the PDF is an American Express statement"""
    amex_keywords = ["American Express", "AMERICAN EXPRESS", "amex", "AMEX", "www.americanexpress.com"]
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in amex_keywords)
