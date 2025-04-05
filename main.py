import pandas as pd
from zipfile import ZipFile
import os
import re
import json
import sqlite3
from utils.extract_text import resume_to_text
from agents.cv_agent import extract_cv_info
from agents.qualification_agent import extract_jd_requirements
from agents.matching_agent import calculate_match_score
from agents.scheduler_agent import send_interview_invite

# Create database schema (delete the old database if it exists)
def create_db():
    # Delete existing database if it exists
    if os.path.exists('recruitment.db'):
        os.remove('recruitment.db')
        print("Existing database deleted.")

    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()

    # Create table for job descriptions
    cursor.execute('''CREATE TABLE IF NOT EXISTS job_descriptions (
                        id INTEGER PRIMARY KEY,
                        job_title TEXT,
                        job_description TEXT,
                        jd_summary TEXT)''')

    # Create table for candidate resumes
    cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        skills TEXT,
                        experience TEXT,
                        resume_path TEXT)''')

    # Create table for match scores
    cursor.execute('''CREATE TABLE IF NOT EXISTS match_scores (
                        id INTEGER PRIMARY KEY,
                        job_id INTEGER,
                        candidate_id INTEGER,
                        match_score REAL,
                        FOREIGN KEY(job_id) REFERENCES job_descriptions(id),
                        FOREIGN KEY(candidate_id) REFERENCES candidates(id))''')

    # Commit and close the database connection
    conn.commit()
    conn.close()
    print("Database created successfully.")

# Store job description and JD summary in SQLite
def store_job_description(job_title, job_description, jd_requirements):
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()
    jd_summary_json = json.dumps(jd_requirements)
    cursor.execute("INSERT INTO job_descriptions (job_title, job_description, jd_summary) VALUES (?, ?, ?)", 
                   (job_title, job_description, jd_summary_json))
    conn.commit()
    conn.close()
    print(f"Stored job description for '{job_title}' in the database.")

# Store candidate information in SQLite
def store_candidate(name, email, skills, experience, resume_path):
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO candidates (name, email, skills, experience, resume_path) VALUES (?, ?, ?, ?, ?)",
                   (name, email, skills, experience, resume_path))
    conn.commit()
    conn.close()
    print(f"Stored candidate '{name}' in the database.")

# Store match score in SQLite
def store_match_score(job_id, candidate_id, match_score):
    conn = sqlite3.connect('recruitment.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO match_scores (job_id, candidate_id, match_score) VALUES (?, ?, ?)",
                   (job_id, candidate_id, match_score))
    conn.commit()
    conn.close()
    print(f"Stored match score {match_score} for job ID {job_id} and candidate ID {candidate_id}.")

# Extract job descriptions from the CSV file
def load_job_descriptions(file_path):
    print(f"Loading job descriptions from {file_path}...")
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    print(f"Loaded {len(df)} job descriptions.")
    return df[['Job Title', 'Job Description']]

# Extract resumes from a zip file
def extract_resumes(zip_path, extract_dir="resumes"):
    print(f"Extracting resumes from {zip_path}...")
    os.makedirs(extract_dir, exist_ok=True)
    with ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    resumes = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]
    print(f"Extracted {len(resumes)} resumes.")
    return resumes

# Extract specific sections from the job description text
def extract_section(text, headers):
    for header in headers:
        pattern = rf"{header}(.*?)(?=\n[A-Z][a-z]+:|\Z)"  
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""

def process_jd_and_cv(jd_requirements, cv_info):
    jd_text = ''
    cv_text = ''

    # Process JD Requirements - Extract only values, discard the headings/keys
    if isinstance(jd_requirements, dict):
        for key, value in jd_requirements.items():
            if isinstance(value, list):
                jd_text += ' '.join(str(item) for item in value) + ' '  # Join list items into a string
            else:
                jd_text += str(value) + ' '  # Directly append the string
    
    # Process CV Information
    # Extract education details correctly
    if isinstance(cv_info.get("education"), list):
        for education_item in cv_info["education"]:
            # Assuming education_item is a dictionary, access 'degree' 
            degree = education_item.get("degree", "")
            # Append the extracted information to cv_text
            cv_text += f"{degree}"
    
    # Process other sections of CV (such as work experience, skills, etc.)
    if isinstance(cv_info.get("work_experience"), list):
        for work_item in cv_info["work_experience"]:
            position = work_item.get("position", "")
            cv_text += f"{position}"
    
    # Process skills section
    if isinstance(cv_info.get("skills"), list):
        cv_text += ' '.join(cv_info["skills"]) + ' '
    
    # Process certifications section
    if isinstance(cv_info.get("certifications"), list):
        for cert_item in cv_info["certifications"]:
            if isinstance(cert_item, dict):
                certification_name = cert_item.get("name", "")
            elif isinstance(cert_item, str):
                certification_name = cert_item
            else:
                certification_name = ""
            cv_text += f"{certification_name} "

    cv_text += ' '.join(cv_info["tech_stack"]) + ' '
    return jd_text, cv_text

# Main pipeline function
def run_pipeline():
    # Initialize database
    create_db()

    # Load job descriptions
    jd_data = load_job_descriptions("job_description.csv")
    resumes = extract_resumes("resumes.zip")
    # Store job descriptions in the database
    for _, row in jd_data.iterrows():
        job_title = row['Job Title']
        job_description = row['Job Description']
        
        # Extract specific sections from the JD text
        full_jd_text = job_description
        desc_section = extract_section(full_jd_text, ['Description:', 'Responsibilities:', 'Qualifications:'])
        
        # JD Agent: Get summary and requirements
        print(f"Extracting JD summary for '{job_title}'...")
        jd_requirements = extract_jd_requirements(desc_section)  # Extract JD requirements
        
        # Store the job description and JD summary in the database
        store_job_description(job_title, job_description, jd_requirements)

        for resume_path in resumes:
            print(f"Processing resume: {resume_path}")
            cv_text = resume_to_text(resume_path)
            if not cv_text.strip():
                continue

            # Extract candidate information
            cv_info = extract_cv_info(cv_text)  
            candidate_email = cv_info.get('email', None)
            
            if not candidate_email:
                print(f"No email found for resume {resume_path}. Skipping...")
                continue

            # Store candidate information in the database
            name = cv_info.get('name', 'Unknown')
            skills = ', '.join(cv_info.get('skills', []))
            experience = cv_info.get('experience', 'Unknown')
            store_candidate(name, candidate_email, skills, experience, resume_path)

            jd_text, cv_text = process_jd_and_cv(jd_requirements, cv_info)
            # Calculate match score
            print(f"Calculating match score for {resume_path}...")
            score = calculate_match_score(jd_text, cv_text)  # Compare JD requirements with CV
            print(f"Match Score for {resume_path}: {score}%")
            
            # Store match score in the database
            store_match_score(job_title, candidate_email, score)

            # Send interview invite if match score is above threshold
            if score >= 80:
                print(f"Sending interview invite to {candidate_email}...")
                send_interview_invite(name, candidate_email, job_title)  # Send interview invite using the candidate's email

if __name__ == "__main__":
    print("Starting the recruitment pipeline...")
    run_pipeline()
    print("Pipeline completed.")
