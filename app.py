import streamlit as st
import os
import shutil
from match_resumes import rank_resumes_from_text

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("📄 AI Resume Screener with Together.ai")

# === Upload Section ===
st.header("Paste Job Description & Upload Resumes")
job_text = st.text_area("📌 Paste Job Description Here", height=200)
resume_files = st.file_uploader("📎 Upload Resumes (PDFs only)", type="pdf", accept_multiple_files=True)

if job_text.strip() and resume_files:
    os.makedirs("resumes", exist_ok=True)

    for file in resume_files:
        with open(os.path.join("resumes", file.name), "wb") as f:
            f.write(file.read())

    st.success("✅ Files uploaded successfully.")

    if st.button("🚀 Run Resume Matcher"):
        with st.spinner("Processing resumes with Together.ai..."):
            ranked, extracted = rank_resumes_from_text("resumes", job_text)

        st.header("📊 Match Results")
        for filename, score in ranked:
            st.subheader(f"📄 {filename} — Score: {round(score, 4)}")
            resume_data = extracted.get(filename, {})
            st.markdown("**🎯 Objective:**")
            st.write(resume_data.get("objective", ""))

            st.markdown("**🛠 Skills:**")
            skills = resume_data.get("skills", [])
            st.write(", ".join(skills) if isinstance(skills, list) else skills)

            st.markdown("**💼 Experience:**")
            st.write(resume_data.get("experience", ""))

            st.markdown("**🎓 Education:**")
            st.write(resume_data.get("education", ""))

            st.markdown("**📂 Projects:**")
            st.write(resume_data.get("projects", ""))

    # Optional cleanup UI
    if st.button("🧹 Clear Uploaded Files"):
        shutil.rmtree("resumes", ignore_errors=True)
        st.success("Cleaned up uploaded resumes.")
else:
    st.info("Paste a job description and upload one or more resumes to begin.")