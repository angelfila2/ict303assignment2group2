
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
health_exp_df = pd.read_csv('ict303assignment2group2-main/data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv', skiprows=4)
life_exp_df = pd.read_csv('ict303assignment2group2-main/data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)
metadata_df = pd.read_csv('ict303assignment2group2-main/data/Metadata_Country_API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv')

# Reshape
health_long = health_exp_df.melt(id_vars=["Country Name", "Country Code"],
                                  value_vars=[str(y) for y in range(2000, 2023)],
                                  var_name="Year", value_name="Health Expenditure")

life_long = life_exp_df.melt(id_vars=["Country Name", "Country Code"],
                              value_vars=[str(y) for y in range(2000, 2023)],
                              var_name="Year", value_name="Life Expectancy")

# Merge
df = pd.merge(health_long, life_long, on=["Country Code", "Year"])
df = pd.merge(df, metadata_df[["Country Code", "IncomeGroup", "Region"]], on="Country Code", how="left")
df.dropna(subset=["Health Expenditure", "Life Expectancy", "IncomeGroup", "Region"], inplace=True)
df["Year"] = df["Year"].astype(int)

# --- 3D Line Plot ---
st.title("Comprehensive Conclusion: Healthcare Expenditure and Life Expectancy Analysis")

st.header("3D Line Plot: Healthcare Spending, Life Expectancy, and Time")
st.markdown("""
This 3D line plot visualizes the trend of healthcare expenditure and life expectancy over time for selected countries and income groups.
It allows for an interactive exploration of how these variables evolve together.
""")

# Default countries and income groups
all_countries = sorted(df["Country Name_x"].unique())
all_groups = sorted(df["IncomeGroup"].unique())
default_countries = ["Australia", "India", "China", "Japan", "Indonesia", "Algeria"]
default_groups = all_groups

# Multiselect for countries and income groups
selected_countries = st.multiselect("Select Countries", all_countries, default=default_countries)
selected_groups = st.multiselect("Select Income Groups", all_groups, default=default_groups)

# Average data by income group
avg_group_data = df.groupby(["IncomeGroup", "Year"])[["Health Expenditure", "Life Expectancy"]].mean().reset_index()

# Filter data for countries
filtered_country_data = df[df["Country Name_x"].isin(selected_countries)]

# Combine data for plotting
plot_data = pd.concat([
    filtered_country_data[filtered_country_data["IncomeGroup"].isin(selected_groups)],
    avg_group_data[avg_group_data["IncomeGroup"].isin(selected_groups)]
])

# 3D line plot
fig_3d_line = px.line_3d(
    plot_data,
    x="Year",
    y="Health Expenditure",
    z="Life Expectancy",
    color="IncomeGroup",
    line_group=plot_data.apply(lambda row: row['Country Name_x'] if 'Country Name_x' in row else row['IncomeGroup'], axis=1),
    hover_name=plot_data.apply(lambda row: row['Country Name_x'] if 'Country Name_x' in row else row['IncomeGroup'], axis=1),
    title="3D Line Plot: Healthcare Spending, Life Expectancy, and Year",
    labels={
        "Health Expenditure": "Health Expenditure (USD)",
        "Life Expectancy": "Life Expectancy (Years)",
        "Year": "Year"
    },
    template="plotly_white"
)

fig_3d_line.update_layout(
    scene=dict(
        xaxis=dict(title="Year"),
        yaxis=dict(title="Health Expenditure (USD)"),
        zaxis=dict(title="Life Expectancy (Years)")
    )
)

st.plotly_chart(fig_3d_line, use_container_width=True)

st.markdown("""
**Key Observations from the 3D Plot:**

* **Comparative Analysis:** The 3D plot allows for a direct comparison of life expectancy and healthcare expenditure trends over time, both across selected countries and income groups.
* **Income Group Trends:** The plot clearly visualizes the distinct trajectories of different income groups, highlighting disparities in both healthcare spending and life expectancy.
* **Country-Specific Variations:** Individual countries exhibit unique patterns, demonstrating that the relationship between healthcare spending and life expectancy is influenced by country-specific factors.
* **Temporal Dynamics:** The plot effectively illustrates the temporal evolution of these variables, showing how they have changed over the years.
* **Interactive Insights:** The interactive nature of the 3D plot enables users to explore and analyze the data from multiple perspectives, facilitating a deeper understanding of the underlying trends.

**Interpretation from the 3D Plot:**

This 3D line plot serves as a powerful tool to synthesize the complex interplay between healthcare expenditure, life expectancy, and time.
It reinforces the findings from our analysis, highlighting the significant impact of income disparities and country-specific factors on healthcare outcomes.
The plot's ability to simultaneously display trends for both income groups and individual countries underscores the multifaceted nature of this relationship.
It also accentuates the importance of considering both temporal trends and cross-sectional differences when analyzing healthcare data.
""")

st.markdown("""
**Comprehensive Conclusion Based on the Entire Analysis:**

This Streamlit application provides a multi-faceted analysis of the relationship between healthcare expenditure 
and life expectancy from 2000 to 2022, considering global, regional, and income-based perspectives.

**Global Trends:**

* The choropleth map and regional line plot illustrate significant geographic disparities in life expectancy, highlighting the need for targeted interventions in less developed regions.

**Income Group Analysis:**

* Consistent with the 3D plot, the animated bar chart and correlation analysis demonstrate a strong positive correlation between income level and life expectancy.
* The 3D plot further accentuates the distinct trajectories of different income groups, corroborating the findings that income disparities significantly impact healthcare outcomes.

**Healthcare Expenditure vs. Life Expectancy:**

* As visualized in the 3D plot, the relationship between healthcare expenditure and life expectancy is not uniform across countries and income groups, suggesting the influence of various socioeconomic and policy-related factors.

**Key Questions Answered Across the Entire Analysis:**

**What are the global disparities in life expectancy?**

* The choropleth map and regional line plot illustrate significant geographic disparities, as also evidenced by the varying trends in the 3D plot.

**How does income level influence life expectancy?**

* The animated bar chart and correlation analysis, supported by the 3D plot, demonstrate a strong positive correlation between income level and life expectancy.

**Does healthcare expenditure correlate with life expectancy, and how does this relationship vary across income groups and countries?**

* Yes, there is a positive correlation, but its strength varies significantly, as visualized in the 3D plot, with high-income countries showing the strongest correlation and upper-middle income countries the weakest.

**Are there disparities in healthcare expenditure between income groups?**

* Yes, High-income countries have a significantly higher healthcare expenditure than lower-income countries, a trend clearly visualized in the 3D plot.

**What is the general trend of life expectancy over time, and how has it been affected by global events?**

* Life expectancy has generally improved, but global events like the COVID-19 pandemic have caused temporary setbacks, as observed in the temporal trends in the 3D plot.

**Does the country that the data is from affect the relationship between healthcare expenditure and life expectancy?**

* Yes, the country that the data is from has a large effect on the relationship between healthcare expenditure and life expectancy, as evidenced by the unique trajectories of individual countries in the 3D plot.

**Summary of Call to Actions:**

**Government Policymakers & Legislators:**

* Prioritize strategic investments in healthcare, focusing on efficient spending and equitable access, particularly in regions with lower life expectancy as highlighted in the choropleth map.
* Implement policies that support preventative care, infrastructure development, and address healthcare disparities, considering the income-based differences visualized in the 3D plot.

**Healthcare Investors & Venture Capitalists:**

* Invest in innovative healthcare solutions that optimize the relationship between expenditure and life expectancy, focusing on technologies and services that improve healthcare delivery and efficiency, especially in underserved regions.

**Philanthropic Organizations & NGOs:**

* Fund initiatives that address healthcare disparities and improve access to essential services in underserved populations, prioritizing regions with lower life expectancy and income groups with poorer healthcare outcomes.

**Healthcare Administrators & Providers:**

* Implement data-driven strategies to optimize healthcare spending and improve patient outcomes, considering the country-specific variations highlighted in the 3D plot.

**General Public & Community Leaders:**

* Advocate for increased healthcare funding and support local initiatives that improve access to quality healthcare, particularly in regions with lower life expectancy and income groups with poorer healthcare outcomes.

These call to actions aim to bridge the gap between healthcare spending and life expectancy, particularly in underserved populations, and promote equitable and efficient healthcare systems globally, addressing the disparities and trends visualized in the 3D plot and other analyses.
""")

