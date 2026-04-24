import json

data = [
    ("The battery life is poor", "battery life", "NEG"),
    ("Battery drains very fast", "battery", "NEG"),
    ("Battery performance is bad", "battery", "NEG"),
    ("Camera quality is amazing", "camera quality", "POS"),
    ("Camera is excellent", "camera", "POS"),
    ("Screen is okay", "screen", "NEU"),
    ("Display is average", "display", "NEU"),
    ("Food was delicious", "food", "POS"),
    ("Service was terrible", "service", "NEG"),
    ("Keyboard is comfortable", "keyboard", "POS"),
    ("Price is too high", "price", "NEG"),
    ("Sound quality is excellent", "sound quality", "POS"),
    ("Camera quality is terrible", "camera quality", "NEG"),
    ("Screen is not good", "screen", "NEG"),
]

dataset = [{"text": t, "aspect": a, "label": l} for t, a, l in data]

with open("asc_data.json", "w") as f:
    json.dump(dataset, f, indent=2)

print("✅ ASC dataset updated")