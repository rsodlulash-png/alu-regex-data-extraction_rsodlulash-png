
#!/usr/bin/env python3

import re
import json
from pathlib import Path
INPUT_FILE = Path("input/raw-text.txt")
OUTPUT_FILE = Path("output/sample-output.json")


def read_input():
    #Read raw text from the input file.
    try:
        text = INPUT_FILE.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} was not found.")
        return None

    return text
def validate_input(text):
    #Perform basic defensive checks on incoming text.

    if not text:
        print("Error: input is empty.")
        return False

    # Prevent processing unexpectedly huge input.
    max_size = 1_000_000

    if len(text) > max_size:
        print("Error: input is too large.")
        return False

    return True

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+\b"
)

ALU_EMAIL_PATTERN = re.compile(
    r"^[a-z]\.[a-z]+"
    r"@(alueducation\.com|alumni\.alueducation\.com|si\.alueducation\.com)$"
)
def classify_email(email):
    #Classify valid ALU emails by their official domain.

    if not ALU_EMAIL_PATTERN.fullmatch(email):
        return "invalid"

    if email.endswith("@alueducation.com"):
        return "ALU official"

    if email.endswith("@alumni.alueducation.com"):
        return "ALU alumni"

    if email.endswith("@si.alueducation.com"):
        return "ALU SI"

    return "other"

def extract_emails(text):
#Extract valid email addresses from the raw text.

    found = EMAIL_PATTERN.findall(text)

    valid = []

    for email in found:
        if classify_email(email) != "invalid":
            valid.append({
                "email": email,
                "type": classify_email(email)
            })

    return valid

