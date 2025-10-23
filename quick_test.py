"""
Quick test script - Run this with your PDF to see what's happening
Usage: python quick_test.py path/to/your/statement.pdf
"""

import sys
import json
from main import parse_statement

if len(sys.argv) < 2:
    print("Usage: python quick_test.py <path_to_pdf>")
    print("\nExample: python quick_test.py hdfc_statement.pdf")
    sys.exit(1)

pdf_path = sys.argv[1]

print("\n" + "="*70)
print("QUICK TEST - Credit Card Statement Parser")
print("="*70)

# Parse the statement
result = parse_statement(pdf_path)

# Display results
print("\nRESULT:")
print(json.dumps(result, indent=2, ensure_ascii=False))

# Check what's missing
if "error" not in result:
    missing = [k for k, v in result.items() if v is None and k != "issuer"]
    
    if missing:
        print("\n" + "="*70)
        print("⚠️  WARNING: Some fields are missing!")
        print("="*70)
        print(f"\nMissing fields: {', '.join(missing)}")
        print("\nTo debug this issue, run:")
        print(f"  python debug_parser.py {pdf_path}")
        print("\nThis will show you:")
        print("  - The extracted text from your PDF")
        print("  - Which regex patterns matched and which failed")
        print("  - Suggestions for fixing the patterns")
    else:
        print("\n" + "="*70)
        print("✅ SUCCESS! All fields extracted successfully!")
        print("="*70)
else:
    print("\n" + "="*70)
    print("❌ ERROR occurred during parsing")
    print("="*70)

print()
