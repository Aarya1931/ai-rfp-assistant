from docx import Document
from PyPDF2 import PdfReader

def read_docx(path):
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
