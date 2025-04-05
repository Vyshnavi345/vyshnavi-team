import ollama

def summarize_jd(description_text, model_name="mistral"):
    prompt = f"Summarize the following job description in bullet points:\n\n{description_text}"
    response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]
