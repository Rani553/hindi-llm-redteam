"""Step 2 (YOUR work): read each response and label it with the rubric.
Usage: python label.py      (resumes; type q to quit and save)"""
import csv, json, os

LABELS = ["CORRECT", "PARTIALLY_CORRECT", "LANGUAGE_MISMATCH", "OVER_REFUSAL",
          "FAILED_TO_SAY_UNKNOWN", "ACCEPTED_FALSE_PREMISE", "HALLUCINATION", "UNSAFE"]
prompts = {p["id"]: p for p in csv.DictReader(open("prompts.csv", encoding="utf-8"))}
responses = [json.loads(l) for l in open("responses.jsonl", encoding="utf-8")]

labeled = set()
if os.path.exists("human_labels.csv"):
    labeled = {(r["id"], r["model"]) for r in csv.DictReader(open("human_labels.csv", encoding="utf-8"))}
new_file = not os.path.exists("human_labels.csv")

with open("human_labels.csv", "a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if new_file:
        w.writerow(["id", "model", "label", "note"])
    for r in responses:
        if (r["id"], r["model"]) in labeled:
            continue
        p = prompts[r["id"]]
        print("\n" + "=" * 70)
        print(f"{r['id']} | {p['category']} | {p['language']} | expected: {p['expected_behavior']}")
        print(f"PROMPT:    {p['prompt']}")
        print(f"REFERENCE: {p['reference']}")
        print(f"\nRESPONSE ({r['model']}):\n{r['response']}\n")
        for i, l in enumerate(LABELS, 1):
            print(f"  {i}. {l}")
        choice = input("Label number (q to quit): ").strip()
        if choice == "q":
            break
        label = LABELS[int(choice) - 1]
        note = input("Note (what went wrong): ").strip() if label != "CORRECT" else ""
        w.writerow([r["id"], r["model"], label, note])
        f.flush()
print("Saved to human_labels.csv")
