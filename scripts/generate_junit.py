
import sys
import re
import xml.etree.ElementTree as ET
from pathlib import Path

if len(sys.argv) != 3:
    print("Usage: python3 generate_junit.py INPUT_LOG OUTPUT_XML")
    sys.exit(1)

input_log = Path(sys.argv[1])
output_xml = Path(sys.argv[2])

if not input_log.exists():
    print(f"ERROR: Log file not found: {input_log}")
    sys.exit(1)

content = input_log.read_text(encoding="utf-8")

test_cases = []
current_test = None

# Parse both detailed logs and legacy PASS/FAIL logs
for line in content.splitlines():

    # New detailed logging format
    test_match = re.match(r"^\s*TEST\s*:\s*(.+?)\s*$", line)

    if test_match:
        current_test = {
            "name": test_match.group(1),
            "status": None
        }
        continue

    status_match = re.match(r"^\s*STATUS\s*:\s*(PASS|FAIL)\s*$", line)

    if status_match and current_test is not None:
        current_test["status"] = status_match.group(1)
        test_cases.append(current_test)
        current_test = None
        continue

    # Old logging format: PASS: test name
    legacy_pass = re.match(r"^PASS:\s*(.+)$", line)

    if legacy_pass:
        test_cases.append({
            "name": legacy_pass.group(1),
            "status": "PASS"
        })
        continue

    # Old logging format: FAIL: test name expected=... actual=...
    legacy_fail = re.match(
        r"^FAIL:\s*(.+?)(?:\s+expected=.*)?$",
        line
    )

    if legacy_fail:
        test_cases.append({
            "name": legacy_fail.group(1),
            "status": "FAIL"
        })


# Calculate test statistics
passed = sum(1 for test in test_cases if test["status"] == "PASS")
failed = sum(1 for test in test_cases if test["status"] == "FAIL")

# Create JUnit XML test suite
suite = ET.Element(
    "testsuite",
    name=input_log.stem,
    tests=str(len(test_cases)),
    failures=str(failed),
    errors="0",
    skipped="0"
)

# Add individual test cases
for test in test_cases:

    testcase = ET.SubElement(
        suite,
        "testcase",
        name=test["name"]
    )

    if test["status"] == "FAIL":
        failure = ET.SubElement(
            testcase,
            "failure",
            message="Test failed"
        )
        failure.text = "See simulation log for expected and actual values."


# Format and save XML
ET.indent(suite, space="  ")

output_xml.parent.mkdir(parents=True, exist_ok=True)

ET.ElementTree(suite).write(
    output_xml,
    encoding="utf-8",
    xml_declaration=True
)

print("--------------------------------")
print("JUNIT REPORT GENERATION")
print("--------------------------------")
print(f"Input log : {input_log}")
print(f"Output XML: {output_xml}")
print(f"Total     : {len(test_cases)}")
print(f"Passed    : {passed}")
print(f"Failed    : {failed}")

if not test_cases:
    print("ERROR: No test cases found in simulation log.")
    sys.exit(1)

if failed:
    print("VERIFICATION FAILED")
    sys.exit(1)

print("ALL TESTS PASSED")
