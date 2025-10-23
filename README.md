# 💳 Credit Card Statement Parser

A Python-based tool to automatically extract key information from credit card statements of major Indian banks. Supports both CLI and web interface.

## 🎯 Features

- **Multi-Bank Support**: Parses statements from 5 major issuers
  - HDFC Bank
  - ICICI Bank
  - SBI Card
  - Axis Bank
  - American Express

- **Automatic Bank Detection**: Identifies the issuer automatically

- **Key Data Extraction**:
  - Card Holder Name
  - Last 4 Digits of Card Number
  - Billing Cycle / Statement Period
  - Payment Due Date
  - Total Amount Due

- **OCR Fallback**: Handles image-based PDFs using Tesseract OCR

- **Streamlit UI**: User-friendly web interface for uploading and parsing statements

- **JSON Output**: Structured data output for easy integration

## 📁 Project Structure

```
credit_card_parser/
│
├── parsers/
│   ├── __init__.py
│   ├── hdfc_parser.py      # HDFC Bank parser
│   ├── icici_parser.py     # ICICI Bank parser
│   ├── sbi_parser.py       # SBI Card parser
│   ├── axis_parser.py      # Axis Bank parser
│   └── amex_parser.py      # American Express parser
│
├── main.py                 # CLI interface
├── app.py                  # Streamlit web interface
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── sample_pdfs/           # Sample statements (not included)
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### For OCR Support (Optional)

**Windows:**
1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

### Install Python Dependencies

```bash
# Clone or download the project
cd credit_card_parser

# Install required packages
pip install -r requirements.txt
```

## 💻 Usage

### Option 1: Command Line Interface (CLI)

```bash
# Basic usage
python main.py path/to/statement.pdf

# With OCR support
python main.py path/to/statement.pdf --ocr
```

**Example Output:**
```json
{
  "issuer": "HDFC Bank",
  "card_holder": "AYUSH KARANI",
  "last_4_digits": "4581",
  "billing_cycle": "01 Sep 2025 - 30 Sep 2025",
  "payment_due_date": "15 Oct 2025",
  "total_amount_due": "₹14,820.00"
}
```

### Option 2: Streamlit Web Interface

```bash
# Start the web app
streamlit run app.py
```

Then:
1. Open your browser to `http://localhost:8501`
2. Upload your PDF statement
3. Click "Parse Statement"
4. View and download results

## 🔧 How It Works

1. **Text Extraction**: Uses `pdfplumber` to extract text from PDF
2. **Bank Detection**: Scans for bank-specific keywords to identify issuer
3. **Pattern Matching**: Applies bank-specific regex patterns to extract data
4. **OCR Fallback**: If text extraction fails, uses `pytesseract` for image-based PDFs
5. **JSON Output**: Returns structured data in JSON format

## 📝 Customization

### Adding New Banks

1. Create a new parser file in `parsers/` directory:
```python
# parsers/newbank_parser.py

def parse_newbank_statement(text: str) -> dict:
    # Add regex patterns for the new bank
    pass

def validate_newbank_statement(text: str) -> bool:
    # Add validation logic
    pass
```

2. Update `parsers/__init__.py` to include new parser

3. Add bank configuration to `main.py`:
```python
BANK_CONFIGS.append({
    "name": "New Bank",
    "validator": validate_newbank_statement,
    "parser": parse_newbank_statement
})
```

### Adjusting Regex Patterns

Each parser file contains regex patterns for extracting data. Modify these patterns if:
- Statement format changes
- Extraction accuracy is low
- New statement variations appear

Example pattern modification in `hdfc_parser.py`:
```python
# Add new pattern to existing list
name_patterns = [
    r"Name\s+on\s+Card[:\s]+([A-Z\s]+?)(?:\n|Card)",
    r"Your\s+New\s+Pattern[:\s]+([A-Z\s]+)",  # Add this
]
```

## 🛡️ Privacy & Security

- **Local Processing**: All parsing happens on your machine
- **No Data Upload**: No information is sent to external servers
- **Temporary Storage**: Uploaded files are deleted after processing
- **No Logging**: Sensitive data is not logged or stored

## ⚠️ Limitations

- **Format Dependency**: Relies on consistent statement formats
- **Regex Accuracy**: May require pattern adjustments for new formats
- **OCR Quality**: Image-based PDFs may have lower accuracy
- **Language Support**: Currently optimized for English statements

## 🐛 Troubleshooting

### "Bank not detected"
- Verify the PDF is from a supported bank
- Check if the PDF contains readable text (not just images)
- Try enabling OCR mode

### "Text extraction failed"
- Enable OCR with `--ocr` flag
- Ensure Tesseract is installed for OCR support
- Check if PDF is password-protected

### Partial or missing data
- Statement format may differ from expected patterns
- Adjust regex patterns in the corresponding parser file
- Check if all required fields are present in the statement

## 📦 Dependencies

- **pdfplumber**: PDF text extraction
- **pytesseract**: OCR for image-based PDFs
- **pdf2image**: Convert PDF pages to images for OCR
- **streamlit**: Web interface
- **pandas**: Data manipulation (optional)
- **Pillow**: Image processing

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch
3. Add your changes (new parsers, improved patterns, bug fixes)
4. Test thoroughly with sample statements
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Built with Python and open-source libraries
- Inspired by the need for automated financial document processing
- Thanks to all contributors and users

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review troubleshooting section

---

**Note**: This tool is for personal use only. Always handle financial documents securely and comply with your bank's terms of service.

**Disclaimer**: This parser is not affiliated with any of the supported banks. Statement formats may change without notice.
