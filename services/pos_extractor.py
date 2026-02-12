import spacy

nlp = spacy.load("en_core_web_sm")

# Only meaningful parts of speech
ALLOWED_POS = {"NOUN", "ADJ", "ADV"}


def extract_keywords(sentence: str) -> list:
    doc = nlp(sentence)

    keywords = []

    for token in doc:
        if (
            token.pos_ in ALLOWED_POS
            and not token.is_stop
            and token.is_alpha
        ):
            keywords.append(token.lemma_.lower())

    return list(set(keywords))
