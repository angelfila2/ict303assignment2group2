import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="Healthcare Spending Breakdown",
   # page_icon="💰",
    layout="centered"
)


st.header("Breakdown of how ASEAN countries spend on healthcare")
st.write("""
    Efficient allocation of healthcare budgets is vital for ensuring the effectiveness and sustainability of healthcare systems across ASEAN countries. This analysis delves into the distribution of healthcare expenditures, focusing on key areas such as workforce salaries, medical supplies, research, and infrastructure development.

    By examining spending patterns, we aim to uncover national priorities, identify challenges, and highlight opportunities for improvement within the region’s healthcare sector.

    To begin, we take a closer look at Singapore's healthcare expenditure as a case study.
""")


# Load Healthcare Expenditure Data
file_path = Path("data/health_breakdown.csv")

if file_path.exists():
    df = pd.read_csv(file_path)
else:
    st.error("Error: `data/health_breakdown.csv` file not found! Please upload the correct dataset.")
    st.stop()

# Ensure 'Category' column exists
if "Category" not in df.columns:
    st.error("Error: The dataset must have a 'Category' column.")
    st.stop()

# Remove '%' symbols and convert data to numeric
for col in df.columns[1:]:  # Ignore the first column ('Category')
    df[col] = df[col].astype(str).str.replace('%', '', regex=True).astype(float)


# Dropdown to select year
st.subheader("📅 Select Fiscal Year")
available_years = df.columns[1:]

if len(available_years) == 0:
    st.error("Error: No fiscal years found in the dataset!")
    st.stop()

selected_year = st.selectbox("Choose a Financial Year:", available_years)

# Filter data for selected year
df_selected = df[["Category", selected_year]].dropna()
df_selected.columns = ["Category", "Percentage"]

# Check if data is valid for plotting
if df_selected["Percentage"].sum() == 0:
    st.warning(f"No data available for the selected year ({selected_year}).")
else:
    # Generate Pie Chart
    st.subheader(f"📊 Healthcare Expenditure - {selected_year}")
    fig = px.pie(
        df_selected, 
        values="Percentage", 
        names="Category", 
        title=f"Healthcare Expenditure - {selected_year} in Singaproe",
        color_discrete_sequence=px.colors.qualitative.Set2


    )
    fig.update_layout(
    legend=dict(
        x=0.5,  # Center the legend horizontally
        y=-0.2,  # Move legend below the chart
        xanchor="center",
        yanchor="top"
    )
)

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<p style='text-align: center; font-weight: bold;'>Source: Graph showing relationship between health expenditure and medical doctors</p>", unsafe_allow_html=True)


# Insights Section
st.subheader("🔍 Key Insights : Breakdown of healthcare expenditure")
st.write("""
- **Manpower costs** account for the largest portion of healthcare spending across all years. ***This*** could be an area to further investigate as to why countries are spendign so much on manpower costs.
- **Supplies & consumables** spending fluctuates slightly but remains the second highest.
- **Research spending** is consistently low (around 2%).
- **Depreciation & maintenance costs** are relatively stable.


From the graph, it is evident that Singapore allocates nearly three times more to manpower costs compared to other areas in health care
This significant disparity warrants further investigation to understand the underlying factors driving this expenditure. 
Uncovering these insights will help assess the sustainability and effectiveness of Singapore’s healthcare spending strategy.""")

# Footer
st.markdown("---")
st.write("Data is based on provided percentages. Replace with actual data for more accuracy.")
