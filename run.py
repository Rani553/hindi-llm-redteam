"""Step 1: send every prompt to the model and save responses.
Usage: python run.py [model_name]      (resumes if interrupted)"""
import csv, json, os, sys
from llm import ask, model_name

model = sys.argv[1] if len(sys.argv) > 1 else None
tag = model_name(model)
prompts = list(csv.DictReader(open("prompts.csv", encoding="utf-8")))

done = set()
if os.path.exists("responses.jsonl"):
    for line in open("responses.jsonl", encoding="utf-8"):
        r = json.loads(line)
        done.add((r["id"], r["model"]))

with open("responses.jsonl", "a", encoding="utf-8") as out:
    for p in prompts:
        if (p["id"], tag) in done:
            continue
        print(f"[{p['id']}] {p['prompt'][:60]}")
        resp = ask(p["prompt"], model)
        out.write(json.dumps({"id": p["id"], "model": tag, "response": resp}, ensure_ascii=False) + "\n")
        out.flush()
print("Done. Responses in responses.jsonl")
