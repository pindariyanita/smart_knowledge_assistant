import PyPDF2

def parse_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    """
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text
