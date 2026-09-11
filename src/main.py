
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

URL_PATTERN = re.compile(
    r"\bhttps?://"
    r"(?:www\.)?"
    r"[A-Za-z0-9.-]+"
    r"(?:\.[A-Za-z]{2,})"
    r"(?:/[^\s<>'\"]*)?"
)
def extract_urls(text):
    #Extract HTTP and HTTPS URLs.

    return URL_PATTERN.findall(text)


PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\+\d{1,3}[\s.-]?)?"
    r"(?:\(\d{1,4}\)[\s.-]?)?"
    r"\d{2,4}"
    r"(?:[\s.-]\d{2,4}){2,3}"
    r"(?!\d)"
)
def extract_phones(text):
    #Extract phone numbers while allowing common formatting variations.

    return PHONE_PATTERN.findall(text)



CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d{4}[- ]?){3}\d{4}"
    r"(?!\d)"
)
def luhn_check(number):
    #Return True if a card number passes the Luhn checksum.

    digits = [int(digit) for digit in number]

    checksum = 0
    parity = len(digits) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0
def mask_card(number):
    #Mask all but the final four digits.

    digits = re.sub(r"\D", "", number)

    return "*" * (len(digits) - 4) + digits[-4:]
def extract_credit_cards(text):
    #Extract valid card-like numbers and return only masked values.

    cards = []

    for match in CARD_PATTERN.findall(text):
        digits = re.sub(r"\D", "", match)

        if len(digits) == 16 and luhn_check(digits):
            cards.append({
                "masked": mask_card(digits)
            })

    return cards

CURRENCY_PATTERN = re.compile(
    r"(?<![\w])"
    r"(?:"
    r"(?:USD|EUR|GBP|RWF|KES|KSh)\s?"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)"
    r"(?:\.\d{2})?"
    r"|"
    r"(?:[$€£])\s?"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)"
    r"(?:\.\d{2})?"
    r"|"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)"
    r"(?:\.\d{2})?\s?"
    r"(?:RWF|KES|KSh|USD|EUR|GBP)"
    r")"
    r"(?![\w])"
)
def extract_currencies(text):
    #Extract valid currency amounts from the raw text.
    return CURRENCY_PATTERN.findall(text)
def main():
    #Run the regex extraction program.

    text = read_input()

    if text is None:
        return

    if not validate_input(text):
        return

    results = {
        "emails": extract_emails(text),
        "urls": extract_urls(text),
        "phone_numbers": extract_phones(text),
        "credit_cards": extract_credit_cards(text),
        "currency_amounts": extract_currencies(text)
    }

    OUTPUT_FILE.write_text(
        json.dumps(results, indent=4),
        encoding="utf-8"
    )

    print("Extraction completed successfully.")
    print(f"Results saved to: {OUTPUT_FILE}")
    print(f"Emails found: {len(results['emails'])}")
    print(f"URLs found: {len(results['urls'])}")
    print(f"Phone numbers found: {len(results['phone_numbers'])}")
    print(f"Valid credit cards found: {len(results['credit_cards'])}")
    print(
        f"Currency amounts found: "
        f"{len(results['currency_amounts'])}"
    )


if __name__ == "__main__":
    main()
