"""
Example usage scripts for Credit Card Statement Parser
Demonstrates various ways to use the parser
"""

import json
from pathlib import Path
from main import parse_statement, extract_text_from_pdf, detect_bank


def example_1_basic_parsing():
    """Example 1: Basic PDF parsing"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic PDF Parsing")
    print("="*60)
    
    pdf_path = "sample_pdfs/hdfc_statement.pdf"
    
    # Check if file exists
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        print("Please add a sample PDF to test with.")
        return
    
    # Parse the statement
    result = parse_statement(pdf_path)
    
    # Display results
    print(json.dumps(result, indent=2, ensure_ascii=False))


def example_2_with_ocr():
    """Example 2: Parsing with OCR fallback"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Parsing with OCR")
    print("="*60)
    
    pdf_path = "sample_pdfs/scanned_statement.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Parse with OCR enabled
    result = parse_statement(pdf_path, use_ocr=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def example_3_batch_processing():
    """Example 3: Process multiple PDFs"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Batch Processing")
    print("="*60)
    
    # Get all PDFs in sample_pdfs directory
    pdf_dir = Path("sample_pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in sample_pdfs/")
        return
    
    results = []
    
    for pdf_file in pdf_files:
        print(f"\nProcessing: {pdf_file.name}")
        result = parse_statement(str(pdf_file))
        results.append({
            "filename": pdf_file.name,
            "data": result
        })
    
    # Save all results to JSON
    output_file = "batch_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Processed {len(results)} files")
    print(f"Results saved to: {output_file}")


def example_4_custom_extraction():
    """Example 4: Custom extraction workflow"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Extraction Workflow")
    print("="*60)
    
    pdf_path = "sample_pdfs/hdfc_statement.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ File not found: {pdf_path}")
        return
    
    # Step 1: Extract text
    print("Step 1: Extracting text...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")
    
    # Step 2: Detect bank
    print("\nStep 2: Detecting bank...")
    bank_config = detect_bank(text)
    
    if bank_config:
        print(f"Detected: {bank_config['name']}")
        
        # Step 3: Parse with detected parser
        print("\nStep 3: Parsing statement...")
        result = bank_config['parser'](text)
        
        # Step 4: Display results
        print("\nStep 4: Results")
        for key, value in result.items():
            print(f"  {key:20s}: {value}")
    else:
        print("❌ Could not detect bank")


def example_5_error_handling():
    """Example 5: Proper error handling"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Error Handling")
    print("="*60)
    
    pdf_path = "sample_pdfs/test_statement.pdf"
    
    try:
        result = parse_statement(pdf_path)
        
        # Check for errors in result
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            print(f"Message: {result['message']}")
        else:
            # Validate extracted data
            missing_fields = [k for k, v in result.items() if v is None]
            
            if missing_fields:
                print(f"⚠️  Warning: Some fields could not be extracted")
                print(f"Missing: {', '.join(missing_fields)}")
            else:
                print("✅ All fields extracted successfully!")
            
            print(json.dumps(result, indent=2, ensure_ascii=False))
    
    except FileNotFoundError:
        print(f"❌ File not found: {pdf_path}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def example_6_export_to_csv():
    """Example 6: Export results to CSV"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Export to CSV")
    print("="*60)
    
    import csv
    
    pdf_dir = Path("sample_pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Parse all statements
    results = []
    for pdf_file in pdf_files:
        result = parse_statement(str(pdf_file))
        if "error" not in result:
            results.append(result)
    
    # Export to CSV
    if results:
        csv_file = "statements_export.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        
        print(f"✅ Exported {len(results)} statements to {csv_file}")
    else:
        print("❌ No valid results to export")


def example_7_filter_by_bank():
    """Example 7: Filter and process by specific bank"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Filter by Bank")
    print("="*60)
    
    target_bank = "HDFC Bank"
    pdf_dir = Path("sample_pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    hdfc_statements = []
    
    for pdf_file in pdf_files:
        result = parse_statement(str(pdf_file))
        
        if result.get("issuer") == target_bank:
            hdfc_statements.append({
                "file": pdf_file.name,
                "data": result
            })
    
    print(f"Found {len(hdfc_statements)} {target_bank} statements")
    
    # Calculate total amount due across all HDFC statements
    if hdfc_statements:
        total = 0
        for stmt in hdfc_statements:
            amount_str = stmt["data"].get("total_amount_due", "₹0")
            # Extract numeric value
            amount = float(amount_str.replace("₹", "").replace(",", ""))
            total += amount
        
        print(f"Total amount due across all {target_bank} statements: ₹{total:,.2f}")


def example_8_summary_report():
    """Example 8: Generate summary report"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Summary Report")
    print("="*60)
    
    pdf_dir = Path("sample_pdfs")
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        return
    
    # Parse all statements
    results = []
    for pdf_file in pdf_files:
        result = parse_statement(str(pdf_file))
        if "error" not in result:
            results.append(result)
    
    if not results:
        print("❌ No valid statements found")
        return
    
    # Generate summary
    print(f"\n📊 SUMMARY REPORT")
    print("-" * 60)
    print(f"Total Statements Processed: {len(results)}")
    
    # Group by bank
    by_bank = {}
    for result in results:
        bank = result.get("issuer", "Unknown")
        by_bank[bank] = by_bank.get(bank, 0) + 1
    
    print("\nStatements by Bank:")
    for bank, count in by_bank.items():
        print(f"  {bank:20s}: {count}")
    
    # Calculate total due
    total_due = 0
    for result in results:
        amount_str = result.get("total_amount_due", "₹0")
        try:
            amount = float(amount_str.replace("₹", "").replace(",", ""))
            total_due += amount
        except:
            pass
    
    print(f"\nTotal Amount Due (All Cards): ₹{total_due:,.2f}")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("CREDIT CARD STATEMENT PARSER - USAGE EXAMPLES")
    print("="*70)
    
    examples = [
        ("Basic Parsing", example_1_basic_parsing),
        ("OCR Parsing", example_2_with_ocr),
        ("Batch Processing", example_3_batch_processing),
        ("Custom Workflow", example_4_custom_extraction),
        ("Error Handling", example_5_error_handling),
        ("Export to CSV", example_6_export_to_csv),
        ("Filter by Bank", example_7_filter_by_bank),
        ("Summary Report", example_8_summary_report),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nNote: Most examples require sample PDFs in the 'sample_pdfs/' directory")
    print("\nTo run a specific example, modify this script or call the function directly.")
    print("\nExample: python -c 'from examples import example_1_basic_parsing; example_1_basic_parsing()'")


if __name__ == "__main__":
    main()
