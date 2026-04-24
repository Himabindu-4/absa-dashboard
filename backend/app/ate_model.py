from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch

model_path = "app/ate_trained_model"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForTokenClassification.from_pretrained(model_path)

label_map = {0: "O", 1: "B-ASP", 2: "I-ASP"}


def extract_aspects(text):
    tokens = text.split()

    inputs = tokenizer(
        tokens,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=2)[0].tolist()

    word_ids = inputs.word_ids()

    aspects = []
    current_aspect = []

    for pred, word_idx in zip(predictions, word_ids):
        if word_idx is None:
            continue

        label = label_map.get(pred, "O")

        if label == "B-ASP":
            if current_aspect:
                aspects.append(" ".join(current_aspect))
                current_aspect = []
            current_aspect.append(tokens[word_idx])

        elif label == "I-ASP" and current_aspect:
            current_aspect.append(tokens[word_idx])

        else:
            if current_aspect:
                aspects.append(" ".join(current_aspect))
                current_aspect = []

    if current_aspect:
        aspects.append(" ".join(current_aspect))

    # 🔥 CLEAN OUTPUT
    return list(set([
        asp.strip()
        for asp in aspects
        if len(asp.strip()) > 2
    ]))