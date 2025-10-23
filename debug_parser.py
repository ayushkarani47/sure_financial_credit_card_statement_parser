"""
Debug script to help identify why parsing is failing
Shows extracted text and tests regex patterns
"""

import re
import sys
from main import extract_text_from_pdf, detect_bank
from parsers.hdfc_parser import parse_hdfc_statement


def debug_statement(pdf_path: str):
    """
    Debug a credit card statement to see what's being extracted
    
    Args:
        pdf_path: Path to the PDF file
    """
    print("="*80)
    print("CREDIT CARD STATEMENT PARSER - DEBUG MODE")
    print("="*80)
    
    # Step 1: Extract text
    print("\n[STEP 1] Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    
    if not text:
        print("❌ ERROR: No text extracted from PDF")
        return
    
    print(f"✅ Extracted {len(text)} characters")
    
    # Step 2: Show first 2000 characters
    print("\n[STEP 2] First 2000 characters of extracted text:")
    print("-"*80)
    print(text[:2000])
    print("-"*80)
    
    # Step 3: Detect bank
    print("\n[STEP 3] Detecting bank...")
    bank_config = detect_bank(text)
    
    if bank_config:
        print(f"✅ Detected: {bank_config['name']}")
    else:
        print("❌ Bank not detected")
        print("\nSearching for bank keywords in text:")
        keywords = ["HDFC", "ICICI", "SBI", "Axis", "American Express", "Amex"]
        for keyword in keywords:
            if keyword.lower() in text.lower():
                print(f"  Found: {keyword}")
        return
    
    # Step 4: Test individual regex patterns
    print("\n[STEP 4] Testing regex patterns for HDFC Bank...")
    print("-"*80)
    
    # Test Card Holder Name
    print("\n📝 Testing Card Holder Name patterns:")
    name_patterns = [
        (r"Name\s+on\s+Card[:\s]+([A-Z\s]+?)(?:\n|Card)", "Name on Card"),
        (r"Card\s+Holder[:\s]+([A-Z\s]+?)(?:\n|Card)", "Card Holder"),
        (r"Dear\s+([A-Z\s]+?)(?:,|\n)", "Dear"),
        (r"Mr\.?\s+([A-Z\s]+?)(?:\n|,)", "Mr."),
        (r"Ms\.?\s+([A-Z\s]+?)(?:\n|,)", "Ms.")
    ]
    
    for pattern, desc in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ {desc}: '{match.group(1).strip()}'")
        else:
            print(f"  ❌ {desc}: No match")
    
    # Test Last 4 Digits
    print("\n💳 Testing Last 4 Digits patterns:")
    card_patterns = [
        (r"Card\s+(?:Number|ending|No\.?)[:\s]+(?:X+\s*)*(\d{4})", "Card Number/ending"),
        (r"(?:X{4}\s+){3}(\d{4})", "XXXX XXXX XXXX 1234"),
        (r"ending\s+(?:with\s+)?(\d{4})", "ending with"),
        (r"Card\s+No\.?\s*[:\s]+[X\*]+(\d{4})", "Card No.")
    ]
    
    for pattern, desc in card_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ {desc}: '{match.group(1)}'")
        else:
            print(f"  ❌ {desc}: No match")
    
    # Test Billing Cycle
    print("\n📅 Testing Billing Cycle patterns:")
    cycle_patterns = [
        (r"Statement\s+Period[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–to]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Statement Period"),
        (r"Billing\s+Cycle[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–to]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Billing Cycle"),
        (r"(\d{1,2}\s+[A-Za-z]{3}\s+\d{4}\s*[-–]+\s*\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Generic date range"),
        (r"From[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})\s+To[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})", "From/To")
    ]
    
    for pattern, desc in cycle_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ {desc}: '{match.group(1)}'")
        else:
            print(f"  ❌ {desc}: No match")
    
    # Test Payment Due Date
    print("\n💰 Testing Payment Due Date patterns:")
    due_date_patterns = [
        (r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Payment Due Date"),
        (r"Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Due Date"),
        (r"Pay\s+by[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})", "Pay by"),
        (r"Payment\s+Due[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})", "Payment Due")
    ]
    
    for pattern, desc in due_date_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ {desc}: '{match.group(1)}'")
        else:
            print(f"  ❌ {desc}: No match")
    
    # Test Total Amount Due
    print("\n💵 Testing Total Amount Due patterns:")
    amount_patterns = [
        (r"Total\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)", "Total Amount Due"),
        (r"Total\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)", "Total Due"),
        (r"Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)", "Amount Due"),
        (r"Minimum\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)", "Minimum Amount Due"),
        (r"(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)\s+Total\s+(?:Amount\s+)?Due", "Reverse pattern")
    ]
    
    for pattern, desc in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            print(f"  ✅ {desc}: '₹{match.group(1)}'")
        else:
            print(f"  ❌ {desc}: No match")
    
    # Step 5: Show final parsed result
    print("\n[STEP 5] Final parsed result:")
    print("-"*80)
    result = parse_hdfc_statement(text)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("-"*80)
    
    # Step 6: Suggestions
    print("\n[STEP 6] Debugging suggestions:")
    print("-"*80)
    
    missing_fields = [k for k, v in result.items() if v is None and k != "issuer"]
    
    if missing_fields:
        print(f"\n⚠️  Missing fields: {', '.join(missing_fields)}")
        print("\nTo fix this, you need to:")
        print("1. Look at the extracted text above (first 2000 chars)")
        print("2. Find the actual format of the missing fields in your PDF")
        print("3. Update the regex patterns in parsers/hdfc_parser.py")
        print("\nExample: If you see 'Cardholder Name: JOHN DOE', add this pattern:")
        print("   r\"Cardholder\\s+Name[:\\s]+([A-Z\\s]+?)(?:\\n|Card)\"")
        print("\nYou can also save the full extracted text to a file:")
        print(f"   python -c \"from main import extract_text_from_pdf; ")
        print(f"   text = extract_text_from_pdf('{pdf_path}'); ")
        print(f"   open('extracted_text.txt', 'w', encoding='utf-8').write(text)\"")
    else:
        print("✅ All fields extracted successfully!")
    
    print("="*80)


def save_extracted_text(pdf_path: str, output_file: str = "extracted_text.txt"):
    """
    Save extracted text to a file for manual inspection
    
    Args:
        pdf_path: Path to the PDF file
        output_file: Output text file path
    """
    text = extract_text_from_pdf(pdf_path)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"✅ Extracted text saved to: {output_file}")
    print(f"   Total characters: {len(text)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_parser.py <path_to_pdf>")
        print("       python debug_parser.py <path_to_pdf> --save-text")
        print("\nExamples:")
        print("  python debug_parser.py statement.pdf")
        print("  python debug_parser.py statement.pdf --save-text")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if "--save-text" in sys.argv:
        save_extracted_text(pdf_path)
    else:
        debug_statement(pdf_path)
