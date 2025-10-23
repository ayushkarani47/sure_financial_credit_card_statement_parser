"""
Credit Card Statement Parser - Main Module
Automatically detects bank and extracts key information from credit card statements
"""

import sys
import json
import pdfplumber
from pathlib import Path
from typing import Dict, Optional

# Import all parsers
from parsers import (
    parse_hdfc_statement, validate_hdfc_statement,
    parse_icici_statement, validate_icici_statement,
    parse_sbi_statement, validate_sbi_statement,
    parse_axis_statement, validate_axis_statement,
    parse_amex_statement, validate_amex_statement
)


# Bank detection and parsing configuration
BANK_CONFIGS = [
    {
        "name": "HDFC Bank",
        "validator": validate_hdfc_statement,
        "parser": parse_hdfc_statement
    },
    {
        "name": "ICICI Bank",
        "validator": validate_icici_statement,
        "parser": parse_icici_statement
    },
    {
        "name": "SBI Card",
        "validator": validate_sbi_statement,
        "parser": parse_sbi_statement
    },
    {
        "name": "Axis Bank",
        "validator": validate_axis_statement,
        "parser": parse_axis_statement
    },
    {
        "name": "American Express",
        "validator": validate_amex_statement,
        "parser": parse_amex_statement
    }
]


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using pdfplumber
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text from all pages
    """
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""
    
    return text


def extract_text_with_ocr(pdf_path: str) -> str:
    """
    Fallback: Extract text using OCR (pytesseract) for image-based PDFs
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text using OCR
    """
    try:
        import pytesseract
        from pdf2image import convert_from_path
        
        text = ""
        images = convert_from_path(pdf_path)
        
        for i, image in enumerate(images):
            page_text = pytesseract.image_to_string(image)
            text += page_text + "\n"
        
        return text
    except ImportError:
        print("Warning: pytesseract or pdf2image not installed. OCR fallback unavailable.")
        return ""
    except Exception as e:
        print(f"Error during OCR extraction: {e}")
        return ""


def detect_bank(text: str) -> Optional[Dict]:
    """
    Detect which bank issued the statement
    
    Args:
        text: Extracted text from PDF
        
    Returns:
        Bank configuration dict or None if not detected
    """
    for bank_config in BANK_CONFIGS:
        if bank_config["validator"](text):
            return bank_config
    
    return None


def parse_statement(pdf_path: str, use_ocr: bool = False) -> Dict:
    """
    Main function to parse credit card statement
    
    Args:
        pdf_path: Path to the PDF statement
        use_ocr: Whether to use OCR fallback
        
    Returns:
        Dictionary containing parsed data
    """
    # Validate file exists
    if not Path(pdf_path).exists():
        return {
            "error": "File not found",
            "message": f"The file {pdf_path} does not exist"
        }
    
    # Extract text from PDF
    print(f"Extracting text from: {pdf_path}")
    text = extract_text_from_pdf(pdf_path)
    
    # Fallback to OCR if text extraction failed or returned minimal text
    if use_ocr and (not text or len(text.strip()) < 100):
        print("Text extraction yielded minimal results. Attempting OCR...")
        text = extract_text_with_ocr(pdf_path)
    
    if not text or len(text.strip()) < 50:
        return {
            "error": "Text extraction failed",
            "message": "Could not extract sufficient text from PDF. Try enabling OCR."
        }
    
    # Detect bank
    print("Detecting bank issuer...")
    bank_config = detect_bank(text)
    
    if not bank_config:
        return {
            "error": "Bank not detected",
            "message": "Could not identify the credit card issuer. Supported banks: HDFC, ICICI, SBI, Axis, Amex"
        }
    
    print(f"Detected: {bank_config['name']}")
    
    # Parse statement using bank-specific parser
    print("Parsing statement...")
    parsed_data = bank_config["parser"](text)
    
    return parsed_data


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_pdf> [--ocr]")
        print("\nExample: python main.py statement.pdf")
        print("         python main.py statement.pdf --ocr")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    use_ocr = "--ocr" in sys.argv
    
    # Parse the statement
    result = parse_statement(pdf_path, use_ocr=use_ocr)
    
    # Output as formatted JSON
    print("\n" + "="*60)
    print("PARSED CREDIT CARD STATEMENT")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*60)


if __name__ == "__main__":
    main()
