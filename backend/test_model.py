from app.ate_model import extract_aspects

# Test sentences
tests = [
    "The food was amazing but service was slow",
    "Battery life is great but screen quality is bad",
    "The keyboard is comfortable and price is reasonable"
]

for text in tests:
    aspects = extract_aspects(text)
    print("\nSentence:", text)
    print("Extracted Aspects:", aspects)