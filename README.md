# ArXiv Summarizer

A Python application that downloads academic papers from arXiv and generates summaries using AI in your mother tongue languge.

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