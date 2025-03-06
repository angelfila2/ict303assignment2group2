import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Page Config
st.set_page_config(page_title='Immunization & Disease Dashboard', page_icon='💉')
st.title("📊 Damian Page Immunisation vs Disease Dashboard")
st.write("This dashboard visualizes immunisation and disease datasets.")

# -----------------------------------------------------------------------------
# Load Data with Caching

@st.cache_data
def load_data():
    DATA_FILENAME = Path(__file__).parent / 'data/immunization_expenditure.csv'
    df = pd.read_csv(DATA_FILENAME)
    df['Year'] = pd.to_numeric(df['Year'])  # Ensure year is numeric
    return df

data = load_data()

# -----------------------------------------------------------------------------
# Sidebar Filters
st.sidebar.header("Filters")

min_year, max_year = data['Year'].min(), data['Year'].max()
selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

countries = data['Country'].unique()
selected_countries = st.sidebar.multiselect("Select Countries", countries, ["USA", "UK", "India", "Brazil"])

# Filter Data
data_filtered = data[(data['Year'].between(*selected_years)) & (data['Country'].isin(selected_countries))]

# -----------------------------------------------------------------------------
# Dashboard Content
st.title("💉 Immunization Expenditure & Infectious Diseases Dashboard")
st.write("Explore immunization spending and its relationship with infectious disease cases.")

# Line Chart - Immunization Expenditure Over Time
st.header("📊 Immunization Expenditure Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=data_filtered, x="Year", y="Expenditure", hue="Country", marker="o", ax=ax)
ax.set_ylabel("Expenditure (Millions)")
ax.set_xlabel("Year")
st.pyplot(fig)

# Scatter Plot - Expenditure vs. Disease Cases
st.header("🔬 Expenditure vs. Infectious Disease Cases")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=data_filtered, x="Expenditure", y="Disease_Cases", hue="Country", size="Population", sizes=(20, 200), alpha=0.7, ax=ax)
ax.set_xlabel("Immunization Expenditure (Millions)")
ax.set_ylabel("Infectious Disease Cases")
st.pyplot(fig)

# Key Metrics
st.header("📌 Key Metrics")
cols = st.columns(3)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]
    with col:
        country_data = data_filtered[data_filtered['Country'] == country]
        latest_year = country_data['Year'].max()
        latest_data = country_data[country_data['Year'] == latest_year]
        
        expenditure = latest_data['Expenditure'].sum()
        cases = latest_data['Disease_Cases'].sum()
        
        st.metric(label=f"{country} ({latest_year})", value=f"${expenditure:,.0f}M", delta=f"{cases:,.0f} Cases")

st.write("Data Source: [Your Dataset Name]")
