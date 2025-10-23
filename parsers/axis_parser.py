"""
Axis Bank Credit Card Statement Parser
Extracts key information from Axis Bank credit card statements
"""

import re
from typing import Dict, Optional


def parse_axis_statement(text: str) -> Dict[str, Optional[str]]:
    """
    Parse Axis Bank credit card statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Dictionary containing parsed data
    """
    data = {
        "issuer": "Axis Bank",
        "card_holder": None,
        "last_4_digits": None,
        "billing_cycle": None,
        "payment_due_date": None,
        "total_amount_due": None
    }
    
    # Extract Card Holder Name
    name_patterns = [
        r"Card\s+(?:Holder|Member)[:\s]+([A-Z\s]+?)(?:\n|Card)",
        r"Name[:\s]+([A-Z\s]+?)(?:\n|Card)",
        r"Dear\s+([A-Z\s]+?)(?:,|\n)",
        r"Mr\.?\s+([A-Z\s]+?)(?:\n|,)",
        r"Ms\.?\s+([A-Z\s]+?)(?:\n|,)",
        r"Customer\s+Name[:\s]+([A-Z\s]+?)(?:\n)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["card_holder"] = match.group(1).strip()
            break
    
    # Extract Last 4 Digits of Card Number
    card_patterns = [
        r"Card\s+(?:Number|No\.?)[:\s]+(?:X+\s*)*(\d{4})",
        r"(?:X{4}\s+){3}(\d{4})",
        r"ending\s+(?:with\s+)?(\d{4})",
        r"[X\*]{12}(\d{4})",
        r"Card\s+ending[:\s]+(\d{4})"
    ]
    
    for pattern in card_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["last_4_digits"] = match.group(1)
            break
    
    # Extract Billing Cycle / Statement Period
    cycle_patterns = [
        r"Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–to]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Billing\s+(?:Cycle|Period)[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–to]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"From[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})\s+To[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
    ]
    
    for pattern in cycle_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                data["billing_cycle"] = f"{match.group(1)} - {match.group(2)}"
            else:
                data["billing_cycle"] = match.group(1).strip()
            break
    
    # Extract Payment Due Date
    due_date_patterns = [
        r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Pay\s+by[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
        r"Payment\s+Due[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
    ]
    
    for pattern in due_date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["payment_due_date"] = match.group(1).strip()
            break
    
    # Extract Total Amount Due
    amount_patterns = [
        r"Total\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
        r"Total\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
        r"Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
        r"Outstanding\s+Amount[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
        r"(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)\s+Total"
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1).strip()
            data["total_amount_due"] = f"₹{amount}"
            break
    
    return data


def validate_axis_statement(text: str) -> bool:
    """
    Validate if the PDF is an Axis Bank statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        True if Axis statement, False otherwise
    """
    axis_keywords = [
        "Axis Bank",
        "AXIS BANK",
        "axis bank",
        "Axis Credit Card",
        "www.axisbank.com"
    ]
    
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in axis_keywords)
