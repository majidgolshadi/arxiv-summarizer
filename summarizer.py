import os
from typing import Optional

import requests

import config
from pdf_parser import parse_pdf_metadata_and_text


def generate_summary(pdf_path: str, title: str, summary_length: str) -> Optional[str]:
    print(f"\n--- Generating Summary for: {os.path.basename(pdf_path)} ---")

    _, text_content = parse_pdf_metadata_and_text(pdf_path)
    if not text_content:
        print(f"[SKIP] Cannot generate summary: No text content extracted from {os.path.basename(pdf_path)}.")
        return None

    word_count_hint = config.WORD_COUNT_HINTS.get(summary_length)
    if not word_count_hint:
        print(f"[ERROR] Unknown summary length: {summary_length}")
        return None

    prompt = f"""
    You are an expert in AI and a university teacher.
    Your task is to read the full text of an academic paper and generate a super simple to understand summary in {config.LANGUAGE}.

    *** CONSTRAINTS ***
    1. Language: The summary MUST be as simple as possible, easy to understand for a dumb software engineer in {config.LANGUAGE}.
    2. Length: The summary should be approximately {word_count_hint} for the problem and {word_count_hint} for the solution.
    3. Title: The paper's title is: "{title}".
    4. Summary Format: It must contain two sections: `problem` and `solution`.
        problem section explaining the problem that the paper is trying to solve
        solution section explaining the solution proposed by the paper.
        For each section, provide concise content.
        The summary text of each must not include titles, explanations, or extra markdown. Start immediately with the summary text.
        When a sentence ends, go to the next line.
        If you can bullet point to explain the content better, do it.
        Put two blank lines between the problem and solution sections.

    *** FULL ARTICLE TEXT ***
    {text_content[:config.MAX_TEXT_CHARS]}
    """

    try:
        print(f"[OLLAMA API] Connecting to {config.MODEL_NAME} at {config.OLLAMA_API_URL}...")
        payload = {"model": config.MODEL_NAME, "prompt": prompt, "stream": False}
        response = requests.post(config.OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to Ollama API at {config.OLLAMA_API_URL}. Is Ollama running?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An API request failed: {e}")
        return None
    except Exception as e:
        print(f"[FAIL] Summary generation failed for {os.path.basename(pdf_path)}: {e}")
        return None
