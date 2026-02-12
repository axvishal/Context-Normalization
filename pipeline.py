import pandas as pd
import sys
from tqdm import tqdm

from services.cleaner import clean_text
from services.bhashini_translate import translate_en_to_hi
from services.pos_extractor import extract_keywords
from services.bedrock_llm import simplify_hindi


def get_row_range():
    """
    Allows:
        python pipeline.py 100 1100
    """
    if len(sys.argv) == 3:
        try:
            start = int(sys.argv[1])
            end = int(sys.argv[2])
            return start, end
        except ValueError:
            return None, None
    return None, None


def main():
    print("🚀 Pipeline started")

    start, end = get_row_range()

    df = pd.read_csv("data/input.csv")

    # Apply slicing if provided
    if start is not None and end is not None:
        df = df[start:end]
        print(f"⚡ Processing rows from {start} to {end}")

    df.columns = df.columns.str.strip().str.lower()

    if "sentence" in df.columns:
        text_col = "sentence"
    elif "grievance_text" in df.columns:
        text_col = "grievance_text"
    else:
        raise ValueError(
            f"No valid text column found. Columns: {df.columns.tolist()}"
        )

    texts = df[text_col].astype(str).str.strip()
    texts = texts[texts != ""]

    print(f"🧮 Total rows to process: {len(texts)}")

    results = []

    for sentence in tqdm(
        texts,
        desc="Processing sentences",
        unit="sentence",
        ncols=100
    ):
        try:
            clean_sentence = clean_text(sentence)

            hindi_original = translate_en_to_hi(clean_sentence)

            keywords = extract_keywords(clean_sentence)

            word_mappings = simplify_hindi(hindi_original, keywords)

            for item in word_mappings:
                results.append({
                    "english_word": item.get("english_word", ""),
                    "hindi_word": item.get("hindi_word", ""),
                    "simplified_hindi": item.get("simplified_hindi", "")
                })

        except Exception as e:
            results.append({
                "english_word": "",
                "hindi_word": "",
                "simplified_hindi": "",
                "error": str(e)
            })

    output_df = pd.DataFrame(results)
    output_df.to_csv("data/output.csv", index=False, encoding="utf-8")

    print("✅ Pipeline executed successfully")
    print("📄 Output saved to data/output.csv")


if __name__ == "__main__":
    main()
