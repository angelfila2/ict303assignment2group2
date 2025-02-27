import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page title and description
st.title("📊 Damian Page Immunisation vs Disease Dashboard")
st.write("This dashboard visualizes immunisation and disease dataset.")

# Load dataset from uploaded CSV files
@st.cache_data
def load_data():
    try:
        immunisation_df = pd.read_csv("/data/Immunisation_Expenditure.xlsx")
        disease_df = pd.read_csv("/data/Infectious_Disease_data.csv")
        return immunisation_df, disease_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Load data
immunisation_df, disease_df = load_data()

# Display dataframes
st.subheader("📌 Immunisation Data")
st.dataframe(immunisation_df)
st.subheader("📌 Disease Data")
st.dataframe(disease_df)

# Visualization: Correlation heatmap for immunisation data
st.subheader("📌 Immunisation Data Correlation Heatmap")
if not immunisation_df.empty:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(immunisation_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.warning("No immunisation data available.")

# Visualization: Correlation heatmap for disease data
st.subheader("📌 Disease Data Correlation Heatmap")
if not disease_df.empty:
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(disease_df.corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)
else:
    st.warning("No disease data available.")

# Select columns for scatter plot
st.subheader("📌 Scatter Plot")
if not immunisation_df.empty and not disease_df.empty:
    x_col = st.selectbox("Select X-axis variable", immunisation_df.columns)
    y_col = st.selectbox("Select Y-axis variable", disease_df.columns)
    fig, ax = plt.subplots()
    sns.scatterplot(x=immunisation_df[x_col], y=disease_df[y_col], ax=ax)
    st.pyplot(fig)
else:
    st.warning("Data not sufficient for scatter plot.")
