
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

passed = re.findall(r"^PASS: (.+)$", content, re.MULTILINE)
failed = re.findall(
    r"^FAIL: (.+?)(?: expected=.*)?$",
    content,
    re.MULTILINE
)

suite = ET.Element(
    "testsuite",
    name=input_log.stem,
    tests=str(len(passed) + len(failed)),
    failures=str(len(failed)),
    errors="0",
    skipped="0"
)

for name in passed:
    ET.SubElement(suite, "testcase", name=name)

for name in failed:
    testcase = ET.SubElement(suite, "testcase", name=name)
    failure = ET.SubElement(testcase, "failure", message="Test failed")
    failure.text = "See simulation log for expected and actual values."

ET.indent(suite, space="  ")

output_xml.parent.mkdir(parents=True, exist_ok=True)
ET.ElementTree(suite).write(
    output_xml,
    encoding="utf-8",
    xml_declaration=True
)

print(f"Generated JUnit report: {output_xml}")
print(f"Passed: {len(passed)}")
print(f"Failed: {len(failed)}")

if not passed and not failed:
    print("ERROR: No test cases found in simulation log.")
    sys.exit(1)

if failed:
    sys.exit(1)
