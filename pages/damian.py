import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings

# Suppress warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Page configuration
st.set_page_config(
    page_title="ASEAN Immunization Dashboard",
    layout="wide"
)

st.title("ASEAN Immunization & Disease Analysis")
st.markdown(
    "Explore the relationship between immunization expenditures and infectious disease cases across ASEAN nations.")


@st.cache_data
def load_data():
    # File Paths
    file1 = "data\Immunization_expenditure.csv"
    file2 = "data\Infectious_Disease.csv"

    # Load data
    df_immunization = pd.read_csv(file1, encoding='ISO-8859-1')
    df_disease = pd.read_csv(file2, encoding='ISO-8859-1')
    return df_immunization, df_disease


# Load data
df_immunization, df_disease = load_data()

# Data Preprocessing - using different variable names
df_immunization['expenditure'] = pd.to_numeric(df_immunization['VALUE'], errors='coerce')
df_vacc = df_immunization[df_immunization['INDCODE'] == 'FIN_GVT_VACC'].copy()
df_imm_summary = (
    df_vacc
    .dropna(subset=['expenditure'])
    .groupby(['COUNTRYNAME', 'YEAR'], as_index=False)['expenditure']
    .sum()
)
df_imm_summary.rename(columns={"expenditure": "immunization_spending"}, inplace=True)

# Different column renaming for disease data
df_disease.columns = df_disease.columns.str.strip().str.upper()
df_disease = df_disease.rename(columns={
    "PERIOD": "YEAR",
    "LOCATION": "COUNTRYNAME",
    "FACTVALUENUMERIC": "disease_cases"
})

# Merge datasets
df_combined = pd.merge(
    df_imm_summary,
    df_disease,
    on=["YEAR", "COUNTRYNAME"],
    how="inner"
)
df_combined = df_combined.dropna(subset=['disease_cases'])

# Convert YEAR to numeric
df_combined['YEAR'] = pd.to_numeric(df_combined['YEAR'], errors='coerce')

# Define ASEAN countries
asean_countries = [
    'Indonesia', 'Malaysia', 'Philippines', 'Singapore', 'Thailand',
    'Vietnam', 'Brunei', 'Cambodia', 'Laos', 'Myanmar'
]

# Filter for ASEAN countries
available_countries = [country for country in asean_countries if country in df_combined['COUNTRYNAME'].unique()]

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Country Selection", "Visualizations", "Data Summary"])

with tab1:
    st.header("Select Countries and Time Period")

    # Different selection method: all countries selected by default
    selected_countries = st.multiselect(
        "Select ASEAN Countries:",
        options=available_countries,
        default=available_countries  # All countries selected by default
    )

    # Year range selection
    years = sorted(df_combined['YEAR'].unique())
    year_range = st.slider(
        "Select Year Range:",
        min_value=int(min(years)),
        max_value=int(max(years)),
        value=(int(min(years)), int(max(years)))
    )

    # Alternative selection method: radio buttons for disease type
    if 'SUBJECT' in df_combined.columns:
        disease_types = sorted(df_combined['SUBJECT'].unique())
        disease_selection = st.radio(
            "Select Disease Type:",
            options=["All"] + disease_types
        )

with tab2:
    # Filter data based on selection
    if not selected_countries:
        st.warning("Please select at least one country to display visualizations.")
    else:
        df_filtered = df_combined[
            (df_combined['COUNTRYNAME'].isin(selected_countries)) &
            (df_combined['YEAR'].between(year_range[0], year_range[1]))
            ]

        # Apply disease filter if selected
        if 'SUBJECT' in df_combined.columns and disease_selection != "All":
            df_filtered = df_filtered[df_filtered['SUBJECT'] == disease_selection]

        if not df_filtered.empty:
            st.header("Visualizations")

            # Visual selection using columns
            col1, col2 = st.columns(2)
            with col1:
                chart_type = st.selectbox(
                    "Select Chart Type:",
                    ["Scatter Plot", "Line Chart", "Bar Chart"]
                )

            with col2:
                metric = st.selectbox(
                    "Select Metric to Analyze:",
                    ["Disease-Expenditure Relationship", "Disease Cases Over Time", "Immunization Spending Over Time"]
                )

            # Create visualizations based on selection
            if metric == "Disease-Expenditure Relationship":
                fig = px.scatter(
                    df_filtered,
                    x="immunization_spending",
                    y="disease_cases",
                    color="COUNTRYNAME",
                    trendline="ols",
                    title="Immunization Spending vs Disease Cases",
                    labels={
                        "immunization_spending": "Immunization Expenditure",
                        "disease_cases": "Disease Cases",
                        "COUNTRYNAME": "Country"
                    },
                    hover_data=["YEAR"]
                )
                st.plotly_chart(fig, use_container_width=True)

                # Show correlation
                st.subheader("Correlation Analysis")
                for country in selected_countries:
                    country_data = df_filtered[df_filtered['COUNTRYNAME'] == country]
                    if len(country_data) > 1:
                        corr = country_data['immunization_spending'].corr(country_data['disease_cases'])
                        st.write(f"{country}: {corr:.2f} correlation")

            elif metric == "Disease Cases Over Time":
                if chart_type == "Line Chart":
                    fig = px.line(
                        df_filtered,
                        x="YEAR",
                        y="disease_cases",
                        color="COUNTRYNAME",
                        title="Disease Cases Over Time",
                        markers=True
                    )
                elif chart_type == "Bar Chart":
                    fig = px.bar(
                        df_filtered,
                        x="YEAR",
                        y="disease_cases",
                        color="COUNTRYNAME",
                        title="Disease Cases by Year",
                        barmode="group"
                    )
                else:  # Default to scatter
                    fig = px.scatter(
                        df_filtered,
                        x="YEAR",
                        y="disease_cases",
                        color="COUNTRYNAME",
                        title="Disease Cases Over Time",
                        size="disease_cases"
                    )
                st.plotly_chart(fig, use_container_width=True)

            else:  # Immunization Spending Over Time
                if chart_type == "Line Chart":
                    fig = px.line(
                        df_filtered,
                        x="YEAR",
                        y="immunization_spending",
                        color="COUNTRYNAME",
                        title="Immunization Spending Over Time",
                        markers=True
                    )
                elif chart_type == "Bar Chart":
                    fig = px.bar(
                        df_filtered,
                        x="YEAR",
                        y="immunization_spending",
                        color="COUNTRYNAME",
                        title="Immunization Spending by Year",
                        barmode="group"
                    )
                else:  # Default to scatter
                    fig = px.scatter(
                        df_filtered,
                        x="YEAR",
                        y="immunization_spending",
                        color="COUNTRYNAME",
                        title="Immunization Spending Over Time",
                        size="immunization_spending"
                    )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("No data available for the selected criteria.")

with tab3:
    if not selected_countries:
        st.warning("Please select at least one country to display data summary.")
    else:
        st.header("Data Summary")

        # Filter data based on selection
        df_filtered = df_combined[
            (df_combined['COUNTRYNAME'].isin(selected_countries)) &
            (df_combined['YEAR'].between(year_range[0], year_range[1]))
            ]

        # Apply disease filter if selected
        if 'SUBJECT' in df_combined.columns and disease_selection != "All":
            df_filtered = df_filtered[df_filtered['SUBJECT'] == disease_selection]

        if not df_filtered.empty:
            # Summary statistics
            summary = df_filtered.groupby('COUNTRYNAME').agg({
                'immunization_spending': ['mean', 'min', 'max'],
                'disease_cases': ['mean', 'min', 'max']
            }).reset_index()

            summary.columns = [
                'Country',
                'Avg Spending', 'Min Spending', 'Max Spending',
                'Avg Cases', 'Min Cases', 'Max Cases'
            ]

            st.dataframe(summary)

            # Data preview
            st.subheader("Data Preview")
            st.dataframe(df_filtered.sort_values(['COUNTRYNAME', 'YEAR']))

            # Download option
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                "Download Data as CSV",
                data=csv,
                file_name="asean_health_data.csv",
                mime="text/csv"
            )
        else:
            st.error("No data available for the selected criteria.")

# Footer
st.markdown("---")
st.markdown("Analysis of ASEAN immunization expenditure and infectious disease cases")
