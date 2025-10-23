"""
Test script for credit card statement parser
Useful for debugging and testing individual parsers
"""

from parsers import (
    parse_hdfc_statement, validate_hdfc_statement,
    parse_icici_statement, validate_icici_statement,
    parse_sbi_statement, validate_sbi_statement,
    parse_axis_statement, validate_axis_statement,
    parse_amex_statement, validate_amex_statement
)


# Sample text snippets for testing (mock data)
SAMPLE_TEXTS = {
    "hdfc": """
    HDFC Bank Credit Card Statement
    Name on Card: AYUSH KARANI
    Card Number: XXXX XXXX XXXX 4581
    Statement Period: 01 Sep 2025 - 30 Sep 2025
    Payment Due Date: 15 Oct 2025
    Total Amount Due: Rs. 14,820.00
    """,
    
    "icici": """
    ICICI Bank Credit Card Statement
    Card Member: AYUSH KARANI
    Card Number: XXXX XXXX XXXX 1234
    Statement Period: 05 Sep 2025 - 04 Oct 2025
    Payment Due Date: 20 Oct 2025
    Total Amount Due: Rs. 25,500.00
    """,
    
    "sbi": """
    SBI Card Statement
    Card Holder: AYUSH KARANI
    Card Number: XXXX XXXX XXXX 5678
    Billing Cycle: 10 Sep 2025 - 09 Oct 2025
    Due Date: 25 Oct 2025
    Total Amount Due: Rs. 18,200.00
    """,
    
    "axis": """
    Axis Bank Credit Card Statement
    Customer Name: AYUSH KARANI
    Card Number: XXXX XXXX XXXX 9012
    Statement Period: 15 Sep 2025 - 14 Oct 2025
    Payment Due Date: 30 Oct 2025
    Total Amount Due: Rs. 32,450.00
    """,
    
    "amex": """
    American Express Statement
    Card Member: AYUSH KARANI
    Account ending: 3456
    Statement Period: 01 Sep 2025 - 30 Sep 2025
    Payment Due: 20 Oct 2025
    Total Amount Due: Rs. 45,000.00
    """
}


def test_parser(bank_name: str, validator_func, parser_func):
    """Test a specific bank parser"""
    print(f"\n{'='*60}")
    print(f"Testing {bank_name.upper()} Parser")
    print('='*60)
    
    text = SAMPLE_TEXTS.get(bank_name.lower(), "")
    
    if not text:
        print(f"❌ No sample text available for {bank_name}")
        return
    
    # Test validation
    is_valid = validator_func(text)
    print(f"✓ Validation: {'PASSED' if is_valid else 'FAILED'}")
    
    if not is_valid:
        print(f"⚠️  Warning: Validator did not recognize {bank_name} text")
    
    # Test parsing
    result = parser_func(text)
    
    print("\nParsed Data:")
    print("-" * 60)
    for key, value in result.items():
        status = "✓" if value else "✗"
        print(f"{status} {key:20s}: {value}")
    
    # Check completeness
    missing_fields = [k for k, v in result.items() if v is None]
    if missing_fields:
        print(f"\n⚠️  Missing fields: {', '.join(missing_fields)}")
    else:
        print("\n✅ All fields extracted successfully!")


def test_all_parsers():
    """Test all bank parsers"""
    print("\n" + "="*60)
    print("CREDIT CARD STATEMENT PARSER - TEST SUITE")
    print("="*60)
    
    parsers = [
        ("hdfc", validate_hdfc_statement, parse_hdfc_statement),
        ("icici", validate_icici_statement, parse_icici_statement),
        ("sbi", validate_sbi_statement, parse_sbi_statement),
        ("axis", validate_axis_statement, parse_axis_statement),
        ("amex", validate_amex_statement, parse_amex_statement),
    ]
    
    for bank_name, validator, parser in parsers:
        test_parser(bank_name, validator, parser)
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETED")
    print("="*60)


if __name__ == "__main__":
    test_all_parsers()
