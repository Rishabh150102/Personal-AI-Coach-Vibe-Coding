# Personal AI Coach

Minimal Streamlit app that sends a coaching prompt to the OpenAI API.

## Requirements

- Python 3.10 or newer
- An OpenAI API key set in the `OPENAI_API_KEY` environment variable

## Install Python

If Python is not installed, download it from the official Python website:

https://www.python.org/downloads/

During installation on Windows, enable the option to add Python to your `PATH`.

## Set Up a Virtual Environment

From this project folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure the OpenAI API Key

PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

macOS or Linux:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run the App

```bash
streamlit run app.py
```

## Run the Prompt Evaluation Script

```bash
python evaluation.py
```
