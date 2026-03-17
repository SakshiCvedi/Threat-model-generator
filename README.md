# Threat Model Generator

An AI-powered CLI tool that analyzes software architecture descriptions 
and generates structured STRIDE-based threat models automatically.

Built with Python, Groq (LLaMA 3.3), and Rich.

---

## What it does

Feed it a README or architecture description → get back a complete
security threat model covering all 6 STRIDE categories, trust boundaries,
risk scores, and immediate action items.

---

## Demo
```
$ py -m app.main README.md --output terminal

Step 1/3: Parsing input...
✓ Input type: markdown

Step 2/3: Generating threat model...
✓ Risk score: 8/10

Step 3/3: Rendering output...

╭─────────────────────────────────╮
│       Threat Model Report       │
│  Flask API · Risk Score: 8/10   │
╰─────────────────────────────────╯

STRIDE Analysis
┌──────────────────────┬───────────┬──────────────────────┐
│ Category             │ Risk      │ Top Threat           │
├──────────────────────┼───────────┼──────────────────────┤
│ Spoofing             │ High      │ JWT token forgery    │
│ Tampering            │ Medium    │ SQL injection        │
│ Elevation of Priv    │ Critical  │ Missing RBAC         │
└──────────────────────┴───────────┴──────────────────────┘
```

---

## Features

- Accepts README.md, .txt files, or raw text descriptions
- Generates STRIDE threat models (6 categories)
- Outputs to terminal (colored table), Markdown, or PDF
- 12 automated tests with mocking
- Clean CLI with `--output` and `--help` flags

---

## Installation
```bash
git clone https://github.com/YOUR_USERNAME/threat-model-gen.git
cd threat-model-gen
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Add your API key to `.env`:
```
GROQ_API_KEY=your_key_here
```

---

## Usage
```bash
# Analyze a README file
py -m app.main README.md

# Generate PDF report
py -m app.main README.md --output pdf

# All formats at once
py -m app.main README.md --output all

# Raw text input
py -m app.main "Flask app with JWT and PostgreSQL" --output terminal
```

---

## Project Structure
```
threat-model-gen/
├── app/
│   ├── main.py        # CLI entry point (typer)
│   ├── parser.py      # Input parser
│   ├── analyzer.py    # Groq API integration
│   ├── renderer.py    # Terminal, Markdown, PDF output
│   └── prompts.py     # STRIDE system prompt
├── tests/             # 12 automated tests (pytest)
├── outputs/           # Generated threat models
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| AI Model | LLaMA 3.3 70B via Groq |
| CLI | Typer |
| Terminal UI | Rich |
| PDF Generation | ReportLab |
| Testing | pytest + unittest.mock |
| Secret Management | python-dotenv |

---

## Sample Output

Generated threat models are saved to `outputs/` as `.md` or `.pdf` files.

---

*Built as a DevSecOps portfolio project — demonstrates shift-left security
tooling, AI integration, and automated threat modeling.*