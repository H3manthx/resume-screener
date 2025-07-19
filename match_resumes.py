from sentence_transformers import SentenceTransformer, util
import os
import pdfplumber

# --- Step 1: Load model ---
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- Step 2: Load job description ---
job_description = """
We are looking for a Data Scientist with strong Python skills, experience in machine learning, and familiarity with data analysis libraries like pandas and scikit-learn. Experience with SQL and data visualization tools is a plus.
"""

job_embedding = model.encode(job_description, convert_to_tensor=True)

# --- Step 3: Load and encode resumes ---
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def embed_resumes(resume_folder):
    scores = []
    for filename in os.listdir(resume_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(resume_folder, filename)
            text = extract_text_from_pdf(path)
            embedding = model.encode(text, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(job_embedding, embedding).item()
            scores.append((filename, similarity))
    return sorted(scores, key=lambda x: x[1], reverse=True)

# --- Step 4: Run and display rankings ---
if __name__ == "__main__":
    results = embed_resumes("resumes")
    print("\n📊 Resume Match Ranking:\n")
    for i, (name, score) in enumerate(results, 1):
        print(f"{i}. {name} — Score: {score:.4f}")