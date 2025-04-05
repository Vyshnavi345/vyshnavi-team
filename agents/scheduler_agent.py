import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_interview_invite(candidate_name, candidate_email, job_title):
    subject = "Interview Invitation"
    body = f"""
    Dear {candidate_name},

    Congratulations! We are pleased to inform you that you have been shortlisted for an interview for the {job_title} position you applied for.

    Please let us know your availability for the interview, and we will schedule it at a convenient time.

    Looking forward to your response.

    Best regards,
    Interview Scheduler Team
    """
    sender_email = "" # Enter the sender email
    sender_password = "" # Enter the sender app password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = candidate_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, candidate_email, msg.as_string())
        print(f"Interview invite sent to: {candidate_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

