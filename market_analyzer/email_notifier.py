# market_analyzer/email_notifier.py
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from market_analyzer import config

def send_weekly_report_email(report_files):
    """ Sends an email with attached reports. """
    sender_email = config.EMAIL_SENDER
    receiver_email = config.EMAIL_RECEIVER
    smtp_server = config.SMTP_SERVER
    smtp_port = config.SMTP_PORT
    smtp_password = config.SMTP_PASSWORD # Secure password handling is crucial in production

    if not sender_email or not receiver_email or not smtp_server or not smtp_port or not smtp_password:
        print("Email configuration is incomplete. Skipping email notification.")
        return False

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = "Weekly Market Analysis Reports"

    body = "Please find attached the weekly market analysis reports."
    message.attach(MIMEText(body, 'plain'))

    for file_path in report_files:
        filename = file_path.split('/')[-1] # Extract filename from path
        attachment = open(file_path, "rb")
        part = MIMEBase('application', "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {filename}")
        message.attach(part)
        attachment.close()

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() # Upgrade connection to secure
        server.login(sender_email, smtp_password)
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email notification sent successfully.")
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

if __name__ == '__main__':
    # Example Usage (assuming you have report files generated):
    example_report_files = ["reports/text/Competitor A Website_last_7_days_20231220.txt", "reports/text/Global_Market_Tendencies_monthly_trends_20231220.txt"] # Replace with actual file paths
    if example_report_files:
        send_weekly_report_email(example_report_files)
    else:
        print("No report files to send via email in this example.")