import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ===========================
# Streamlit Page Configuration
# ===========================
st.set_page_config(
    page_title="Healthcare Workforce & Expenditure",
    page_icon="🏥",
    layout="wide"
)

# ===========================
# Sidebar - File Upload
# ===========================
st.sidebar.header("📂 Upload Workforce Data")
workforce_file = st.sidebar.file_uploader("Upload workforce.csv", type=["csv"])

st.sidebar.header("📂 Upload Healthcare Expenditure Data")
healthcare_file = st.sidebar.file_uploader("Upload healthcareExpenditure.csv", type=["csv"])

# Load default files if not uploaded
if workforce_file is None:
    workforce_path = Path(__file__).parent / "data/workforce.csv"
    if workforce_path.exists():
        workforce_file = open(workforce_path, "rb")

if healthcare_file is None:
    healthcare_path = Path(__file__).parent / "data/healthcareExpenditure.csv"
    if healthcare_path.exists():
        healthcare_file = open(healthcare_path, "rb")

if workforce_file and healthcare_file:
    df_workforce = pd.read_csv(workforce_file)
    df_healthcare = pd.read_csv(healthcare_file, skiprows=4)

    # ===========================
    # Data Cleaning & Processing
    # ===========================
    df_workforce.columns = df_workforce.columns.astype(str).str.strip()
    df_healthcare.columns = df_healthcare.columns.astype(str).str.strip()

    # Convert "Year" column to numeric
    if "Year" in df_workforce.columns:
        df_workforce["Year"] = pd.to_numeric(df_workforce["Year"], errors='coerce')

    # Filter for year 2015
    df_workforce_filtered = df_workforce[df_workforce["Year"] == 2015].dropna()

    # Select relevant workforce categories
    categories = [
        "Medical doctors (per 10 000 population)", 
        "Nursing and midwifery personnel (per 10 000 population)", 
        "Dentists (per 10 000 population)", 
        "Pharmacists  (per 10 000 population)"
    ]
    
    valid_categories = [col for col in categories if col in df_workforce_filtered.columns]

    # Calculate Total Healthcare Workers if valid columns exist
    if valid_categories:
        df_workforce_filtered["Total Healthcare Workers"] = df_workforce_filtered[valid_categories].sum(axis=1)

    # Rename for merging
    if "Countries, territories and areas" in df_workforce_filtered.columns:
        df_workforce_filtered = df_workforce_filtered.rename(columns={"Countries, territories and areas": "Country Name"})

    # ===========================
    # Process Healthcare Expenditure Data
    # ===========================
    expected_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    available_columns = [col for col in expected_columns if col in df_healthcare.columns]

    if available_columns:
        df_melted = df_healthcare.melt(id_vars=available_columns, var_name="Year", value_name="Value")
        df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
        df_healthcare_filtered = df_melted[df_melted["Year"] == 2015].dropna()

        # Keep only necessary columns
        df_healthcare_filtered = df_healthcare_filtered[['Country Name', 'Year', 'Value']]
    else:
        st.error("Healthcare expenditure dataset is missing required columns.")
        st.stop()

    # ===========================
    # Merge Datasets
    # ===========================
    df_merged = pd.merge(df_workforce_filtered, df_healthcare_filtered, on=["Country Name", "Year"], how="inner")
    df_merged = df_merged.rename(columns={"Value": "Healthcare Expenditure"})

    # ===========================
    # Sidebar Selection
    # ===========================
    country_list = sorted(df_merged["Country Name"].unique())
    selected_countries = st.sidebar.multiselect("Select Countries", country_list, default=country_list[:10])

    # Filter dataset based on selection
    df_filtered = df_merged[df_merged["Country Name"].isin(selected_countries)]

    # ===========================
    # Visualization
    # ===========================
    st.title("📊 Healthcare Workforce vs. Expenditure Dashboard")
    st.markdown("This dashboard explores the correlation between healthcare workforce and expenditure in 2015.")

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Scatter Plot: Healthcare Expenditure vs. Workforce")

        fig, ax = plt.subplots(figsize=(10, 6))
        
        if not df_filtered.empty:
            sns.scatterplot(data=df_filtered, x="Healthcare Expenditure", y="Total Healthcare Workers", color="blue", alpha=0.7, ax=ax)
            sns.regplot(data=df_filtered, x="Healthcare Expenditure", y="Total Healthcare Workers", scatter=False, color="red", ax=ax)

            ax.set_xlabel("Healthcare Expenditure (per capita)")
            ax.set_ylabel("Total Healthcare Workers (per 10,000 population)")
            ax.set_title("Correlation between Healthcare Expenditure and Total Healthcare Workers")
            ax.grid(True, linestyle="--", alpha=0.6)
        else:
            ax.text(0.5, 0.5, "No data available for selected countries", ha='center', va='center', fontsize=12)

        st.pyplot(fig)

    with col2:
        st.subheader("Data Table")
        st.dataframe(df_filtered[['Country Name', 'Healthcare Expenditure', 'Total Healthcare Workers']])

else:
    st.warning("Please upload both workforce and healthcare expenditure CSV files to proceed.")
