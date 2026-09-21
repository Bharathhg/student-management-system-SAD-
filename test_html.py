"""
CI Test: Validates that templates/index.html contains
the correct HTML form field name attributes expected by app.py.

Rules:
- Input for student name must have: name="name"
- Input for USN must have:          name="usn"
- Input for department must have:   name="dept"
- Input for student name must have: id="name"

If any field name is wrong (e.g., name="student_name" instead of name="name"),
this test FAILS and the CI pipeline is blocked from deploying.
"""

import sys
from html.parser import HTMLParser

HTML_FILE = "templates/index.html"

# Required form fields: {name attribute: id attribute}
REQUIRED_FIELDS = {
    "name": "name",
    "usn": "usn",
    "dept": "dept",
}


class FormFieldParser(HTMLParser):
    """Parses HTML and collects all input field attributes."""
    def __init__(self):
        super().__init__()
        self.inputs = []  # List of {attr: value} dicts for each <input>

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            attr_dict = dict(attrs)
            self.inputs.append(attr_dict)


def run_tests():
    print(f"=== CI HTML Form Validation Test ===")
    print(f"Checking file: {HTML_FILE}\n")

    # Read the HTML file
    try:
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"FAIL: {HTML_FILE} not found!")
        sys.exit(1)

    # Parse all input fields
    parser = FormFieldParser()
    parser.feed(html_content)

    # Build a lookup: name_attr -> id_attr from discovered inputs
    found_fields = {}
    for inp in parser.inputs:
        inp_type = inp.get("type", "text")
        if inp_type == "submit":
            continue  # Skip submit buttons
        name_attr = inp.get("name", "")
        id_attr = inp.get("id", "")
        found_fields[name_attr] = id_attr

    print(f"Found form input fields: {found_fields}\n")

    failures = []

    # Check each required field
    for required_name, required_id in REQUIRED_FIELDS.items():
        if required_name not in found_fields:
            failures.append(
                f"FAIL: Missing input with name=\"{required_name}\". "
                f"Found names: {list(found_fields.keys())}"
            )
        else:
            actual_id = found_fields[required_name]
            if actual_id != required_id:
                failures.append(
                    f"FAIL: Input name=\"{required_name}\" has id=\"{actual_id}\" "
                    f"but expected id=\"{required_id}\"."
                )
            else:
                print(f"  PASS: name=\"{required_name}\" with id=\"{required_id}\" exists.")

    print()

    if failures:
        print("=== CI FAILED ===")
        for f in failures:
            print(f"  {f}")
        print("\nFix the HTML form field names to match what app.py expects.")
        sys.exit(1)
    else:
        print("=== CI PASSED: All required form fields are correct! ===")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
