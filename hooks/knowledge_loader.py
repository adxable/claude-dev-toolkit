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
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.knowledge_retriever import KnowledgeRetriever


def should_retrieve(prompt: str) -> bool:
    """
    Determine if we should attempt knowledge retrieval for this prompt.

    Skip retrieval for very short prompts, commands, or system messages.
    """
    # Skip empty or very short prompts
    if not prompt or len(prompt.strip()) < 10:
        return False

    prompt_lower = prompt.lower().strip()

    # Skip if it's just a command
    if prompt_lower.startswith('/') and len(prompt_lower.split()) == 1:
        return False

    # Skip common non-question patterns
    skip_patterns = [
        'yes', 'no', 'ok', 'okay', 'thanks', 'thank you',
        'continue', 'proceed', 'go ahead', 'stop', 'cancel',
        'good', 'great', 'perfect', 'nice', 'cool'
    ]
    if prompt_lower in skip_patterns:
        return False

    return True


def main():
    """Hook entry point - runs on UserPromptSubmit."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get("prompt", "")

        if not should_retrieve(prompt):
            sys.exit(0)

        # Get the retriever
        retriever = KnowledgeRetriever()

        # Retrieve and format relevant fragments
        output = retriever.retrieve_and_format(
            prompt=prompt,
            top_k=5,
            format_style="context"
        )

        if output:
            print(output)

            # Mark fragments as accessed
            results = retriever.retrieve(prompt, top_k=5)
            if results:
                fragments = [f for f, _ in results]
                try:
                    retriever.mark_retrieved(fragments)
                except Exception:
                    pass  # Don't fail if tracking update fails

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except ImportError:
        # Knowledge store not available - silently skip
        sys.exit(0)
    except Exception as e:
        print(f"Knowledge loader error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
