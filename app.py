import streamlit as st
import os
import shutil
from match_resumes import rank_resumes_from_text

st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("AI Resume Screener")

st.header("Paste Job Description and Upload Resumes")

# Get job description as text
job_text = st.text_area("Paste Job Description", height=200)

# Upload one or more resume files
resume_files = st.file_uploader("Upload Resumes (PDFs only)", type="pdf", accept_multiple_files=True)

if job_text.strip() and resume_files:
    os.makedirs("resumes", exist_ok=True)

    for file in resume_files:
        with open(os.path.join("resumes", file.name), "wb") as f:
            f.write(file.read())

    st.success("Files uploaded.")

    if st.button("Run Matcher"):
        with st.spinner("Matching resumes..."):
            ranked, extracted = rank_resumes_from_text("resumes", job_text)

        st.header("Results")
        for filename, score in ranked:
            st.subheader(f"{filename} — Score: {round(score, 4)}")
            resume_data = extracted.get(filename, {})

            st.markdown("**Objective:**")
            st.write(resume_data.get("objective", ""))

            st.markdown("**Skills:**")
            skills = resume_data.get("skills", [])
            st.write(", ".join(skills) if isinstance(skills, list) else skills)

            st.markdown("**Experience:**")
            st.write(resume_data.get("experience", ""))

            st.markdown("**Education:**")
            st.write(resume_data.get("education", ""))

            st.markdown("**Projects:**")
            st.write(resume_data.get("projects", ""))

    if st.button("Clear Files"):
        shutil.rmtree("resumes", ignore_errors=True)
        st.success("Files cleared.")
else:
    st.info("Paste a job description and upload at least one resume to continue.")