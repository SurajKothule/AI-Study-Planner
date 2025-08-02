import os
import docx
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import cohere
from flask import jsonify

# Load environment variables
load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def extract_text_from_resume(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".docx":
        doc = docx.Document(filepath)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == ".pdf":
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text.strip()
    else:
        raise ValueError("Only .txt, .docx, and .pdf files are supported")


def generate_interview_questions(resume_text):
    import cohere
    import os

    co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def call(prompt):
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=3000,
            temperature=0.7
        )
        return response.generations[0].text.strip()

    # Step 1: Q1–Q15
    first_prompt = f"""
You are an interviewer reviewing this resume:

\"\"\"{resume_text}\"\"\"

Generate Q1 to Q15 realistic interview questions with answers in the format:

Q1: [question]  
A: [answer]  
...
Q15:  
A:
"""
    first_part = call(first_prompt)

    # Step 2: Q16–Q25
    second_prompt = f"""
Here is the same resume:

\"\"\"{resume_text}\"\"\"

Now generate Q16 to Q25 interview questions with answers in the same format.
"""
    second_part = call(second_prompt)

    combined = first_part + "\n" + second_part

    # --- Parse combined into JSON array ---
    lines = combined.strip().split("\n")
    qa_pairs = []
    current_qa = {}

    for line in lines:
        if line.startswith("Q"):
            if current_qa:
                qa_pairs.append(current_qa)
            current_qa = {"question": line.partition(":")[2].strip(), "answer": ""}
        elif line.startswith("A:"):
            current_qa["answer"] = line[2:].strip()
        elif current_qa:
            current_qa["answer"] += " " + line.strip()

    if current_qa:
        qa_pairs.append(current_qa)

    return qa_pairs
