import spacy

nlp = spacy.load("en_core_web_sm")

def extract_keywords(sentence: str) -> list:
    doc = nlp(sentence)

    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "VERB", "ADJ", "PRON"]:
            keywords.append(token.lemma_.lower())

    return list(set(keywords))
