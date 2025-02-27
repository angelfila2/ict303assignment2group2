import streamlit as st
import pandas as pd

st.title("Daven Page")
st.write("This page loads and processes GDP data.")

@st.cache_data
def load_gdp_data():
    # Load and return GDP dataset (adjust file path accordingly)
    return pd.read_csv("data/gdp_data.csv")

df = load_gdp_data()
st.dataframe(df)

