import os
import json
import subprocess
import requests
from typing import Optional
from pdf_parser import parse_pdf_metadata_and_text # Assuming pdf_parser.py is available and works

# 
def generate_farsi_summary(pdf_path: str, title: str, summary_length: str) -> Optional[str]:
    """
    Generates a Farsi summary of the PDF content using the local Ollama API.

    Args:
        pdf_path: Full path to the PDF file.
        title: The English title of the paper.
        summary_length: 'short' or 'medium' for summary length control.

    Returns:
        The generated Farsi summary text, or None if generation fails.
    """
    print(f"\n--- Generating Summary for: {os.path.basename(pdf_path)} ---")
    
    # 1. Read the text content from the PDF
    _, text_content = parse_pdf_metadata_and_text(pdf_path)
    
    if not text_content:
        print(f"[SKIP] Cannot generate summary: No text content extracted from {os.path.basename(pdf_path)}.")
        return None

    # 2. Determine length and create prompt
    if summary_length == 'short':
        word_count_hint = "150–250 words"
    elif summary_length == 'medium':
        word_count_hint = "400–700 words"
    else:
        print(f"[ERROR] Unknown summary length: {summary_length}")
        return None

    # The prompt structure is crucial for AI model interaction
    prompt = f"""
    You are an expert academic summarization system. 
    Your task is to read the full text of an academic paper and generate a summary in Farsi (Persian).
    
    *** CONSTRAINTS ***
    1. Language: The summary MUST be in formal, academic Farsi (Persian).
    2. Length: The summary should be approximately {word_count_hint}.
    3. Tone: Maintain a highly academic and formal tone.
    4. Title: The paper's title is: "{title}".
    5. Summary Format: Provide ONLY the summary text. Do not include titles, explanations, or extra markdown. Start immediately with the summary text.
    
    *** FULL ARTICLE TEXT ***
    {text_content[:10000]} 
    """ # Truncate text to prevent overly long context window usage

    # 3. Connect to Ollama and generate summary
    try:
        OLLAMA_API_URL = "http://localhost:11434/api/generate"
        MODEL_NAME = "gemma4"
        
        print(f"[OLLAMA API] Connecting to {MODEL_NAME} at {OLLAMA_API_URL}...")
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        summary_text = data.get("response", "").strip()
        
        return summary_text

    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to Ollama API at {OLLAMA_API_URL}. Is Ollama running?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] An API request failed: {e}")
        return None
    except Exception as e:
        print(f"[FAIL] Summary generation failed for {os.path.basename(pdf_path)}: {e}")
        return None