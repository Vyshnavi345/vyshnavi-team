# 🧠 AutoRecruit: Intelligent Resume-to-Interview Pipeline

**⚠️ IMPORTANT: Enter the sender email and sender app password in `scheduler_agent.py` for the system to send emails properly.**

This project is a multi-agent, AI-driven recruitment automation system designed to streamline candidate evaluation, job matching, and scheduling — all while ensuring **data privacy with on-premise technologies**.

---

## 🚀 Overview

The system automates and optimizes the hiring process using four intelligent agents:

- **Qualification Agent**: Extracts job requirements from descriptions and structures them for comparison.
- **CV Agent**: Processes candidate resumes and generates structured profiles.
- **Matching Agent**: Calculates a semantic match score between job descriptions and resumes.
- **Scheduler Agent**: Sends interview invites to top-matched candidates securely via email.

---

## 🧩 Project Structure

| File/Folder                | Description                                                                 |
|----------------------------|-----------------------------------------------------------------------------|
| `agents/cv_agent.py`       | Extracts and structures candidate CV data.                                 |
| `agents/matching_agent.py` | Compares candidate profiles with job requirements using TF-IDF and cosine similarity. |
| `agents/qualification_agent.py` | Parses job descriptions to extract structured job requirements.         |
| `agents/scheduler_agent.py` | Sends personalized interview invitations via SMTP.                        |
| `utils/extract_text.py`   | Utility for extracting text from resumes or job descriptions.              |
| `checking_the_data.py`    | Used for checking the recruitment.db                  |
| `job_description.csv`     | CSV file containing job role information.                                  |
| `main.py`                 | Main script to run the full recruitment pipeline.                          |
| `recruitment.db`          | SQLite database to store processed job and candidate data.                 |
| `requirements.txt`        | List of Python dependencies for the project.                               |
| `resumes.zip`             | A zipped folder containing resumes to be parsed.                           |
| `README.md`               | You're reading it! 📖                                                       |

---

## 🛠️ Technologies Used

- **Python**
- **Ollama** (for LLM-based extraction)
- **TF-IDF + Cosine Similarity** (for matching)
- **SQLite** (lightweight DB for local storage)
- **SMTP (smtplib)** (for sending emails)

---

## 📦 Installation & Run

Follow these steps to set up and run the project on your machine:

```bash
# 1. Clone the repository
git clone https://github.com/Vyshnavi345/vyshnavi-team.git
cd vyshnavi-team

# 2. Install required Python packages
pip install -r requirements.txt

# 3. Edit the scheduler agent to enable email sending
# Open agents/scheduler_agent.py and update:
# sender_email = "youremail@example.com"
# sender_password = "your-app-password"

# 4. Run the full recruitment pipeline
python main.py
