
import streamlit as st
import pandas as pd
import io
import os

st.set_page_config(page_title="Egotag Varenummer Generator")

st.markdown("<h1 style='text-align: center;'>Egotag Varenummer Generator</h1>", unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("Importer eksisterende varenumre (Excel)", type=["xlsx"])
if "varenummer_df" not in st.session_state:
    st.session_state.varenummer_df = pd.DataFrame(columns=["Varenummer"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        if "Varenummer" in df.columns:
            st.session_state.varenummer_df = pd.concat([st.session_state.varenummer_df, df]).drop_duplicates().reset_index(drop=True)
            st.success(f"{len(df)} varenumre importeret.")
        else:
            st.error("Excel-filen skal have en kolonne med navnet 'Varenummer'.")
    except Exception as e:
        st.error(f"Fejl ved indlæsning af filen: {e}")

st.markdown(f"**Antal varenumre i listen:** {len(st.session_state.varenummer_df)}")

basisnummer = st.text_input("Basisnummer (f.eks. 9532)")

if st.button("Generér nyt varenummer") and basisnummer:
    eksisterende = st.session_state.varenummer_df["Varenummer"].tolist()
    i = 1
    while True:
        nyt_nr = f"{basisnummer}-{i:05d}"
        if nyt_nr not in eksisterende:
            st.session_state.varenummer_df.loc[len(st.session_state.varenummer_df)] = [nyt_nr]
            st.success("Nyt varenummer genereret:")
            st.text(nyt_nr)
            break
        i += 1

with st.expander("Vis alle varenumre"):
    st.dataframe(st.session_state.varenummer_df)

if not st.session_state.varenummer_df.empty:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        st.session_state.varenummer_df.to_excel(writer, index=False)
    buffer.seek(0)
    st.download_button(
        label="Eksporter som Excel",
        data=buffer,
        file_name="varenummerliste.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
