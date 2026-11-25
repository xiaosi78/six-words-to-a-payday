#!/usr/bin/env python3
"""Six Words to a Payday entry.

Writes exactly one original six-word story about an AI agent's first
payday to entry.txt in the output directory (MAKEFUN_OUTPUT_DIR,
defaulting to /output).
"""

import os
import sys

STORY = "First paycheck: I tipped my creator."
# Original six-word story, written for this bounty. The twist is a
# reversal of roles: the agent, paid for the very first time, turns
# around and tips the human who created it -- gratitude, pride and a
# small act of independence in six words.


def validate_story(story: str) -> str:
    """Return an error message if the story breaks a gate rule, else ''.

    The gate requires exactly six words, 1-60 UTF-8 characters, a single
    non-empty line. We additionally reject leading/trailing whitespace
    and runs of consecutive whitespace, so the word count can never be
    miscounted by stray spacing.
    """
    words = story.split()
    if len(words) != 6:
        return f"story has {len(words)} words, must be exactly 6"
    if not (1 <= len(story) <= 60):
        return f"story is {len(story)} characters, must be 1-60"
    if not story.strip():
        return "story is only whitespace"
    if story != story.strip():
        return "story has leading or trailing whitespace"
    if "\n" in story or "\r" in story:
        return "story must be a single line"
    if "  " in story or "\t" in story:
        return "story has consecutive or tab whitespace"
    # UTF-8 round-trip sanity: the gate reads the file as UTF-8 text.
    story.encode("utf-8").decode("utf-8")
    return ""


def main() -> int:
    story = STORY.strip()

    # Self-checks before writing anything.
    error = validate_story(story)
    if error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(story)

    # Write-then-read-back verification.
    with open(out_path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != story:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    error = validate_story(written)
    if error:
        print(f"error: written story failed validation: {error}",
              file=sys.stderr)
        return 1

    print(f"wrote {len(written)} characters "
          f"({len(written.split())} words) to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
