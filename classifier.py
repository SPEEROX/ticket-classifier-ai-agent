"""
AI-Driven Customer Support Ticket Classifier
Uses OpenAI API to classify messages by category and priority.
"""

import json
import sys
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
client = OpenAI()  # Reads OPENAI_API_KEY from environment

SYSTEM_PROMPT = """You are a support ticket classifier.
Classify the given message into:
- Category: Billing, Technical Issue, Account, General Inquiry
- Priority: High (urgent or blocking issues), Medium (moderate issues), Low (general or informational queries)

Return ONLY valid JSON with no extra text:
{
  "category": "",
  "priority": ""
}"""


def classify_message(message: str) -> dict:
    """
    Classify a single support message using the OpenAI API.

    Args:
        message: The customer support message text.

    Returns:
        A dict with keys: message, category, priority.

    Raises:
        ValueError: If the API response cannot be parsed as valid JSON.
        openai.OpenAIError: On API-level errors.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f'Message: "{message}"'},
        ],
        temperature=0,  # Deterministic for classification
        max_tokens=100,
        response_format={"type": "json_object"},  # Enforce JSON mode
    )

    raw = response.choices[0].message.content.strip()

    try:
        result = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from API: {raw!r}") from e

    # Validate expected keys
    for key in ("category", "priority"):
        if key not in result:
            raise ValueError(f"Missing key '{key}' in API response: {result}")

    return {
        "message": message,
        "category": result["category"],
        "priority": result["priority"],
    }


def classify_messages(messages: list[str]) -> list[dict]:
    """
    Classify a list of support messages.

    Args:
        messages: List of message strings.

    Returns:
        List of classification dicts (message, category, priority).
    """
    results = []
    for i, msg in enumerate(messages, 1):
        print(f"  [{i}/{len(messages)}] Classifying: {msg[:60]}...", file=sys.stderr)
        try:
            classified = classify_message(msg)
            results.append(classified)
        except Exception as e:
            # Graceful degradation: include error info instead of crashing
            print(f"  ⚠ Error on message {i}: {e}", file=sys.stderr)
            results.append(
                {
                    "message": msg,
                    "category": "Unknown",
                    "priority": "Unknown",
                    "error": str(e),
                }
            )
    return results


def main():
    # Default sample messages
    messages = [
        "My payment got deducted but service is not activated",
        "App crashes every time I login",
        "How to change my email address?",
        "I was charged twice for my subscription this month",
        "The dashboard doesn't load on Safari",
        "What are your business hours?",
        "I can't reset my password, the link is expired",
        "Need an invoice for my last purchase",
    ]

    # Allow JSON input from stdin: echo '["msg1","msg2"]' | python classifier.py
    if not sys.stdin.isatty():
        try:
            messages = json.load(sys.stdin)
            if not isinstance(messages, list):
                raise ValueError("Input must be a JSON array of strings.")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error reading input: {e}", file=sys.stderr)
            sys.exit(1)

    print(f"Classifying {len(messages)} message(s)...\n", file=sys.stderr)
    results = classify_messages(messages)

    # Pretty-print JSON output to stdout
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
