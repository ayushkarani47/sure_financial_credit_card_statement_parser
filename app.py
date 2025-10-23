"""
Streamlit UI for Credit Card Statement Parser
Upload PDF statements and view parsed results
"""

import streamlit as st
import json
from pathlib import Path
import tempfile
from main import parse_statement

# Page configuration
st.set_page_config(
    page_title="Credit Card Statement Parser",
    page_icon="💳",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">💳 Credit Card Statement Parser</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Extract key information from your credit card statements</div>', unsafe_allow_html=True)

# File upload section
st.markdown("### 📄 Upload Your Statement")
uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=['pdf'],
    help="Upload your credit card statement in PDF format"
)

# OCR option
use_ocr = st.checkbox(
    "Enable OCR (for image-based PDFs)",
    help="Use this option if your PDF contains scanned images instead of text"
)

# Parse button
if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    if st.button("🔍 Parse Statement", type="primary"):
        with st.spinner("Processing your statement..."):
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name
            
            try:
                # Parse the statement
                result = parse_statement(tmp_path, use_ocr=use_ocr)
                
                # Display results
                st.markdown("---")
                st.markdown("### 📊 Parsed Results")
                
                if "error" in result:
                    st.markdown(f"""
                        <div class="error-box">
                            <strong>❌ Error:</strong> {result['error']}<br>
                            <strong>Message:</strong> {result['message']}
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="success-box">
                            <strong>✅ Successfully parsed statement from {result.get('issuer', 'Unknown')}</strong>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display in two columns
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 👤 Personal Information")
                        st.markdown(f"**Card Holder:** {result.get('card_holder', 'Not found')}")
                        st.markdown(f"**Last 4 Digits:** {result.get('last_4_digits', 'Not found')}")
                        st.markdown(f"**Issuer:** {result.get('issuer', 'Not found')}")
                    
                    with col2:
                        st.markdown("#### 💰 Payment Information")
                        st.markdown(f"**Billing Cycle:** {result.get('billing_cycle', 'Not found')}")
                        st.markdown(f"**Payment Due Date:** {result.get('payment_due_date', 'Not found')}")
                        st.markdown(f"**Total Amount Due:** {result.get('total_amount_due', 'Not found')}")
                    
                    # JSON output
                    st.markdown("---")
                    st.markdown("#### 📋 JSON Output")
                    st.json(result)
                    
                    # Download button
                    json_str = json.dumps(result, indent=2, ensure_ascii=False)
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json_str,
                        file_name=f"parsed_statement_{uploaded_file.name.replace('.pdf', '')}.json",
                        mime="application/json"
                    )
                
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
            
            finally:
                # Clean up temporary file
                Path(tmp_path).unlink(missing_ok=True)


# Supported banks info
st.markdown("### 🏦 Supported Banks")
cols = st.columns(5)
banks = ["HDFC Bank", "ICICI Bank", "SBI Card", "Axis Bank", "American Express"]
for col, bank in zip(cols, banks):
    col.info(bank)

#st.markdown("---")


# Information section
st.markdown("---")
st.markdown("### ℹ️ Information")

with st.expander("📌 What data is extracted?"):
    st.markdown("""
    - **Card Holder Name**: Name of the credit card holder
    - **Last 4 Digits**: Last 4 digits of the card number
    - **Billing Cycle**: Statement period (from date - to date)
    - **Payment Due Date**: Date by which payment must be made
    - **Total Amount Due**: Total outstanding amount
    """)

with st.expander("🔒 Privacy & Security"):
    st.markdown("""
    - All processing is done locally on your machine
    - No data is sent to external servers
    - Uploaded files are temporarily stored and deleted after processing
    - Your financial information remains private and secure
    """)

with st.expander("❓ Troubleshooting"):
    st.markdown("""
    - **Bank not detected**: Make sure the PDF is from one of the supported banks
    - **Data not extracted**: Try enabling OCR if your PDF contains scanned images
    - **Partial data**: Some statements may have different formats; regex patterns may need adjustment
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #666;">Built with ❤️ using Python, pdfplumber, and Streamlit</div>',
    unsafe_allow_html=True
)
