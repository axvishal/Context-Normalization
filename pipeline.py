import pandas as pd
from tqdm import tqdm

from services.cleaner import clean_text
from services.bhashini_translate import translate_en_to_hi
from services.pos_extractor import extract_keywords
from services.bedrock_llm import simplify_hindi


def main():
    print("🚀 Pipeline started")

    # =========================
    # Load input CSV
    # =========================
    df = pd.read_csv("data/input.csv")

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Detect text column automatically
    if "sentence" in df.columns:
        text_col = "sentence"
    elif "grievance_text" in df.columns:
        text_col = "grievance_text"
    else:
        raise ValueError(
            f"No valid text column found. Available columns: {df.columns.tolist()}"
        )

    # =========================
    # Clean & validate text rows
    # =========================
    texts = df[text_col].astype(str).str.strip()
    texts = texts[texts != ""]

    print(f"🧾 Using column: {text_col}")
    print(f"🧮 Total rows found: {len(texts)}")

    if texts.empty:
        raise ValueError("No valid text rows found after cleaning input CSV.")

    results = []

    # =========================
    # Main Processing Loop
    # =========================
    for sentence in tqdm(
        texts,
        desc="Processing sentences",
        unit="sentence",
        ncols=100
    ):
        try:
            # Step 1: Clean text
            clean_sentence = clean_text(sentence)

            # Step 2: English → Hindi (Bhashini)
            hindi_original = translate_en_to_hi(clean_sentence)

            # Step 3: Keyword extraction (spaCy)
            keywords = extract_keywords(clean_sentence)

            # Step 4: Simplify Hindi (AWS Bedrock)
            hindi_simplified = simplify_hindi(hindi_original, keywords)

            results.append({
                "english": clean_sentence,
                "hindi_original": hindi_original,
                "hindi_simplified": hindi_simplified
            })

        except Exception as e:
            # Fail-safe: continue even if one row fails
            results.append({
                "english": sentence,
                "hindi_original": "",
                "hindi_simplified": "",
                "error": str(e)
            })

    # =========================
    # Save Output
    # =========================
    output_df = pd.DataFrame(results)
    output_df.to_csv("data/output.csv", index=False, encoding="utf-8")

    print("✅ Pipeline executed successfully")
    print("📄 Output saved to: data/output.csv")


if __name__ == "__main__":
    main()
