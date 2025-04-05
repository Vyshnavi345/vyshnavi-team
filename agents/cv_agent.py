import ollama
import json

def extract_cv_info(resume_text, model_name="mistral"):
    prompt = f"""
You are an AI Resume Parser.

Extract and return the following information in JSON format only, using short and structured values:

- "name": Full name
- "email": Email address
- "phone": Phone number
- "education": List of degrees with field of study and institution
- "work_experience": Job titles, companies, and duration
- "skills": Key soft and technical skills (e.g., leadership, problem-solving)
- "tech_stack": List of tools, frameworks, libraries, programming languages
- "certifications": Certifications with names
- "achievements": Key achievements, awards, or recognitions

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    try:
        response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
        result_text = response["message"]["content"]
        parsed = json.loads(result_text)
        return parsed

    except Exception as e:
        print("Error during resume extraction:", e)
        return {}
