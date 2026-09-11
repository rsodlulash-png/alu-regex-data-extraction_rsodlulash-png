# ALU Facilitator Support API - Regex Data Extraction

## Project Overview

This project is a Python-based regex data extraction program.

The program processes raw text representing data received from an external **ALU Facilitator Support API**. The incoming data is treated as untrusted input, and regular expressions are used to identify and extract useful structured information.

The program extracts five types of data:

* Email addresses
* URLs
* Phone numbers
* Credit card numbers
* Currency amounts

The extracted information is saved in a structured JSON file.

## Project Purpose

The purpose of this project is to demonstrate how regular expressions can be used to process large amounts of raw text and convert useful information into structured data.

The raw text contains realistic facilitator support information, including:

* Facilitator names
* ALU email addresses
* Alternative email addresses
* Phone numbers
* Facilitator profile URLs
* Financial information
* Invalid data
* Malformed input
* Security test data

## Project Structure

```text
alu-regex-data-extraction_rsodlulash-png/
├── input/
│   └── raw-text.txt
├── src/
│   └── main.py
├── output/
│   └── sample-output.json
└── README.md
```

### `input/raw-text.txt`

Contains the raw facilitator support API data that the program processes.

### `src/main.py`

Contains the Python program, regular expressions, validation functions, extraction functions, and security checks.

### `output/sample-output.json`

Contains the structured results produced by the program.

### `README.md`

Contains the project documentation and instructions.

## Requirements

* Python 3
  
The project uses Python's built-in:

* `re` module for regular expressions
* `json` module for JSON output
* `pathlib` for file handling

## How to Run the Program

From the project root directory, run:

```bash
python3 src/main.py
```

If the program runs successfully, it will display information similar to:

```text
Extraction completed successfully.
Results saved to: output/sample-output.json
Emails found: 4
URLs found: 4
Phone numbers found: 5
Valid credit cards found: 2
Currency amounts found: 7
```

The exact numbers depend on the contents of the input file and the validation rules.

# Data Extraction

## 1. Email Addresses

The email regex identifies emails using the following format:

```text
initial.surname@domain
```

Examples from the facilitator data include:

```text
n.mokoena@alueducation.com
n.mokoena@gmail.com
t.molefe@alumni.alueducation.com
a.kamanzi@si.alueducation.com
```

The email pattern supports the following domains in the sample data:

* `alueducation.com`
* `alumni.alueducation.com`
* `si.alueducation.com`
* `gmail.com`

Malformed email addresses are not accepted.

Examples of invalid emails in the test data include:

```text
bad-email@@example.com
wrong-email@.com
another-invalid-email@
facilitator@alueducation
@alueducation.com
```

## 2. ALU Email Validation

A separate ALU email pattern is used to validate official ALU email addresses.

The expected format is:

```text
initial.surname@ALU-domain
```

The supported ALU domains are:

```text
@alueducation.com
@alumni.alueducation.com
@si.alueducation.com
```

For example:

```text
n.mokoena@alueducation.com
```

is classified as:

```text
ALU official
```

While:

```text
t.molefe@alumni.alueducation.com
```

is classified as:

```text
ALU alumni
```

And:

```text
a.kamanzi@si.alueducation.com
```

is classified as:

```text
ALU SI
```

An alternative Gmail address such as:

```text
n.mokoena@gmail.com
```

is not classified as an ALU email.

## 3. URLs

The URL regex extracts HTTP and HTTPS URLs.

Examples include:

```text
https://www.alueducation.com/facilitators/naledi-mokoena
https://alumni.alueducation.com/facilitators/thabo-molefe
https://si.alueducation.com/facilitators/aisha-kamanzi
https://www.example.org/help/facilitators
```

The pattern supports:

* `http://`
* `https://`
* Optional `www.`
* Domain names
* URL paths

Invalid URLs in the input are ignored.

Examples:

```text
https://
http://
www.invalid-url
```

## 4. Phone Numbers

The phone regex supports common phone-number formats.

Examples from the input include:

```text
+250 788 421 936
+27 (71) 234-9087
+250-783-555-219
0788 654 321
```

The program is designed to handle variations such as:

* International country codes
* Spaces
* Hyphens
* Parentheses
* Local phone-number formats

Malformed values such as:

```text
12345
+250
+27
```

are not considered valid phone numbers.

## 5. Credit Card Numbers

The program identifies card-like numbers containing 16 digits.

The regex supports common separators such as:

```text
4111 1111 1111 1111
5500-0000-0000-0004
```

After a card number is extracted, the program uses the **Luhn algorithm** to check whether the number passes the required checksum.

Invalid card-like values such as:

```text
4111-1111-1111
1234 5678 9012 3456
```

are rejected.

### Security

Credit card numbers are not written to the output in full.

Instead, they are masked so that only the final four digits are visible.

For example:

```text
4111 1111 1111 1111
```

becomes something similar to:

```text
************1111
```

This reduces unnecessary exposure of sensitive information.

# 6. Currency Amounts

The currency regex extracts realistic currency amounts from the facilitator support data.

The project currently supports:

* RWF
* USD
* EUR
* GBP
* KES / KSh
* `$`
* `€`
* `£`

Examples from the input include:

```text
RWF 250,000
RWF 350,000
USD 1,500.00
$1,250.50
€850.75
£2,000
KSh 45,000
```

The pattern supports:

* Currency codes before amounts
* Currency codes after amounts
* Currency symbols
* Thousands separators
* Decimal amounts

Malformed currency values are included in the input as negative test cases:

```text
RWF abc
USD
$hello
€xyz
```

These should not be extracted as valid currency amounts.

# Security Considerations

The data received from an external API is treated as **untrusted input**.

The program demonstrates basic defensive programming by:

* Checking that the input exists
* Rejecting empty input
* Limiting the maximum input size
* Using regular expressions to identify expected patterns
* Ignoring malformed data
* Validating extracted credit card numbers using the Luhn algorithm
* Masking credit card numbers before writing them to output
* Never executing extracted text as Python code
* Never executing HTML or JavaScript from the input
* Never treating SQL-like strings as database commands

The raw input contains security test examples such as:

```text
<script>alert("test")</script>
<img src="javascript:alert('xss')">

DROP TABLE facilitators;
DROP TABLE support_cases;

' OR '1'='1
"; DELETE FROM facilitators; --
```

These values are treated only as **text**.

The program does not execute them.

No `eval()`, `exec()`, shell execution, or database execution is performed on extracted input.

# Input Realism and Testing

The input file was designed to simulate realistic data returned from a facilitator support API.

It contains a mixture of:

### Valid data

```text
n.mokoena@alueducation.com
+250 788 421 936
https://www.alueducation.com/facilitators/naledi-mokoena
RWF 250,000
```

### Alternative data

```text
n.mokoena@gmail.com
```

### Different formatting

```text
+250-783-555-219
+27 (71) 234-9087
$1,250.50
€850.75
```

### Invalid data

```text
bad-email@@example.com
https://
RWF abc
12345
```

### Security test data

```text
<script>alert("test")</script>
DROP TABLE facilitators;
' OR '1'='1
```

This mixture allows the program to demonstrate both **successful extraction** and **defensive handling of unexpected input**.

# Testing the Python File

Before running the complete program, Python syntax can be checked with:

```bash
python3 -m py_compile src/main.py
```

If there are no errors, run:

```bash
python3 src/main.py
```

Then inspect the generated file:

```bash
cat output/sample-output.json
```

# Conclusion

This project demonstrates how Python regular expressions can be used to extract structured information from realistic raw API data.

The program focuses on:

* Regex-based extraction
* Input validation
* Realistic data variations
* Security awareness
* Sensitive-data protection
* Structured JSON output

The final result converts unstructured facilitator support information into useful structured data while treating incoming information as untrusted.



