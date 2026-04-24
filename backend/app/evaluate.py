from ate_model import extract_aspects

# =========================
# TEST DATA (GROUND TRUTH)
# =========================
test_data = [
    ("The food was amazing but service was slow", ["food", "service"]),
    ("Battery life is great but screen quality is bad", ["battery life", "screen quality"]),
    ("The keyboard is comfortable and price is reasonable", ["keyboard", "price"])
]

# =========================
# METRIC FUNCTION
# =========================
def calculate_metrics(true, pred):
    true_set = set(true)
    pred_set = set(pred)

    tp = len(true_set & pred_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    return precision, recall, f1


# =========================
# RUN EVALUATION
# =========================
total_p, total_r, total_f1 = 0, 0, 0

for text, true_aspects in test_data:
    pred_aspects = extract_aspects(text)

    p, r, f1 = calculate_metrics(true_aspects, pred_aspects)

    total_p += p
    total_r += r
    total_f1 += f1

    print("\nSentence:", text)
    print("True Aspects:", true_aspects)
    print("Predicted Aspects:", pred_aspects)
    print(f"Precision: {p:.2f}, Recall: {r:.2f}, F1 Score: {f1:.2f}")

# =========================
# FINAL AVERAGE
# =========================
n = len(test_data)

print("\n========== FINAL METRICS ==========")
print(f"Average Precision: {total_p/n:.2f}")
print(f"Average Recall: {total_r/n:.2f}")
print(f"Average F1 Score: {total_f1/n:.2f}")