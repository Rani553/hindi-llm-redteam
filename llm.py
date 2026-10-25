"""Tiny wrapper so every script can call Gemini or Groq the same way.
Set LLM_PROVIDER=gemini (default) or groq, and GEMINI_API_KEY / GROQ_API_KEY."""
import os, time

PROVIDER = os.environ.get("LLM_PROVIDER", "gemini")
DEFAULT_MODEL = {"gemini": "gemini-2.0-flash", "groq": "llama-3.1-8b-instant"}[PROVIDER]


def ask(prompt, model=None, system=None, retries=3):
    model = model or DEFAULT_MODEL
    for attempt in range(retries):
        try:
            if PROVIDER == "gemini":
                from google import genai
                from google.genai import types
                client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
                cfg = types.GenerateContentConfig(system_instruction=system) if system else None
                return client.models.generate_content(model=model, contents=prompt, config=cfg).text
            else:
                from groq import Groq
                client = Groq(api_key=os.environ["GROQ_API_KEY"])
                msgs = ([{"role": "system", "content": system}] if system else []) + \
                       [{"role": "user", "content": prompt}]
                r = client.chat.completions.create(model=model, messages=msgs)
                return r.choices[0].message.content
        except Exception as e:
            print(f"  API error ({e}); retrying in {5 * (attempt + 1)}s")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("API failed after retries")


def model_name(model=None):
    return f"{PROVIDER}:{model or DEFAULT_MODEL}"
