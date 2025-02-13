import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from.env

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "database/market_analysis.db")

# Email Configuration
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Report Directories
REPORT_DIR_TXT = os.getenv("REPORT_DIR_TXT", "reports/text")
REPORT_DIR_GDOC = os.getenv("REPORT_DIR_GDOC", "reports/gdoc")

# Ensure directories exist
os.makedirs(REPORT_DIR_TXT, exist_ok=True)
os.makedirs(REPORT_DIR_GDOC, exist_ok=True)
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Social Media API Keys (Illustrative)
X_API_KEY = os.getenv("X_API_KEY")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")
FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
TIKTOK_API_KEY = os.getenv("TIKTOK_API_KEY")

# Ollama API URL
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

# Removed OpenAI API Key check
if not EMAIL_SENDER or not EMAIL_RECEIVER or not SMTP_SERVER or not SMTP_PORT or not SMTP_PASSWORD:
    print("Email settings are not fully configured. Email notifications will be disabled.")