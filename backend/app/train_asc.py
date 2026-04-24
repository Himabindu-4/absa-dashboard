import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer
)
import numpy as np
from sklearn.metrics import accuracy_score

# =========================
# LOAD DATA
# =========================
df1 = pd.read_excel("app/data/Restaurants_Train_v2.xlsx")
df2 = pd.read_excel("app/data/Laptop_Train_v2.xlsx")

df = pd.concat([df1, df2], ignore_index=True)

print("Original size:", len(df))

# =========================
# CLEAN DATA (FIXED)
# =========================

# keep only valid polarity values
df = df[df["polarity"].isin(["negative", "neutral", "positive"])]

# drop missing text/aspect
df = df.dropna(subset=["Sentence", "Aspect Term"])

# map labels
label_map = {"negative": 0, "neutral": 1, "positive": 2}
df["label"] = df["polarity"].map(label_map)

# remove any remaining bad rows
df = df.dropna(subset=["label"])

# convert to int
df["label"] = df["label"].astype(int)

print("✅ Cleaned dataset size:", len(df))
print("Labels:", df["polarity"].unique())

# =========================
# FORMAT INPUT
# =========================
texts = []
labels = []

for _, row in df.iterrows():
    text = str(row["Sentence"])
    aspect = str(row["Aspect Term"])

    # sentence pair format
    combined = f"{text} [SEP] {aspect}"

    texts.append(combined)
    labels.append(row["label"])

dataset = Dataset.from_dict({
    "text": texts,
    "label": labels
})

# split
dataset = dataset.train_test_split(test_size=0.1)

# =========================
# TOKENIZER
# =========================
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

def tokenize(example):
    return tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=128
    )

dataset = dataset.map(tokenize)

# =========================
# MODEL
# =========================
model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=3
)

# =========================
# TRAINING (FAST)
# =========================
training_args = TrainingArguments(
    output_dir="app/asc_model",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=1,
    max_steps=300
)

# =========================
# METRICS
# =========================
def compute_metrics(p):
    preds = np.argmax(p.predictions, axis=1)
    return {"accuracy": accuracy_score(p.label_ids, preds)}

# =========================
# TRAINER
# =========================
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    compute_metrics=compute_metrics
)

# =========================
# TRAIN
# =========================
trainer.train()

# =========================
# EVALUATE
# =========================
metrics = trainer.evaluate()
print("✅ Accuracy:", round(metrics["eval_accuracy"], 4))

# =========================
# SAVE MODEL
# =========================
model.save_pretrained("app/asc_model")
tokenizer.save_pretrained("app/asc_model")

print("✅ ASC model saved")