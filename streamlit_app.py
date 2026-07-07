"""
DataHub — Streamlit POC z pełnym testem komponentów.
Sprawdza czy iframe proxy poprawnie obsługuje wszystkie widgety Streamlit.
"""
import time
import random
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(
    page_title="DataHub — Streamlit Test",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Streamlit — Test komponentów w iframe")
st.markdown("---")

# ===========================================================================
# Zakładki (tabs)
# ===========================================================================
tab_intro, tab_interakcja, tab_dane, tab_wykresy, tab_symulacja = st.tabs([
    "ℹ️ Info", "🖱️ Interakcja", "📊 Dane", "📈 Wykresy", "⏳ Symulacja"
])

# ===========================================================================
# TAB 1 — Info
# ===========================================================================
with tab_intro:
    st.success("Streamlit działa poprawnie w ramach DataHub przez iframe!")

    st.write(
        "Test wszechstronności proxy — wszystkie główne widgety Streamlit "
        "powinny działać bezproblemowo przez iframe."
    )

    with st.expander("ℹ️ Jak to działa"):
        st.markdown("""
        1. **FastAPI** uruchamia Streamlit jako subprocess na porcie 8501
        2. **FastAPI proxy** przekierowuje `/streamlit/` → `localhost:8501/streamlit/`
        3. **Vue.js** wyświetla Streamlit w `<iframe src="/streamlit/">`
        """)

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Status", "Online ✅", "0ms latency")
    col_b.metric("Uptime", "12h 34m", "0 restarts")
    col_c.metric("Sesje", "1", "aktywna")

# ===========================================================================
# TAB 2 — Interakcja
# ===========================================================================
with tab_interakcja:
    st.subheader("Formularze i przyciski")

    # --- Przycisk z licznikiem ---
    if "click_count" not in st.session_state:
        st.session_state.click_count = 0
        st.session_state.items = []

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🔘 Kliknij mnie", use_container_width=True):
            st.session_state.click_count += 1
            st.rerun()
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.click_count = 0
            st.session_state.items = []
            st.rerun()
    with col2:
        st.info(f"Kliknięć: **{st.session_state.click_count}**")
        if st.session_state.click_count > 0:
            st.progress(min(st.session_state.click_count / 20, 1.0))
            if st.session_state.click_count >= 20:
                st.success("Osiągnięto 20 kliknięć! 🎉")

    # --- Checkboxy ---
    st.markdown("---")
    cols = st.columns(4)
    fruits = {}
    for i, fruit in enumerate(["Jabłko 🍎", "Gruszka 🍐", "Banan 🍌", "Wiśnia 🍒"]):
        with cols[i]:
            fruits[fruit] = st.checkbox(fruit, value=(i == 0))
    selected = [k for k, v in fruits.items() if v]
    if selected:
        st.write(f"Wybrano: {', '.join(selected)}")

    # --- Selectbox + Slider ---
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        option = st.selectbox(
            "Wybierz opcję",
            ["Opcja A", "Opcja B", "Opcja C", "Opcja D"],
        )
        st.write(f"Wybrano: **{option}**")
    with col_s2:
        value = st.slider("Suwak zakresu", 0, 100, 50)
        st.write(f"Wartość: **{value}**")

    # --- Text input + Text area ---
    name = st.text_input("Twoje imię:", value="Testowy User")
    message = st.text_area("Wiadomość:", "To jest test iframe proxy...")
    if name:
        st.success(f"Cześć **{name}**! Wiadomość: _{message}_")

    # --- Radio + Toggle ---
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        color = st.radio("Ulubiony kolor:", ["Czerwony", "Zielony", "Niebieski"], horizontal=True)
    with col_r2:
        enabled = st.toggle("Włącz powiadomienia", value=True)
    st.write(f"Kolor: **{color}** | Powiadomienia: **{'ON' if enabled else 'OFF'}**")

# ===========================================================================
# TAB 3 — Dane (DataFrame, tabela)
# ===========================================================================
with tab_dane:
    st.subheader("Pandas DataFrame")

    # --- Generowanie danych ---
    np.random.seed(42)
    n_rows = st.slider("Liczba wierszy:", 5, 50, 15)

    df = pd.DataFrame({
        "ID": range(1, n_rows + 1),
        "Produkt": [random.choice(["Alpha", "Beta", "Gamma", "Delta", "Epsilon"]) for _ in range(n_rows)],
        "Kategoria": [random.choice(["A", "B", "C"]) for _ in range(n_rows)],
        "Ilość": np.random.randint(1, 100, n_rows),
        "Cena": np.round(np.random.uniform(10, 500, n_rows), 2),
        "Data": pd.date_range("2026-01-01", periods=n_rows, freq="D"),
        "Status": [random.choice(["Aktywny", "Zawieszony", "Zakończony"]) for _ in range(n_rows)],
    })
    df["Wartość"] = df["Ilość"] * df["Cena"]

    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.dataframe(df, use_container_width=True, height=350)
    with col_d2:
        st.subheader("Statystyki")
        st.dataframe(df.describe(), use_container_width=True)

    # --- Tabela statyczna + JSON ---
    st.markdown("---")
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.subheader("Tabela (statyczna)")
        st.table(df.head(5))
    with col_j2:
        st.subheader("JSON")
        st.json(df[["ID", "Produkt", "Wartość"]].head(3).to_dict(orient="records"))

    # --- Filtrowanie ---
    st.markdown("---")
    st.subheader("Filtrowanie danych")
    kategoria = st.selectbox("Filtruj po kategorii:", ["Wszystkie"] + sorted(df["Kategoria"].unique().tolist()))
    filtered = df if kategoria == "Wszystkie" else df[df["Kategoria"] == kategoria]
    st.write(f"Znaleziono: **{len(filtered)}** wierszy")
    st.dataframe(filtered, use_container_width=True)

# ===========================================================================
# TAB 4 — Wykresy
# ===========================================================================
with tab_wykresy:
    st.subheader("Wykresy")

    chart_data = pd.DataFrame({
        "Miesiąc": pd.date_range("2026-01-01", periods=12, freq="ME"),
        "Przychód": np.random.randint(10000, 50000, 12),
        "Koszt": np.random.randint(8000, 40000, 12),
        "Zysk": np.random.randint(-5000, 15000, 12),
    })

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("Słupkowy")
        st.bar_chart(chart_data.set_index("Miesiąc")[["Przychód", "Koszt"]], height=300)
    with col_g2:
        st.subheader("Liniowy")
        st.line_chart(chart_data.set_index("Miesiąc")[["Przychód", "Koszt", "Zysk"]], height=300)

    st.subheader("Powierzchniowy")
    st.area_chart(chart_data.set_index("Miesiąc")[["Przychód", "Koszt"]], height=250)

    st.markdown("---")
    st.subheader("Mapa (punkty)")
    map_data = pd.DataFrame({
        "lat": np.random.uniform(49.0, 54.5, 50),
        "lon": np.random.uniform(14.0, 24.0, 50),
    })
    st.map(map_data, height=350)

# ===========================================================================
# TAB 5 — Symulacja wykonania skryptu
# ===========================================================================
with tab_symulacja:
    st.subheader("⏳ Symulacja długiego procesu")

    st.warning(
        "Ta symulacja testuje czy iframe proxy poprawnie obsługuje "
        "iteracyjne aktualizacje Streamlit (progress bar + placeholder)."
    )

    if st.button("▶️ Uruchom symulację 5-sekundową", type="primary", use_container_width=True):
        progress_bar = st.progress(0, text="Przygotowanie...")
        status_text = st.empty()
        steps = 20

        for i in range(steps):
            progress = (i + 1) / steps
            time.sleep(0.25)

            phase = "Inicjalizacja" if i < 5 else "Przetwarzanie" if i < 12 else "Finalizacja"
            status_text.info(f"Krok {i+1}/{steps} — {phase} ({progress:.0%})")
            progress_bar.progress(progress, text=f"{progress:.0%} — {phase}")

            if i == 7:
                status_text.warning("⚠️ Wykryto anomalię — kontynuuję...")
            if i == 14:
                status_text.success("✅ Przetwarzanie zakończone — czyszczenie...")

        progress_bar.progress(1.0, text="✅ Gotowe!")
        status_text.success("Symulacja zakończona pomyślnie! 🎉")
        st.balloons()

    # --- Drugi, krótszy test ---
    st.markdown("---")
    st.subheader("Szybki test 2-sekundowy")
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        if st.button("📊 Generuj CSV", use_container_width=True):
            with st.spinner("Generowanie..."):
                time.sleep(2)
            st.success("CSV gotowy!")
    with col_q2:
        if st.button("📄 Generuj PDF", use_container_width=True):
            with st.spinner("Generowanie..."):
                time.sleep(2)
            st.success("PDF gotowy!")
    with col_q3:
        if st.button("📧 Wyślij raport", use_container_width=True):
            with st.spinner("Wysyłanie..."):
                time.sleep(2)
            st.success("Raport wysłany!")

    # --- Status ładowania ---
    st.markdown("---")
    st.subheader("Lazy loading (st.empty)")
    if st.button("⏳ Pokaż kroki", use_container_width=True):
        placeholder = st.empty()
        for step in ["Ładowanie konfiguracji...", "Połączenie z bazą...", "Pobieranie danych...", "Przetwarzanie...", "Gotowe ✅"]:
            placeholder.info(step)
            time.sleep(0.8)
        placeholder.success("Wszystkie kroki zakończone!")

# ===========================================================================
# Footer
# ===========================================================================
st.markdown("---")
st.caption("DataHub — Streamlit test komponentów | v0.4.12")
