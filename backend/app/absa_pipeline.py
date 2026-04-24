from transformers import AutoTokenizer, AutoModelForTokenClassification, AutoModelForSequenceClassification
import torch

# =========================
# LOAD MODELS
# =========================
ate_tokenizer = AutoTokenizer.from_pretrained("app/ate_model")
ate_model = AutoModelForTokenClassification.from_pretrained("app/ate_model")

asc_tokenizer = AutoTokenizer.from_pretrained("app/asc_model")
asc_model = AutoModelForSequenceClassification.from_pretrained("app/asc_model")

id2label_ate = {0: "O", 1: "B-ASP", 2: "I-ASP"}
id2label_asc = {0: "negative", 1: "neutral", 2: "positive"}


# =========================
# EXTRACT ASPECTS (ATE)
# =========================
def extract_aspects(text):
    inputs = ate_tokenizer(text, return_tensors="pt", truncation=True)
    outputs = ate_model(**inputs)

    preds = torch.argmax(outputs.logits, dim=2)[0].tolist()
    tokens = ate_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

    aspects = []
    current = []

    for token, label_id in zip(tokens, preds):
        label = id2label_ate[label_id]

        if label == "B-ASP":
            if current:
                aspects.append(" ".join(current))
                current = []
            current.append(token)

        elif label == "I-ASP":
            current.append(token)

        else:
            if current:
                aspects.append(" ".join(current))
                current = []

    if current:
        aspects.append(" ".join(current))

    # clean tokens
    aspects = [a.replace("##", "") for a in aspects]

    return list(set(aspects))


# =========================
# CLASSIFY SENTIMENT (ASC)
# =========================
def classify_aspect(text, aspect):
    combined = f"{text} [SEP] {aspect}"

    inputs = asc_tokenizer(combined, return_tensors="pt", truncation=True)
    outputs = asc_model(**inputs)

    probs = torch.softmax(outputs.logits, dim=1)[0]
    pred = torch.argmax(probs).item()

    return {
        "term": aspect,
        "sentiment": id2label_asc[pred],
        "confidence": round(probs[pred].item(), 3)
    }


# =========================
# FULL PIPELINE
# =========================
def analyze_text(text):
    aspects = extract_aspects(text)

    results = []
    for asp in aspects:
        results.append(classify_aspect(text, asp))

    return results