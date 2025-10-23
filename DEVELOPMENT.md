# 🛠️ Development Guide

Guide for developers who want to extend or customize the Credit Card Statement Parser.

## 🏗️ Architecture

### Project Structure

```
credit_card_parser/
├── parsers/              # Bank-specific parsers
│   ├── __init__.py      # Package initialization
│   ├── hdfc_parser.py   # HDFC Bank parser
│   ├── icici_parser.py  # ICICI Bank parser
│   ├── sbi_parser.py    # SBI Card parser
│   ├── axis_parser.py   # Axis Bank parser
│   └── amex_parser.py   # American Express parser
├── main.py              # CLI interface & core logic
├── app.py               # Streamlit web interface
├── test_parser.py       # Test suite
└── requirements.txt     # Dependencies
```

### Data Flow

```
PDF File
    ↓
[Text Extraction] (pdfplumber)
    ↓
[OCR Fallback] (pytesseract) - if needed
    ↓
[Bank Detection] (keyword matching)
    ↓
[Bank-Specific Parser] (regex patterns)
    ↓
[Structured JSON Output]
```

## 🔧 Adding a New Bank Parser

### Step 1: Create Parser File

Create `parsers/newbank_parser.py`:

```python
"""
New Bank Credit Card Statement Parser
"""

import re
from typing import Dict, Optional


def parse_newbank_statement(text: str) -> Dict[str, Optional[str]]:
    """
    Parse New Bank credit card statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Dictionary containing parsed data
    """
    data = {
        "issuer": "New Bank",
        "card_holder": None,
        "last_4_digits": None,
        "billing_cycle": None,
        "payment_due_date": None,
        "total_amount_due": None
    }
    
    # Add regex patterns here
    # Example:
    name_pattern = r"Card\s+Holder[:\s]+([A-Z\s]+)"
    match = re.search(name_pattern, text, re.IGNORECASE)
    if match:
        data["card_holder"] = match.group(1).strip()
    
    # Add more patterns for other fields...
    
    return data


def validate_newbank_statement(text: str) -> bool:
    """
    Validate if the PDF is a New Bank statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        True if New Bank statement, False otherwise
    """
    keywords = ["New Bank", "www.newbank.com"]
    text_lower = text.lower()
    return any(keyword.lower() in text_lower for keyword in keywords)
```

### Step 2: Update Package Init

Edit `parsers/__init__.py`:

```python
from .newbank_parser import parse_newbank_statement, validate_newbank_statement

__all__ = [
    # ... existing exports ...
    'parse_newbank_statement',
    'validate_newbank_statement',
]
```

### Step 3: Register in Main

Edit `main.py` to add to `BANK_CONFIGS`:

```python
from parsers import (
    # ... existing imports ...
    parse_newbank_statement, validate_newbank_statement
)

BANK_CONFIGS = [
    # ... existing configs ...
    {
        "name": "New Bank",
        "validator": validate_newbank_statement,
        "parser": parse_newbank_statement
    }
]
```

### Step 4: Add Test Case

Edit `test_parser.py`:

```python
SAMPLE_TEXTS["newbank"] = """
    New Bank Credit Card Statement
    Card Holder: AYUSH KARANI
    Card Number: XXXX XXXX XXXX 1111
    Statement Period: 01 Oct 2025 - 31 Oct 2025
    Payment Due Date: 15 Nov 2025
    Total Amount Due: Rs. 10,000.00
"""

# Add to parsers list in test_all_parsers()
parsers = [
    # ... existing parsers ...
    ("newbank", validate_newbank_statement, parse_newbank_statement),
]
```

## 📝 Writing Regex Patterns

### Best Practices

1. **Start Broad, Then Narrow**: Begin with flexible patterns, refine as needed
2. **Test Variations**: Account for different date formats, spacing, etc.
3. **Use Non-Greedy Matching**: Prefer `.*?` over `.*`
4. **Case Insensitive**: Use `re.IGNORECASE` flag
5. **Multiple Patterns**: Provide fallback patterns for different formats

### Common Pattern Examples

#### Name Extraction
```python
name_patterns = [
    r"Name\s+on\s+Card[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Card\s+Holder[:\s]+([A-Z\s]+?)(?:\n)",
    r"Dear\s+([A-Z\s]+?)(?:,|\n)",
]
```

#### Card Number (Last 4 Digits)
```python
card_patterns = [
    r"Card\s+Number[:\s]+(?:X+\s*)*(\d{4})",
    r"(?:X{4}\s+){3}(\d{4})",
    r"ending\s+(?:with\s+)?(\d{4})",
]
```

#### Date Extraction
```python
date_patterns = [
    r"Due\s+Date[:\s]+(\d{1,2}\s+[A-Za-z]{3}\s+\d{4})",
    r"Due[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{4})",
]
```

#### Amount Extraction
```python
amount_patterns = [
    r"Total\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
    r"Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)",
]
```

### Testing Regex Patterns

Use Python's interactive shell or a regex tester:

```python
import re

text = "Total Amount Due: Rs. 14,820.00"
pattern = r"Total\s+Amount\s+Due[:\s]+(?:Rs\.?|INR|₹)\s*([\d,]+\.?\d*)"

match = re.search(pattern, text, re.IGNORECASE)
if match:
    print(match.group(1))  # Output: 14,820.00
```

## 🧪 Testing

### Run All Tests
```bash
python test_parser.py
```

### Test Specific Bank
```python
from test_parser import test_parser
from parsers import parse_hdfc_statement, validate_hdfc_statement

test_parser("hdfc", validate_hdfc_statement, parse_hdfc_statement)
```

### Test with Real PDF
```bash
python main.py path/to/statement.pdf
```

## 🐛 Debugging Tips

### 1. Print Extracted Text
```python
import pdfplumber

with pdfplumber.open("statement.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        print(f"--- Page {i+1} ---")
        print(page.extract_text())
```

### 2. Test Regex Patterns Interactively
```python
import re

text = """Your extracted text here"""
pattern = r"Your\s+Pattern[:\s]+(.+)"

matches = re.findall(pattern, text, re.IGNORECASE)
print(matches)
```

### 3. Check Bank Detection
```python
from main import detect_bank

text = """Your statement text"""
bank = detect_bank(text)
print(f"Detected: {bank['name'] if bank else 'Unknown'}")
```

## 🔄 Continuous Improvement

### Collecting Feedback

1. **Log Failed Extractions**: Track which fields fail most often
2. **Version Statements**: Note statement format changes over time
3. **User Reports**: Gather feedback on accuracy

### Updating Patterns

When statement formats change:

1. Get sample of new format
2. Identify what changed
3. Update regex patterns
4. Test with both old and new formats
5. Deploy update

## 📊 Performance Optimization

### For Large Batches

```python
from concurrent.futures import ThreadPoolExecutor
from main import parse_statement

pdf_files = ["file1.pdf", "file2.pdf", "file3.pdf"]

with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(parse_statement, pdf_files))
```

### Caching

For repeated parsing of same file:

```python
import hashlib
import json
from pathlib import Path

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def parse_with_cache(pdf_path):
    cache_dir = Path(".cache")
    cache_dir.mkdir(exist_ok=True)
    
    file_hash = get_file_hash(pdf_path)
    cache_file = cache_dir / f"{file_hash}.json"
    
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    
    result = parse_statement(pdf_path)
    cache_file.write_text(json.dumps(result))
    
    return result
```

## 🚀 Deployment

### As a Web Service

Use FastAPI:

```python
from fastapi import FastAPI, UploadFile
from main import parse_statement
import tempfile

app = FastAPI()

@app.post("/parse")
async def parse_endpoint(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        tmp.write(await file.read())
        result = parse_statement(tmp.name)
    return result
```

### As a Package

Create `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="credit-card-parser",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pdfplumber>=0.10.3",
        "pytesseract>=0.3.10",
    ],
)
```

Install: `pip install -e .`

## 📚 Resources

- **Regex Testing**: https://regex101.com/
- **pdfplumber Docs**: https://github.com/jsvine/pdfplumber
- **Tesseract OCR**: https://github.com/tesseract-ocr/tesseract
- **Streamlit Docs**: https://docs.streamlit.io/

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Happy Coding! 🚀**
