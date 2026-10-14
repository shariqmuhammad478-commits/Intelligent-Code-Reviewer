#!/usr/bin/env python3
"""
Intelligent Code Reviewer & Explainer
DecodeLabs | Generative AI Project 4 (Optional Mastery Phase)

IPO Architecture:
  1. Ingest Payload      → Read source file as raw string
  2. Context Orchestration → Strict system instructions + Gemini
  3. Deterministic Markdown → Validate + render with rich
"""

import os
import sys
import argparse
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich import box

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("ERROR: GOOGLE_API_KEY not found.")
    print("→ Copy .env.example to .env and add your Gemini API key.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Strict analytical persona (exactly as defined in the slides)
SYSTEM_INSTRUCTION = """
You are a cold, analytical Senior Code Quality Assurance Engineer.
You only output valid code blocks and direct bullet points.
Do not write friendly greetings.
Do not add any conversational filler, explanations outside the required sections, or extra text.

Always respond in EXACTLY this format and nothing else:

## BUG_REPORT
- List every syntax anomaly, logical vulnerability, performance issue, and code-smell as direct, concise bullet points.
- Be technical and precise.

## REFACTORED_CODE
```python
# Complete corrected, optimized, and compilable code goes here.
# Preserve original functionality while fixing all identified issues.
```
"""

console = Console()


# ---------------------------------------------------------------------------
# Phase 1: Input & Payload Capture
# ---------------------------------------------------------------------------
def read_code_file(file_path: str) -> str:
    """
    Safely stream the target source file into memory as a raw string.
    Preserves all whitespace, indentation, and line endings.
    Handles the three classic failure modes defined in the slides.
    """
    path = Path(file_path)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.strip():
            raise ValueError(f"File is empty: {file_path}")

        return content

    except FileNotFoundError:
        raise FileNotFoundError(
            f"The specified path does not point to a valid file: {file_path}"
        )
    except PermissionError:
        raise PermissionError(
            f"The file has restricted read permissions: {file_path}"
        )
    except UnicodeDecodeError as exc:
        raise UnicodeDecodeError(
            "utf-8", b"", 0, 1,
            f"Unexpected encoding characters (possible binary asset): {file_path}"
        ) from exc


# ---------------------------------------------------------------------------
# Phase 2: Context Orchestration
# ---------------------------------------------------------------------------
def analyze_code(raw_code: str) -> str:
    """
    Send the raw code payload to Gemini under the strict analytical persona.
    The system instruction hard-codes the required output contract.
    """
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=SYSTEM_INSTRUCTION,
    )

    response = model.generate_content(raw_code)
    return response.text


# ---------------------------------------------------------------------------
# Structured Output Validation
# ---------------------------------------------------------------------------
def validate_response(text: str) -> bool:
    """
    Reject any response that does not contain both required section headers.
    This prevents malformed reports from ever reaching the rendering stage.
    """
    has_bug_report = "## BUG_REPORT" in text
    has_refactored = "## REFACTORED_CODE" in text
    return has_bug_report and has_refactored


# ---------------------------------------------------------------------------
# Phase 3: Deterministic Markdown Rendering
# ---------------------------------------------------------------------------
def render_output(response_text: str) -> None:
    """
    Apply rich Markdown rendering so that fenced code blocks receive
    language-aware syntax highlighting directly in the terminal.
    """
    console.print()
    console.print(
        Panel.fit(
            "[bold green]Intelligent Code Reviewer & Explainer[/bold green]\n"
            "[dim]DecodeLabs  •  Project 4  •  Analytical Gatekeeper[/dim]",
            border_style="green",
            box=box.ROUNDED,
        )
    )
    console.print()
    console.print(Markdown(response_text))
    console.print()


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Intelligent Code Reviewer & Explainer – DecodeLabs Project 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python main.py\n"
            "  python main.py sample_buggy.py\n"
            "  python main.py path/to/your_script.js\n"
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        default="sample_buggy.py",
        help="Path to the source file to review (default: sample_buggy.py)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = args.file

    try:
        console.print(f"[cyan]→ Ingesting payload:[/cyan] {file_path}")
        raw_code = read_code_file(file_path)

        console.print("[cyan]→ Context orchestration (Gemini Analytical Gatekeeper)...[/cyan]")
        response = analyze_code(raw_code)

        console.print("[cyan]→ Validating structured output...[/cyan]")
        if not validate_response(response):
            console.print(
                Panel(
                    "[bold red]✗ Response Rejected[/bold red]\n\n"
                    "The model failed to return both required section headers:\n"
                    "  • ## BUG_REPORT\n"
                    "  • ## REFACTORED_CODE\n\n"
                    "Malformed reports are never pushed to the pipeline.",
                    border_style="red",
                    title="Validation Failed",
                )
            )
            console.print("\n[dim]Raw model response:[/dim]")
            console.print(response)
            sys.exit(1)

        console.print("[bold green]✓ Validation passed[/bold green]")
        render_output(response)

    except (FileNotFoundError, PermissionError, ValueError) as exc:
        console.print(f"[bold red]Input Error:[/bold red] {exc}")
        sys.exit(1)
    except UnicodeDecodeError as exc:
        console.print(f"[bold red]Encoding Error:[/bold red] {exc.reason}")
        sys.exit(1)
    except Exception as exc:
        console.print(f"[bold red]Unexpected Error:[/bold red] {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
