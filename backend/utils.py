from pdfminer.high_level import extract_text
from docx import Document
import os

def extract_text_from_file(file_path):
    if file_path.endswith('.pdf'):
        return extract_text(file_path)
    elif file_path.endswith('.docx'):
        doc = Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])
    elif file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ""
