import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def read_all_resumes(folder_path):
    resume_texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            full_path = os.path.join(folder_path, filename)
            text = extract_text_from_pdf(full_path)
            resume_texts[filename] = text
    return resume_texts

if __name__ == "__main__":
    folder = "resumes"
    resumes = read_all_resumes(folder)
    for name, text in resumes.items():
        print(f"\n--- {name} ---\n{text[:1000]}...\n")