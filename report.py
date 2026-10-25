"""Step 4: numbers for your README/resume -> report.md"""
import os
import pandas as pd

prompts = pd.read_csv("prompts.csv")
human = pd.read_csv("human_labels.csv").fillna("")
df = human.merge(prompts, on="id")
df["failed"] = df["label"] != "CORRECT"

lines = ["# Results\n", f"Responses labeled: {len(df)}  |  Overall failure rate: {df['failed'].mean():.0%}\n"]
for col in ["model", "category", "language"]:
    t = df.groupby(col)["failed"].agg(["count", "mean"]).rename(columns={"count": "n", "mean": "failure_rate"})
    t["failure_rate"] = (t["failure_rate"] * 100).round(0).astype(int).astype(str) + "%"
    lines += [f"\n## Failure rate by {col}\n", t.to_markdown(), ""]
lines += ["\n## Label counts\n", df["label"].value_counts().to_markdown(), ""]

if os.path.exists("judge_labels.csv"):
    from sklearn.metrics import cohen_kappa_score
    j = df.merge(pd.read_csv("judge_labels.csv"), on=["id", "model"])
    agree = (j["label"] == j["judge_label"]).mean()
    kappa = cohen_kappa_score(j["label"], j["judge_label"])
    lines += [f"\n## LLM judge vs human\n", f"Agreement: {agree:.0%}  |  Cohen's kappa: {kappa:.2f}\n",
              pd.crosstab(j["label"], j["judge_label"]).to_markdown(), "\n### Disagreements\n"]
    for _, r in j[j["label"] != j["judge_label"]].iterrows():
        lines.append(f"- **{r['id']}** human={r['label']} judge={r['judge_label']} — {r['judge_reason']}")

lines += ["\n## Failures (for error analysis)\n"]
for _, r in df[df["failed"]].iterrows():
    lines.append(f"- **{r['id']}** [{r['category']}/{r['language']}] {r['label']}: {r['note']}")

open("report.md", "w", encoding="utf-8").write("\n".join(lines))
print("\n".join(lines[:2]))
print("Full report -> report.md")
