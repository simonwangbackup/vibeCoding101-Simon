#!/usr/bin/env python3
"""
PDF to Markdown Converter
Converts PDF files to clean markdown format
"""

import PyPDF2
import re
import os

def clean_text(text):
    """
    Clean extracted PDF text for better markdown formatting
    """
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common PDF extraction issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Add space between camelCase
    text = re.sub(r'(\.)([A-Z])', r'\1 \2', text)     # Add space after periods
    text = re.sub(r'([a-z])(\d)', r'\1 \2', text)     # Add space between letters and numbers
    
    # Remove page numbers and headers/footers (common patterns)
    text = re.sub(r'\b\d+\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\s*', '', text, flags=re.MULTILINE)
    
    return text.strip()

def format_as_markdown(text):
    """
    Convert cleaned text to markdown format
    """
    lines = text.split('\n')
    markdown_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Detect potential headings (lines that are short and start with capital letters)
        if len(line) < 100 and line[0].isupper() and not line.endswith('.'):
            # Check if it looks like a heading
            words = line.split()
            if len(words) <= 10 and all(word[0].isupper() or word.lower() in ['and', 'or', 'of', 'in', 'on', 'at', 'to', 'for', 'with'] for word in words):
                markdown_lines.append(f"\n## {line}\n")
                continue
        
        # Regular paragraph text
        markdown_lines.append(line)
    
    return '\n'.join(markdown_lines)

def convert_pdf_to_markdown(input_pdf, output_md):
    """
    Convert PDF file to markdown format
    """
    try:
        print(f"🔄 Processing PDF: {input_pdf}")
        
        # Check if input file exists
        if not os.path.exists(input_pdf):
            print(f"❌ Error: Input file {input_pdf} not found!")
            return False
        
        # Open and read PDF
        with open(input_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            print(f"📄 PDF has {len(pdf_reader.pages)} pages")
            
            # Extract text from all pages
            full_text = ""
            for page_num, page in enumerate(pdf_reader.pages, 1):
                print(f"📖 Processing page {page_num}...")
                page_text = page.extract_text()
                full_text += page_text + "\n"
        
        # Clean and format the text
        print("🧹 Cleaning extracted text...")
        cleaned_text = clean_text(full_text)
        
        print("📝 Converting to markdown format...")
        markdown_text = format_as_markdown(cleaned_text)
        
        # Add markdown header
        markdown_content = f"""# Converted Article

*Converted from PDF: {os.path.basename(input_pdf)}*

---

{markdown_text}

---

*End of converted content*
"""
        
        # Save to output file
        with open(output_md, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)
        
        print(f"✅ Successfully converted PDF to markdown!")
        print(f"📁 Input: {input_pdf}")
        print(f"📁 Output: {output_md}")
        print(f"📊 Extracted {len(cleaned_text)} characters")
        print(f"📝 Preview (first 300 chars):")
        print("-" * 50)
        print(markdown_content[:300] + "...")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return False

def main():
    """
    Main function to run the PDF conversion
    """
    # File paths
    input_pdf = "/workspaces/vibeCoding101-Simon/GCAP3056/AgentProcessPDF/article.pdf"
    output_md = "/workspaces/vibeCoding101-Simon/GCAP3056/AgentProcessPDF/converted_article.md"
    
    print("🚀 Starting PDF to Markdown conversion...")
    print("=" * 60)
    
    success = convert_pdf_to_markdown(input_pdf, output_md)
    
    if success:
        print("=" * 60)
        print("🎉 Conversion completed successfully!")
    else:
        print("=" * 60)
        print("💥 Conversion failed!")

if __name__ == "__main__":
    main()
