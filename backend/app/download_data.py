from datasets import load_dataset
import json

# Load working ABSA dataset (SemEval-style)
dataset = load_dataset("tomaarsen/absa-restaurants")

data = []

for item in dataset["train"]:
    tokens = item["tokens"]
    labels = item["tags"]

    converted_labels = []
    for tag in labels:
        if tag == 0:
            converted_labels.append("O")
        elif tag == 1:
            converted_labels.append("B-ASP")
        elif tag == 2:
            converted_labels.append("I-ASP")
        else:
            converted_labels.append("O")

    data.append({
        "tokens": tokens,
        "labels": converted_labels
    })

# Save file
with open("absa_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Dataset ready!")