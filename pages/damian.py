import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

# Page Config
st.set_page_config(page_title='Immunization & Disease Dashboard', page_icon='💉')

# -----------------------------------------------------------------------------
# Load Data with Caching

@st.cache_data
def load_data():
    DATA_FILENAME = Path(__file__).parent / 'data/Immunization_expenditure.csv'
    if not DATA_FILENAME.exists():
        st.error(f"File not found: {DATA_FILENAME}")
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILENAME)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')  # Ensure year is numeric
    df.dropna(subset=['Year'], inplace=True)  # Remove invalid year rows
    return df

data = load_data()

if data.empty:
    st.stop()

# -----------------------------------------------------------------------------
# Sidebar Filters
st.sidebar.header("Filters")

if not data.empty:
    min_year, max_year = int(data['Year'].min()), int(data['Year'].max())
    selected_years = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))
    
    countries = sorted(data['Country'].dropna().unique())
    selected_countries = st.sidebar.multiselect("Select Countries", countries, countries[:3] if len(countries) > 0 else [])

    # Filter Data
    data_filtered = data[(data['Year'].between(*selected_years)) & (data['Country'].isin(selected_countries))]
else:
    data_filtered = pd.DataFrame()

# -----------------------------------------------------------------------------
# Dashboard Content
st.title("💉 Immunization Expenditure & Infectious Diseases Dashboard")
st.write("Explore immunization spending and its relationship with infectious disease cases.")

# Line Chart - Immunization Expenditure Over Time
st.header("📊 Immunization Expenditure Over Time")
if not data_filtered.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=data_filtered, x="Year", y="Expenditure", hue="Country", marker="o", ax=ax)
    ax.set_ylabel("Expenditure (Millions)")
    ax.set_xlabel("Year")
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

# Scatter Plot - Expenditure vs. Disease Cases
st.header("🔬 Expenditure vs. Infectious Disease Cases")
if not data_filtered.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(data=data_filtered, x="Expenditure", y="Disease_Cases", hue="Country", size="Population", sizes=(20, 200), alpha=0.7, ax=ax)
    ax.set_xlabel("Immunization Expenditure (Millions)")
    ax.set_ylabel("Infectious Disease Cases")
    st.pyplot(fig)
else:
    st.warning("No data available for selected filters.")

# Key Metrics
st.header("📌 Key Metrics")
if not data_filtered.empty:
    cols = st.columns(min(3, len(selected_countries)))
    
    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]
        with col:
            country_data = data_filtered[data_filtered['Country'] == country]
            if not country_data.empty:
                latest_year = int(country_data['Year'].max())
                latest_data = country_data[country_data['Year'] == latest_year]
                
                if not latest_data.empty:
                    expenditure = latest_data['Expenditure'].sum()
                    cases = latest_data['Disease_Cases'].sum()
                    st.metric(label=f"{country} ({latest_year})", value=f"${expenditure:,.0f}M", delta=f"{cases:,.0f} Cases")
else:
    st.warning("No data available for selected filters.")

st.write("Data Source: [Your Dataset Name]")
