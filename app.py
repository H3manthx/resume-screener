import streamlit as st
import pdfplumber
from sentence_transformers import SentenceTransformer, util
import tempfile
import os

# --- Load model ---
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# --- Helper: Extract text from PDF ---
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# --- UI ---
st.title("📄 AI Resume Screener")
st.markdown("Paste a job description and upload resumes to rank candidates.")

job_desc = st.text_area("📝 Job Description", height=200)

uploaded_files = st.file_uploader("📤 Upload Resumes (PDF only)", type=["pdf"], accept_multiple_files=True)

if st.button("🔍 Match Resumes"):
    if not job_desc or not uploaded_files:
        st.warning("Please provide both a job description and at least one resume.")
    else:
        with st.spinner("Analyzing..."):
            job_embedding = model.encode(job_desc, convert_to_tensor=True)
            results = []

            for file in uploaded_files:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name

                try:
                    resume_text = extract_text_from_pdf(tmp_path)
                    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
                    score = util.pytorch_cos_sim(job_embedding, resume_embedding).item()
                    results.append((file.name, score))
                except Exception as e:
                    st.error(f"Error processing {file.name}: {e}")
                finally:
                    os.remove(tmp_path)

            results.sort(key=lambda x: x[1], reverse=True)

        # --- Show results ---
        st.subheader("📊 Resume Match Results")
        for rank, (name, score) in enumerate(results, 1):
            st.write(f"{rank}. **{name}** — Match Score: `{score:.4f}`")