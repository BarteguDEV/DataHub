"""
DDT — Streamlit POC
Prosta aplikacja Streamlit uruchamiana równolegle z Flask.
"""
import streamlit as st

st.set_page_config(
    page_title="DDT — Streamlit POC",
    page_icon="⚙️",
    layout="centered",
)

st.title("DDT — Developer Dev Tools")
st.markdown("---")

st.success("Streamlit działa poprawnie w ramach DataHub!")

st.write(
    "To jest prosty POC (proof of concept) mający potwierdzić, "
    "że Streamlit może być uruchomiony równolegle z Flask na "
    "tym samym Azure App Service."
)

with st.expander("ℹ️ Jak to działa"):
    st.markdown("""
    1. **Startup script** (`startup.sh`) uruchamia Streamlit na porcie 8501
    2. **Flask proxy** przekierowuje żądania z `/streamlit/` do `localhost:8501`
    3. **Vue frontend** wyświetla Streamlit w iframe pod `/streamlit/`
    """)

st.markdown("---")
st.subheader("Test interakcji")

name = st.text_input("Wpisz swoje imię:", value="Developer")
if name:
    st.write(f"Cześć, **{name}**! 👋")

col1, col2 = st.columns(2)
with col1:
    st.metric("CPU", "45%", "8%")
with col2:
    st.metric("RAM", "2.4 GB", "-12%")

st.markdown("---")
st.caption("DataHub — POC Streamlit | v0.4.6")
