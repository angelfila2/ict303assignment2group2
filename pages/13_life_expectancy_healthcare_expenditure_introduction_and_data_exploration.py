import pandas as pd
import plotly.express as px
import streamlit as st



# App title
st.title("Healthcare Expenditure: A Key Driver of Life Expectancy?")
st.markdown("The fundamental question we seek to address is whether increased healthcare expenditure directly translates "
            "to improvements in life expectancy. This analysis explores the global relationship between healthcare spending and life expectancy "
            "outcomes from 2000 to 2022. We hypothesize that countries with higher healthcare expenditure per capita will demonstrate higher average life expectancies, "
            "and we will examine the data to validate this assumption.")



st.markdown("---")



st.header("Life Expectancy Data Exploration (2000–2022)")
st.markdown("Visualize global life expectancy trends by country and region.")

# Load life expectancy data
life_expectancy_df = pd.read_csv('data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)
metadata_df = pd.read_csv("data/Metadata_Country_API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv")

# Clean and reshape
life_expectancy_df = life_expectancy_df[['Country Name', 'Country Code'] + [str(year) for year in range(2000, 2023)]]
df_long = life_expectancy_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Life Expectancy"
)
df_long.dropna(subset=["Life Expectancy"], inplace=True)
df_long["Year"] = df_long["Year"].astype(int)

# Merge region info
df_long = df_long.merge(metadata_df[["Country Code", "Region"]], on="Country Code", how="left")

# --- Choropleth Map ---
st.subheader("Global Life Expectancy: A World of Inequality")
st.markdown("The choropleth map serves to visually represent the global distribution "
            "of life expectancy for a selected year, highlighting the stark geographic "
            "disparities that persist across nations. It aims to underscore "
            "the inequalities in health outcomes, particularly the significant "
            "differences between country, regions and those facing economic and "
            "healthcare challenges, thus setting the stage for further analysis into "
            "the factors driving these disparities")
selected_year = st.slider("Select Year", 2000, 2022, 2010)
map_df = df_long[df_long["Year"] == selected_year]

choropleth_map = px.choropleth(
    map_df,
    locations="Country Code",
    color="Life Expectancy",
    hover_name="Country Name",
    color_continuous_scale="Viridis",
    projection="natural earth",
    title=f"Regional Disparities in Life Expectancy in {selected_year}"
)
choropleth_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
st.plotly_chart(choropleth_map, use_container_width=True)

st.markdown("""
**Key Observations (Choropleth Map for 2010):**

* **Distinct Geographic Pattern:** The map reveals a clear geographic pattern in life expectancy, with darker shades (indicating lower life expectancy) concentrated in specific regions.
* **Sub-Saharan Africa's Low Life Expectancy:** Sub-Saharan Africa is predominantly depicted in dark purple and blue hues, showing a significantly lower life expectancy compared to other regions.
* **High Life Expectancy in Developed Regions:** North America, Europe, and Australia are largely represented in yellow and light green, indicating higher life expectancy.
* **Varied Life Expectancy in Asia and South America:** Asia and South America show a mix of colors, suggesting a wider range of life expectancies within these continents.
* **Clear Gradient:** The color gradient from dark purple to bright yellow provides a clear visual representation of the spectrum of life expectancy across the globe.

**Interpretation (Choropleth Map for 2010):**

This choropleth map for the year 2010 visually underscores the significant global disparities in life expectancy. 
Notably, Sub-Saharan Africa stands out with the lowest life expectancies, likely reflecting factors such as limited access to healthcare, poverty, 
and disease prevalence. In contrast, developed regions like North America and Europe exhibit higher life expectancies, 
indicative of better healthcare infrastructure and living conditions. The varied hues across Asia and South America suggest a more nuanced picture, 
where life expectancy is influenced by diverse socioeconomic factors within these regions. Overall, this map highlights the stark inequalities in health outcomes worldwide, 
emphasizing the need for targeted interventions and investments to improve life expectancy in less developed areas.
""")


# --- Line Plot by Region ---
st.subheader("Life Expectancy Trends: Regional Progress and Persistent Disparities (2000–2022)")
st.markdown(" This line chart shows how average life expectancy changed from 2000 to 2022 across different global regions. "
            "The purpose is to compare life expectancy trends and disparities between regions over time.")
region_df = df_long.dropna(subset=["Region"])
region_avg = region_df.groupby(["Region", "Year"])["Life Expectancy"].mean().reset_index()

line_chart = px.line(
    region_avg,
    x="Year",
    y="Life Expectancy",
    color="Region",
    markers=True,
    title="Average Life Expectancy by Region (2000–2022)"
)
line_chart.update_layout(
    yaxis_title="Life Expectancy",
    xaxis_title="Year",
    template="plotly_white"
)

st.plotly_chart(line_chart, use_container_width=True)

st.markdown("""
**Key Observations:**

* **Overall Improvement:** Life expectancy has risen across all regions from 2000 to 2022.
* **Persistent Gap:** Significant differences in life expectancy remain between regions, 
with high-income regions consistently higher than low-income regions.
* **Sub-Saharan Africa's Progress:** Sub-Saharan Africa shows the fastest rate of improvement, 
though it started from the lowest point.
* **Recent Dip:** A slight decline in life expectancy is noticeable around 2020, 
likely due to global events like the COVID-19 pandemic.

**Interpretation:**

This chart demonstrates that while global life expectancy has generally improved, regional disparities 
persist. The faster improvement in Sub-Saharan Africa suggests potential for progress, but the continued 
gap highlights the need for further investigation into the factors influencing life expectancy, 
setting the stage for exploring the impact of healthcare expenditure.
""")







st.subheader("Life Expectancy Trends: A Comparative Analysis Across Income Groups (2000-2022)")
import pandas as pd
import plotly.express as px
import streamlit as st

# --- Load Data ---
life_expectancy_df = pd.read_csv('data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)
metadata_df = pd.read_csv("data/Metadata_Country_API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv")

# --- Process Data ---
life_expectancy_df = life_expectancy_df[['Country Name', 'Country Code'] + [str(year) for year in range(2000, 2023)]]
life_expectancy_df_long = life_expectancy_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Life Expectancy"
)

life_expectancy_df_long = life_expectancy_df_long.merge(
    metadata_df[["Country Code", "IncomeGroup"]],
    on="Country Code",
    how="left"
)

life_expectancy_df_long.dropna(subset=["Life Expectancy", "IncomeGroup"], inplace=True)
life_expectancy_df_long["Year"] = life_expectancy_df_long["Year"].astype(int)

income_avg = life_expectancy_df_long.groupby(["Year", "IncomeGroup"])["Life Expectancy"].mean().reset_index()

# color map
color_map = {
    'High income': '#006BA4',
    'Low income': '#A2C8EC',
    'Lower middle income': '#E3120B',
    'Upper middle income': '#FAC0BE'
}
# --- Create Plot ---
avg_life_expectancy_by_group_income = px.bar(
    income_avg,
    x="IncomeGroup",
    y="Life Expectancy",
    animation_frame="Year",
    color="IncomeGroup",
    title="Average Life Expectancy by Income Group (2000-2022): Animated Bar Chart",
    labels={"Life Expectancy": "Life Expectancy (Years)", "IncomeGroup": "Income Group"},
    color_discrete_map=color_map
)

avg_life_expectancy_by_group_income.update_layout(
    xaxis_title="Income Group",
    yaxis_title="Average Life Expectancy"
)

# --- Display Plot in Streamlit ---
st.markdown("""
The animated bar chart below isto visualizes the average life expectancy for four income groups
 (High, Low, Lower Middle, Upper Middle) from 2000 to 2022, 
 showing how life expectancy changes over time within each group. The purpose is to clearly 
 illustrate and compare life expectancy disparities between income groups over 
 a 22-year period, highlighting trends and the impact of global events
""")
st.plotly_chart(avg_life_expectancy_by_group_income, use_container_width=True)

# --- Create Table for Display ---
pivot_table = income_avg.pivot_table(
    index="Year",
    columns="IncomeGroup",
    values="Life Expectancy"
)

# --- Display Table in Streamlit ---
st.subheader("Tabular Overview: Life Expectancy by Income Group and Year")
st.dataframe(pivot_table)

# --- Interpretation Section ---
st.markdown("**Key Observations:**")

st.markdown("""
* **Persistent Gaps:** High-income countries consistently show the highest life expectancy, while low-income countries show the lowest.
* **Progressive Increase:** Most income groups demonstrate a gradual increase in average life expectancy over the years.
* **Pandemic Drop:** A clear dip in life expectancy is visible around 2020-2021 across all groups, reflecting the impact of the COVID-19 pandemic.
* **Visual Trend:** The animation effectively showcases the year-by-year changes and the consistent disparities.
""")

st.markdown("**Interpretation:**")

st.markdown("""
* **Income Impact:** The chart reinforces the strong correlation between income level and life expectancy, indicating that socioeconomic factors significantly influence health outcomes.
* **Global Health Progress:** The upward trend suggests general improvements in global healthcare, but the gaps highlight persistent inequalities.
* **Pandemic Vulnerability:** The pandemic's impact demonstrates that all populations are vulnerable, but lower-income groups are disproportionately affected.
* **Long term Trend:** Even with the pandemic impact, the long term trend is that life expectancy is increasing.
""")





st.markdown("---")




# --- Healthcare Expenditure Section ---
st.header("Healthcare Expenditure Data Exploration")
st.subheader("Healthcare Spending Disparities: Income Group Trends (2000–2022)")
st.markdown("""
This area chart visualizes the average healthcare expenditure per capita across 
different income groups from 2000 to 2022. Its purpose is to illustrate the evolution of 
healthcare spending and highlight the persistent disparities in investment between high-income 
and low-income countries. This analysis aims to set the stage for exploring the potential correlation 
between healthcare expenditure and life expectancy, a central question in our investigation.
""")

# Load healthcare expenditure data
health_exp_df = pd.read_csv("data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv", skiprows=4)
metadata_df = pd.read_csv("data/Metadata_Country_API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv")

# Reshape to long format
health_exp_long = health_exp_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Health Expenditure"
)

# Merge with income group info
merged_df = pd.merge(
    health_exp_long,
    metadata_df[["Country Code", "IncomeGroup"]],
    on="Country Code",
    how="left"
)

# Clean and group
merged_df.dropna(subset=["Health Expenditure", "IncomeGroup"], inplace=True)
merged_df["Year"] = merged_df["Year"].astype(int)

income_trend = merged_df.groupby(["IncomeGroup", "Year"])["Health Expenditure"].mean().reset_index()

# Define a custom color sequence (high contrast, colorblind-friendly)
custom_colors = px.colors.qualitative.Set2

# Plot area chart
fig = px.area(
    income_trend,
    x="Year",
    y="Health Expenditure",
    color="IncomeGroup",
    title="Healthcare Expenditure per Capita by Income Group (2000–2022)",
    labels={"Health Expenditure": "Health Expenditure (USD)", "IncomeGroup": "Income Group"},
    color_discrete_sequence=custom_colors
)

fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
**Key Observations:**

* **Dominance of High-Income Spending:** High-income countries exhibit significantly 
higher healthcare spending per capita throughout the entire period, with a dramatic 
surge after 2020.
* **Gradual Growth in Middle-Income:** Upper-middle income countries show a gradual 
increase in spending, particularly accelerating after 2010. Lower-middle income countries 
also show a similar gradual increase, but at a lower level.
* **Stagnation in Low-Income:** Low-income countries maintain a consistently low 
level of healthcare expenditure per capita, with minimal growth over the two decades.
* **Widening Expenditure Gap:** The gap in healthcare spending between high-income 
and low-income countries has widened substantially, especially after 2020.

**Interpretation:**

This visualization clearly demonstrates the stark disparities in healthcare spending 
across different income groups. The consistent dominance of high-income countries, 
coupled with the minimal growth in low-income countries, suggests an uneven distribution 
of healthcare resources globally. The dramatic increase in spending by high-income 
countries after 2020 may reflect increased investment in response to global health 
crises or advancements in medical technology. The widening gap raises critical 
questions about the impact of these spending disparities on life expectancy and 
overall health outcomes across different income levels, warranting further investigation 
into the relationship between healthcare expenditure and life expectancy.
""")
