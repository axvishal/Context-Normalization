# Context Normalization Pipeline

An end-to-end NLP pipeline for cleaning English text, translating it to Hindi using the Bhashini API, extracting key linguistic features, and simplifying Hindi text using AWS Bedrock LLMs.

This project is designed for real-world datasets (e.g., grievance text, free-form sentences) and includes progress tracking, fault tolerance, and clean modular design.

---

## 🚀 Features

- CSV-based input processing
- Robust text cleaning & normalization
- English → Hindi translation via **Bhashini**
- Keyword extraction using **spaCy**
- Hindi simplification using **AWS Bedrock (Claude)**
- Automatic text column detection
- Progress bar with ETA (`tqdm`)
- Per-row error handling
- Clean, modular architecture

---

## 📁 Project Structure

Context Normalization/
│
├── data/
│ ├── input.csv # Input CSV file
│ ├── output.csv # Generated output
│
├── config/
│ └── settings.py # Environment variable loader
│
├── services/
│ ├── cleaner.py
│ ├── bhashini_translate.py
│ ├── pos_extractor.py
│ ├── bedrock_llm.py
│
├── pipeline.py # Main pipeline script
├── requirements.txt
├── README.md
├── .env # NOT committed (gitignored)
└── .gitignore


---

## 🧠 How the Pipeline Works

1. Reads text from a CSV file
2. Cleans and normalizes English sentences
3. Translates text from English to Hindi using Bhashini
4. Extracts linguistic keywords (nouns, verbs, adjectives, pronouns)
5. Identifies and replaces complex Hindi words using AWS Bedrock
6. Writes results to a CSV file

---

## 🔧 Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd Context-Normalization
2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3️⃣ Install Dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm
4️⃣ Configure Environment Variables
Create a .env file in the project root:

BHASHINI_API_KEY=your_bhashini_api_key
BHASHINI_USER_ID=your_bhashini_user_id
BHASHINI_API_URL=https://dhruva-api.bhashini.gov.in/services/inference/pipeline

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
⚠️ Never commit .env to GitHub

▶️ Running the Pipeline
python pipeline.py
Output will be saved to:

data/output.csv
🧪 Input Format
The input CSV must contain one text column, such as:

sentence
This is a sample sentence
or

grievance_text
Non receipt of pension since last year
The pipeline auto-detects the correct column.

📌 Notes
Python version: 3.11 (recommended)

spaCy is not compatible with Python 3.14+

AWS Bedrock permissions must allow bedrock:InvokeModel

📜 License
MIT License


---

# 🚫 `.gitignore` (IMPORTANT)

Create **`.gitignore`** in root:

```gitignore
# Virtual environment
venv/

# Environment variables
.env
.env.*

# Python cache
__pycache__/
*.pyc

# Data outputs
data/output.csv

# OS files
.DS_Store
