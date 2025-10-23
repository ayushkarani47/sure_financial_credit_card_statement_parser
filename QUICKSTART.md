# 🚀 Quick Start Guide

Get started with the Credit Card Statement Parser in 5 minutes!

## ⚡ Fast Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Test the Parsers

Run the test suite to verify everything works:

```bash
python test_parser.py
```

You should see output showing all 5 bank parsers being tested with sample data.

## 🎯 Usage Examples

### Example 1: Parse via CLI

```bash
python main.py path/to/your/statement.pdf
```

**Output:**
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

### Example 2: Parse Image-based PDF

```bash
python main.py statement.pdf --ocr
```

### Example 3: Use Web Interface

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## 📊 What Gets Extracted?

| Field | Description | Example |
|-------|-------------|---------|
| **Issuer** | Bank name | HDFC Bank |
| **Card Holder** | Your name | AYUSH KARANI |
| **Last 4 Digits** | Card number | 4581 |
| **Billing Cycle** | Statement period | 01 Sep 2025 - 30 Sep 2025 |
| **Due Date** | Payment deadline | 15 Oct 2025 |
| **Amount Due** | Total to pay | ₹14,820.00 |

## 🏦 Supported Banks

✅ HDFC Bank  
✅ ICICI Bank  
✅ SBI Card  
✅ Axis Bank  
✅ American Express  

## 🔧 Troubleshooting

### Issue: "Bank not detected"

**Solution:** 
- Verify your PDF is from a supported bank
- Check if the PDF contains text (not just images)
- Try with `--ocr` flag

### Issue: "Text extraction failed"

**Solution:**
- Install Tesseract OCR
- Use `--ocr` flag
- Ensure PDF is not password-protected

### Issue: Missing or incorrect data

**Solution:**
- Statement format may vary
- Check the parser file for your bank in `parsers/` directory
- Adjust regex patterns if needed

## 💡 Tips

1. **Better Accuracy**: Use original PDFs downloaded from bank portals
2. **OCR Quality**: Ensure scanned statements are high resolution
3. **Privacy**: Never share actual statements; use redacted samples for testing
4. **Batch Processing**: Loop through multiple files in a script

## 📝 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Customize parsers for your specific statement formats
- Integrate with your financial tracking tools
- Contribute improvements back to the project

## 🆘 Need Help?

- Check [README.md](README.md) for detailed docs
- Review parser files in `parsers/` directory
- Run `python test_parser.py` to test parsers
- Open an issue if you find bugs

---

**Happy Parsing! 💳✨**
