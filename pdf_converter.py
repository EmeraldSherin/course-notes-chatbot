"""
PDF to Text Converter for Course Notes
======================================
Converts PDF files to text files for better chatbot processing.

Install: pip install pdfplumber
"""

import os
import pdfplumber
from pathlib import Path


def convert_pdf_to_text(pdf_path: str, output_dir: str = None):
    """
    Convert a single PDF to text file.
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Directory to save text file (default: same as PDF)
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            print(f"Converting: {pdf_path}")
            print(f"Total pages: {len(pdf.pages)}")
            
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    text += f"\n--- Page {i+1} ---\n"
                    text += page_text
                    
            # Determine output path
            if output_dir is None:
                output_dir = os.path.dirname(pdf_path)
            
            # Create output filename
            pdf_name = Path(pdf_path).stem
            output_path = os.path.join(output_dir, f"{pdf_name}.txt")
            
            # Save text file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            print(f"✅ Saved to: {output_path}")
            print(f"Total characters: {len(text)}\n")
            
            return output_path
            
    except Exception as e:
        print(f"❌ Error converting {pdf_path}: {e}")
        return None


def convert_all_pdfs_in_directory(directory: str, output_dir: str = None):
    """
    Convert all PDFs in a directory to text files.
    
    Args:
        directory: Directory containing PDFs
        output_dir: Directory to save text files (default: same directory)
    """
    if output_dir is None:
        output_dir = directory
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all PDF files
    pdf_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    
    print(f"Found {len(pdf_files)} PDF files\n")
    print("="*60)
    
    converted = 0
    failed = 0
    
    for pdf_path in pdf_files:
        result = convert_pdf_to_text(pdf_path, output_dir)
        if result:
            converted += 1
        else:
            failed += 1
    
    print("="*60)
    print(f"\n✅ Converted: {converted}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Text files saved to: {output_dir}")


def main():
    """Main function to run the converter."""
    
    # Configuration
    notes_directory = "course_notes"  # Change this to your directory
    
    print("PDF to Text Converter")
    print("="*60)
    print(f"Processing directory: {notes_directory}\n")
    
    if not os.path.exists(notes_directory):
        print(f"❌ Directory not found: {notes_directory}")
        print("Please create the directory and add your PDF files.")
        return
    
    # Convert all PDFs
    convert_all_pdfs_in_directory(notes_directory)
    
    print("\n✅ Conversion complete!")
    print("You can now run your chatbot with the text files.")


if __name__ == "__main__":
    main()