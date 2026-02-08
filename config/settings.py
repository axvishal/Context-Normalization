import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# BHASHINI
# ===============================
BHASHINI_API_KEY = os.getenv("BHASHINI_API_KEY")
BHASHINI_USER_ID = os.getenv("BHASHINI_USER_ID")
BHASHINI_API_URL = os.getenv("BHASHINI_API_URL")

# ===============================
# AWS BEDROCK
# ===============================
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID")
