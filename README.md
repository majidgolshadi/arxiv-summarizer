# ArXiv Summarizer

A Python application that downloads academic papers from arXiv and generates summaries using AI in your mother tongue.

<img width="2319" height="1329" alt="Screenshot 2026-06-25 at 08 45 04" src="https://github.com/user-attachments/assets/45c95391-2f75-43f3-a0d4-253582ec6aab" />



## Description

If you're subscribed to the arXiv mailing list, you likely receive emails containing numerous paper links and descriptions. From the email content, it is often difficult to understand what each paper is trying to solve, making it challenging to decide which ones are worth investing your time in.

With this application, you simply copy the email content into a text file and provide it as input. The application extracts all paper links, analyzes their content, and generates concise summaries in your preferred language, helping you quickly identify the papers most relevant to your interests.


## Features

- Download PDF papers from arXiv
- Extract paper metadata and content
- Generate summaries using local AI
- Organized output in date-stamped directories
- Support for both short and medium length summaries

## Requirements

- Python 3.6+
- Ollama (with gemma4 model)
- Internet connection for downloading papers

## Installation

1. Clone or download this repository
2. Install required Python packages:
   ```bash
   python3 -m venv venv 
   source venv/bin/activate
   pip3 install -r requirements.txt
   ```

## Usage

1. Create a text file containing arXiv email subscription content:
   ```
   https://arxiv.org/abs/2501.12345
   XXXX
   XX
   XXXXX
   XXXXXXXXXXX
   https://arxiv.org/abs/2501.67890
   ```

2. Run the application:
   ```bash
   python main.py --input your_input_file.txt --summary-length short
   ```
   
   Or for medium length summaries:
   ```bash
   python main.py --input your_input_file.txt  --summary-length medium
   ```

## Output

Summaries are saved in a date-stamped directory structure:
```
YYYY_Mon_DD/summary/2501.12345.txt
```

Each summary file contains:
- Paper title
- Two blank lines
- Farsi summary with problem and solution sections

## Note

This application requires a local Ollama instance running with the `gemma4` model. Make sure Ollama is installed and the model is pulled before running the application.

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Pull the gemma4 model
ollama pull gemma4
```

## NotebookLM Export (optional)

When you archive papers, the app can automatically create a Google NotebookLM notebook and add the selected PDFs as sources.

### Setup

1. Enable the feature in `config.yaml`:
   ```yaml
   notebooklm_export: true
   ```

2. Install the Playwright browser used for automation:
   ```bash
   pip install "notebooklm-py[browser]"
   playwright install chromium
   ```

3. Log in to your Google account once:
   ```bash
   notebooklm login
   ```
   This opens a browser window. Sign in and close it — your session is saved locally.

### Usage

After setup, archiving papers from the UI will automatically create a notebook named **"AI - arXiv - YYYY Mon DD"** in your NotebookLM account with the selected PDFs added as sources.

If you see "NotebookLM: auth required" in the UI, run `notebooklm login` again to refresh your session.
