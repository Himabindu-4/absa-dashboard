import json

data = []

sentences = [
    ("The food was great but service was slow", ["food", "service"]),
    ("The service was excellent and food quality was amazing", ["service", "food quality"]),
    ("Battery life is great but screen quality is bad", ["battery life", "screen quality"]),
    ("The screen is bright but battery drains fast", ["screen", "battery"]),
    ("Keyboard is smooth and touchpad is responsive", ["keyboard", "touchpad"]),
    ("The laptop price is high but performance is good", ["price", "performance"]),
    ("Camera quality is excellent", ["camera quality"]),
    ("Sound quality is poor", ["sound quality"]),
    ("The display is sharp and clear", ["display"]),
    ("Packaging was bad but product quality is good", ["packaging", "product quality"]),
    ("Food taste is amazing and ambience is nice", ["food taste", "ambience"]),
    ("The waiter service was terrible", ["service"]),
    ("Battery backup is strong", ["battery backup"]),
    ("Screen resolution is very high", ["screen resolution"]),
    ("The keyboard keys are soft", ["keyboard"]),
    ("Price is reasonable for this product", ["price"]),
    ("The food quality was poor", ["food quality"]),
    ("Service was quick and efficient", ["service"]),
    ("Camera is bad in low light", ["camera"]),
    ("The display brightness is excellent", ["display brightness"]),
    ("Sound is clear and loud", ["sound"]),
    ("Packaging quality is excellent", ["packaging quality"]),
    ("The laptop performance is fast", ["performance"]),
    ("Battery charging is slow", ["battery"]),
    ("The food presentation was nice", ["food presentation"]),
]

for text, aspects in sentences:
    tokens = text.split()
    labels = ["O"] * len(tokens)

    for asp in aspects:
        asp_tokens = asp.split()
        for i in range(len(tokens)):
            if tokens[i:i+len(asp_tokens)] == asp_tokens:
                labels[i] = "B-ASP"
                for j in range(1, len(asp_tokens)):
                    labels[i+j] = "I-ASP"

    data.append({
        "tokens": tokens,
        "labels": labels
    })

with open("absa_data.json", "w") as f:
    json.dump(data, f, indent=2)

print("✅ Improved dataset created")