import fitz  # PyMuPDF
from docx import Document

def resume_to_text(path):
    if path.endswith(".pdf"):
        doc = fitz.open(path)
        return " ".join([page.get_text() for page in doc])
    elif path.endswith(".docx"):
        doc = Document(path)
        return " ".join([p.text for p in doc.paragraphs])
    elif path.endswith(".txt"):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""
