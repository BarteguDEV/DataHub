"""
Test generowania raportów AI — sprawdza czy skrypt kończy się sukcesem i pliki istnieją.
"""
import subprocess
import os
import sys


REPORTS_DIR = os.path.join(os.path.dirname(__file__), "..", "ai-reports")
SCRIPT = os.path.join(os.path.dirname(__file__), "..", "generate_ai_reports.py")

EXPECTED_REPORTS = [
    "sql-performance-advisor.html",
    "sql-code-review.html",
    "sql-lineage.html",
    "etl-dependency.html",
    "etl-complexity.html",
    "data-flow.html",
    "duplicate-logic.html",
    "data-mapping.html",
    "deployment-risk.html",
    "oracle-impact.html",
    "data-quality.html",
    "test-generator.html",
    "doc-generator.html",
    "release-summary.html",
    "scheduler-optimization.html",
]


def test_generate_ai_reports_exit_code():
    """Skrypt generowania raportów kończy się z kodem 0."""
    if not os.path.exists(SCRIPT):
        print(f"[SKIP] {SCRIPT} nie istnieje — pomijam")
        return
    result = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Skrypt zakończył się błędem:\n{result.stderr}"


def test_all_reports_exist():
    """Wszystkie 15 raportów istnieje w katalogu ai-reports/."""
    if not os.path.exists(REPORTS_DIR):
        print(f"[SKIP] {REPORTS_DIR} nie istnieje — pomijam")
        return
    for report in EXPECTED_REPORTS:
        path = os.path.join(REPORTS_DIR, report)
        assert os.path.exists(path), f"Brak raportu: {report}"
        assert os.path.getsize(path) > 0, f"Raport pusty: {report}"


def test_reports_have_title():
    """Każdy raport HTML zawiera tytuł."""
    if not os.path.exists(REPORTS_DIR):
        print(f"[SKIP] {REPORTS_DIR} nie istnieje — pomijam")
        return
    for report in EXPECTED_REPORTS:
        path = os.path.join(REPORTS_DIR, report)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                content = f.read()
                assert "<title>" in content or "<h1" in content, f"Brak tytułu w: {report}"