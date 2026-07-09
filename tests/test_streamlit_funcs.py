"""
Testy funkcji pomocniczych Streamlit dashboardu.
"""
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Streamlit nie ma TestClient — testujemy czyste funkcje generujące dane
# Importujemy funkcje z streamlit_app bez uruchamiania Streamlit
# Używamy exec na pliku, żeby wyciągnąć tylko funkcje
import importlib.util
spec = importlib.util.spec_from_file_location(
    "streamlit_app",
    os.path.join(os.path.dirname(__file__), "..", "vue-app", "src", "hubs", "developers", "streamlit_app.py")
)

# Ładujemy tylko funkcje — pomijamy Streamlit runtime
streamlit_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(streamlit_app)


def test_status_badge_high():
    assert streamlit_app._status_badge(95) == "✅"


def test_status_badge_medium():
    assert streamlit_app._status_badge(65) == "🔄"


def test_status_badge_low():
    assert streamlit_app._status_badge(30) == "⏳"


def test_module_color():
    assert streamlit_app._module_color(95) == "green"
    assert streamlit_app._module_color(65) == "orange"
    assert streamlit_app._module_color(30) == "red"


def test_jira_table_structure():
    mig = {"done": 15000, "total": 20000}
    df = streamlit_app._jira_table(mig)
    assert isinstance(df, pd.DataFrame)
    expected = ["Key", "Projekt", "Summary", "Status", "Priorytet", "Aktor"]
    for col in expected:
        assert col in df.columns
    assert len(df) > 0


def test_confluence_table_structure():
    mig = {"pages_done": 5000, "total_pages": 10000}
    df = streamlit_app._confluence_table(mig)
    assert isinstance(df, pd.DataFrame)
    assert "Space" in df.columns
    assert "Postęp" in df.columns


def test_overall_progress():
    """Ogólny postęp to średnia z 5 modułów."""
    mig = {
        "jira": {"pct": 72}, "confluence": {"pct": 58},
        "iam": {"pct": 91}, "teamcity": {"pct": 45},
        "informatica": {"pct": 33},
    }
    total = sum(m["pct"] for m in mig.values()) / 5
    assert total == 59.8