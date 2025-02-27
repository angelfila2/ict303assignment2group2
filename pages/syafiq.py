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
# Load Workforce Data
# ===========================
# st.sidebar.header("📂 Upload Workforce Data")
# workforce_file = st.sidebar.file_uploader("Upload workforce.csv", type=["csv"])

# st.sidebar.header("📂 Upload Healthcare Expenditure Data")
# healthcare_file = st.sidebar.file_uploader("Upload healthcareExpenditure.csv", type=["csv"])

DATA_FILENAME1 = Path(__file__).parent/'data/workforce.csv'
workforce_file = pd.read_csv(DATA_FILENAME1)

DATA_FILENAME2 = Path(__file__).parent/'data/healthcareExpenditure.csv'
healthcare_file = pd.read_csv(DATA_FILENAME2)
if workforce_file and healthcare_file:
    df_workforce = pd.read_csv(DATA_FILENAME1)
    df_healthcare = pd.read_csv(DATA_FILENAME2, skiprows=4)  # Skipping first 4 rows

    # Clean column names
    df_workforce.columns = df_workforce.columns.astype(str).str.strip()
    df_healthcare.columns = df_healthcare.columns.astype(str).str.strip()

    # Convert "Year" column to numeric
    df_workforce["Year"] = pd.to_numeric(df_workforce["Year"], errors='coerce')

    # Filter for year 2015
    df_workforce_filtered = df_workforce[df_workforce["Year"] == 2015].dropna()

    # Select relevant healthcare workforce categories
    categories = [
        "Medical doctors (per 10 000 population)", 
        "Nursing and midwifery personnel (per 10 000 population)", 
        "Dentists (per 10 000 population)", 
        "Pharmacists  (per 10 000 population)"
    ]

    # Ensure only existing columns are used
    valid_categories = [col for col in categories if col in df_workforce_filtered.columns]

    # Add "Total Healthcare Workers" column
    df_workforce_filtered["Total Healthcare Workers"] = df_workforce_filtered[valid_categories].sum(axis=1)

    # Rename workforce column for merging
    if "Countries, territories and areas" in df_workforce_filtered.columns:
        df_workforce_filtered = df_workforce_filtered.rename(columns={"Countries, territories and areas": "Country Name"})

    # ===========================
    # Process Healthcare Expenditure Data
    # ===========================
    expected_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
    available_columns = [col for col in expected_columns if col in df_healthcare.columns]

    # Melt dataset
    df_melted = df_healthcare.melt(id_vars=available_columns, var_name="Year", value_name="Value")

    # Convert "Year" column to numeric
    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')

    # Filter for year 2015
    df_healthcare_filtered = df_melted[df_melted["Year"] == 2015].dropna()

    # Keep relevant columns
    df_healthcare_filtered = df_healthcare_filtered[['Country Name', 'Year', 'Value']]

    # ===========================
    # Merge Datasets
    # ===========================
    df_merged = pd.merge(df_workforce_filtered, df_healthcare_filtered, on=["Country Name", "Year"], how="inner")

    # Rename column for clarity
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
        sns.scatterplot(data=df_filtered, x="Healthcare Expenditure", y="Total Healthcare Workers", color="blue", alpha=0.7, ax=ax)
        sns.regplot(data=df_filtered, x="Healthcare Expenditure", y="Total Healthcare Workers", scatter=False, color="red", ax=ax)

        # Labels and title
        ax.set_xlabel("Healthcare Expenditure (per capita)")
        ax.set_ylabel("Total Healthcare Workers (per 10,000 population)")
        ax.set_title("Correlation between Healthcare Expenditure and Total Healthcare Workers")
        ax.grid(True, linestyle="--", alpha=0.6)

        st.pyplot(fig)

    with col2:
        st.subheader("Data Table")
        st.dataframe(df_filtered[['Country Name', 'Healthcare Expenditure', 'Total Healthcare Workers']])

else:
    st.warning("Please upload both workforce and healthcare expenditure CSV files to proceed.")

