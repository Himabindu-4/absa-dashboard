import pandas as pd
import json
import re

# ==============================
# LOAD BOTH DATASETS
# ==============================
df1 = pd.read_excel("app/data/Restaurants_Train_v2.xlsx")
df2 = pd.read_excel("app/data/Laptop_Train_v2.xlsx")

# Combine
df = pd.concat([df1, df2], ignore_index=True)

print("✅ Loaded rows:", len(df))
print("Columns:", df.columns)

data = []

# ==============================
# PROCESS EACH ROW
# ==============================
for _, row in df.iterrows():
    text = str(row["Sentence"])
    aspect = str(row["Aspect Term"])

    # skip empty
    if aspect == "nan":
        continue

    start = int(row["from"])
    end = int(row["to"])

    # ------------------------------
    # TOKENIZE
    # ------------------------------
    tokens = re.findall(r"\w+|\S", text)

    labels = ["O"] * len(tokens)

    # ------------------------------
    # CREATE TOKEN SPANS
    # ------------------------------
    token_spans = []
    current_pos = 0

    for token in tokens:
        idx = text.find(token, current_pos)

        if idx == -1:
            continue

        start_idx = idx
        end_idx = idx + len(token)

        token_spans.append((start_idx, end_idx))
        current_pos = end_idx

    # ------------------------------
    # APPLY BIO LABELS
    # ------------------------------
    for i, (s, e) in enumerate(token_spans):
        if s >= start and e <= end:
            if s == start:
                labels[i] = "B-ASP"
            else:
                labels[i] = "I-ASP"

    data.append({
        "tokens": tokens,
        "labels": labels
    })

# ==============================
# SAVE OUTPUT
# ==============================
with open("app/ate_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Saved:", len(data), "samples")