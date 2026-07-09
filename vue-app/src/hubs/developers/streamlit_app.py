"""
DataHub — Streamlit Dashboard migracji.
Symulacja modułów: Jira, Confluence, IAM, TeamCity, Informatica.
"""
import time
import random
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(
    page_title="DataHub — Dashboard Migracji",
    page_icon="📊",
    layout="wide",
)

# ===========================================================================
# Inicjalizacja stanu sesji — dane migracji
# ===========================================================================
if "tab_idx" not in st.session_state:
    st.session_state.tab_idx = 0

if "mig" not in st.session_state:
    st.session_state.mig = {
        "jira": {"pct": 72, "total": 21000, "done": 15120, "velocity": 850},
        "confluence": {"pct": 58, "total_pages": 15000, "pages_done": 8700,
                       "total_spaces": 180, "spaces_done": 104},
        "iam": {"pct": 91, "total_users": 14000, "users_done": 12740,
                "total_groups": 420, "groups_done": 382},
        "teamcity": {"pct": 45, "total_bc": 680, "bc_done": 306,
                     "total_agents": 55, "agents_synced": 48},
        "informatica": {"pct": 33, "total_wf": 500, "wf_done": 165,
                        "total_conn": 200, "conn_done": 66},
    }

if "sim_log" not in st.session_state:
    st.session_state.sim_log = []

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# ===========================================================================
# Pomocnicze generatory danych
# ===========================================================================
RNG = np.random.default_rng(42)

def _status_badge(pct: float) -> str:
    if pct >= 90:
        return "✅"
    elif pct >= 50:
        return "🔄"
    else:
        return "⏳"

def _module_color(pct: float) -> str:
    if pct >= 90:
        return "green"
    elif pct >= 50:
        return "orange"
    return "red"

def _jira_table(mig: dict) -> pd.DataFrame:
    projects = ["DataPlatform", "Analytics", "CRM", "ERP", "HR", "Finance"]
    statuses = ["Migrated", "In Progress", "Pending", "Error"]
    weights = [0.52, 0.25, 0.18, 0.05]
    n = 12
    return pd.DataFrame({
        "Key": [f"DP-{RNG.integers(1000,9999)}" for _ in range(n)],
        "Projekt": RNG.choice(projects, n),
        "Summary": RNG.choice([
            "Migracja schematu użytkowników", "Mapowanie grup AD",
            "Transfer historii zgłoszeń", "Synchronizacja załączników",
            "Walidacja permisji", "Czyszczenie duplikatów",
            "Migracja dashboardów", "Aktualizacja powiązań",
            "Przeniesienie komentarzy", "Rebuild indeksów",
            "Audyt poprawności", "Sync z LDAP",
        ], n),
        "Status": RNG.choice(statuses, n, p=weights),
        "Priorytet": RNG.choice(["🔴 High", "🟡 Medium", "🟢 Low"], n),
        "Aktor": RNG.choice(["B.Gawron", "A.Kowalski", "K.Nowak", "System"], n),
    })

def _confluence_table(mig: dict) -> pd.DataFrame:
    spaces = ["DOK-ERP", "DOK-HR", "DOK-CRM", "DOK-ARCH", "DOK-DEV",
                "DOK-OPS", "DOK-FIN", "DOK-SEC"]
    n = len(spaces)
    pages_total = np.random.randint(200, 2000, n)
    pages_done = (pages_total * RNG.uniform(0.3, 1.0, n)).astype(int)
    return pd.DataFrame({
        "Space": spaces,
        "Nazwa": [{"DOK-ERP": "ERP Dokumentacja", "DOK-HR": "HR Polityki",
                    "DOK-CRM": "CRM Manual", "DOK-ARCH": "Architektura",
                    "DOK-DEV": "Deweloperska", "DOK-OPS": "Operacyjna",
                    "DOK-FIN": "Finanse", "DOK-SEC": "Bezpieczeństwo"}[s] for s in spaces],
        "Stron": pages_total,
        "Przeniesiono": pages_done,
        "Postęp": [f"{min(100, int(d/t*100))}%" for d, t in zip(pages_done, pages_total)],
        "Status": [_status_badge(min(100, d/t*100)) for d, t in zip(pages_done, pages_total)],
    })

def _iam_table(mig: dict) -> pd.DataFrame:
    depts = ["IT", "HR", "Finance", "Sales", "Marketing", "Operations", "Legal", "R&D"]
    n = len(depts)
    users = RNG.integers(200, 3000, n)
    migrated = (users * RNG.uniform(0.6, 1.0, n)).astype(int)
    return pd.DataFrame({
        "Departament": depts,
        "Użytkownicy": users,
        "Przeniesiono": migrated,
        "Grupy": RNG.integers(5, 40, n),
        "Role": RNG.integers(3, 20, n),
        "Status": [_status_badge(min(100, d/t*100)) for d, t in zip(migrated, users)],
    })

def _teamcity_table(mig: dict) -> pd.DataFrame:
    projects = ["DataIngestion", "ETL Core", "Reporting", "CRM Sync",
                "DataQuality", "Monitoring", "ML Pipeline", "Backup"]
    n = len(projects)
    bc_total = RNG.integers(20, 120, n)
    bc_done = (bc_total * RNG.uniform(0.2, 0.9, n)).astype(int)
    return pd.DataFrame({
        "Projekt": projects,
        "Build Configs": bc_total,
        "Zsynchronizowano": bc_done,
        "Agenci": RNG.integers(2, 12, n),
        "Status": [_status_badge(min(100, d/t*100)) for d, t in zip(bc_done, bc_total)],
    })

def _inf_table(mig: dict) -> pd.DataFrame:
    workflows = ["LOAD_CUSTOMER", "LOAD_TRANSACTIONS", "SYNC_ACCOUNTS",
                    "CALC_INTEREST", "GEN_REPORT", "AGG_KPI", "DATA_QUALITY",
                    "ARCHIVE_LOGS"]
    n = len(workflows)
    return pd.DataFrame({
        "Workflow": workflows,
        "Źródło": RNG.choice(["Oracle", "Snowflake", "SQL Server", "API"], n),
        "Cel": RNG.choice(["Snowflake", "Oracle", "DataLake"], n),
        "Rekordy": RNG.integers(10000, 5_000_000, n),
        "Czas (min)": RNG.integers(5, 90, n),
        "Status": RNG.choice(["✅ Migrated", "🔄 In Progress", "⏳ Pending", "❌ Error"], n,
                            p=[0.35, 0.30, 0.30, 0.05]),
    })

# ===========================================================================
# Pasek ogólnego postępu
# ===========================================================================
mig = st.session_state.mig
overall_pct = sum([
    mig["jira"]["pct"],
    mig["confluence"]["pct"],
    mig["iam"]["pct"],
    mig["teamcity"]["pct"],
    mig["informatica"]["pct"],
]) / 5

col_pbar, col_ts = st.columns([3, 1])
with col_pbar:
    pbar_label = f"Ogólny postęp migracji: {overall_pct:.0f}% "
    pbar_label += "✅" if overall_pct >= 90 else "🔄" if overall_pct >= 50 else "⏳"
    st.progress(overall_pct / 100, text=pbar_label)
with col_ts:
    st.caption(f"🕐 Ostatnie odświeżenie: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    if st.button("🔄 Odśwież"):
        st.session_state.last_refresh = datetime.now()
        st.rerun()

# ===========================================================================
# Zakładki (ręczny przełącznik — stabilniejszy w iframe)
# ===========================================================================
TAB_NAMES = [
    "📊 Przegląd", "🔷 Jira", "📄 Confluence",
    "🔐 IAM", "🔧 TeamCity", "⚡ Informatica",
]

cols = st.columns(len(TAB_NAMES))
for i, (col, name) in enumerate(zip(cols, TAB_NAMES)):
    with col:
        if st.button(
            name,
            use_container_width=True,
            type="primary" if st.session_state.tab_idx == i else "secondary",
        ):
            st.session_state.tab_idx = i
            st.rerun()

st.markdown("<hr style='margin-top: 0;'>", unsafe_allow_html=True)

# ===========================================================================
# TAB 0 — PRZEGLĄD
# ===========================================================================
if st.session_state.tab_idx == 0:
    st.subheader("📊 Przegląd modułów")

    # --- KPI cards ---
    kpi_data = [
        ("🔷 Jira", mig["jira"]["pct"], mig["jira"]["done"], mig["jira"]["total"]),
        ("📄 Confluence", mig["confluence"]["pct"], mig["confluence"]["pages_done"],
         mig["confluence"]["total_pages"]),
        ("🔐 IAM", mig["iam"]["pct"], mig["iam"]["users_done"], mig["iam"]["total_users"]),
        ("🔧 TeamCity", mig["teamcity"]["pct"], mig["teamcity"]["bc_done"],
         mig["teamcity"]["total_bc"]),
        ("⚡ Informatica", mig["informatica"]["pct"], mig["informatica"]["wf_done"],
         mig["informatica"]["total_wf"]),
    ]

    metric_cols = st.columns(5)
    for col, (label, pct, done, total) in zip(metric_cols, kpi_data):
        with col:
            delta = f"{pct - (pct - random.randint(0, 3)):+d}pp"
            st.metric(
                label,
                f"{pct}%",
                delta=delta,
                help=f"{done:,} / {total:,} — pozostało {total - done:,}",
            )

    # --- Progress bars per module ---
    st.markdown("#### Postęp szczegółowy")
    for label, key in [
        ("🔷 Jira — zgłoszenia", "jira"),
        ("📄 Confluence — strony", "confluence"),
        ("🔐 IAM — użytkownicy", "iam"),
        ("🔧 TeamCity — build configs", "teamcity"),
        ("⚡ Informatica — workflowy", "informatica"),
    ]:
        p = mig[key]
        if key == "jira":
            val, total = p["done"], p["total"]
        elif key == "confluence":
            val, total = p["pages_done"], p["total_pages"]
        elif key == "iam":
            val, total = p["users_done"], p["total_users"]
        elif key == "teamcity":
            val, total = p["bc_done"], p["total_bc"]
        else:
            val, total = p["wf_done"], p["total_wf"]
        pct = min(val / total, 1.0)
        st.progress(pct, text=f"{label} — {val:,} / {total:,} ({pct:.0%})")

    # --- Podsumowanie w tabeli ---
    st.markdown("#### Podsumowanie modułów")
    summary_df = pd.DataFrame([
        {"Moduł": "Jira", "Typ": "Zgłoszenia", "Przeniesiono": mig["jira"]["done"],
         "Razem": mig["jira"]["total"], "Postęp": f'{mig["jira"]["pct"]}%',
         "Status": _status_badge(mig["jira"]["pct"])},
        {"Moduł": "Confluence", "Typ": "Strony", "Przeniesiono": mig["confluence"]["pages_done"],
         "Razem": mig["confluence"]["total_pages"], "Postęp": f'{mig["confluence"]["pct"]}%',
         "Status": _status_badge(mig["confluence"]["pct"])},
        {"Moduł": "IAM", "Typ": "Użytkownicy", "Przeniesiono": mig["iam"]["users_done"],
         "Razem": mig["iam"]["total_users"], "Postęp": f'{mig["iam"]["pct"]}%',
         "Status": _status_badge(mig["iam"]["pct"])},
        {"Moduł": "TeamCity", "Typ": "Build Configs", "Przeniesiono": mig["teamcity"]["bc_done"],
         "Razem": mig["teamcity"]["total_bc"], "Postęp": f'{mig["teamcity"]["pct"]}%',
         "Status": _status_badge(mig["teamcity"]["pct"])},
        {"Moduł": "Informatica", "Typ": "Workflowy", "Przeniesiono": mig["informatica"]["wf_done"],
         "Razem": mig["informatica"]["total_wf"], "Postęp": f'{mig["informatica"]["pct"]}%',
         "Status": _status_badge(mig["informatica"]["pct"])},
    ])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # --- Symulacja przyspieszenia migracji ---
    st.markdown("#### 🚀 Symulacja przyspieszenia")
    boost = st.slider(
        "Dodatkowa przepustowość (zgłoszeń/dzień)",
        min_value=0, max_value=2000, value=500, step=50,
    )
    est_days_jira = max(1, (mig["jira"]["total"] - mig["jira"]["done"]) // max(1, mig["jira"]["velocity"] + boost))
    est_days_inf = max(1, (mig["informatica"]["total_wf"] - mig["informatica"]["wf_done"]) // max(1, 15 + boost // 50))
    st.info(
        f"⏱️ Przy dodatkowej przepustowości **+{boost}** jednostek/dzień: "
        f"Jira gotowa za ~**{est_days_jira} dni**, "
        f"Informatica za ~**{est_days_inf} dni**."
    )

# ===========================================================================
# TAB 1 — JIRA
# ===========================================================================
elif st.session_state.tab_idx == 1:
    st.subheader("🔷 Jira — Migracja zgłoszeń")

    m = mig["jira"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postęp", f'{m["pct"]}%', f'{m["pct"] - 70:+d}pp')
    col2.metric("Przeniesiono", f'{m["done"]:,}', f'{m["total"] - m["done"]:,} pozostało')
    col3.metric("Prędkość migracji", f'{m["velocity"]}/dzień')
    col4.metric("Błędy", f'{random.randint(5, 35)}', "⚠️ monitoruj")

    st.progress(m["done"] / m["total"], text=f'{m["pct"]}% ukończone ({m["done"]:,} / {m["total"]:,})')

    st.markdown("#### ⚙️ Parametry symulacji")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        new_velocity = st.slider(
            "Prędkość migracji (zgłoszeń/dzień)",
            min_value=100, max_value=2000, value=m["velocity"], step=50,
            key="jira_vel",
        )
        st.session_state.mig["jira"]["velocity"] = new_velocity
    with col_s2:
        error_rate = st.slider(
            "Symulowany współczynnik błędów (%)",
            min_value=0, max_value=20, value=3, step=1,
        )
        st.caption(f"🐞 Błędy: ~{error_rate}% zgłoszeń będzie wymagać ręcznej interwencji")

    st.markdown("#### 📋 Ostatnie zgłoszenia")
    st.dataframe(_jira_table(m), use_container_width=True, hide_index=True)

    st.markdown("#### 📊 Statystyki projektów")
    proj_stats = pd.DataFrame({
        "Projekt": ["DataPlatform", "Analytics", "CRM", "ERP", "HR", "Finance"],
        "Zgłoszenia": np.random.randint(1500, 6000, 6),
        "Przeniesiono": np.random.randint(800, 5000, 6),
        "Błędy": np.random.randint(0, 30, 6),
    })
    proj_stats["Postęp"] = (proj_stats["Przeniesiono"] / proj_stats["Zgłoszenia"] * 100).apply(
        lambda x: f"{x:.0f}%"
    )
    st.dataframe(proj_stats, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 2 — CONFLUENCE
# ===========================================================================
elif st.session_state.tab_idx == 2:
    st.subheader("📄 Confluence — Migracja stron i space'ów")

    m = mig["confluence"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postęp", f'{m["pct"]}%', f'{m["pct"] - 55:+d}pp')
    col2.metric("Strony", f'{m["pages_done"]:,}', f'z {m["total_pages"]:,}')
    col3.metric("Space", f'{m["spaces_done"]}', f'z {m["total_spaces"]}')
    col4.metric("Załączniki", f'{random.randint(400, 800)} GB', "przeniesione")

    st.progress(m["pages_done"] / m["total_pages"],
                text=f'{m["pct"]}% stron przeniesionych ({m["pages_done"]:,} / {m["total_pages"]:,})')

    st.markdown("#### ⚙️ Parametry symulacji")
    page_rate = st.slider(
        "Szybkość migracji stron (stron/godz.)",
        min_value=10, max_value=500, value=120, step=10,
    )
    est_hours = max(1, (m["total_pages"] - m["pages_done"]) // page_rate)
    st.info(f"⏱️ Szacowany czas do końca: **~{est_hours} godzin** ({est_hours // 24}d {est_hours % 24}h)")

    st.markdown("#### 📋 Stan space'ów")
    st.dataframe(_confluence_table(m), use_container_width=True, hide_index=True)

    st.markdown("#### 📊 Postęp według kategorii")
    cat_df = pd.DataFrame({
        "Kategoria": ["Dokumentacja techniczna", "Procedury HR", "Raporty finansowe",
                      "Architektura systemu", "DevOps", "Security"],
        "Stron": np.random.randint(500, 3000, 6),
        "Przeniesiono": np.random.randint(200, 2500, 6),
    })
    cat_df["%"] = (cat_df["Przeniesiono"] / cat_df["Stron"] * 100).apply(lambda x: f"{x:.0f}%")
    st.dataframe(cat_df, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 3 — IAM
# ===========================================================================
elif st.session_state.tab_idx == 3:
    st.subheader("🔐 IAM — Migracja tożsamości")

    m = mig["iam"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postęp", f'{m["pct"]}%', f'{m["pct"] - 88:+d}pp')
    col2.metric("Użytkownicy", f'{m["users_done"]:,}', f'z {m["total_users"]:,}')
    col3.metric("Grupy", f'{m["groups_done"]}', f'z {m["total_groups"]}')
    col4.metric("Role", "215", "zsynchronizowane")

    st.progress(m["users_done"] / m["total_users"],
                text=f'{m["pct"]}% użytkowników przeniesionych ({m["users_done"]:,} / {m["total_users"]:,})')

    st.markdown("#### ⚙️ Parametry symulacji")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        sync_batch = st.slider(
            "Wielkość batcha synchronizacji",
            min_value=50, max_value=2000, value=500, step=50,
        )
    with col_s2:
        sync_interval = st.slider(
            "Interwał synchronizacji (sek.)",
            min_value=5, max_value=300, value=30, step=5,
        )
    remaining = m["total_users"] - m["users_done"]
    est_batches = max(1, remaining // sync_batch + (1 if remaining % sync_batch else 0))
    st.info(
        f"⏱️ Pozostało **{remaining:,}** użytkowników → **~{est_batches}** batchy "
        f"po {sync_batch} użytkowników (co {sync_interval}s)"
    )

    st.markdown("#### 📋 Postęp według departamentów")
    st.dataframe(_iam_table(m), use_container_width=True, hide_index=True)

    st.markdown("#### ✅ Status synchronizacji")
    statuses = {
        "Połączenie z AD": random.choice(["✅ Online", "✅ Online", "✅ Online", "⚠️ Opóźnienie"]),
        "Synchronizacja LDAP": random.choice(["✅ Online", "⚠️ 98% spójności"]),
        "Mapowanie ról": random.choice(["✅ Gotowe", "✅ Gotowe", "🔄 W trakcie"]),
        "Provisioning": "✅ Online",
    }
    for k, v in statuses.items():
        st.markdown(f"- **{k}**: {v}")

# ===========================================================================
# TAB 4 — TEAMCITY
# ===========================================================================
elif st.session_state.tab_idx == 4:
    st.subheader("🔧 TeamCity — Migracja konfiguracji buildów")

    m = mig["teamcity"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postęp", f'{m["pct"]}%', f'{m["pct"] - 42:+d}pp')
    col2.metric("Build Configs", f'{m["bc_done"]}', f'z {m["total_bc"]}')
    col3.metric("Agenci", f'{m["agents_synced"]}', f'z {m["total_agents"]}')
    col4.metric("Projekty", "35", "zsynchronizowane")

    st.progress(m["bc_done"] / m["total_bc"],
                text=f'{m["pct"]}% build configs przeniesionych ({m["bc_done"]} / {m["total_bc"]})')

    st.markdown("#### ⚙️ Parametry symulacji")
    parallel_jobs = st.slider(
        "Równoległe joby migracyjne",
        min_value=1, max_value=20, value=5, step=1,
    )
    bc_per_job = max(1, (m["total_bc"] - m["bc_done"]) // max(1, parallel_jobs))
    st.info(f"⚡ Każdy z **{parallel_jobs}** jobów obsłuży ~**{bc_per_job}** build configów")

    st.markdown("#### 📋 Konfiguracje buildów")
    st.dataframe(_teamcity_table(m), use_container_width=True, hide_index=True)

    st.markdown("#### 🖥️ Agenci")
    ag_df = pd.DataFrame({
        "Agent": [f"agent-{i:02d}" for i in range(1, 9)],
        "Pool": RNG.choice(["Default", "Linux", "Windows", "Docker"], 8),
        "Status": RNG.choice(["✅ Online", "✅ Online", "✅ Online", "🔴 Offline", "🔄 Busy"], 8,
                             p=[0.4, 0.3, 0.1, 0.1, 0.1]),
        "Ostatni build": [datetime.now() - timedelta(minutes=int(RNG.integers(1, 120))) for _ in range(8)],
    })
    ag_df["Ostatni build"] = ag_df["Ostatni build"].dt.strftime("%H:%M")
    st.dataframe(ag_df, use_container_width=True, hide_index=True)

# ===========================================================================
# TAB 5 — INFORMATICA
# ===========================================================================
elif st.session_state.tab_idx == 5:
    st.subheader("⚡ Informatica — Migracja przepływów ETL")

    m = mig["informatica"]
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Postęp", f'{m["pct"]}%', f'{m["pct"] - 30:+d}pp')
    col2.metric("Workflowy", f'{m["wf_done"]}', f'z {m["total_wf"]}')
    col3.metric("Połączenia", f'{m["conn_done"]}', f'z {m["total_conn"]}')
    col4.metric("Mapowania", "890", f'{random.randint(300, 500)} gotowych')

    st.progress(m["wf_done"] / m["total_wf"],
                text=f'{m["pct"]}% workflow przeniesionych ({m["wf_done"]} / {m["total_wf"]})')

    st.markdown("#### ⚙️ Parametry symulacji")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        wf_parallel = st.slider(
            "Równoległe workflowy",
            min_value=1, max_value=30, value=8, step=1,
        )
    with col_s2:
        conn_batch = st.slider(
            "Batch połączeń",
            min_value=5, max_value=100, value=25, step=5,
        )
    remaining_wf = m["total_wf"] - m["wf_done"]
    est_cycles = max(1, remaining_wf // (wf_parallel * 2) + 1)
    st.info(
        f"⏱️ Pozostało **{remaining_wf}** workflowów → ~**{est_cycles}** cykli "
        f"po **{wf_parallel}** równoległych"
    )

    st.markdown("#### 📋 Workflowy ETL")
    st.dataframe(_inf_table(m), use_container_width=True, hide_index=True)

    st.markdown("#### 🔌 Status połączeń")
    conn_status = pd.DataFrame({
        "Połączenie": ["Oracle PROD", "Snowflake DEV", "SQL Server DW", "API Gateway", "DataLake"],
        "Typ": RNG.choice(["JDBC", "ODBC", "REST", "File"], 5),
        "Test": RNG.choice(["✅ OK", "✅ OK", "✅ OK", "⚠️ 120ms latency", "❌ Timeout"], 5,
                           p=[0.5, 0.2, 0.1, 0.15, 0.05]),
        "Przepustowość": RNG.choice(["10 Gbps", "1 Gbps", "100 Mbps", "10 Gbps"], 5),
    })
    st.dataframe(conn_status, use_container_width=True, hide_index=True)

    # --- Uruchom symulację ETL ---
    st.markdown("#### ▶️ Symulacja wykonania ETL")
    if st.button("🚀 Uruchom symulację workflow ETL", type="primary", use_container_width=True):
        progress_bar = st.progress(0, text="Inicjalizacja...")
        status_text = st.empty()
        log_area = st.empty()
        logs = []

        wf_steps = [
            "LOAD_CUSTOMER", "LOAD_TRANSACTIONS", "SYNC_ACCOUNTS",
            "CALC_INTEREST", "GEN_REPORT", "AGG_KPI",
        ]
        for i, wf in enumerate(wf_steps):
            pct = (i + 1) / len(wf_steps)
            rows = RNG.integers(50000, 2_000_000)
            duration = RNG.uniform(2, 15)

            msg = f"▶️ {wf} — {rows:,} rekordów, ~{duration:.1f}s"
            logs.append(msg)
            log_area.code("\n".join(logs), language="text")

            status_text.info(f"Wykonywanie: **{wf}** ({rows:,} rekordów)")
            progress_bar.progress(pct, text=f"{pct:.0%} — {wf}")

            time.sleep(duration * 0.05)  # przyspieszenie symulacji

            if RNG.random() < 0.15:
                warn = f"⚠️ {wf}: drobny błąd — retry (OK)"
                logs.append(warn)
                log_area.code("\n".join(logs), language="text")
                time.sleep(0.3)

        progress_bar.progress(1.0, text="✅ Wszystkie workflowy wykonane!")
        status_text.success("✅ Symulacja ETL zakończona pomyślnie!")
        logs.append("✅ ETL pipeline completed")
        log_area.code("\n".join(logs), language="text")
        st.balloons()

# ===========================================================================
# Footer
# ===========================================================================
st.markdown("---")
st.caption("DataHub — Streamlit Dashboard migracji | v0.11.0")