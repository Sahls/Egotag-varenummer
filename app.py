
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Egotag Varenummer Generator")

st.image("egotag_logo.png", use_column_width=True)

st.title("Egotag Varenummer Generator")

# Session state for storage
if 'varenummer_df' not in st.session_state:
    if os.path.exists("varenummer_data.csv"):
        st.session_state.varenummer_df = pd.read_csv("varenummer_data.csv")
    else:
        st.session_state.varenummer_df = pd.DataFrame(columns=["Basisnummer", "UniktNummer", "Varenummer"])

# Helper function
def generate_varenummer(basisnummer):
    existing = st.session_state.varenummer_df[st.session_state.varenummer_df["Basisnummer"] == basisnummer]
    next_number = 1 if existing.empty else existing["UniktNummer"].max() + 1
    varenummer = f"{basisnummer}-{next_number:05d}"
    return next_number, varenummer

# Upload
uploaded_file = st.file_uploader("Importer varenumre fra Excel", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if {"Basisnummer", "UniktNummer"}.issubset(df.columns):
        df["Varenummer"] = df.apply(lambda row: f"{row['Basisnummer']}-{int(row['UniktNummer']):05d}", axis=1)
        st.session_state.varenummer_df = pd.concat([st.session_state.varenummer_df, df], ignore_index=True).drop_duplicates()
        st.success(f"{len(df)} varenumre importeret.")

# Basisnummer input
basisnummer = st.text_input("Basisnummer (f.eks. 9532)")
if basisnummer and basisnummer.isdigit():
    if st.button("Generer varenummer"):
        unikt, varenummer = generate_varenummer(basisnummer)
        new_entry = pd.DataFrame([[basisnummer, unikt, varenummer]], columns=["Basisnummer", "UniktNummer", "Varenummer"])
        st.session_state.varenummer_df = pd.concat([st.session_state.varenummer_df, new_entry], ignore_index=True)
        st.success("Nyt varenummer genereret:")
        st.text_input("Kopier varenummeret", varenummer)

# Save updated list
st.session_state.varenummer_df.to_csv("varenummer_data.csv", index=False)

# Info and export
st.markdown(f"**Antal varenumre:** {len(st.session_state.varenummer_df)}")

if st.button("Vis alle varenumre"):
    st.dataframe(st.session_state.varenummer_df)

st.download_button("Eksporter som Excel", st.session_state.varenummer_df.to_excel(index=False), file_name="varenummerliste.xlsx")
