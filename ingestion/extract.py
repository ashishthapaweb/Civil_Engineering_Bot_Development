import re
from pathlib import Path
import pymupdf.layout #important before importing pymupdf4llm
import pymupdf
import pymupdf4llm
# Local modules
from ingestion.clean import clean_markdown

def extract_and_clean_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF using PyMuPDF and return the clean markdown string.
    
    Parameters:
   ----------
    pdf_path: str
        Path to the PDF file.
        
    Returns:
   -------
    str
        Clean markdown extracted from the PDF.
    """
    
    pdf_path = Path(pdf_path)
    out_path = pdf_path.with_suffix(".md")
    
    if out_path.exists():
        return out_path.read_text(encoding="utf-8")
    
    doc = pymupdf.open(pdf_path)
    print(f"Document with pages {doc.page_count} loaded.")
    
    md = pymupdf4llm.to_markdown(doc, pages=None, embed_images=False, ignore_images=True, ignore_graphics=True, header=False, footer=False, show_progress=True)
    
    # Clean markdown
    md_clean = clean_markdown(md)

    suffix = ".md"
    out_path.write_bytes(md_clean.encode())
    
    return md_clean