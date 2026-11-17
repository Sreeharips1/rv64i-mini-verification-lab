
import sys
import re
import html
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT = "RV64I Mini Verification Lab"
REPORT_DIR = Path("reports")

TEST_SUITES = [
    ("ALU", REPORT_DIR / "alu-simulation.log"),
    ("Register File", REPORT_DIR / "register-file-simulation.log"),
    ("Integrated Datapath", REPORT_DIR / "datapath-simulation.log"),
]

def get_git_info():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True
        ).strip()

        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()

        return commit, branch
    except Exception:
        return "Unknown", "Unknown"


def parse_log(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing simulation log: {path}")

    content = path.read_text(encoding="utf-8")

    passed = re.findall(r"^PASS: (.+)$", content, re.MULTILINE)
    failed = re.findall(
        r"^FAIL: (.+?)(?: expected=.*)?$",
        content,
        re.MULTILINE
    )

    if not passed and not failed:
        raise ValueError(f"No test results found in {path}")

    return passed, failed


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    commit, branch = get_git_info()
    generated = datetime.now().astimezone().strftime("%d %b %Y, %I:%M:%S %p %Z")

    total_passed = 0
    total_failed = 0
    suite_sections = []

    for suite_name, log_path in TEST_SUITES:
        passed, failed = parse_log(log_path)

        total_passed += len(passed)
        total_failed += len(failed)

        rows = []

        for name in passed:
            rows.append(
                f'<tr><td>{html.escape(name)}</td>'
                '<td class="pass">PASS</td></tr>'
            )

        for name in failed:
            rows.append(
                f'<tr><td>{html.escape(name)}</td>'
                '<td class="fail">FAIL</td></tr>'
            )

        suite_sections.append(f"""
        <section>
            <h2>{html.escape(suite_name)}</h2>
            <p>Passed: {len(passed)} | Failed: {len(failed)}</p>
            <table>
                <tr><th>Test case</th><th>Status</th></tr>
                {''.join(rows)}
            </table>
        </section>
        """)

    total = total_passed + total_failed
    overall_status = "ALL TESTS PASSED" if total_failed == 0 else "TESTS FAILED"
    status_class = "pass" if total_failed == 0 else "fail"

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RV64I Verification Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    max-width: 950px;
    margin: 35px auto;
    padding: 20px;
    background: #f4f6f9;
    color: #222;
}}
header, section, .summary {{
    background: white;
    padding: 22px;
    margin-bottom: 20px;
    border-radius: 10px;
}}
h1 {{ color: #17365d; }}
.summary {{
    display: flex;
    justify-content: space-around;
    text-align: center;
    flex-wrap: wrap;
}}
.metric {{ font-size: 28px; font-weight: bold; }}
.pass {{ color: #16803c; font-weight: bold; }}
.fail {{ color: #c62828; font-weight: bold; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{
    padding: 11px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}}
th {{ background: #eaf0f7; }}
.meta {{ color: #555; }}
</style>
</head>
<body>
<header>
<h1>RV64I Verification Test Report</h1>
<p><strong>Project:</strong> {PROJECT}</p>
<p class="meta"><strong>Git commit:</strong> {html.escape(commit)}</p>
<p class="meta"><strong>Branch:</strong> {html.escape(branch)}</p>
<p class="meta"><strong>Generated:</strong> {html.escape(generated)}</p>
</header>

<div class="summary">
<div><div class="metric">{total}</div>Total Tests</div>
<div><div class="metric pass">{total_passed}</div>Passed</div>
<div><div class="metric fail">{total_failed}</div>Failed</div>
</div>

<section>
<h2 class="{status_class}">{overall_status}</h2>
</section>

{''.join(suite_sections)}

</body>
</html>
"""

    output = REPORT_DIR / "verification-report.html"
    output.write_text(document, encoding="utf-8")

    print(f"HTML report generated: {output}")
    print(f"Total tests: {total}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(overall_status)

    if total_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

import sys
import re
import html
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT = "RV64I Mini Verification Lab"
REPORT_DIR = Path("reports")

TEST_SUITES = [
    ("ALU", REPORT_DIR / "alu-simulation.log"),
    ("Register File", REPORT_DIR / "register-file-simulation.log"),
    ("Integrated Datapath", REPORT_DIR / "datapath-simulation.log"),
]

def get_git_info():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True
        ).strip()

        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()

        return commit, branch
    except Exception:
        return "Unknown", "Unknown"


def parse_log(path):
    if not path.exists():
        raise FileNotFoundError(f"Missing simulation log: {path}")

    content = path.read_text(encoding="utf-8")

    passed = re.findall(r"^PASS: (.+)$", content, re.MULTILINE)
    failed = re.findall(
        r"^FAIL: (.+?)(?: expected=.*)?$",
        content,
        re.MULTILINE
    )

    if not passed and not failed:
        raise ValueError(f"No test results found in {path}")

    return passed, failed


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    commit, branch = get_git_info()
    generated = datetime.now().astimezone().strftime("%d %b %Y, %I:%M:%S %p %Z")

    total_passed = 0
    total_failed = 0
    suite_sections = []

    for suite_name, log_path in TEST_SUITES:
        passed, failed = parse_log(log_path)

        total_passed += len(passed)
        total_failed += len(failed)

        rows = []

        for name in passed:
            rows.append(
                f'<tr><td>{html.escape(name)}</td>'
                '<td class="pass">PASS</td></tr>'
            )

        for name in failed:
            rows.append(
                f'<tr><td>{html.escape(name)}</td>'
                '<td class="fail">FAIL</td></tr>'
            )

        suite_sections.append(f"""
        <section>
            <h2>{html.escape(suite_name)}</h2>
            <p>Passed: {len(passed)} | Failed: {len(failed)}</p>
            <table>
                <tr><th>Test case</th><th>Status</th></tr>
                {''.join(rows)}
            </table>
        </section>
        """)

    total = total_passed + total_failed
    overall_status = "ALL TESTS PASSED" if total_failed == 0 else "TESTS FAILED"
    status_class = "pass" if total_failed == 0 else "fail"

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RV64I Verification Report</title>
<style>
body {{
    font-family: Arial, sans-serif;
    max-width: 950px;
    margin: 35px auto;
    padding: 20px;
    background: #f4f6f9;
    color: #222;
}}
header, section, .summary {{
    background: white;
    padding: 22px;
    margin-bottom: 20px;
    border-radius: 10px;
}}
h1 {{ color: #17365d; }}
.summary {{
    display: flex;
    justify-content: space-around;
    text-align: center;
    flex-wrap: wrap;
}}
.metric {{ font-size: 28px; font-weight: bold; }}
.pass {{ color: #16803c; font-weight: bold; }}
.fail {{ color: #c62828; font-weight: bold; }}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{
    padding: 11px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}}
th {{ background: #eaf0f7; }}
.meta {{ color: #555; }}
</style>
</head>
<body>
<header>
<h1>RV64I Verification Test Report</h1>
<p><strong>Project:</strong> {PROJECT}</p>
<p class="meta"><strong>Git commit:</strong> {html.escape(commit)}</p>
<p class="meta"><strong>Branch:</strong> {html.escape(branch)}</p>
<p class="meta"><strong>Generated:</strong> {html.escape(generated)}</p>
</header>

<div class="summary">
<div><div class="metric">{total}</div>Total Tests</div>
<div><div class="metric pass">{total_passed}</div>Passed</div>
<div><div class="metric fail">{total_failed}</div>Failed</div>
</div>

<section>
<h2 class="{status_class}">{overall_status}</h2>
</section>

{''.join(suite_sections)}

</body>
</html>
"""

    output = REPORT_DIR / "verification-report.html"
    output.write_text(document, encoding="utf-8")

    print(f"HTML report generated: {output}")
    print(f"Total tests: {total}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(overall_status)

    if total_failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
