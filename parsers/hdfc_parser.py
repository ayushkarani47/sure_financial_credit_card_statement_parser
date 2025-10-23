"""
HDFC Bank Credit Card Statement Parser
Extracts key information from HDFC credit card statements
"""

import re
from typing import Dict, Optional


def parse_hdfc_statement(text: str) -> Dict[str, Optional[str]]:
    """
    Parse HDFC Bank credit card statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Dictionary containing parsed data
    """
    data = {
        "issuer": "HDFC Bank",
        "card_holder": None,
        "last_4_digits": None,
        "billing_cycle": None,
        "payment_due_date": None,
        "total_amount_due": None
    }
    
    # Extract Card Holder Name
    # Pattern: Name on Card: AYUSH KARANI or similar variations
    name_patterns = [
        r"Card\s+holder\s+Name\s*:\s*([A-Z][A-Za-z\s]+?)(?:\n|Name:|Address:|For|$)",
        r"Name\s+on\s+Card[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Card\s*Holder[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Cardholder[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Primary\s+Member[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Customer\s+Name[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Account\s+Holder[:\s]+([A-Z][A-Z\s]+?)(?:\n|Card|Number|\d)",
        r"Dear\s+([A-Z][A-Z\s]+?)(?:,|\n)",
        r"Mr\.?\s+([A-Z][A-Z\s]+?)(?:\n|,)",
        r"Ms\.?\s+([A-Z][A-Z\s]+?)(?:\n|,)",
        r"Mrs\.?\s+([A-Z][A-Z\s]+?)(?:\n|,)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["card_holder"] = match.group(1).strip()
            break
    
    # Extract Last 4 Digits of Card Number
    # Pattern: Card ending with 4581 or XXXX XXXX XXXX 4581
    card_patterns = [
        r"(\d{4})\s+(\d{4})\s+(\d{4})\s+(\d{4})",  # Full card number like 1234 5678 9012 3456
        r"Card\s+(?:Number|ending|No\.?|number)[:\s]+(?:X+\s*)*(\d{4})",
        r"Card\s+No\.?\s*[:\s]*[X\*]+(\d{4})",
        r"(?:X{4}\s+){3}(\d{4})",
        r"(?:\*{4}\s+){3}(\d{4})",
        r"ending\s+(?:with\s+)?(\d{4})",
        r"Card\s+ending\s+in\s+(\d{4})",
        r"(?:XXXX|xxxx|\*{4})\s*(?:XXXX|xxxx|\*{4})\s*(?:XXXX|xxxx|\*{4})\s*(\d{4})",
        r"Card:\s*[X\*]+(\d{4})",
        r"(?:Card|CARD)\s+[X\*]{4,}\s*(\d{4})"
    ]
    
    for pattern in card_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # If pattern has 4 groups (full card number), take the last group
            if len(match.groups()) == 4:
                data["last_4_digits"] = match.group(4)
            else:
                data["last_4_digits"] = match.group(1)
            break
    
    # Extract Billing Cycle / Statement Period
    # Pattern: 01 Sep 2025 - 30 Sep 2025 or Statement Period: DD MMM YYYY to DD MMM YYYY
    cycle_patterns = [
        r"Opening/Closing\s+Date\s+(\d{1,2}/\d{1,2}/[A-Z]{2})\s*[-–]\s*(\d{1,2}/\d{1,2}/[A-Z]{2})",
        r"Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\s*[-–to\s]+\s*\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Billing\s+Cycle[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\s*[-–to\s]+\s*\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Statement\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\s*[-–to\s]+\s*\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Period[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\s*[-–to\s]+\s*\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4}\s*[-–]+\s*\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"From[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})\s+To[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"(\d{1,2}[/-]\d{1,2}[/-]\d{4})\s+(?:to|-)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
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
    # Pattern: Payment Due Date: 15 Oct 2025
    due_date_patterns = [
        r"Payment\s+due\s+date\s*:\s*(\d{1,2}/\d{1,2}/\d{4})",
        r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Pay\s+by[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Payment\s+Due[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Due\s+on[:\s]+(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"Payment\s+Due\s+Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"Due\s+Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
        r"Pay\s+by[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})"
    ]
    
    for pattern in due_date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            data["payment_due_date"] = match.group(1).strip()
            break
    
    # Extract Total Amount Due
    # Pattern: Total Amount Due: ₹14,820.00 or Rs. 14,820.00
    amount_patterns = [
        r"New\s+Balance\s+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Total\s+balance\s*:\s*(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Total\s+Amount\s+Due[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Total\s+Due[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Amount\s+Due[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Total\s+Outstanding[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Outstanding\s+Amount[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Amount\s+Payable[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"Payable[:\s]+(?:\$|Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)",
        r"(?:\$|Rs\.?|INR|₹)\s*([\d,]+\.?\d*)\s+Total\s+(?:Amount\s+)?Due",
        r"(?:\$|Rs\.?|INR|₹)\s*([\d,]+\.?\d*)\s+(?:is\s+)?(?:the\s+)?Total"
    ]
    
    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = match.group(1).strip()
            data["total_amount_due"] = f"₹{amount}"
            break
    
    return data


def validate_hdfc_statement(text: str) -> bool:
    """
    Validate if the PDF is an HDFC Bank statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        True if HDFC statement, False otherwise
    """
    hdfc_keywords = [
        "HDFC Bank",
        "HDFC BANK",
        "hdfc bank",
        "HDFC Credit Card",
        "www.hdfcbank.com"
    ]
    
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in hdfc_keywords)
