import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Print the current working directory to help locate the file
st.write("Current working directory:", os.getcwd())

# Streamlit page title and description
st.title("📊 Damian Page Immunisation vs Disease Dashboard")
st.write("This dashboard visualizes immunisation and disease datasets.")

# Load dataset from predefined file paths
@st.cache_data
def load_data():
    try:
        # Update file paths based on your provided structure
        immunisation_path = "gdp-dashboard/data/Immunization_expenditure.csv"
        disease_path = "gdp-dashboard/data/Infectious_Disease.csv"
        
        # Check if the files exist
        if not os.path.exists(immunisation_path):
            st.error(f"File not found: {immunisation_path}")
            return pd.DataFrame(), pd.DataFrame()
        if not os.path.exists(disease_path):
            st.error(f"File not found: {disease_path}")
            return pd.DataFrame(), pd.DataFrame()

        immunisation_df = pd.read_excel(immunisation_path)
        disease_df = pd.read_csv(disease_path)
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
