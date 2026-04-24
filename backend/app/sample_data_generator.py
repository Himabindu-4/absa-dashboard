import json

data = [
    {
        "tokens": ["The", "food", "was", "amazing", "but", "service", "was", "slow"],
        "labels": ["O", "B-ASP", "O", "O", "O", "B-ASP", "O", "O"]
    },
    {
        "tokens": ["Battery", "life", "is", "good", "but", "screen", "quality", "is", "bad"],
        "labels": ["B-ASP", "I-ASP", "O", "O", "O", "B-ASP", "I-ASP", "O", "O"]
    },
    {
        "tokens": ["The", "keyboard", "is", "comfortable"],
        "labels": ["O", "B-ASP", "O", "O"]
    },
    {
        "tokens": ["Food", "quality", "was", "poor"],
        "labels": ["B-ASP", "I-ASP", "O", "O"]
    },
    {
        "tokens": ["The", "price", "is", "reasonable"],
        "labels": ["O", "B-ASP", "O", "O"]
    }
]

with open("absa_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Sample dataset created")