import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from together_section_extractor import extract_resume_text, query_together, PROMPT_TEMPLATE

load_dotenv()
model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert a resume to an embedding vector using parsed skills and experience
def get_resume_embedding(resume_path):
    try:
        text = extract_resume_text(resume_path)
        prompt = PROMPT_TEMPLATE.format(resume_text=text[:3000])
        parsed = query_together(prompt)

        combined = f"Skills: {'; '.join(parsed['skills']) if isinstance(parsed['skills'], list) else parsed['skills']}\n"
        combined += f"Experience: {parsed['experience']}"

        return model.encode(combined, convert_to_tensor=True), parsed
    except Exception as e:
        print(f"Error processing {resume_path}: {e}")
        return None, {}

# Compare resumes with job description from a .txt file
def rank_resumes(resume_folder, job_description_path):
    with open(job_description_path, "r", encoding="utf-8") as f:
        job_text = f.read()

    return rank_resumes_from_text(resume_folder, job_text)

# Compare resumes with job description directly from pasted text
def rank_resumes_from_text(resume_folder, job_description_text):
    job_embedding = model.encode(job_description_text, convert_to_tensor=True)
    scores = []
    parsed_outputs = {}

    for filename in tqdm(os.listdir(resume_folder)):
        if not filename.lower().endswith(".pdf"):
            continue

        path = os.path.join(resume_folder, filename)
        emb, parsed = get_resume_embedding(path)
        if emb is None:
            continue

        similarity = util.cos_sim(job_embedding, emb).item()
        scores.append((filename, similarity))
        parsed_outputs[filename] = parsed

    ranked = sorted(scores, key=lambda x: x[1], reverse=True)

    print("\nResume Ranking:")
    for file, score in ranked:
        print(f"{file} — Score: {round(score, 4)}")

    return ranked, parsed_outputs

if __name__ == "__main__":
    resumes_folder = "resumes"
    jd_path = "job_description.txt"
    ranked, extracted = rank_resumes(resumes_folder, jd_path)

    with open("ranked_results.json", "w") as f:
        json.dump({"ranked": ranked, "parsed_resumes": extracted}, f, indent=2)
