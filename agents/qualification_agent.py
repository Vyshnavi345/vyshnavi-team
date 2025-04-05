import ollama
import json

def extract_jd_requirements(qualifications_text, model_name="mistral"):
    prompt = f"""
You are an AI Job Qualifications Extractor.

Your task is to read the provided text and extract the most **specific and relevant qualifications** in JSON format. Focus only on important keywords such as degrees, skills, tools, and technologies.

🔍 When the text mentions:
- A **degree** (e.g., "Bachelor’s degree", "Master’s in a related field"), expand "related field" into common technical domains:
  - Include related fields such as ["Computer Science", "Software Engineering", "Information Technology", "Cybersecurity", "Data Science"].
  - For example: "Bachelor’s in Computer Science or related field" → include ["Bachelor’s", "Computer Science", "Software Engineering", "Information Technology"]

📦 Extract and return a JSON object with the following keys:

- "required_degrees": List of degree(s) and expanded related fields.  
- "required_skills": Technical and soft skills (e.g., ["problem-solving", "communication", "attention to detail"]).  
- "required_languages": Programming languages only (e.g., ["Python", "Java", "C++"]).  
- "required_cloud_platforms": Cloud services mentioned (e.g., ["AWS", "Azure", "GCP"]).  
- "required_tools_technologies": Technologies, frameworks, databases, etc. (e.g., ["Docker", "React", "MySQL"]).  
- "required_experience": If experience is mentioned, extract it as-is (e.g., "3+ years", "entry-level").

Return output as clean, properly formatted **JSON only**, with no explanations or additional text.

Text:
\"\"\"
{qualifications_text}
\"\"\"
"""
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    try:
        return json.loads(response["message"]["content"])
    except Exception as e:
        print("Error extracting JD qualifications:", e)
        return {}
