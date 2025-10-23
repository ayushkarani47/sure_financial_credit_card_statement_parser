# Sample PDFs Directory

This directory is for storing sample credit card statements for testing purposes.

## ⚠️ Important Privacy Notice

**DO NOT** commit actual credit card statements to version control!

## 📋 Guidelines

1. **Redact Sensitive Information**: Before adding any sample PDFs:
   - Remove or mask full card numbers (keep only last 4 digits)
   - Redact transaction details
   - Remove personal addresses and contact information
   - Mask account numbers

2. **Create Test Files**: For testing, you can:
   - Use redacted versions of old statements
   - Create mock statements with dummy data
   - Request sample formats from banks (if available)

3. **File Naming**: Use descriptive names:
   - `hdfc_sample_redacted.pdf`
   - `icici_test_statement.pdf`
   - `sbi_mock_statement.pdf`

## 🧪 Testing

To test the parser with your samples:

```bash
# CLI
python main.py sample_pdfs/hdfc_sample_redacted.pdf

# Web UI
streamlit run app.py
# Then upload through the interface
```

## 🔒 Security

- Add `*.pdf` to `.gitignore` to prevent accidental commits
- Never share actual statements publicly
- Use this directory only for local testing

---

**Remember**: Financial documents contain sensitive information. Always handle them securely!
