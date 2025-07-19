# AI Resume Screener

This is a tool to match resumes with a job description using open-source language models and embeddings.

## What It Does

You upload a job description (in `.txt`) and one or more resumes (in `.pdf`).

The app reads the resumes, extracts the content, and uses an AI model to break it into fields like:
- Objective
- Skills
- Experience
- Education
- Projects

Then it compares those fields with the job description using embeddings. It gives a score showing how well each resume matches the job.

## How It Works

- Uses Together.ai's Mistral model to extract structured info from resumes
- Uses `sentence-transformers` to create embeddings
- Compares job and resume embeddings using cosine similarity
- Shows the results in a simple Streamlit app

## Files

- `app.py`: The Streamlit web app
- `match_resumes.py`: Logic to rank resumes
- `together_section_extractor.py`: Resume parsing using Together.ai

## Requirements

Install these:
```bash
pip install streamlit pdfplumber sentence-transformers scikit-learn python-dotenv
```

Also create a `.env` file with:
```
TOGETHER_API_KEY=your_actual_key
```

## How To Run

```bash
streamlit run app.py
```

## Notes

- Job description must be plain text
- Resumes must be in PDF format

## Possible Improvements

- Let users paste job description instead of uploading
- Add filters by skills, years, etc.
- Show visual comparisons
- Allow other LLMs (Hugging Face, Claude)
- Add login system for tracking uploads

## Status

It works. The AI extraction is good enough for basic matching. Not perfect, but useful.

## Author

Built by a data science student for learning and real use.
