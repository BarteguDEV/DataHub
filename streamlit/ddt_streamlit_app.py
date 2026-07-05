"""
DDT — Developer Dev Tools (aplikacja Streamlit)
Uruchom: streamlit run ddt_streamlit_app.py --server.port 8501

Każdy moduł pokazuje dane w prosty sposób:
  st.subheader('Nazwa')
  st.write('opis')
  st.dataframe(df)
  st.plotly_chart(fig)
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# --------------------------------------------------------------
# KONFIGURACJA STRONY
# --------------------------------------------------------------
st.set_page_config(
    page_title="DDT — Developer Dev Tools",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------------------
# SZTUCZNE DANE
# --------------------------------------------------------------

def get_jira_data():
    statuses = ["Open", "In Progress", "In Review", "Done", "Blocked"]
    priorities = ["Critical", "High", "Medium", "Low"]
    types = ["Bug", "Story", "Task", "Epic"]
    projects = ["CORE-BANK", "PAYMENTS", "ONBOARDING", "REPORTING"]
    assignees = ["bgawron", "anowak", "kzielinski", "mwisniewski"]

    rows = []
    for i in range(20):
        created = datetime.now() - timedelta(days=random.randint(0, 30))
        rows.append({
            "Key": f"DDT-{1000+i}",
            "Summary": random.choice([
                "Implementacja endpointu API", "Fix NPE w module rozliczeń",
                "Dodanie logowania audytowego", "Optymalizacja zapytania SQL",
                "Refaktoryzacja serwisu", "Testy jednostkowe",
                "Dokumentacja API", "Migracja danych",
            ]),
            "Type": random.choice(types),
            "Priority": random.choice(priorities),
            "Status": random.choice(statuses),
            "Assignee": random.choice(assignees),
            "Project": random.choice(projects),
            "Created": created.strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


def get_confluence_data():
    spaces = ["DDT", "CORE", "PAY", "ARCH"]
    rows = []
    for i in range(10):
        rows.append({
            "Title": random.choice([
                "Architektura systemu", "API Reference v2",
                "Runbook — deploy", "Standardy kodowania",
                "Decision log Q2", "Schema bazy danych",
                "Instrukcja uruchomienia", "Policy bezpieczeństwa",
            ]),
            "Space": random.choice(spaces),
            "Author": random.choice(["bgawron", "anowak", "kzielinski"]),
            "Updated": (datetime.now() - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d"),
            "Views": random.randint(10, 500),
        })
    return pd.DataFrame(rows)


def get_iam_data():
    roles = ["Developer", "Senior Developer", "Tech Lead", "DevOps"]
    rows = []
    for i in range(15):
        rows.append({
            "Username": f"user{i+1:03d}",
            "Role": random.choice(roles),
            "Status": random.choice(["Active", "Active", "Active", "Inactive"]),
            "MFA": random.choice(["Yes", "No"]),
            "Last Login": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


def get_teamcity_data():
    projects = ["core-banking-api", "payment-gateway", "data-pipeline", "report-engine"]
    rows = []
    for i in range(15):
        started = datetime.now() - timedelta(hours=random.randint(0, 72))
        rows.append({
            "Build": f"TC-{10000+i}",
            "Project": random.choice(projects),
            "Branch": random.choice(["main", "develop", "feature/new-api", "fix/NPE-123"]),
            "Status": random.choice(["Success", "Success", "Success", "Failed", "Running"]),
            "Started": started.strftime("%m-%d %H:%M"),
            "Duration": f"{random.randint(1, 30)}m",
        })
    return pd.DataFrame(rows)


def get_informatica_data():
    rows = []
    for i in range(12):
        rows.append({
            "Workflow": random.choice([
                "wf_LOAD_CUSTOMER", "wf_LOAD_TRANSACTIONS", "wf_SYNC_ACCOUNTS",
                "wf_CALC_INTEREST", "wf_GEN_REPORT", "wf_AGG_DAILY_KPI",
            ]),
            "Folder": random.choice(["PROD_ETL", "DEV_ETL"]),
            "Status": random.choice(["Succeeded", "Succeeded", "Succeeded", "Failed", "Running"]),
            "Rows": random.randint(1000, 5000000),
            "Start Time": (datetime.now() - timedelta(hours=random.randint(0, 48))).strftime("%H:%M"),
        })
    return pd.DataFrame(rows)

# --------------------------------------------------------------
# INTERFEJS
# --------------------------------------------------------------

# --------------------------------------------------------------
# PRZYCISK ZAMKNIJ STREAMLIT (zawsze na górze sidebaru)
# --------------------------------------------------------------
st.sidebar.markdown(
    """
    <style>
    div.close-btn {
        margin-bottom: 16px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    div.close-btn > a {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 12px 16px;
        border-radius: 8px;
        border: 1px solid #ff1744;
        background: rgba(255,23,68,0.08);
        color: #ff5252;
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.15s;
        font-family: 'Inter', -apple-system, sans-serif;
        cursor: pointer;
    }
    div.close-btn > a:hover {
        background: #ff1744;
        color: #fff;
    }
    </style>
    <div class="close-btn">
        <a href="http://localhost:3000" target="_self">
            ✕ Zamknij Streamlit
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("## ⚙️ DDT")
st.sidebar.markdown("Zalogowany: **bgawron** • Developer")

module = st.sidebar.radio(
    "Wybierz moduł",
    ["Home", "Jira", "Confluence", "IAM", "TeamCity", "Informatica"],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("Streamlit • v0.1.0 POC")

# --------------------------------------------------------------
# HOME
# --------------------------------------------------------------
if module == "Home":
    st.title("⚙️ DDT — Developer Dev Tools")
    st.write("Centralny zestaw narzędzi developerskich. Wybierz moduł z bocznego menu.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Zadania Jira", "24", "+3 dziś")
    with col2:
        st.metric("Strony Confluence", "10", "2 nowe")
    with col3:
        st.metric("Użytkownicy IAM", "15", "")
    with col4:
        st.metric("Buildy dziś", "12", "90% pass")

    st.subheader("Ostatnie aktywności")
    st.write("""
    - **bgawron** zaktualizował DDT-1042 *(15 min temu)*
    - **anowak** dodał stronę 'API Reference v2' *(1h temu)*
    - **kzielinski** uruchomił build TC-10042 *(2h temu)*
    - **mwisniewski** zatwierdził workflow w PowerCenter *(3h temu)*
    """)

# --------------------------------------------------------------
# JIRA
# --------------------------------------------------------------
elif module == "Jira":
    st.title("🔧 Jira Integration")
    st.write("Zarządzanie zadaniami, sprintami i workflow.")

    df = get_jira_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open", len(df[df["Status"] == "Open"]))
    with col2:
        st.metric("In Progress", len(df[df["Status"] == "In Progress"]))
    with col3:
        st.metric("Done", len(df[df["Status"] == "Done"]))
    with col4:
        st.metric("Blocked", len(df[df["Status"] == "Blocked"]))

    st.subheader("Tickets by Status")
    fig = px.bar(
        df["Status"].value_counts().reset_index(),
        x="Status", y="count",
        color="Status",
        color_discrete_map={
            "Open": "#00e5ff", "In Progress": "#ff9100",
            "In Review": "#536dfe", "Done": "#00c853", "Blocked": "#ff1744",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------
# CONFLUENCE
# --------------------------------------------------------------
elif module == "Confluence":
    st.title("📋 Confluence Space")
    st.write("Dokumentacja techniczna, wiki i baza wiedzy.")

    df = get_confluence_data()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Opublikowane", len(df))
    with col2:
        st.metric("Łącznie wyświetleń", f"{df['Views'].sum():,}")
    with col3:
        st.metric("Przestrzenie", df["Space"].nunique())

    st.subheader("Strony per Space")
    fig = px.bar(
        df["Space"].value_counts().reset_index(),
        x="Space", y="count",
        color="count",
        color_continuous_scale=["#1a237e", "#00e5ff"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------
# IAM
# --------------------------------------------------------------
elif module == "IAM":
    st.title("🔐 IAM Manager")
    st.write("Zarządzanie dostępami, rolami i uprawnieniami.")

    df = get_iam_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Aktywni", len(df[df["Status"] == "Active"]))
    with col2:
        st.metric("MFA Enabled", len(df[df["MFA"] == "Yes"]))
    with col3:
        st.metric("Role", df["Role"].nunique())
    with col4:
        st.metric("Nieaktywni", len(df[df["Status"] == "Inactive"]))

    st.subheader("Struktura ról")
    fig = px.pie(
        df["Role"].value_counts().reset_index(),
        values="count", names="Role",
        color_discrete_sequence=["#00c853", "#00e5ff", "#536dfe", "#ff9100"],
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------
# TEAMCITY
# --------------------------------------------------------------
elif module == "TeamCity":
    st.title("🔄 TeamCity CI/CD")
    st.write("Pipeline'y budowania, testowania i deploy'u.")

    df = get_teamcity_data()
    success = len(df[df["Status"] == "Success"])
    failed = len(df[df["Status"] == "Failed"])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Passed", success)
    with col2:
        st.metric("Failed", failed)
    with col3:
        rate = success / max(len(df) - len(df[df["Status"] == "Running"]), 1) * 100
        st.metric("Pass Rate", f"{rate:.0f}%")

    st.subheader("Build Status")
    fig = px.pie(
        df["Status"].value_counts().reset_index(),
        values="count", names="Status",
        color_discrete_map={
            "Success": "#00c853", "Failed": "#ff1744",
            "Running": "#00e5ff", "Pending": "#ff9100",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(df, use_container_width=True, hide_index=True)

# --------------------------------------------------------------
# INFORMATICA
# --------------------------------------------------------------
elif module == "Informatica":
    st.title("🗄️ Informatica PowerCenter")
    st.write("Monitorowanie workflow ETL i przetwarzania danych.")

    df = get_informatica_data()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Succeeded", len(df[df["Status"] == "Succeeded"]))
    with col2:
        st.metric("Failed", len(df[df["Status"] == "Failed"]))
    with col3:
        st.metric("Running", len(df[df["Status"] == "Running"]))
    with col4:
        st.metric("Rows total", f"{df['Rows'].sum():,}")

    st.subheader("Workflow Status")
    fig = px.bar(
        df["Status"].value_counts().reset_index(),
        x="Status", y="count",
        color="Status",
        color_discrete_map={
            "Succeeded": "#00c853", "Failed": "#ff1744",
            "Running": "#00e5ff", "Aborted": "#ff9100",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Raw data")
    st.dataframe(df, use_container_width=True, hide_index=True)
