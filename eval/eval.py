import os
import json
from backend.extractor import extract_receipt_data

POSITIVE_SET = {
    "supermarket-receipt.png",
    "Detailed-Grocery-Payment-Receipt-Samples.jpg",
    "regular-receipt.png",
    "veggie-grocery-receipt_orig.jpeg",
    "long-receipt.jpg",
}

NEGATIVE_SET = {
    "blurry-receipt.jpeg",
    "grocery-receipt-lighting.jpeg",
    "covered-receipt.jpg",
    "wrinkly-grocery-receipt.jpg",
}

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg"}

def is_valid_file(filename):
    return any(filename.lower().endswith(ext) for ext in VALID_EXTENSIONS)

def compute_metrics(result):
    items = result.get("items", [])
    predicted_total = result.get("total", 0)

    total_items = len(items)

    # -----------------------
    # CATEGORY ACCURACY
    # -----------------------
    missing_categories = sum(
        1 for i in items if not i.get("category")
    )

    category_accuracy = (
        1 - (missing_categories / total_items)
        if total_items > 0
        else 0
    )

    # -----------------------
    # TOTAL ERROR (RELATIVE)
    # -----------------------
    computed_total = sum(
        i.get("total_price", 0) for i in items
    )

    if predicted_total > 0:
        relative_total_error = abs(computed_total - predicted_total) / predicted_total
    else:
        relative_total_error = 0

    return {
        "items": total_items,
        "missing_categories": missing_categories,
        "category_accuracy": category_accuracy,
        "relative_total_error": relative_total_error,
    }

def summarize(name, group):
    if not group:
        print(f"\n===== {name} =====")
        print("No data")
        return

    avg = lambda k: sum(x[k] for x in group) / len(group)

    print(f"\n===== {name} =====")
    print(f"Avg items: {avg('items'):.2f}")
    print(f"Avg missing categories: {avg('missing_categories'):.2f}")
    print(f"Avg category accuracy: {avg('category_accuracy'):.2f}")
    print(f"Avg relative total error: {avg('relative_total_error'):.2f}")

def run_eval(dataset_path="eval/receipts"):
    results = []
    pos_stats = []
    neg_stats = []

    for file in os.listdir(dataset_path):

        if not is_valid_file(file):
            continue

        path = os.path.join(dataset_path, file)

        print(f"\n--- Running: {file} ---")

        try:
            with open(path, "rb") as f:
                result = extract_receipt_data(f.read())

            metrics = compute_metrics(result)

            is_positive = file in POSITIVE_SET
            label = "POSITIVE" if is_positive else "NEGATIVE"

            print(f"{label} TEST CASE")
            print(metrics)

            results.append((file, metrics, is_positive))

            if is_positive:
                pos_stats.append(metrics)
            else:
                neg_stats.append(metrics)

        except Exception as e:
            print(f"❌ Crash: {e}")

    print("\n====================")
    print("EVALUATION SUMMARY")
    print("====================")

    summarize("POSITIVE SET", pos_stats)
    summarize("NEGATIVE SET", neg_stats)

if __name__ == "__main__":
    run_eval()