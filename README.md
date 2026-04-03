# 🧠 Personal AI Coach

A Streamlit web app that delivers personalized coaching advice powered by the OpenAI API. Choose from four distinct coaching personas, fine-tune the style, and get actionable guidance on any challenge — career, productivity, mindset, or beyond.

---

## ✨ Features

- **4 Coaching Personas** — Supportive, Direct, Reflective, and Strategic
- **Style Controls** — Adjust warmth, directness, and response length to suit your needs
- **Coaching Focus** — Target specific outcomes: Motivation, Clarity, Action Plan, Accountability, or Confidence
- **Multi-language Output** — Translate responses into 7 languages including Hindi, Spanish, French, and more
- **Session Memory** — Maintains conversation context across turns (configurable window of 6 messages)
- **Clean Chat UI** — Styled chat bubbles with a dark theme, rendered in a wide-layout interface

---

## 📸 Preview

> Supportive, Direct, Reflective, and Strategic coaches respond to your input with structured advice, reframing, and accountability prompts.

---

## 🗂 Project Structure

```
personal-ai-coach/
├── app.py             # Main Streamlit application
├── prompts.py         # Persona definitions and prompt templates
├── evaluation.py      # Offline prompt evaluation / test script
├── requirements.txt   # Python dependencies
├── .env               # Your API key (never committed — see setup)
└── .gitignore
```

---

## ⚙️ Requirements

- Python 3.10 or newer
- An OpenAI API key

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

> ⚠️ Never commit this file. It is already listed in `.gitignore`.

Alternatively, set the environment variable directly in your terminal:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🧪 Running the Prompt Evaluation Script

To test that prompts are assembled correctly without making any API calls:

```bash
python evaluation.py
```

This runs three predefined test cases across different personas and reports which checks pass or fail.

---

## 🎛 Sidebar Settings

| Setting | Options | Description |
|---|---|---|
| Persona | Supportive, Direct, Reflective, Strategic | Sets the coaching style and tone |
| Warmth | Low / Medium / High | Controls emotional warmth in responses |
| Directness | Low / Medium / High | Controls how blunt or gentle the advice is |
| Response Length | Brief / Balanced / Detailed | Controls how long responses are |
| Coaching Focus | Motivation, Clarity, Action Plan, Accountability, Confidence | Steers the coaching objective |
| Response Language | English, Hindi, Spanish, French, German, Portuguese, Japanese | Translates assistant responses |
| Session Memory | Toggle on/off | Enables multi-turn context |
| Model | Text input | Defaults to `gpt-4o-mini`; swap in any OpenAI model |

---

## 🌐 Supported Languages

English · Hindi · Spanish · French · German · Portuguese · Japanese

---

## 🤖 Coaching Personas

| Persona | Style |
|---|---|
| **Supportive Coach** | Warm, encouraging, focused on small wins and reducing overwhelm |
| **Direct Coach** | Blunt, action-oriented, challenges excuses and drives follow-through |
| **Reflective Coach** | Calm and curious, surfaces patterns and assumptions behind the problem |
| **Strategic Coach** | Structured and outcome-focused, prioritizes the highest-leverage next move |

---

## 📦 Dependencies

```
openai>=1.0.0
streamlit>=1.30.0
python-dotenv>=1.0.0
```

---

## 🔒 Security Notes

- Your API key is loaded from a `.env` file or environment variable — it is never hardcoded in the source
- `.env` is excluded from version control via `.gitignore`
- No user data is stored or logged by the app

