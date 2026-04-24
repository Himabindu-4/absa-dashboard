import pandas as pd
import numpy as np
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer
)

from datasets import Dataset
from sklearn.model_selection import train_test_split
from seqeval.metrics import f1_score

# -----------------------------
# LOAD DATA
# -----------------------------
df1 = pd.read_excel("app/data/Restaurants_Train_v2.xlsx")
df2 = pd.read_excel("app/data/Laptop_Train_v2.xlsx")

df = pd.concat([df1, df2])
df.columns = [c.lower().strip() for c in df.columns]

# -----------------------------
# BUILD SENTENCE + LABELS
# -----------------------------
sentences = []
labels = []

label_map = {"O": 0, "B-ASP": 1, "I-ASP": 2}
id2label = {v: k for k, v in label_map.items()}

grouped = df.groupby("sentence")

for sentence, group in grouped:
    tokens = sentence.split()
    tags = ["O"] * len(tokens)

    for _, row in group.iterrows():
        aspect = str(row["aspect term"]).split()
        for i in range(len(tokens)):
            if tokens[i:i+len(aspect)] == aspect:
                tags[i] = "B-ASP"
                for j in range(1, len(aspect)):
                    tags[i+j] = "I-ASP"

    sentences.append(tokens)
    labels.append([label_map[t] for t in tags])

# -----------------------------
# TOKENIZER
# -----------------------------
tokenizer = AutoTokenizer.from_pretrained("roberta-base")

def tokenize_and_align(examples):
    tokenized = tokenizer(
        examples["tokens"],
        is_split_into_words=True,
        truncation=True,
        padding="max_length",
        max_length=128
    )

    new_labels = []

    for i, label in enumerate(examples["labels"]):
        word_ids = tokenized.word_ids(batch_index=i)
        aligned = []
        prev = None

        for word_id in word_ids:
            if word_id is None:
                aligned.append(-100)
            elif word_id != prev:
                aligned.append(label[word_id])
            else:
                aligned.append(label[word_id])
            prev = word_id

        new_labels.append(aligned)

    tokenized["labels"] = new_labels
    return tokenized

dataset = Dataset.from_dict({
    "tokens": sentences,
    "labels": labels
})

train_test = dataset.train_test_split(test_size=0.1)
train_ds = train_test["train"].map(tokenize_and_align, batched=True)
test_ds = train_test["test"].map(tokenize_and_align, batched=True)

# -----------------------------
# MODEL
# -----------------------------
model = AutoModelForTokenClassification.from_pretrained(
    "roberta-base",
    num_labels=3
)

# -----------------------------
# TRAINING SETTINGS (IMPROVED)
# -----------------------------
training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_steps=50,
    save_steps=200
)

# -----------------------------
# METRICS
# -----------------------------
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=2)
    true = p.label_ids

    true_labels = []
    pred_labels = []

    for pred, lab in zip(preds, true):
        curr_pred = []
        curr_true = []

        for p_, l_ in zip(pred, lab):
            if l_ != -100:
                curr_pred.append(id2label[p_])
                curr_true.append(id2label[l_])

        true_labels.append(curr_true)
        pred_labels.append(curr_pred)

    return {"f1": f1_score(true_labels, pred_labels)}

# -----------------------------
# TRAIN
# -----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
    compute_metrics=compute_metrics
)

trainer.train()

metrics = trainer.evaluate()
print("✅ F1 Score:", round(metrics["eval_f1"], 4))

# -----------------------------
# SAVE
# -----------------------------
model.save_pretrained("app/ate_model")
tokenizer.save_pretrained("app/ate_model")

print("✅ ATE model saved")