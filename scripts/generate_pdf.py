import re
import os
import subprocess
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
)

PROJECT = "RV64I Mini Verification Lab"
REPORT_DIR = Path("reports")
OUTPUT = REPORT_DIR / "verification-report.pdf"

TEST_SUITES = [
    ("ALU", REPORT_DIR / "alu-simulation.log"),
    ("Register File", REPORT_DIR / "register-file-simulation.log"),
    ("Integrated Datapath", REPORT_DIR / "datapath-simulation.log"),
]


def get_git_info():
    try:
        git_commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            text=True
        ).strip()

        git_branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True
        ).strip()

    except Exception:
        git_commit = "Unknown"
        git_branch = "Unknown"

    commit = (
        os.getenv("CI_COMMIT_SHORT_SHA")
        or os.getenv("GIT_COMMIT")
        or git_commit
    )

    branch = (
        os.getenv("CI_COMMIT_REF_NAME")
        or os.getenv("BRANCH_NAME")
        or git_branch
    )

    return commit, branch


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


def add_page_number(canvas, document):
    canvas.saveState()

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        20 * mm,
        12 * mm,
        "RV64I Mini Verification Lab"
    )

    canvas.drawRightString(
        190 * mm,
        12 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    commit, branch = get_git_info()
    generated = datetime.now().astimezone().strftime(
        "%d %b %Y, %I:%M:%S %p %Z"
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=26,
        textColor=colors.HexColor("#17365D"),
        alignment=TA_CENTER,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#17365D"),
        spaceBefore=12,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        parent=styles["Normal"],
        fontSize=8,
        leading=11,
    ))

    styles.add(ParagraphStyle(
        name="TestName",
        parent=styles["Normal"],
        fontSize=8,
        leading=10,
        wordWrap="CJK",
    ))

    story = []

    story.append(Paragraph(
        "RV64I Verification Test Report",
        styles["ReportTitle"]
    ))

    story.append(Paragraph(
        PROJECT,
        ParagraphStyle(
            "ProjectSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=11,
            textColor=colors.grey,
        )
    ))

    story.append(Spacer(1, 12))

    metadata = [
        ["Git Commit", commit],
        ["Branch", branch],
        ["Generated", generated],
        ["Simulation Tool", "Verilator"],
        ["HDL", "SystemVerilog"],
    ]

    metadata_table = Table(
        metadata,
        colWidths=[38 * mm, 130 * mm]
    )

    metadata_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF0F7")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#17365D")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(metadata_table)
    story.append(Spacer(1, 18))

    total_passed = 0
    total_failed = 0
    suite_results = []

    for suite_name, log_path in TEST_SUITES:
        passed, failed = parse_log(log_path)

        total_passed += len(passed)
        total_failed += len(failed)

        suite_results.append((suite_name, passed, failed))

    total = total_passed + total_failed
    overall_status = (
        "ALL TESTS PASSED"
        if total_failed == 0
        else "TESTS FAILED"
    )

    story.append(Paragraph(
        "Verification Summary",
        styles["SectionHeading"]
    ))

    summary_data = [
        ["Total Tests", "Passed", "Failed", "Status"],
        [
            str(total),
            str(total_passed),
            str(total_failed),
            overall_status,
        ],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[35 * mm, 35 * mm, 35 * mm, 63 * mm]
    )

    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EAF0F7")),
        ("TEXTCOLOR", (1, 1), (1, 1), colors.HexColor("#16803C")),
        ("TEXTCOLOR", (2, 1), (2, 1), colors.HexColor("#C62828")),
        ("TEXTCOLOR", (3, 1), (3, 1),
         colors.HexColor("#16803C" if total_failed == 0 else "#C62828")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 8))

    status_color = "#16803C" if total_failed == 0 else "#C62828"

    story.append(Paragraph(
        f'<font color="{status_color}"><b>{overall_status}</b></font>',
        styles["Heading2"]
    ))

    story.append(Paragraph(
        "Test Results by Suite",
        styles["SectionHeading"]
    ))

    suite_summary = [["Test Suite", "Passed", "Failed", "Total"]]

    for suite_name, passed, failed in suite_results:
        suite_summary.append([
            suite_name,
            str(len(passed)),
            str(len(failed)),
            str(len(passed) + len(failed)),
        ])

    suite_table = Table(
        suite_summary,
        colWidths=[80 * mm, 29 * mm, 29 * mm, 30 * mm]
    )

    suite_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17365D")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))

    story.append(suite_table)

    for suite_name, passed, failed in suite_results:
        story.append(Paragraph(
            f"{suite_name} — Individual Test Results",
            styles["SectionHeading"]
        ))

        rows = [["Test Case", "Result"]]

        for name in passed:
            rows.append([
                Paragraph(name, styles["TestName"]),
                "PASS",
            ])

        for name in failed:
            rows.append([
                Paragraph(name, styles["TestName"]),
                "FAIL",
            ])

        test_table = Table(
            rows,
            colWidths=[125 * mm, 43 * mm],
            repeatRows=1
        )

        test_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAF0F7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17365D")),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN", (1, 0), (1, -1), "CENTER"),
            ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#16803C")),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))

        for row_index in range(1, len(rows)):
            if rows[row_index][1] == "FAIL":
                test_table.setStyle(TableStyle([
                    ("TEXTCOLOR", (1, row_index), (1, row_index),
                     colors.HexColor("#C62828")),
                ]))

        story.append(KeepTogether([
            test_table,
            Spacer(1, 8),
        ]))

    story.append(Spacer(1, 15))

    story.append(Paragraph(
        "End of Verification Report",
        ParagraphStyle(
            "EndNote",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            textColor=colors.grey,
            fontSize=9,
        )
    ))

    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="RV64I Verification Test Report",
        author="RV64I Mini Verification Lab",
    )

    document.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    print(f"PDF report generated: {OUTPUT}")
    print(f"Total tests: {total}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(overall_status)

    if total_failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
