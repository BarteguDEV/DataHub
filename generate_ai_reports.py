"""
Generator pełnych raportów HTML dla AI Hub.
Uruchom:  python generate_ai_reports.py
Generuje 15 plików .html do katalogu ai-reports/
"""

import os
import html as html_mod

OUT = os.path.join(os.path.dirname(__file__), "ai-reports")

# ────────────────────── HEAD / FOOTER ──────────────────────
HEAD = """<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — AI Generated</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Inter', -apple-system, sans-serif; background: #0b0d11; color: #e8eaed; padding: 40px; }}
  .container {{ max-width: 1000px; margin: 0 auto; }}
  .header {{ margin-bottom: 40px; }}
  .header h1 {{ font-size: 28px; font-weight: 700; color: {accent}; }}
  .header .meta {{ color: rgba(232,234,237,0.4); font-size: 13px; margin-top: 8px; }}
  .kpi-row {{ display:grid; grid-template-columns: repeat(4,1fr); gap:16px; }}
  .kpi {{ }}
  .kpi-num {{ font-size:28px; font-weight:700; color:{accent}; }}
  .kpi-label {{ font-size:12px; color:rgba(232,234,237,0.5); margin-top:4px; }}
  .section {{ background:#16181f; border:1px solid rgba(255,255,255,0.08); border-radius:12px; padding:24px; margin-bottom:24px; }}
  .section h2 {{ font-size:18px; font-weight:600; margin-bottom:16px; color:{accent2}; }}
  .row {{ display:flex; align-items:center; gap:12px; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.04); }}
  .row:last-child {{ border:none; }}
  .name {{ font-family:'JetBrains Mono',monospace; font-size:13px; color:#e8eaed; flex:1; }}
  .badge {{ font-size:11px; padding:2px 10px; border-radius:100px; }}
  .badge-green {{ background:rgba(0,200,83,0.1); color:#00c853; }}
  .badge-blue {{ background:rgba(83,109,254,0.1); color:#536dfe; }}
  .badge-red {{ background:rgba(255,23,68,0.1); color:#ff1744; }}
  .badge-amber {{ background:rgba(255,145,0,0.1); color:#ff9100; }}
  .badge-purple {{ background:rgba(124,77,255,0.1); color:#7c4dff; }}
  .tag {{ display:inline-block; font-size:11px; padding:2px 8px; border-radius:4px; background:rgba(255,255,255,0.04); color:rgba(232,234,237,0.5); margin-right:4px; }}
  .sql {{ background:#0b0d11; border-radius:8px; padding:16px; font-family:'JetBrains Mono',monospace; font-size:12px; line-height:1.6; color:rgba(232,234,237,0.7); overflow-x:auto; margin-top:12px; }}
  .key {{ color:#536dfe; }}
  .tref {{ color:#00e5ff; }}
  .recommend {{ padding:12px 16px; border-radius:8px; margin-bottom:8px; display:flex; gap:12px; align-items:flex-start; }}
  .recommend-icon {{ font-size:18px; flex-shrink:0; }}
  .recommend-text {{ font-size:13px; line-height:1.5; color:rgba(232,234,237,0.8); }}
  .rec-high {{ background:rgba(0,200,83,0.06); border-left:3px solid #00c853; }}
  .rec-med {{ background:rgba(83,109,254,0.06); border-left:3px solid #536dfe; }}
  .rec-low {{ background:rgba(255,145,0,0.06); border-left:3px solid #ff9100; }}
  .gantt {{ background:#0b0d11; border-radius:8px; padding:20px; margin-top:12px; }}
  .gantt-title {{ font-size:11px; font-weight:600; color:rgba(232,234,237,0.4); margin-bottom:16px; letter-spacing:0.5px; }}
  .gantt-row {{ display:flex; align-items:center; gap:12px; margin-bottom:10px; }}
  .gantt-row:last-child {{ margin-bottom:0; }}
  .gantt-label {{ font-family:'JetBrains Mono',monospace; font-size:11px; color:#e8eaed; width:200px; flex-shrink:0; text-align:right; }}
  .gantt-track {{ flex:1; height:22px; position:relative; background:rgba(255,255,255,0.03); border-radius:4px; overflow:visible; }}
  .gantt-bar {{ position:absolute; top:0; left:0; height:100%; border-radius:4px; min-width:4px; display:flex; align-items:center; padding:0 8px; }}
  .gantt-bar span {{ font-size:9px; font-weight:600; color:#000; white-space:nowrap; }}
  .gantt-collision {{ position:absolute; top:-4px; width:14px; height:30px; background:rgba(255,23,68,0.2); border:1px dashed #ff1744; border-radius:3px; z-index:2; }}
  .gantt-footer {{ display:flex; justify-content:space-between; font-size:10px; color:rgba(232,234,237,0.3); margin-top:8px; font-family:'JetBrains Mono',monospace; }}
  .hbar {{ display:flex; align-items:center; gap:12px; padding:6px 0; }}
  .hbar-label {{ font-size:12px; color:rgba(232,234,237,0.6); width:120px; flex-shrink:0; }}
  .hbar-track {{ flex:1; height:18px; background:rgba(255,255,255,0.03); border-radius:100px; overflow:hidden; position:relative; }}
  .hbar-fill {{ height:100%; border-radius:100px; display:flex; align-items:center; justify-content:flex-end; padding:0 8px; min-width:20px; }}
  .hbar-fill span {{ font-size:9px; font-weight:700; color:#000; }}
  .hbar-value {{ font-size:12px; font-weight:600; width:60px; flex-shrink:0; text-align:right; }}
  .footer {{ text-align:center; color:rgba(232,234,237,0.2); font-size:12px; padding:40px 0; }}
  .width-ctrl {{ display:flex; align-items:center; gap:8px; margin-bottom:24px; padding:8px 16px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:8px; }}
  .width-ctrl span {{ font-size:11px; color:rgba(232,234,237,0.4); }}
  .width-ctrl input {{ flex:1; -webkit-appearance:none; appearance:none; height:4px; border-radius:100px; background:rgba(255,255,255,0.08); outline:none; cursor:pointer; }}
  .width-ctrl input::-webkit-slider-thumb {{ -webkit-appearance:none; appearance:none; width:14px; height:14px; border-radius:50%; background:#536dfe; border:2px solid #16181f; cursor:pointer; }}
  .width-ctrl input::-moz-range-thumb {{ width:14px; height:14px; border-radius:50%; background:#536dfe; border:2px solid #16181f; cursor:pointer; }}
  .width-ctrl .wval {{ font-size:11px; font-weight:600; color:rgba(232,234,237,0.6); min-width:36px; text-align:right; font-family:'JetBrains Mono',monospace; }}
</style>
</head>
<body>
<div class="container" id="report-container">
  <div class="header">
    <h1>{icon} {title}</h1>
    <div class="meta">{meta}</div>
  </div>
  <div class="width-ctrl">
    <span>⊞ Szerokość</span>
    <input type="range" id="widthSlider" min="600" max="1600" step="50" value="1000" oninput="document.getElementById('report-container').style.maxWidth=this.value+'px';document.getElementById('wval').textContent=this.value">
    <span class="wval" id="wval">1000</span>
  </div>"""

FOOTER = """  <div class="footer">Raport wygenerowany przez AI • Enterprise Hub Portal • POC v0.9.0</div>
</div>
</body>
</html>"""

# ────────────────────── HELPERS ──────────────────────
def esc(t):
    return html_mod.escape(str(t))

def section(title, body):
    return f'  <div class="section">\n    <h2>{title}</h2>\n{body}  </div>\n'

def kpi(label, value, color=None):
    c = f'color:{color};' if color else ''
    return f'<div class="kpi"><div class="kpi-num" style="{c}">{esc(value)}</div><div class="kpi-label">{esc(label)}</div></div>'

def row_item(name, badge, tag=None):
    t = f'<span class="tag">{esc(tag)}</span>' if tag else ''
    return f'  <div class="row"><span class="badge {badge}">{esc(badge.replace("badge-","").upper())}</span><span class="name">{esc(name)}</span>{t}</div>\n'

def sql_block(code):
    return f'  <div class="sql">{code}</div>\n'

def rec_item(level, icon, text):
    return f'  <div class="recommend rec-{level}"><span class="recommend-icon">{icon}</span><span class="recommend-text">{esc(text)}</span></div>\n'


# ────────────────────── REPORTS ──────────────────────

reports = []

# ──── 1. SQL Performance Advisor ────
reports.append(dict(
    id="sql-performance-advisor",
    accent="#7c4dff", accent2="#536dfe",
    icon="⚡", title="SQL Performance Advisor",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: Oracle / Snowflake",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Performance Score","92","#7c4dff")}
      {kpi("Przeanalizowanych zapytań","47")}
      {kpi("Problemy wykryte","12")}
      {kpi("Szacowany zysk wydajności","+35%","#00c853")}
    </div>""") +
    section("🔴 Krytyczne problemy", """
    <div class="row"><span class="badge badge-red">FTS</span><span class="name">FULL TABLE SCAN na CORE.TRANSACTIONS (18M rows)</span><span class="tag">brak indeksu</span></div>
    <div class="row"><span class="badge badge-red">CARTESIAN</span><span class="name">CARTESIAN JOIN w widoku V_MONTHLY_REPORT</span><span class="tag">brak klucza JOIN</span></div>
    <div class="row"><span class="badge badge-amber">DISTINCT</span><span class="name">Niepotrzebny DISTINCT w 2 zapytaniach agregujących</span><span class="tag">nadmiarowy</span></div>
    <div class="row"><span class="badge badge-amber">INDEX</span><span class="name">Brak indeksu kompozytowego na (customer_id, transaction_date)</span><span class="tag">wydajność</span></div>
    """) +
    section("📄 Optymalizacja SQL", """
    <div class="sql">
<span class="key">-- Oryginał (czas: 12.4s)</span><br>
<span class="key">SELECT DISTINCT</span> c.name, <span class="key">SUM</span>(t.amount)<br>
<span class="key">FROM</span> <span class="tref">CORE.CUSTOMERS</span> c<br>
<span class="key">JOIN</span> <span class="tref">CORE.TRANSACTIONS</span> t <span class="key">ON</span> 1=1<br>
<span class="key">WHERE</span> c.status = 'ACTIVE'<br>
<span class="key">GROUP BY</span> c.name<br><br>
<span class="key">-- Optymalizacja AI (szacowany czas: 1.8s)</span><br>
<span class="key">SELECT</span> c.name, <span class="key">SUM</span>(t.amount)<br>
<span class="key">FROM</span> <span class="tref">CORE.CUSTOMERS</span> c<br>
<span class="key">INNER JOIN</span> <span class="tref">CORE.TRANSACTIONS</span> t <span class="key">ON</span> c.customer_id = t.customer_id<br>
<span class="key">WHERE</span> c.status = 'ACTIVE'<br>
<span class="key">GROUP BY</span> c.name
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Dodaj indeks kompozytowy na (customer_id, transaction_date DESC) w tabeli CORE.TRANSACTIONS')}
    {rec_item('high','🔷','Zamień CARTESIAN JOIN na INNER JOIN z kluczem w V_MONTHLY_REPORT')}
    {rec_item('med','🔷','Usuń DISTINCT w zapytaniach z GROUP BY — jest nadmiarowy')}
    {rec_item('low','🔷','Rozważ partycjonowanie tabel faktów miesięcznie')}
    """)
))

# ──── 2. AI Code Review for SQL ────
reports.append(dict(
    id="sql-code-review",
    accent="#651fff", accent2="#d500f9",
    icon="🔍", title="AI Code Review for SQL",
    meta="Wygenerowano przez AI • 2026-07-07 • Standard: SQL Best Practices",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Code Quality","74","#651fff")}
      {kpi("Przejrzane zapytania","23")}
      {kpi("Uwagi","18")}
      {kpi("Poprawione SQL","12","#00c853")}
    </div>""") +
    section("⚠️ Naruszenia standardów", """
    <div class="row"><span class="badge badge-red">CRIT</span><span class="name">SELECT * w 8 widokach produkcyjnych</span><span class="tag">wydajność</span></div>
    <div class="row"><span class="badge badge-red">CRIT</span><span class="name">Brak obsługi NULL w kolumnach numerycznych (12 miejsc)</span><span class="tag">poprawność</span></div>
    <div class="row"><span class="badge badge-amber">WARN</span><span class="name">Niespójne nazewnictwo: CamelCase vs SNAKE_CASE</span><span class="tag">czytelność</span></div>
    <div class="row"><span class="badge badge-amber">WARN</span><span class="name">Brak komentarzy w złożonych CTE (>10 linii)</span><span class="tag">utrzymywalność</span></div>
    <div class="row"><span class="badge badge-blue">INFO</span><span class="name">Możliwość uproszczenia: 3 zapytania z niepotrzebnymi podzapytaniami</span><span class="tag">refactor</span></div>
    """) +
    section("📄 Przykład: SELECT * → jawne kolumny", """
    <div class="sql">
<span class="key">-- Przed:</span><br>
<span class="key">CREATE OR REPLACE VIEW</span> V_CUSTOMER_ACTIVE <span class="key">AS</span><br>
<span class="key">SELECT</span> * <span class="key">FROM</span> <span class="tref">CORE.CUSTOMERS</span> <span class="key">WHERE</span> status = 'ACTIVE'<br><br>
<span class="key">-- Po (AI):</span><br>
<span class="key">CREATE OR REPLACE VIEW</span> V_CUSTOMER_ACTIVE <span class="key">AS</span><br>
<span class="key">SELECT</span><br>
&nbsp;&nbsp;customer_id, name, segment, status,<br>
&nbsp;&nbsp;created_date, last_login, email, phone,<br>
&nbsp;&nbsp;address_city, address_country, risk_score, kyc_flag<br>
<span class="key">FROM</span> <span class="tref">CORE.CUSTOMERS</span><br>
<span class="key">WHERE</span> status = 'ACTIVE'
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Zamień SELECT * na jawne kolumny we wszystkich widokach produkcyjnych')}
    {rec_item('high','🔷','Dodaj COALESCE lub NVL dla kolumn numerycznych w zapytaniach agregujących')}
    {rec_item('med','🔷','Ustandaryzuj nazewnictwo na SNAKE_CASE — przeprowadź refactoring)')}
    {rec_item('med','🔷','Dodaj komentarze do każdego CTE dłuższego niż 10 linii')}
    {rec_item('low','🔷','Rozbij złożone zapytania na mniejsze, testowalne fragmenty')}
    """)
))

# ──── 3. SQL Lineage Report ────
reports.append(dict(
    id="sql-lineage",
    accent="#00c853", accent2="#00e5ff",
    icon="🧬", title="SQL Lineage Report",
    meta="Wygenerowano przez AI • 2026-07-04 • Źródło: Oracle / Snowflake",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Tabele źródłowe","24")}
      {kpi("Widoki","12")}
      {kpi("Procesy ETL","8")}
      {kpi("Zależności","156","#ff9100")}
    </div>""") +
    section("🧬 Lineage — Główny przepływ danych", """
    <div class="row"><span class="badge badge-green">TABLE</span><span class="name">CORE.CUSTOMERS</span><span class="tag">12 kolumn</span></div>
    <div class="row"><span class="badge badge-blue">VIEW</span><span class="name">CORE.V_CUSTOMER_ACTIVE</span><span class="tag">WHERE status='ACTIVE'</span></div>
    <div class="row"><span class="badge badge-amber">ETL</span><span class="name">wf_LOAD_CUSTOMER_DAILY</span><span class="tag">PowerCenter</span></div>
    <div class="row"><span class="badge badge-green">TABLE</span><span class="name">DWH.FACT_CUSTOMER_DAILY</span><span class="tag">25 kolumn, 2.4M rows</span></div>
    <div class="row"><span class="badge badge-green">TABLE</span><span class="name">CORE.TRANSACTIONS</span><span class="tag">18 kolumn</span></div>
    <div class="row"><span class="badge badge-amber">ETL</span><span class="name">wf_LOAD_TRANSACTIONS</span><span class="tag">PowerCenter</span></div>
    <div class="row"><span class="badge badge-green">TABLE</span><span class="name">DWH.FACT_TRANSACTIONS</span><span class="tag">32 kolumny, 18M rows</span></div>
    <div class="row"><span class="badge badge-blue">VIEW</span><span class="name">DWH.V_DAILY_KPI</span><span class="tag">Aggregacja dzienna</span></div>
    """) +
    section("🔎 Zależności krytyczne", """
    <div class="row"><span class="badge badge-red">CRITICAL</span><span class="name">DWH.FACT_DAILY_KPI ← CORE.TRANSACTIONS</span><span class="tag">Brak indeksu</span></div>
    <div class="row"><span class="badge badge-amber">WARNING</span><span class="name">DWH.V_CUSTOMER_365 ← CORE.CUSTOMERS</span><span class="tag">Full scan 5M</span></div>
    """) +
    section("📄 Przykładowy SQL", """
    <div class="sql">
<span class="key">SELECT</span> c.customer_id, c.name, c.segment,<br>
&nbsp;&nbsp;<span class="key">SUM</span>(t.amount) <span class="key">AS</span> total_transactions,<br>
&nbsp;&nbsp;<span class="key">COUNT</span>(<span class="key">DISTINCT</span> t.account_id) <span class="key">AS</span> accounts_used<br>
<span class="key">FROM</span> <span class="tref">CORE.CUSTOMERS</span> c<br>
<span class="key">LEFT JOIN</span> <span class="tref">CORE.TRANSACTIONS</span> t<br>
&nbsp;&nbsp;<span class="key">ON</span> c.customer_id = t.customer_id<br>
&nbsp;&nbsp;<span class="key">AND</span> t.transaction_date &gt;= <span class="key">SYSDATE</span> - <span class="key">INTERVAL</span> '30' <span class="key">DAY</span><br>
<span class="key">WHERE</span> c.status = 'ACTIVE'<br>
<span class="key">GROUP BY</span> c.customer_id, c.name, c.segment
    </div>""")
))

# ──── 4. ETL Dependency Analyzer ────
reports.append(dict(
    id="etl-dependency",
    accent="#00c853", accent2="#00e676",
    icon="🔗", title="ETL Dependency Analyzer",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: Informatica PowerCenter XML",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Workflow","24")}
      {kpi("Mappingi","67")}
      {kpi("Sesje","89")}
      {kpi("Pokrycie analizy","88%","#00c853")}
    </div>""") +
    section("⚠️ Wykryte problemy", """
    <div class="row"><span class="badge badge-red">UNUSED</span><span class="name">3 mappingi nieużywane od >6 miesięcy</span><span class="tag">m_ACCOUNT_ARCHIVE, m_LOAN_CALC_OLD, m_CUSTOMER_BACKUP</span></div>
    <div class="row"><span class="badge badge-red">ORPHAN</span><span class="name">2 osierocone workflow bez sesji</span><span class="tag">wf_DEPRECATED_LOAD, wf_TEST_BATCH</span></div>
    <div class="row"><span class="badge badge-amber">COMPLEX</span><span class="name">5 mappingów >50 transformacji</span><span class="tag">krytyczna złożoność</span></div>
    <div class="row"><span class="badge badge-amber">DUPLICATE</span><span class="name">7 duplikujących się transformacji Expression</span><span class="tag">EXP_TAX_CALC występuje 4x</span></div>
    <div class="row"><span class="badge badge-blue">SESSIONS</span><span class="name">2 nieużywane sesje (s_LOAD_OLD_ACCOUNTS, s_BACKUP_2024)</span><span class="tag">czyszczenie</span></div>
    """) +
    section("🗺️ Mapa zależności (top 5)", """
    <div class="sql">
wf_MAIN_LOAD<br>
&nbsp;&nbsp;├── s_LOAD_CUSTOMERS → m_LOAD_CUSTOMERS → CORE.CUSTOMERS<br>
&nbsp;&nbsp;├── s_LOAD_ACCOUNTS → m_LOAD_ACCOUNTS → CORE.ACCOUNTS<br>
&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;└── m_LOAD_ACCOUNTS używa: SQ_ACCOUNTS, EXP_CALC_BALANCE, RTR_ACCOUNT_TYPE, UPD_STRATEGY<br>
&nbsp;&nbsp;├── s_LOAD_TRANSACTIONS → m_LOAD_TRANSACTIONS → CORE.TRANSACTIONS<br>
&nbsp;&nbsp;└── s_LOAD_PRODUCTS → m_LOAD_PRODUCTS → CORE.PRODUCTS<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└── m_LOAD_PRODUCTS zawiera LOOKUP na PRICING_TABLE
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Usuń 3 nieużywane mappingi i 2 sesje — redukcja kosztów utrzymania o ~15%')}
    {rec_item('high','🔷','Podziel 5 złożonych mappingów na warstwy (Staging → Core → Output)')}
    {rec_item('med','🔷','Wydziel powielone Expression EXP_TAX_CALC do shared object w repozytorium')}
    {rec_item('med','🔷','Usuń 2 osierocone workflow lub podłącz je do działających sesji')}
    """)
))

# ──── 5. ETL Complexity Report ────
reports.append(dict(
    id="etl-complexity",
    accent="#00e676", accent2="#69f0ae",
    icon="📊", title="ETL Complexity Report",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: Informatica PowerCenter",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Complexity Score","72","#ffab00")}
      {kpi("Śr. transformacji","34")}
      {kpi("Mappingi krytyczne","8")}
      {kpi("Najwyższy wynik","94/100","#ff1744")}
    </div>""") +
    section("🏆 Ranking złożoności mappingów", """
    <div class="row"><span class="badge badge-red">94</span><span class="name">FCT_SALES_LOAD</span><span class="tag">78 transformacji, 12 lookupów</span></div>
    <div class="row"><span class="badge badge-red">91</span><span class="name">DIM_CUSTOMER_FULL</span><span class="tag">65 transformacji, 9 lookupów, 3 Joiner</span></div>
    <div class="row"><span class="badge badge-amber">87</span><span class="name">FCT_DAILY_KPI</span><span class="tag">58 transformacji, 8 lookupów</span></div>
    <div class="row"><span class="badge badge-amber">82</span><span class="name">M_RISK_EXPOSURE</span><span class="tag">52 transformacje, 5 Stored Procedure</span></div>
    <div class="row"><span class="badge badge-blue">76</span><span class="name">DIM_PRODUCT_HIERARCHY</span><span class="tag">48 transformacji, 2 Nested Mapping</span></div>
    """) +
    section("📊 Rozkład Complexity Score", """
    <div style="background:#0b0d11; border-radius:8px; padding:16px; margin-top:12px;">
      <div class="hbar">
        <span class="hbar-label">Prosty (0-30)</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:14%;background:#00c853;"><span>8</span></div></div>
        <span class="hbar-value">8</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Średni (31-60)</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:30%;background:#536dfe;"><span>17</span></div></div>
        <span class="hbar-value">17</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Trudny (61-85)</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:42%;background:#ff9100;"><span>24</span></div></div>
        <span class="hbar-value">24</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Krytyczny (>85)</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:14%;background:#ff1744;"><span>8</span></div></div>
        <span class="hbar-value" style="color:#ff1744;">8 ⚠️</span>
      </div>
      <div style="font-size:12px; color:#ff1744; margin-top:12px;">⚠️ 8 mappingów krytycznych wymaga natychmiastowej refaktoryzacji</div>
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Refaktoryzuj 8 mappingów z score >85 — podziel na mniejsze komponenty')}
    {rec_item('high','🔷','Wprowadź limit 40 transformacji na mapping jako standard jakości')}
    {rec_item('med','🔷','Dodaj warstwę stagingową dla lookupów — redukcja zależności')}
    {rec_item('med','🔷','Utwórz szablony ETL dla powtarzalnych wzorców (SCD, deduplikacja)')}
    """)
))

# ──── 6. Data Flow Visualizer ────
reports.append(dict(
    id="data-flow",
    accent="#00bcd4", accent2="#18ffff",
    icon="🌐", title="Data Flow Visualizer",
    meta="Wygenerowano przez AI • 2026-07-07 • Źródło: SQL + XML",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Źródła","3")}
      {kpi("Węzły pośrednie","25")}
      {kpi("Raporty końcowe","24")}
      {kpi("Największy przepływ","12M rows/d","#ff9100")}
    </div>""") +
    section("⬇️ Graf przepływu danych", """
    <div class="sql">
<span style="color:#00c853;">SOURCE</span> Core Banking<br>
&nbsp;&nbsp;│ 12M rows/dzień<br>
&nbsp;&nbsp;▼<br>
<span style="color:#536dfe;">LANDING</span> LND_CORE_DAILY<br>
&nbsp;&nbsp;│ 12M rows → walidacja + deduplikacja<br>
&nbsp;&nbsp;▼<br>
<span style="color:#536dfe;">LANDING</span> LND_CORE_HISTORY<br>
&nbsp;&nbsp;│ 48M rows (pełna historia)<br>
&nbsp;&nbsp;▼<br>
<span style="color:#ff9100;">BUFF</span> BUFF_CORE_INTEGRATION<br>
&nbsp;&nbsp;│ Procesy: merge, lookup, transform<br>
&nbsp;&nbsp;├──▶ <span style="color:#00e5ff;">DM</span> DM_CUSTOMER_DIM<br>
&nbsp;&nbsp;├──▶ <span style="color:#00e5ff;">DM</span> DM_ACCOUNT_DIM<br>
&nbsp;&nbsp;├──▶ <span style="color:#00e5ff;">DM</span> DM_PRODUCT_DIM<br>
&nbsp;&nbsp;└──▶ <span style="color:#00e5ff;">DM</span> DM_FACT_TRANSACTIONS<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──▶ 📊 Raport Dzienny KPI<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;├──▶ 📊 Raport Miesięczny<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└──▶ 📊 Raport Regulacyjny
    </div>""") +
    section("⚠️ Wąskie gardła", """
    <div class="row"><span class="badge badge-red">>4h</span><span class="name">Węzeł BUFF_CORE_INTEGRATION — przetwarzanie trwa >4h</span><span class="tag">opóźnienie</span></div>
    <div class="row"><span class="badge badge-amber">2h</span><span class="name">DM_FACT_TRANSACTIONS — indeksowanie po każdym batchu</span><span class="tag">wydajność</span></div>
    """) +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Zoptymalizuj węzeł BUFF — dodaj indeksy i partycjonowanie')}
    {rec_item('med','🔷','Przesuń indeksowanie do osobnego okna poza godzinami batch')}
    {rec_item('med','🔷','Dodaj monitoring przepływu dla krytycznych węzłów (alert >2h)')}
    """)
))

# ──── 7. Duplicate Logic Detector ────
reports.append(dict(
    id="duplicate-logic",
    accent="#009688", accent2="#4db6ac",
    icon="📋", title="Duplicate Logic Detector",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: SQL + PowerCenter",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Duplikacje","23")}
      {kpi("CASE WHEN","8","#ff5252")}
      {kpi("JOIN","5")}
      {kpi("Expression","7")}
      {kpi("Funkcje PL/SQL","3")}
    </div>""") +
    section("🔁 Identyczne fragmenty", """
    <div class="row"><span class="badge badge-red">×4</span><span class="name">CASE WHEN status IN ('A','B','C') THEN 'ACTIVE' ELSE 'INACTIVE' END</span><span class="tag">EXP_TAX_CALC x4</span></div>
    <div class="row"><span class="badge badge-red">×3</span><span class="name">LEFT JOIN PRICING_TABLE pt ON pt.product_id = p.id AND pt.eff_date = (SELECT MAX(...))</span><span class="tag">JOIN powielony</span></div>
    <div class="row"><span class="badge badge-amber">×2</span><span class="name">IIF(ISNULL(amount), 0, amount) * IIF(ISNULL(rate), default_rate, rate)</span><span class="tag">Expression x2</span></div>
    <div class="row"><span class="badge badge-amber">×2</span><span class="name">FUNCTION calculate_tax(p_amount, p_rate) RETURN NUMBER</span><span class="tag">PL/SQL x2</span></div>
    """) +
    section("💰 Szacowany koszt utrzymania duplikacji", """
    <div class="sql">
Koszt utrzymania duplikacji: <span style="color:#ff1744;">~120h/rok</span><br>
  - CASE WHEN: 4 miejsca × 2h zmiana × 2/rok = 16h<br>
  - JOIN: 3 miejsca × 3h zmiana × 2/rok = 18h<br>
  - Expression: 7 miejsc × 1h zmiana × 4/rok = 28h<br>
  - PL/SQL: 2 miejsca × 4h zmiana × 2/rok = 16h<br>
  - Testy regression: ~42h/rok<br><br>
<span style="color:#00c853;">Oszczędność po refaktoryzacji: ~100h/rok</span>
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Wydziel powielony CASE WHEN do osobnego widoku lub funkcji SQL')}
    {rec_item('high','🔷','Stwórz funkcję PL/SQL dla powielonego JOIN z PRICING_TABLE')}
    {rec_item('med','🔷','Zrefaktoryzuj Expression do shared object w repozytorium Informatica')}
    {rec_item('low','🔷','Wprowadź regułę CI/CD: blokada deployu przy >2 duplikacjach tego samego fragmentu')}
    """)
))

# ──── 8. Data Mapping Prototype ────
reports.append(dict(
    id="data-mapping",
    accent="#ff9100", accent2="#ffc400",
    icon="🗺️", title="Data Mapping Prototype",
    meta="Wygenerowano przez AI • 2026-07-04 • Źródło: Core Banking → DWH",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Pola źródłowe","156")}
      {kpi("Pola targetowe","142")}
      {kpi("Pokrycie","84%","#ff9100")}
      {kpi("Luki","14","#ff1744")}
    </div>""") +
    section("🗃️ Mapowanie głównych encji", """
    <div class="row"><span class="badge badge-green">OK</span><span class="name">CUSTOMER_ID → DIM_CUSTOMER.CUST_ID (typ: NUMBER→NUMBER)</span><span class="tag">direct</span></div>
    <div class="row"><span class="badge badge-green">OK</span><span class="name">CUSTOMER_NAME → DIM_CUSTOMER.FULL_NAME (VARCHAR2→VARCHAR2)</span><span class="tag">direct</span></div>
    <div class="row"><span class="badge badge-green">OK</span><span class="name">ACCOUNT_BALANCE → FACT_ACCOUNTS.BALANCE_AMOUNT (NUMBER(18,2)→NUMBER(20,2))</span><span class="tag">rzutowanie</span></div>
    <div class="row"><span class="badge badge-amber">TRF</span><span class="name">BIRTH_DATE → DIM_CUSTOMER.AGE_GROUP (DATE→VARCHAR2)</span><span class="tag">CASE WHEN wiek</span></div>
    <div class="row"><span class="badge badge-red">GAP</span><span class="name">BRAK → DIM_CUSTOMER.RISK_SEGMENT</span><span class="tag">brak źródła</span></div>
    <div class="row"><span class="badge badge-red">GAP</span><span class="name">BRAK → DIM_PRODUCT.PRODUCT_CATEGORY</span><span class="tag">brak źródła</span></div>
    """) +
    section("🔧 Transformacje", """
    <div class="sql">
<span style="color:#536dfe;">-- Transformacja wieku</span><br>
<span class="key">CASE</span><br>
&nbsp;&nbsp;<span class="key">WHEN</span> months_between(SYSDATE, birth_date)/12 &lt; 18 <span class="key">THEN</span> 'UNDER_18'<br>
&nbsp;&nbsp;<span class="key">WHEN</span> months_between(SYSDATE, birth_date)/12 &lt; 35 <span class="key">THEN</span> '18-35'<br>
&nbsp;&nbsp;<span class="key">WHEN</span> months_between(SYSDATE, birth_date)/12 &lt; 60 <span class="key">THEN</span> '36-60'<br>
&nbsp;&nbsp;<span class="key">ELSE</span> '60+'<br>
<span class="key">END</span>
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Uzupełnij 14 brakujących mapowań — zweryfikuj z zespołem biznesowym')}
    {rec_item('med','🔷','Zweryfikuj logikę transformacji AGE_GROUP z regułami biznesowymi')}
    {rec_item('low','🔷','Dodaj automatyzację walidacji mapowania po deploymencie')}
    """)
))

# ──── 9. Deployment Risk Analyzer ────
reports.append(dict(
    id="deployment-risk",
    accent="#ff5252", accent2="#ff8a80",
    icon="⚠️", title="Deployment Risk Analyzer",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: Jira + Git + XML",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Risk Score","68","#ff5252")}
      {kpi("Zmienione workflow","4")}
      {kpi("Krytyczne tabele","8")}
      {kpi("Procesy downstream","12")}
    </div>""") +
    section("📋 Ocena ryzyka", """
    <div class="row"><span class="badge badge-red">HIGH</span><span class="name">Ryzyko: WYSOKIE — wymagany restart schedulerów + wpływ na 12 procesów</span></div>
    <div class="row"><span class="badge badge-red">HIGH</span><span class="name">Zmiana dotyczy 8 krytycznych tabel (FCT_SALES, FCT_TRANSACTIONS, DIM_CUSTOMER)</span></div>
    <div class="row"><span class="badge badge-amber">MED</span><span class="name">Brak testów regresyjnych dla 3 mappingów (m_LOAD_ACCOUNTS, m_RISK_CALC, m_KPI_DAILY)</span></div>
    <div class="row"><span class="badge badge-amber">MED</span><span class="name">Wymagany restart schedulerów AutomateNow (okno: 2h przerwy)</span></div>
    <div class="row"><span class="badge badge-blue">LOW</span><span class="name">Rollback: przygotowany skrypt wycofania zmian (zweryfikowany)</span></div>
    """) +
    section("📄 Zmiany w tym release (Jira)", """
    <div class="sql">
<span style="color:#536dfe;">DATAHUB-2389</span> — Dodanie kolumny risk_segment do DIM_CUSTOMER [CRITICAL]<br>
<span style="color:#536dfe;">DATAHUB-2391</span> — Modyfikacja wf_LOAD_CUSTOMERS [HIGH]<br>
<span style="color:#536dfe;">DATAHUB-2395</span> — Optymalizacja wf_LOAD_TRANSACTIONS [MEDIUM]<br>
<span style="color:#536dfe;">DATAHUB-2402</span> — Poprawka indeksu na FACT_TRANSACTIONS [LOW]
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Wykonaj pełny regression test przed deploymentem (szczególnie 3 mappingi bez testów)')}
    {rec_item('high','🔷','Zaplanuj okno wdrożeniowe poza godzinami batch (rekomendacja: niedziela 6:00-10:00)')}
    {rec_item('med','🔷','Przygotuj i zweryfikuj rollback script dla każdej zmiany')}
    {rec_item('med','🔷','Powiadom właścicieli 12 procesów downstream o planowanym oknie')}
    """)
))

# ──── 10. Oracle Object Impact Analyzer ────
reports.append(dict(
    id="oracle-impact",
    accent="#ff1744", accent2="#d50000",
    icon="🎯", title="Oracle Object Impact Analyzer",
    meta="Wygenerowano przez AI • 2026-07-07 • Źródło: Oracle Dictionary",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Impact Score","81","#ff1744")}
      {kpi("Zależne widoki","34")}
      {kpi("Procedury","12")}
      {kpi("Mappingi ETL","7")}
      {kpi("Raporty BI","4")}
    </div>""") +
    section("🎯 Obiekt: FCT_SALES (analiza wpływu)", """
    <div class="row"><span class="badge badge-red">CRIT</span><span class="name">34 widoki bezpośrednio zależne od FCT_SALES</span></div>
    <div class="row"><span class="badge badge-red">CRIT</span><span class="name">12 procedur PL/SQL wymagających rekompilacji</span></div>
    <div class="row"><span class="badge badge-amber">HIGH</span><span class="name">7 mappingów PowerCenter korzystających z tabeli</span></div>
    <div class="row"><span class="badge badge-amber">HIGH</span><span class="name">4 raporty BI (PowerBI/Tableau) oparte na widokach zależnych</span></div>
    <div class="row"><span class="badge badge-blue">INFO</span><span class="name">3 indeksy do przebudowania po zmianie struktury</span></div>
    """) +
    section("🗺️ Ścieżki zależności (przykład)", """
    <div class="sql">
FCT_SALES<br>
&nbsp;&nbsp;├──▶ V_SALES_DAILY (widok)<br>
&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;├──▶ V_KPI_MONTHLY (widok) → raport BI "Miesięczne KPI"<br>
&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;└──▶ PKG_SALES_REPORT.proc_calc_daily (procedura)<br>
&nbsp;&nbsp;├──▶ V_SALES_BY_REGION (widok) → raport BI "Sprzedaż regionalna"<br>
&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;└──▶ m_LOAD_REGION_KPI (mapping PowerCenter)<br>
&nbsp;&nbsp;├──▶ m_LOAD_SALES_FACT (mapping PowerCenter)<br>
&nbsp;&nbsp;│&nbsp;&nbsp;&nbsp;&nbsp;└──▶ wf_DAILY_SALES_LOAD (workflow)<br>
&nbsp;&nbsp;└──▶ PKG_ETL_VALIDATION.proc_validate_sales (procedura)
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Przeanalizuj wszystkie 34 widoki — zidentyfikuj które można pominąć w trakcie zmiany')}
    {rec_item('high','🔷','Zaplanuj zmianę poza godzinami szczytu — oszacowany czas: 4h')}
    {rec_item('med','🔷','Powiadom właścicieli 4 raportów BI o planowanej zmianie struktury')}
    {rec_item('med','🔷','Przygotuj skrypt rekompilacji widoków i procedur po zmianie')}
    """)
))

# ──── 11. Data Quality Analyzer ────
reports.append(dict(
    id="data-quality",
    accent="#ffab00", accent2="#ffd740",
    icon="🛡️", title="Data Quality Analyzer",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: Oracle + Snowflake",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Quality Score","76","#ffab00")}
      {kpi("NULL rate","12.4%","#ff1744")}
      {kpi("Duplikaty PK","2 345","#ff5252")}
      {kpi("Outliers","8")}
    </div>""") +
    section("🔴 Znalezione problemy", """
    <div class="row"><span class="badge badge-red">NULL</span><span class="name">12.4% NULL w kolumnie CUSTOMER_DIM.EMAIL (248k rekordów)</span></div>
    <div class="row"><span class="badge badge-red">DUP</span><span class="name">2 345 duplikatów PK w tabeli CUSTOMER_DIM (customer_id)</span></div>
    <div class="row"><span class="badge badge-amber">DATE</span><span class="name">Niespójność dat między DM (2026-07-07) a Raportami (2026-07-06)</span></div>
    <div class="row"><span class="badge badge-amber">OUT</span><span class="name">8 wartości odstających w kolumnie FINANCIAL.AMOUNT (>3σ od średniej)</span></div>
    <div class="row"><span class="badge badge-blue">FK</span><span class="name">456 osieroconych rekordów w FACT_TRANSACTIONS (brakujące CUSTOMER_ID)</span></div>
    """) +
    section("📈 Trend jakości danych (ostatnie 30 dni)", """
    <div style="background:#0b0d11; border-radius:8px; padding:16px; margin-top:12px;">
      <div class="hbar">
        <span class="hbar-label">NULL rate</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:41%;background:#ff1744;"><span>12.4%</span></div></div>
        <span class="hbar-value" style="color:#ff1744;">12.4% ↑</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Duplikaty</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:30%;background:#ff9100;"><span>2 345</span></div></div>
        <span class="hbar-value" style="color:#00c853;">2 345 ↓</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Outliers</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:10%;background:#536dfe;"><span>8</span></div></div>
        <span class="hbar-value">8 →</span>
      </div>
      <div class="hbar">
        <span class="hbar-label">Spójność FK</span>
        <div class="hbar-track"><div class="hbar-fill" style="width:15%;background:#ffab00;"><span>456</span></div></div>
        <span class="hbar-value" style="color:#ff1744;">456 ↑</span>
      </div>
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Uruchom proces czyszczenia duplikatów — DEDUP_CUSTOMER (est. czas: 45min)')}
    {rec_item('high','🔷','Dodaj constraint NOT NULL na kolumnę EMAIL w CUSTOMER_DIM')}
    {rec_item('med','🔷','Zweryfikuj zakresy dat w procesie ETL — różnica 1 dnia między warstwami')}
    {rec_item('med','🔷','Utwórz job monitorowania jakości z alertami >5% NULL rate')}
    {rec_item('low','🔷','Usuń osierocone rekordy w FACT_TRANSACTIONS (456 rows)')}
    """)
))

# ──── 12. Auto Test Generator ────
reports.append(dict(
    id="test-generator",
    accent="#d500f9", accent2="#e040fb",
    icon="🧪", title="Auto Test Generator",
    meta="Wygenerowano przez AI • 2026-07-04 • Źródło: SQL + ETL",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Testy wygenerowane","45")}
      {kpi("Pokrycie","67%","#d500f9")}
      {kpi("Brakujące referencje","12")}
      {kpi("Duplikacje","8")}
    </div>""") +
    section("🧪 Lista wygenerowanych testów (top 10)", """
    <div class="row"><span class="badge badge-green">PASS</span><span class="name">TC-001: Sprawdź czy CUSTOMER_ID nie jest NULL po ETL</span></div>
    <div class="row"><span class="badge badge-green">PASS</span><span class="name">TC-002: Walidacja sumy TRANSACTION_AMOUNT = źródło</span></div>
    <div class="row"><span class="badge badge-green">PASS</span><span class="name">TC-003: Sprawdź czy DATE nie zawiera wartości przyszłych</span></div>
    <div class="row"><span class="badge badge-red">FAIL</span><span class="name">TC-004: Sprawdź spójność FK między FACT_TRANSACTIONS a CUSTOMER_DIM</span></div>
    <div class="row"><span class="badge badge-red">FAIL</span><span class="name">TC-005: Walidacja zakresu AMOUNT (brak wartości ujemnych dla kredytów)</span></div>
    <div class="row"><span class="badge badge-amber">WARN</span><span class="name">TC-006: Sprawdź czy nie ma duplikatów PK w tabelach wymiarowych</span></div>
    <div class="row"><span class="badge badge-green">PASS</span><span class="name">TC-007: Walidacja typu danych (DATE vs VARCHAR2)</span></div>
    <div class="row"><span class="badge badge-amber">WARN</span><span class="name">TC-008: Sprawdź czy sumy zgadzają się między warstwami (DM ↔ BUFF)</span></div>
    """) +
    section("📄 Przykładowy test (SQL)", """
    <div class="sql">
<span class="key">-- TC-004: Spójność FK</span><br>
<span class="key">SELECT</span> COUNT(*) <span class="key">AS</span> orphaned_records<br>
<span class="key">FROM</span> <span class="tref">DWH.FACT_TRANSACTIONS</span> f<br>
<span class="key">LEFT JOIN</span> <span class="tref">DWH.DIM_CUSTOMER</span> d <span class="key">ON</span> f.customer_id = d.customer_id<br>
<span class="key">WHERE</span> d.customer_id <span class="key">IS NULL</span><br><br>
<span style="color:#ff1744;">→ FAIL: 456 osieroconych rekordów</span>
    </div>""") +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Dodaj testy dla przypadków brzegowych (NULL, puste zbiory, duże wolumeny)')}
    {rec_item('high','🔷','Automatyzuj walidację po deploymentach — integracja z pipelinem CI/CD')}
    {rec_item('med','🔷','Rozszerz pokrycie testami z 67% do 85% (priorytet: krytyczne procesy)')}
    """)
))

# ──── 13. Documentation Generator ────
reports.append(dict(
    id="doc-generator",
    accent="#448aff", accent2="#82b1ff",
    icon="📄", title="Documentation Generator",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: SQL + XML + Jira",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Procesy udokumentowane","5","#00c853")}
      {kpi("Diagramy","3")}
      {kpi("Formaty","3")}
      {kpi("Stron dokumentacji","47")}
    </div>""") +
    section("📑 Proces: LOAD_CUSTOMER_DAILY", """
    <div class="sql">
<span style="color:#536dfe;">OPIS BIZNESOWY:</span><br>
Proces ładowania klientów z Core Banking do DWH. Odświeżanie dzienne przyrostowe.<br><br>
<span style="color:#536dfe;">OPIS TECHNICZNY:</span><br>
- Źródło: CORE.CUSTOMERS (Oracle, 12 kolumn)<br>
- Cel: DWH.DIM_CUSTOMER (25 kolumn)<br>
- Transformacje: SCD Type 2, deduplikacja, walidacja email<br>
- Workflow: wf_LOAD_CUSTOMER_DAILY (PowerCenter)<br>
- Scheduler: AutomateNow, codziennie 03:00<br>
- Czas wykonania: ~35 minut<br>
- Ostatni deployment: 2026-06-28<br><br>
<span style="color:#536dfe;">ZALEŻNOŚCI:</span><br>
  Poprzedza: wf_LOAD_ACCOUNTS, wf_CALC_KPI<br>
  Wymaga: wf_LOAD_REFERENCE_DATA<br>
  Właściciel: Zespół ETL (Jan Kowalski)
    </div>""") +
    section("✅ Wygenerowane pliki", """
    <div class="row"><span class="badge badge-green">MD</span><span class="name">docs/LOAD_CUSTOMER_DAILY.md</span><span class="tag">Markdown</span></div>
    <div class="row"><span class="badge badge-blue">HTML</span><span class="name">docs/LOAD_CUSTOMER_DAILY.html</span><span class="tag">HTML (z diagramem)</span></div>
    <div class="row"><span class="badge badge-red">PDF</span><span class="name">docs/LOAD_CUSTOMER_DAILY.pdf</span><span class="tag">PDF (gotowy do druku)</span></div>
    """) +
    section("✅ Rekomendacje", f"""
    {rec_item('med','🔷','Dodaj sekcję SLA dla każdego procesu (oczekiwany czas, RTO, RPO)')}
    {rec_item('med','🔷','Zintegruj z Confluence API — automatyczna publikacja dokumentacji')}
    {rec_item('low','🔷','Dodaj sekcję "Najczęstsze problemy" z rozwiązaniami')}
    """)
))

# ──── 14. Release Summary Generator ────
reports.append(dict(
    id="release-summary",
    accent="#2979ff", accent2="#448aff",
    icon="🚀", title="Release Summary Generator",
    meta="Wygenerowano przez AI • 2026-07-07 • Źródło: Jira + Git + TeamCity",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Zmiany","12")}
      {kpi("Jira tickets","8")}
      {kpi("Nowe tabele","3")}
      {kpi("Usunięte obiekty","2")}
    </div>""") +
    section("📋 Executive Summary", """
    <div class="sql">
<span style="color:#536dfe;">Release:</span> R-2026.07<br>
<span style="color:#536dfe;">Data:</span> 2026-07-12 (planowana)<br>
<span style="color:#536dfe;">Zakres:</span> Optymalizacja procesów ETL + nowe kolumny w DIM_CUSTOMER<br>
<span style="color:#536dfe;">Zmienione workflow:</span> wf_LOAD_CUSTOMERS, wf_LOAD_TRANSACTIONS, wf_KPI_DAILY, wf_RISK_CALC<br>
<span style="color:#536dfe;">Nowe tabele:</span> DWH.RISK_SEGMENT_DIM, DWH.AUDIT_CUSTOMER_CHANGES, STG.CUSTOMER_STAGING<br>
<span style="color:#536dfe;">Usunięte:</span> DWH.V_CUSTOMER_OLD (widok), STG.CUSTOMER_TEMP (tabela)<br>
<span style="color:#536dfe;">Wymagany restart schedulerów:</span> TAK (okno: 2h)<br><br>
<span style="color:#ff1744;">⚠️ Ryzyko: Średnie — zalecany such-run przed deploymentem</span>
    </div>""") +
    section("✅ Checklista post-deployment", """
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Zweryfikuj poprawność danych w DIM_CUSTOMER (nowe kolumny)</span></div>
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Uruchom testy regresyjne (45 testów)</span></div>
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Sprawdź czy schedulery wystartowały poprawnie po restarcie</span></div>
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Zweryfikuj raporty BI po zmianie struktury</span></div>
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Zaktualizuj runbook i dokumentację techniczną</span></div>
    <div class="row"><span class="badge badge-amber">☐</span><span class="name">Wyślij powiadomienie do zespołów downstream</span></div>
    """) +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Wykonaj such-run (próbny deployment) na środowisku testowym 2 dni przed')}
    {rec_item('med','🔷','Przygotuj raport po-wdrożeniowy dla kierownictwa (PDF)')}
    {rec_item('med','🔷','Zaktualizuj runbook o nowe procedury restartu schedulerów')}
    """)
))

# ──── 15. Scheduler Optimization Report ────
reports.append(dict(
    id="scheduler-optimization",
    accent="#00e5ff", accent2="#18ffff",
    icon="⏱️", title="Scheduler Optimization Report",
    meta="Wygenerowano przez AI • 2026-07-08 • Źródło: AutomateNow",
    body=section("📊 Podsumowanie", f"""
    <div class="kpi-row">
      {kpi("Optymalizacja","40%","#00e5ff")}
      {kpi("Kolizje","5")}
      {kpi("Joby >6h","3")}
      {kpi("Wąskie gardła","2")}
    </div>""") +
    section("⚠️ Wykryte problemy", """
    <div class="row"><span class="badge badge-red">COLL</span><span class="name">Kolizja: wf_LOAD_CUSTOMERS i wf_CALC_RISK w oknie 03:00-04:00</span></div>
    <div class="row"><span class="badge badge-red">COLL</span><span class="name">Kolizja: wf_LOAD_TRANSACTIONS i m_REFRESH_MVIEWS w oknie 04:00-05:00</span></div>
    <div class="row"><span class="badge badge-amber">LONG</span><span class="name">wf_LOAD_TRANSACTIONS: czas wykonania 6h 12min (okno 8h)</span></div>
    <div class="row"><span class="badge badge-amber">LONG</span><span class="name">m_REFRESH_MVIEWS: czas wykonania 4h 45min</span></div>
    <div class="row"><span class="badge badge-amber">BOT</span><span class="name">Wąskie gardło: proces ładowania DM — sekwencyjny, mógłby być równoległy</span></div>
    """) +
    section("📊 Propozycja nowego harmonogramu (Gantt)", """
    <div class="gantt">
      <div class="gantt-title">OBECNIE (czas: 8h)</div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_REFERENCE_DATA</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:25%;background:#536dfe;"><span>2h</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_CUSTOMERS</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:25%;background:#7c4dff;"><span>2h</span></div>
          <div class="gantt-collision" style="left:25%;" title="Kolizja"></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_TRANSACTIONS</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:77%;background:#ff9100;"><span>6h 12min</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">m_REFRESH_MVIEWS</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:59%;background:#00bcd4;"><span>4h 45min</span></div>
          <div class="gantt-collision" style="left:25%;" title="Kolizja"></div>
        </div>
      </div>
      <div class="gantt-footer"><span>00:00</span><span>02:00</span><span>04:00</span><span>06:00</span><span>08:00</span></div>
    </div>

    <div class="gantt" style="margin-top:16px;">
      <div class="gantt-title" style="color:#00c853;">PROPONOWANY (czas: 5h)</div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_REFERENCE_DATA</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:40%;background:#536dfe;"><span>2h</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_CUSTOMERS</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:40%;background:#7c4dff;"><span>2h</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_TRANSACTIONS (p1)</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:60%;background:#ff9100;"><span>3h</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">wf_LOAD_TRANSACTIONS (p2)</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:60%;background:#ff9100;left:20%;opacity:0.7;"><span>3h</span></div>
        </div>
      </div>
      <div class="gantt-row">
        <span class="gantt-label">m_REFRESH_MVIEWS</span>
        <div class="gantt-track">
          <div class="gantt-bar" style="width:80%;background:#00bcd4;left:20%;"><span>4h</span></div>
        </div>
      </div>
      <div class="gantt-footer"><span>00:00</span><span>01:00</span><span>02:00</span><span>03:00</span><span>04:00</span><span>05:00</span></div>
    </div>
    """) +
    section("✅ Rekomendacje", f"""
    {rec_item('high','🔷','Przesuń wf_LOAD_CUSTOMERS na 01:00 — eliminacja kolizji z wf_CALC_RISK')}
    {rec_item('high','🔷','Podziel wf_LOAD_TRANSACTIONS na 2 równoległe partie (oszczędność ~3h)')}
    {rec_item('med','🔷','Przesuń m_REFRESH_MVIEWS na 06:00 — poza oknem batchowym')}
    {rec_item('low','🔷','Wprowadź monitoring czasu wykonania jobów z alertem >4h')}
    """)
))


# ────────────────────── GENERATE ──────────────────────
def make_html(r):
    body = r["body"]
    html = (HEAD + body + FOOTER).format(**r)
    return html

def main():
    os.makedirs(OUT, exist_ok=True)
    for r in reports:
        fname = f"{r['id']}.html"
        path = os.path.join(OUT, fname)
        html = make_html(r)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] {fname}")
    print(f"\nWygenerowano {len(reports)} raportów w {OUT}")

if __name__ == "__main__":
    main()
