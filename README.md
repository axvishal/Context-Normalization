# Context Normalization Pipeline

> An intelligent NLP pipeline for multilingual text processing, combining translation, keyword extraction, and AI-powered text simplification.

An end-to-end solution for cleaning English text, translating it to Hindi using the **Bhashini API**, extracting linguistic features, and simplifying complex Hindi text using **AWS Bedrock LLMs** (Claude). Designed for real-world datasets including grievance text, feedback forms, and free-form user input.

---

## ✨ Features

- 📊 **CSV-based batch processing** - Handle thousands of rows efficiently
- 🧹 **Intelligent text cleaning** - Remove noise and normalize input
- 🌐 **English → Hindi translation** - Via Bhashini API (Government of India)
- 🔍 **Keyword extraction** - Extract meaningful nouns/adjectives/adverbs using spaCy NLP
- 🤖 **AI-powered simplification** - Simplify complex Hindi using AWS Bedrock Claude
- 🎯 **Auto-detection** - Automatically identifies text columns
- ⚡ **Progress tracking** - Real-time progress bar with ETA
- 🛡️ **Fault-tolerant** - Continues processing even if individual rows fail
- 🧩 **Modular design** - Clean separation of concerns, easily extensible

---

## 📁 Project Structure

```
Context Normalization/
├── data/
│   ├── input.csv              # Input dataset
│   └── output.csv             # Processed results
│
├── config/
│   └── settings.py            # Environment variable configuration
│
├── services/
│   ├── cleaner.py             # Text cleaning & normalization
│   ├── bhashini_translate.py  # Bhashini API integration
│   ├── pos_extractor.py       # spaCy-based keyword extraction
│   └── bedrock_llm.py         # AWS Bedrock LLM interface
│
├── pipeline.py                # Main orchestration script
├── test_env.py                # Environment validation script
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (NOT committed)
├── .gitignore
└── README.md
```

---

## 🔄 Pipeline Workflow

```
Input CSV → Clean Text → Translate (EN→HI) → Extract Keywords → Simplify Hindi → Output CSV
     ↓           ↓              ↓                  ↓                  ↓            ↓
  Raw Data   Normalized    Bhashini API      spaCy NLP         AWS Bedrock   Results
```

### Step-by-Step Process

1. **Load & Validate** - Read CSV and detect text column (`sentence` or `grievance_text`)
2. **Clean Text** - Remove special characters, normalize whitespace
3. **Translate** - Convert English text to Hindi using Bhashini API
4. **Extract Keywords** - Identify nouns, adjectives, and adverbs using spaCy
5. **Simplify** - Use AWS Bedrock Claude to map complex Hindi words to simpler alternatives
6. **Export** - Save word-level mappings to CSV

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Active internet connection (for API calls)
- **Bhashini API credentials** ([Get here](https://bhashini.gov.in/))
- **AWS Account** with Bedrock access ([Setup guide](https://aws.amazon.com/bedrock/))

### Installation

**1️⃣ Clone the Repository**

```bash
git clone <your-repo-url>
cd "Context Normalization"
```

**2️⃣ Create Virtual Environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

**3️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**4️⃣ Configure Environment Variables**

Create a `.env` file in the project root:

```env
# Bhashini API Configuration
BHASHINI_API_KEY=your_bhashini_api_key_here
BHASHINI_USER_ID=your_bhashini_user_id_here
BHASHINI_API_URL=https://dhruva-api.bhashini.gov.in/services/inference/pipeline

# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION=ap-south-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

⚠️ **Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

**5️⃣ Verify Setup**

```bash
python test_env.py
```

This validates all environment variables are correctly configured.

---

## 💻 Usage

### Running the Pipeline

```bash
python pipeline.py
```

### Input Format

Place your CSV file at `data/input.csv` with one of these column names:

**Option 1:** Column named `sentence`
```csv
sentence
This is a sample English sentence
Another example text for processing
```

**Option 2:** Column named `grievance_text`
```csv
grievance_text
Non receipt of pension since last year
Street light not working in our locality
```

The pipeline automatically detects the correct column.

### Output

Results are saved to `data/output.csv` with the following structure:

```csv
english_word,hindi_word,simplified_hindi,error
"extremely","अत्यधिक","बहुत",
```

**Columns:**
- `english_word` - Keyword extracted from English
- `hindi_word` - Matching word from the Hindi translation
- `simplified_hindi` - Simplified Hindi substitute
- `error` - Error message (if processing failed for that row)

Each row represents a word-level mapping, not a full sentence rewrite.

---

## 🧩 Module Documentation

### `services/cleaner.py`
Removes special characters, normalizes whitespace, and prepares text for processing.

### `services/bhashini_translate.py`
Integrates with Bhashini API for English to Hindi translation. Government-approved translation service.

### `services/pos_extractor.py`
Uses spaCy's English model to extract keywords (nouns, adjectives, adverbs) for context-aware simplification.

### `services/bedrock_llm.py`
Interfaces with AWS Bedrock (Claude) to simplify complex Hindi text while preserving meaning.

---

## 🛠️ Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Solution: Ensure virtual environment is activated and dependencies installed
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**2. Bhashini API Errors**
- Verify your API key and user ID in `.env`
- Check internet connection
- Confirm API URL is correct

**3. AWS Bedrock Access Denied**
- Ensure your AWS account has Bedrock enabled in your region
- Verify IAM permissions include `bedrock:InvokeModel`
- Check if the model ID is correct for your region

**4. Column Not Found Error**
```
ValueError: No valid text column found
```
- Ensure your CSV has either `sentence` or `grievance_text` column
- Check for typos or extra spaces in column names

**5. Empty Output**
```
ValueError: No valid text rows found after cleaning input CSV
```
- Verify `data/input.csv` contains actual text data
- Check that rows aren't all empty or whitespace

---

## 📊 Performance

- **Speed:** ~2-5 seconds per sentence (depends on API response times)
- **Batch Processing:** Handles 1000+ rows with progress tracking
- **Memory:** Minimal footprint (~100MB for typical datasets)
- **Error Handling:** Failed rows don't stop the pipeline

---

## 🔐 API Requirements

### Bhashini API
- Free for government and research use
- Register at [bhashini.gov.in](https://bhashini.gov.in/)
- Supports 22+ Indian languages

### AWS Bedrock
- Pay-per-use pricing
- Requires AWS account with Bedrock access
- Claude 3 Sonnet recommended for quality/cost balance

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review API documentation for Bhashini and AWS Bedrock

---

## 🙏 Acknowledgments

- **Bhashini** - Ministry of Electronics & IT, Government of India
- **AWS Bedrock** - For providing Claude LLM access
- **spaCy** - For powerful NLP capabilities

---

**Built with ❤️ for multilingual NLP**

📌 Notes
Python version: 3.11 (recommended)

spaCy is not compatible with Python 3.14+

AWS Bedrock permissions must allow bedrock:InvokeModel

📜 License
MIT License


---

## ⚠️ Large files & Git LFS

The repository currently contains a large CSV (`data/input.csv`) which is over GitHub's recommended size limit (50 MB). Large files in the Git history can cause push and clone issues. Recommended options:

- Move large data files out of the repository and add them to `.gitignore`.
- Use Git LFS to store large files instead of keeping them in the main Git history.

If you want to track `data/input.csv` with Git LFS, run:

```bash
git lfs install
git lfs track "data/input.csv"
git add .gitattributes
git add data/input.csv
git commit -m "Move data/input.csv to Git LFS"
git push origin main
```

If the large file is already committed and you want to remove it from history, consider using `git filter-repo` or the `bfg-repo-cleaner` to rewrite history and remove the blob. Rewriting history requires coordination with collaborators and a force-push:

```bash
# Example outline (use with caution)
git clone --mirror <repo-url>
cd <repo-name>.git
git filter-repo --path data/input.csv --invert-paths
git push --force
```

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
