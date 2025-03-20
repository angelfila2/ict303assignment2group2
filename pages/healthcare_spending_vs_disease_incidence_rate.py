import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go

st.title("Healthcare Spending vs. Disease Incidence Rate (2000-2023)")

# Cache data loading for efficiency
@st.cache_data
def load_data():
    df_health_expenditure = pd.read_csv("data/current_health_expenditure_per_capita.csv", skiprows=4)
    df_tb_incidence = pd.read_csv("data/incidence_of_tuberculosis_per_100000.csv", skiprows=4)
    df_measles_cases = pd.read_excel("data/Measles reported cases and incidence 2025-12-02 18-23 UTC.xlsx", sheet_name="Sheet1")
    df_final_merged = pd.read_csv("data/final_merged_dataset.csv")  # 3D Plot Dataset

    # Data cleaning
    df_health_expenditure.rename(columns={"Country Name": "Country"}, inplace=True)
    df_tb_incidence.rename(columns={"Country Name": "Country"}, inplace=True)
    df_measles_cases.rename(columns={"Country / Region": "Country"}, inplace=True)

    df_measles_cases.iloc[:, 2:] = df_measles_cases.iloc[:, 2:].apply(pd.to_numeric, errors='coerce') / 10
    df_health_expenditure.iloc[:, 2:] = df_health_expenditure.iloc[:, 2:].apply(pd.to_numeric, errors='coerce') * 1000

    df_measles_cases_melted = df_measles_cases.melt(id_vars=["Country", "Disease"], var_name="Year", value_name="Measles Incidence Rate")
    df_measles_cases_melted["Year"] = pd.to_numeric(df_measles_cases_melted["Year"], errors='coerce')

    df_health_expenditure_melted = df_health_expenditure.melt(id_vars=["Country"], var_name="Year", value_name="Healthcare Spending Per 100,000 People ($)")
    df_health_expenditure_melted["Year"] = pd.to_numeric(df_health_expenditure_melted["Year"], errors='coerce')

    df_tb_melted = df_tb_incidence.melt(id_vars=["Country"], var_name="Year", value_name="TB Incidence Rate")
    df_tb_melted["Year"] = pd.to_numeric(df_tb_melted["Year"], errors='coerce')

    df_measles_merged = pd.merge(df_measles_cases_melted, df_health_expenditure_melted, on=["Country", "Year"], how="inner")
    df_tb_merged = pd.merge(df_tb_melted, df_health_expenditure_melted, on=["Country", "Year"], how="inner")

    return df_measles_merged, df_tb_merged, df_final_merged

df_measles_merged, df_tb_merged, df_final_merged = load_data()

# User Selection for Disease
disease_selection = st.radio("Select Disease to Compare", ["Tuberculosis", "Measles"])
df_selected = df_tb_merged if disease_selection == "Tuberculosis" else df_measles_merged

# Year Range Selection
year_range = st.slider("Select Year Range", min_value=2000, max_value=2023, value=(2000, 2023))

#  Ensure 'Year' is numeric and drop NaNs before conversion
df_selected['Year'] = pd.to_numeric(df_selected['Year'], errors='coerce')  # Convert to numeric
df_selected = df_selected.dropna(subset=['Year'])  # Remove rows with NaN years
df_selected['Year'] = df_selected['Year'].astype(int)  # Convert safely to integer

# Apply filtering after cleaning data
df_selected = df_selected[(df_selected['Year'] >= year_range[0]) & (df_selected['Year'] <= year_range[1])]

# Scatter Plot Section (Unchanged)
st.subheader(f"Scatter Plot: Healthcare Spending vs. {disease_selection} Incidence")
if df_selected.empty:
    st.warning("Not enough data available for the selected filters. Try adjusting your selections.")
else:
    fig = px.scatter(df_selected,
                     x="Healthcare Spending Per 100,000 People ($)",
                     y="TB Incidence Rate" if disease_selection == "Tuberculosis" else "Measles Incidence Rate",
                     color="Country",
                     hover_data=["Year"],
                     title=f"Healthcare Spending vs. {disease_selection} Incidence Rate ({year_range[0]}-{year_range[1]})")

    fig.update_xaxes(type="log")
    st.plotly_chart(fig)

# New 3D Plot Section (Separate)
st.subheader("3D Interactive Plot: Healthcare Spending vs. Communicable Disease Incidence")

# Convert dataset for 3D plot
df_melted = df_final_merged.melt(id_vars=['Year', 'Healthcare Spending per 100,000'],
                                 value_vars=['TB Incidence', 'Measles Incidence'],
                                 var_name='Disease',
                                 value_name='Incidence')

# Generate 3D Line Plot
fig_3d = px.line_3d(df_melted,
                    x='Year',
                    y='Healthcare Spending per 100,000',
                    z='Incidence',
                    color='Disease',
                    title='3D Interactive: Healthcare Spending vs. Communicable Disease Incidence')

st.plotly_chart(fig_3d)

# Observations & Insights
st.subheader("Key Observations")
st.write("- **Tuberculosis:** Generally shows a negative correlation with increased healthcare spending.")
st.write("- **Measles:** Shows fluctuations due to the effect of vaccination programs.")
st.write("- **Diminishing Returns:** High healthcare spending does not always lead to lower disease incidence.")

# Call to Action
st.subheader("Call to Action")
st.write("- **Increase targeted healthcare funding.**")
st.write("- **Strengthen vaccination & disease prevention programs.**")
st.write("- **Enhance data collection & monitoring.**")
