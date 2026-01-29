#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Loader Hook (UserPromptSubmit)

Reads the user prompt, performs semantic retrieval against the knowledge store,
and prints matched fragments as context to stdout.

Runs alongside smart_context_loader.py (which handles skill suggestions).
This hook handles knowledge fragment retrieval.
"""

import json
import sys

from utils.knowledge_retriever import format_results, retrieve


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        if not prompt or len(prompt.strip()) < 5:
            sys.exit(0)

        results = retrieve(prompt)

        if results:
            output = format_results(results)
            print(output)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Error in knowledge_loader: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
