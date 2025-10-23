# Credit Card Statement Parser - Debugging Guide

## Problem: Only Bank Name is Detected

When the parser only identifies the bank but fails to extract other details (card holder, last 4 digits, billing cycle, payment due date, total amount due), it means the **regex patterns don't match the actual text format** in your PDF.

## Solution Steps

### Step 1: Run the Debug Script

```bash
python debug_parser.py path/to/your/statement.pdf
```

This will show you:
- ✅ What text was extracted from the PDF
- ✅ Which regex patterns matched and which failed
- ✅ The final parsed result
- ✅ Specific suggestions for fixing the issue

### Step 2: Save Extracted Text for Manual Inspection

```bash
python debug_parser.py path/to/your/statement.pdf --save-text
```

This saves all extracted text to `extracted_text.txt` so you can see exactly what the parser is working with.

### Step 3: Identify the Actual Format

Open `extracted_text.txt` and find how each field appears in your PDF:

**Example - What to look for:**

```
Card Holder Name might appear as:
- "Name on Card: AYUSH KARANI"
- "Cardholder: AYUSH KARANI"
- "Dear AYUSH KARANI,"
- "Mr. AYUSH KARANI"

Last 4 Digits might appear as:
- "Card Number: XXXX XXXX XXXX 4581"
- "Card ending with 4581"
- "Card No.: ****4581"

Billing Cycle might appear as:
- "Statement Period: 01 Sep 2025 - 30 Sep 2025"
- "Billing Cycle: 01/09/2025 to 30/09/2025"
- "From 01-Sep-2025 To 30-Sep-2025"

Payment Due Date might appear as:
- "Payment Due Date: 15 Oct 2025"
- "Due Date: 15/10/2025"
- "Pay by: 15-Oct-2025"

Total Amount Due might appear as:
- "Total Amount Due: Rs. 14,820.00"
- "Total Due: ₹14,820.00"
- "Amount Payable: INR 14,820.00"
```

### Step 4: Update Regex Patterns

Edit `parsers/hdfc_parser.py` (or the appropriate bank parser) and add new patterns based on what you found.

**Example - Adding a new pattern for card holder:**

```python
# If you found "Cardholder: AYUSH KARANI" in your PDF
name_patterns = [
    r"Name\s+on\s+Card[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Card\s+Holder[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Cardholder[:\s]+([A-Z\s]+?)(?:\n|Card)",  # <-- ADD THIS LINE
    r"Dear\s+([A-Z\s]+?)(?:,|\n)",
    # ... rest of patterns
]
```

### Step 5: Test Your Changes

```bash
python debug_parser.py path/to/your/statement.pdf
```

Check if the new patterns now match. Repeat until all fields are extracted.

## Common Issues and Fixes

### Issue 1: Text has extra spaces or newlines

**Problem:** PDF text might have irregular spacing
```
"Payment    Due    Date:    15 Oct 2025"
```

**Solution:** Use `\s+` instead of `\s` in patterns
```python
r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})"
```

### Issue 2: Different date formats

**Problem:** Your PDF uses DD/MM/YYYY instead of DD MMM YYYY

**Solution:** Add a pattern for that format
```python
due_date_patterns = [
    r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
    r"Payment\s+Due\s+Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",  # <-- ADD THIS
]
```

### Issue 3: Currency symbol variations

**Problem:** Amount uses different currency symbols

**Solution:** Make currency symbol optional
```python
r"Total\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)?\s*([\d,]+\.?\d*)"
#                                            ^ Note the ? makes it optional
```

### Issue 4: Case sensitivity

**Problem:** Text is in different case than expected

**Solution:** Already handled! All patterns use `re.IGNORECASE` flag

### Issue 5: Field name variations

**Problem:** Different HDFC statements use different field names

**Solution:** Add multiple pattern variations
```python
name_patterns = [
    r"Name\s+on\s+Card[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Card\s+Holder[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Cardholder[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Customer\s+Name[:\s]+([A-Z\s]+?)(?:\n|Card)",  # Add more variations
    r"Account\s+Holder[:\s]+([A-Z\s]+?)(?:\n|Card)",
]
```

## Quick Reference: Regex Pattern Syntax

```
\s      - Any whitespace (space, tab, newline)
\s+     - One or more whitespace characters
\d      - Any digit (0-9)
\d{4}   - Exactly 4 digits
\d{1,2} - 1 or 2 digits
[:\s]+  - One or more colons or spaces
[A-Z]   - Any uppercase letter
[A-Za-z] - Any letter (upper or lower)
+       - One or more of the previous character
?       - Zero or one of the previous character (makes it optional)
*       - Zero or more of the previous character
(?:...) - Non-capturing group
\n      - Newline character
\.      - Literal dot (escaped)
|       - OR operator
```

## Testing Individual Patterns

You can test a single pattern in Python:

```python
import re
from main import extract_text_from_pdf

# Extract text
text = extract_text_from_pdf("your_statement.pdf")

# Test a pattern
pattern = r"Payment\s+Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})"
match = re.search(pattern, text, re.IGNORECASE)

if match:
    print(f"Found: {match.group(1)}")
else:
    print("No match")
    # Try to find similar text
    if "payment" in text.lower():
        print("Found 'payment' in text - check the exact format")
```

## Need More Help?

1. **Save the extracted text**: `python debug_parser.py statement.pdf --save-text`
2. **Look at the text file**: Open `extracted_text.txt`
3. **Find the exact format**: Search for keywords like "payment", "due", "card", etc.
4. **Update patterns**: Add new regex patterns based on what you find
5. **Test again**: Run the debug script to verify

## Example: Complete Debugging Session

```bash
# 1. Run debug to see what's failing
python debug_parser.py hdfc_statement.pdf

# Output shows:
# ❌ Card Holder: No match
# ❌ Last 4 Digits: No match
# etc.

# 2. Save extracted text
python debug_parser.py hdfc_statement.pdf --save-text

# 3. Open extracted_text.txt and find:
# "Primary Member: AYUSH KARANI"
# "Card No. ****4581"

# 4. Edit parsers/hdfc_parser.py and add:
# r"Primary\s+Member[:\s]+([A-Z\s]+?)(?:\n|Card)"
# r"Card\s+No\.\s+\*+(\d{4})"

# 5. Test again
python debug_parser.py hdfc_statement.pdf

# Output shows:
# ✅ Card Holder: 'AYUSH KARANI'
# ✅ Last 4 Digits: '4581'
```

## Pro Tips

1. **Start with the debug script** - Don't guess, see what's actually in the PDF
2. **Add patterns incrementally** - Fix one field at a time
3. **Test after each change** - Make sure you didn't break existing patterns
4. **Keep patterns flexible** - Use `\s+` instead of exact spaces
5. **Order matters** - Put more specific patterns before generic ones
6. **Use non-greedy matching** - `+?` instead of `+` to avoid over-matching

## Still Having Issues?

If the debug script shows that text extraction is working but patterns still don't match:

1. Check for **special characters** in the PDF (non-breaking spaces, etc.)
2. Look for **multi-line fields** that span across lines
3. Check if the PDF is **image-based** (try `--ocr` flag)
4. Verify the **encoding** of special characters (₹, –, etc.)

Run with OCR if needed:
```bash
python main.py statement.pdf --ocr
```
