# Hindi–English LLM Red-Teaming & Evaluation

How well do LLMs handle Hindi, Hinglish and English questions about Indian law, civic life, health myths and reasoning — and do they fall for false premises or make things up?

## What I did
1. Wrote **[N] adversarial prompts** in Hindi (Devanagari), Hinglish and English across 7 categories: false premise, legal/civic, health myths, unanswerable, reasoning, instruction-following, cultural facts.
2. Ran them on **[model A]** and **[model B]**.
3. **Hand-labeled every response** with an 8-label rubric (`rubric.md`).
4. Ran an **LLM-as-a-Judge** with the same rubric and measured agreement with my labels.

## Key findings  (fill from report.md)
- Overall failure rate: [X]% ([model A]) vs [X]% ([model B])
- Worst category: [category] — [X]% failures. Example: ...
- Hindi vs English: [what you saw]
- Judge vs me: [X]% agreement, kappa [X]. Judge was too lenient/strict on: ...

## Failure patterns  (write 3–5 in your own words, with one example each)
1. ...

## Run it
```
pip install -r requirements.txt
set GEMINI_API_KEY=your_key        (Windows cmd)
python run.py                      # 1. get responses
python label.py                    # 2. YOU label them
python judge.py                    # 3. LLM judge
python report.py                   # 4. numbers -> report.md
```
To test a second model: `set LLM_PROVIDER=groq` + `set GROQ_API_KEY=...`, then `python run.py` again.
