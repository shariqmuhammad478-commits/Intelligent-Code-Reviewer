# Intelligent Code Reviewer & Explainer

**DecodeLabs | Generative AI | Project 4 (Optional Mastery Phase)**

A production-grade developer utility that analyzes source code, identifies bugs, and returns a structured bug report + optimized code using Google Gemini.

This tool follows the exact IPO architecture defined in the Project 4 slides:

1. **Ingest Payload** – Reads raw source files (`.py`, `.js`, `.java`, etc.) as strings while preserving whitespace and indentation.
2. **Context Orchestration** – Applies strict system instructions to force the model into an analytical (non-conversational) mode.
3. **Deterministic Markdown** – Validates the response and renders it with syntax highlighting in the terminal.

---

## Features

- Strict analytical persona (no conversational filler)
- Forced structured output (`## BUG_REPORT` + `## REFACTORED_CODE`)
- Response validation layer (rejects malformed outputs)
- Beautiful terminal rendering with `rich` (syntax highlighting)
- Robust error handling (FileNotFound, Permission, UnicodeDecode)
- Command-line support for any source file

---

## Setup

1. **Clone / Extract** the project folder.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Key**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste your Google Gemini API key:
   ```
   GOOGLE_API_KEY=AIzaSy...
   ```

4. **Run**
   ```bash
   # Using the included sample file
   python main.py

   # Or review any other file
   python main.py path/to/your/code.py
   python main.py path/to/script.js
   ```

---

## Output Format (Strict)

The model is forced to return **only** this structure:

```
## BUG_REPORT
- Concise technical bullet points

## REFACTORED_CODE
```python
# Corrected & optimized code
```
```

Any response missing these exact headers is rejected by the validation layer.

---

## Project Structure

```
intelligent_code_reviewer/
├── main.py              # Main application
├── sample_buggy.py      # Sample file with intentional issues
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Key Design Decisions (Aligned with Slides)

| Slide Concept              | Implementation                          |
|---------------------------|-----------------------------------------|
| Analytical Gatekeeper     | Cold system instruction, no greetings   |
| Structured Output         | Forced `## BUG_REPORT` + `## REFACTORED_CODE` |
| Validation Layer          | Explicit header checks before rendering |
| Deterministic Markdown    | `rich.markdown` with syntax highlighting|
| Input Triage              | Try/except for FileNotFound, Permission, Unicode |

---

**DecodeLabs • Batch 2026**
