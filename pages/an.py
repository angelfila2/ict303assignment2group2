import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# ===========================
# Streamlit Page Configuration
# ===========================
st.set_page_config(
    page_title="Healthcare & Disease Trends",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Healthcare Spending & Disease/Mortality Trends")

# ===========================
# Sidebar for File Uploads
# ===========================
st.sidebar.header("📂 Upload Datasets")

uploaded_3d_file = st.sidebar.file_uploader("Upload dataset for 3D Line Graph (CSV)", type=["csv"])
uploaded_mortality_file = st.sidebar.file_uploader("Upload dataset for Mortality Analysis (CSV)", type=["csv"])

# ===========================
# Load Data Function
# ===========================
@st.cache_data
def load_data(file):
    return pd.read_csv(file)

# ===========================
# 3D Interactive Line Graph
# ===========================
if uploaded_3d_file:
    final_data = load_data(uploaded_3d_file)

    # Check required columns
    required_columns = {'Year', 'Healthcare Spending per 100,000', 'TB Incidence', 'Measles Incidence'}
    
    if not required_columns.issubset(final_data.columns):
        st.error(f"Missing required columns: {required_columns - set(final_data.columns)}")
    else:
        st.subheader("📌 3D Interactive Line Graph")

        # Sidebar Year Filter
        min_year, max_year = int(final_data["Year"].min()), int(final_data["Year"].max())
        selected_year = st.sidebar.slider("Select Year", min_year, max_year, max_year)

        # Filter dataset
        filtered_data = final_data[final_data["Year"] == selected_year]

        fig = px.line_3d(
            final_data.melt(id_vars=['Year', 'Healthcare Spending per 100,000'],
                            value_vars=['TB Incidence', 'Measles Incidence'],
                            var_name='Disease',
                            value_name='Incidence'),
            x='Year',
            y='Healthcare Spending per 100,000',
            z='Incidence',
            color='Disease',
            title='3D Interactive: Healthcare Spending vs. Communicable Disease Incidence',
            labels={'Year': 'Year (2000-2023)',
                    'Healthcare Spending per 100,000': 'Healthcare Spending per 100,000 ($)',
                    'Incidence': 'Disease Incidence per 100,000',
                    'Disease': 'Type of Disease'}
        )

        st.plotly_chart(fig)
        st.subheader("📋 Data Table")
        st.dataframe(filtered_data)

# ===========================
# Combined Line Graph (Mortality vs. Healthcare Spending)
# ===========================
if uploaded_mortality_file:
    df_grouped = load_data(uploaded_mortality_file)

    # Check required columns
    required_columns = {'Income Group', 'Year', 'Healthcare Spending Per 100k', 
                        'Maternal Mortality Rate', 'Infant Mortality Rate', 'NCD Mortality Rate'}
    
    if not required_columns.issubset(df_grouped.columns):
        st.error(f"Missing required columns: {required_columns - set(df_grouped.columns)}")
    else:
        st.subheader("📌 Healthcare Spending vs. Mortality Trends")

        # Sidebar Income Group Selection
        income_group_selected = st.sidebar.selectbox("Select Income Group", df_grouped["Income Group"].unique())

        # Filter data
        filtered_data = df_grouped[df_grouped["Income Group"] == income_group_selected]

        fig, ax1 = plt.subplots(figsize=(12, 6))
        colors = {"Low income": "red", "Middle income": "orange", "High income": "green"}
        ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Plot Healthcare Spending vs. Mortality
        ax1.plot(filtered_data["Healthcare Spending Per 100k"], filtered_data["NCD Mortality Rate"],
                 label="NCD Mortality Rate", color=colors[income_group_selected], linestyle="-")
        ax1.plot(filtered_data["Healthcare Spending Per 100k"], filtered_data["Maternal Mortality Rate"],
                 label="Maternal Mortality Rate", color=colors[income_group_selected], linestyle="dashed")

        ax1.set_xlabel("Healthcare Spending per 100,000 People (Log Scale)")
        ax1.set_ylabel("NCD & Maternal Mortality Rate (per 100,000 people)", color="black")
        ax1.tick_params(axis="y", labelcolor="black")
        ax1.set_xscale("log")

        # Create second Y-axis for Infant Mortality Rate
        ax2 = ax1.twinx()
        ax2.plot(filtered_data["Healthcare Spending Per 100k"], filtered_data["Infant Mortality Rate"],
                 label="Infant Mortality Rate", color=colors[income_group_selected], linestyle="dotted")

        ax2.set_ylabel("Infant Mortality Rate (per 1,000 live births)", color="black")
        ax2.tick_params(axis="y", labelcolor="black")
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

        plt.title(f"Healthcare Spending vs. Mortality ({income_group_selected})")
        plt.legend()
        st.pyplot(fig)

        # ===========================
        # Show Data Table
        # ===========================
        st.subheader("📋 Data Table")
        st.dataframe(filtered_data[['Income Group', 'Healthcare Spending Per 100k', 
                                    'Maternal Mortality Rate', 'Infant Mortality Rate', 'NCD Mortality Rate']])


