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
life_expectancy_df = pd.read_csv('ict303assignment2group2-main/data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)
metadata_df = pd.read_csv("ict303assignment2group2-main/data/Metadata_Country_API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv")

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





st.markdown("---")






# start of analysis relationship between healthcare spending and life expectancy
import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm

# --- Load Datasets ---
health_exp_df = pd.read_csv("ict303assignment2group2-main/data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv", skiprows=4)
life_expectancy_df = pd.read_csv("ict303assignment2group2-main/data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv", skiprows=4)

# --- Reshape Both to Long Format ---
health_exp_long = health_exp_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Health Expenditure"
)

life_exp_long = life_expectancy_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Life Expectancy"
)

# --- Merge on Country Code and Year ---
merged_long = pd.merge(
    health_exp_long,
    life_exp_long,
    on=["Country Code", "Year"],
    suffixes=("_Health", "_Life")
)

st.header("The Link: Healthcare Spending and Life Expectancy")
st.markdown("""
 The scatter plot under is to assess directly the relationship between healthcare expenditure and life expectancy, we performed a regression analysis.
This allows us to quantify the impact of healthcare spending on life expectancy, controlling for other factors.
""")
# --- Clean ---
merged_long.dropna(subset=["Health Expenditure", "Life Expectancy"], inplace=True)
merged_long["Year"] = merged_long["Year"].astype(int)

# --- Year Selection ---
year_options = ["All Years"] + list(range(2000, 2023))
selected_year = st.selectbox("Select Year for Analysis", year_options, index=0)

# --- Analysis Based on Year Selection ---
if selected_year == "All Years":
    data_to_use = merged_long
else:
    data_to_use = merged_long[merged_long["Year"] == selected_year]

# --- Regression with statsmodels ---
X = data_to_use['Health Expenditure']
y = data_to_use['Life Expectancy']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()

# --- Extract values ---
slope = model.params['Health Expenditure']
r_squared = model.rsquared
p_value = model.pvalues['Health Expenditure']
correlation = data_to_use['Health Expenditure'].corr(data_to_use['Life Expectancy'])

# --- Create Scatter Plot with Color ---
plot_title = f"Regression: Health Expenditure vs Life Expectancy ({selected_year})" \
    if selected_year != "All Years" \
    else "Regression: Health Expenditure vs Life Expectancy (2000–2022, All Countries)"

regression_plot = px.scatter(
    data_to_use,
    x="Health Expenditure",
    y="Life Expectancy",
    trendline="ols",
    title=plot_title,
    labels={
        "Health Expenditure": "Health Expenditure per Capita (USD)",
        "Life Expectancy": "Life Expectancy (Years)"
    },
    log_x=True,
    template="plotly_dark",  # Use a dark template for better color contrast
    color="Year" if selected_year == "All Years" else None, #add color for all years
)

regression_plot.update_layout(
    xaxis_title="Health Expenditure per Capita (USD, Log Scale)",
    yaxis_title="Life Expectancy (Years)",
    plot_bgcolor='rgba(0,0,0,0)', #make background transparent
    paper_bgcolor='rgba(0,0,0,0)', #make background transparent
    font_color="white" #change font color
)

# --- Display in Streamlit ---
st.plotly_chart(regression_plot, use_container_width=True)

st.markdown(f"""
**Regression Analysis ({selected_year}):**

* **Slope:** {slope:.4f}
* **R-squared:** {r_squared:.4f}
* **P-value:** {p_value:.4f} ({"Statistically significant" if p_value < 0.05 else "Not significant"})
* **Correlation:** {correlation:.4f}
""")

st.markdown("**Key Observations:**")

st.markdown("""
* **Positive Correlation:** The scatter plot clearly shows a positive correlation between healthcare expenditure per 
capita (log scale) and life expectancy. As healthcare spending increases, life expectancy tends to rise.
* **Non-Linear Relationship:** The regression line (red curve) is not a straight line, indicating a non-linear relationship. 
The rate of increase in life expectancy slows down as healthcare spending increases, suggesting diminishing returns at higher expenditure levels.
* **Color Gradient Over Time:** The color gradient from dark purple (2000) to bright yellow (2020) illustrates 
how the relationship has evolved over time. While the positive correlation persists, the distribution of data points shifts, 
indicating changes in healthcare spending and life expectancy across different countries.
* **Moderate R-squared:** The R-squared value of 0.3162 suggests that while healthcare spending is a significant 
predictor of life expectancy, it doesn't explain all the variability. Other factors also play a role.
* **Statistically Significant:** The p-value of 0.0000 indicates that the relationship is statistically significant, 
meaning it's unlikely to have occurred by chance.
* **Moderate Correlation:** The correlation coefficient of 0.5623 indicates a moderately strong positive relationship between the two variables.
""")

st.markdown("**Interpretation:**")

st.markdown("""
This plot provides compelling evidence that increased healthcare expenditure is associated with higher life expectancy. 
However, the non-linear relationship suggests that there are limits to how much additional spending can improve life expectancy. 
It also implies that efficiency and strategic allocation of healthcare resources are crucial. The statistically significant relationship, 
along with the moderate R-squared and correlation, underscores the importance of healthcare investment as one of the key factors influencing 
life expectancy. The color gradient highlights the consistency of this relationship over time, reinforcing the argument 
that sustained investment in healthcare can lead to long-term improvements in life expectancy.
""")

st.markdown("**Call to Action for Target Audiences:**")

st.markdown("""
**Government Policymakers & Legislators:**

* Prioritize strategic investments in healthcare, focusing on efficient spending and equitable access. Implement policies that support preventative care, infrastructure development, and address healthcare disparities to maximize life expectancy improvements. Use this data to justify increased and targeted healthcare funding, demonstrating the tangible return on investment in terms of improved life expectancy.

**Healthcare Investors & Venture Capitalists:**

* Invest in innovative healthcare solutions that optimize the relationship between expenditure and life expectancy. Focus on technologies and services that improve healthcare delivery and efficiency, especially in areas where investments yield the highest returns. Leverage this analysis to identify promising investment opportunities that not only generate financial returns but also contribute to improving global health outcomes.

**Philanthropic Organizations & NGOs:**

* Fund initiatives that address healthcare disparities and improve access to essential services in underserved populations. Prioritize programs focused on maternal and child health, disease prevention, and community-based care. Use this data to guide your funding strategies and maximize impact, demonstrating how targeted investments can lead to significant improvements in life expectancy in vulnerable populations.

**Healthcare Administrators & Providers:**

* Implement data-driven strategies to optimize healthcare spending and improve patient outcomes. Focus on efficiency, quality of care, and patient-centered models. Use this analysis to inform resource allocation and drive improvements in healthcare delivery, demonstrating how strategic investments can lead to better health outcomes and longer life expectancy.

**General Public & Community Leaders:**

* Advocate for increased healthcare funding and support local initiatives that improve access to quality healthcare. Engage with elected officials to prioritize healthcare in policy decisions. Use this analysis to underscore the importance of healthcare investments in your community, highlighting the direct link between healthcare spending and improved life expectancy.
""")



st.markdown("---")
# start of healthcare expenditure vs life expectancy in selected countries



# --- Load Datasets ---
health_exp_df = pd.read_csv('ict303assignment2group2-main/data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv', skiprows=4)
life_expectancy_df = pd.read_csv('ict303assignment2group2-main/data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)

# --- Reshape Both to Long Format ---
health_exp_long = health_exp_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Health Expenditure"
)

life_exp_long = life_expectancy_df.melt(
    id_vars=["Country Name", "Country Code"],
    value_vars=[str(year) for year in range(2000, 2023)],
    var_name="Year",
    value_name="Life Expectancy"
)

# --- Merge datasets ---
merged_long = pd.merge(
    health_exp_long,
    life_exp_long,
    on=["Country Code", "Year"],
    suffixes=("_Health", "_Life")
)

# --- Drop missing values and convert year to int ---
merged_long.dropna(subset=["Health Expenditure", "Life Expectancy"], inplace=True)
merged_long["Year"] = merged_long["Year"].astype(int)

# --- Country Selection ---
all_countries = sorted(merged_long["Country Name_Life"].unique())
default_countries = ["Australia","India", "China", "Japan", "Indonesia", "Algeria"]
selected_countries = st.multiselect("Select Countries for Analysis", all_countries, default=default_countries)

# --- Filter for selected countries ---
filtered_df = merged_long[merged_long["Country Name_Life"].isin(selected_countries)].copy()

# --- Calculate regression statistics for each country ---
regression_results = {}
for country in selected_countries:
    country_data = filtered_df[filtered_df["Country Name_Life"] == country]
    if not country_data.empty:  # check if the country has data
        X = country_data["Health Expenditure"]
        y = country_data["Life Expectancy"]
        X = sm.add_constant(X)
        model = sm.OLS(y, X).fit()
        regression_results[country] = {
            "slope": model.params["Health Expenditure"],
            "r_squared": model.rsquared,
            "p_value": model.pvalues["Health Expenditure"]
        }
    else:
        regression_results[country] = None

# --- Plot with trendline for each country ---
fig = px.scatter(
    filtered_df,
    x="Health Expenditure",
    y="Life Expectancy",
    color="Country Name_Life",
    trendline="ols",
    title="Country-Specific Trends: Healthcare Expenditure vs. Life Expectancy",
    labels={
        "Health Expenditure": "Health Expenditure per Capita (USD)",
        "Life Expectancy": "Life Expectancy (Years)",
        "Country Name_Life": "Country"
    },
    log_x=True,
    template="plotly_white"
)
st.header("Comparative Analysis: Healthcare Spending vs Life Expectancy (Selected Countries, 2000-2022)")
st.markdown("""
This plot compares the relationship between healthcare expenditure per capita 
and life expectancy across six selected countries (Australia, India, China, 
Japan, Indonesia, and Algeria) from 2000 to 2022. 
Its purpose is to visually and statistically illustrate the varying degrees 
to which healthcare spending correlates with life expectancy 
in different national contexts, providing insights into the efficiency 
and effectiveness of healthcare investments.
""")
st.plotly_chart(fig, use_container_width=True)

# --- Display regression statistics in a table ---
st.markdown("**Regression Analysis: Statistical Summary**")

table_data = []
for country in selected_countries:
    if regression_results[country] is not None:
        stats = regression_results[country]
        table_data.append({
            "Country": country,
            "Slope": f"{stats['slope']:.4f}",
            "R-squared": f"{stats['r_squared']:.4f}",
            "P-value": f"{stats['p_value']:.4f}"
        })
    else:
        table_data.append({
            "Country": country,
            "Slope": "N/A",
            "R-squared": "N/A",
            "P-value": "N/A"
        })

st.table(table_data)

# --- Key observation and Interpretation and Call to Action ---
st.markdown("**Key Observations:**")

st.markdown("""
* **Positive Correlation:** All six countries (Australia, India, China, Japan, Indonesia, Algeria) show a positive 
correlation between healthcare expenditure per capita and life expectancy.
* **Varying Strengths of Correlation:** Australia and China exhibit strong linear relationships (high R-squared). 
Japan and Indonesia have weaker correlations (lower R-squared). Algeria has a moderate R-squared. India has a high R-squared and a steep slope.
* **Slope Differences:** India has a significantly steeper slope, suggesting a greater impact of healthcare spending on life expectancy. Australia and Japan have very shallow slopes.
* **Statistical Significance:** All p-values are very low, indicating statistically significant correlations.
* **Logarithmic X-Axis:** The x-axis uses a logarithmic scale to show data across a wide range of spending.
""")

st.markdown("**Interpretation:**")

st.markdown("""
* **Country-Specific Healthcare Dynamics:** The relationship between healthcare spending and life expectancy 
is not uniform, suggesting influences from healthcare system efficiency, policies, and socioeconomic conditions.
* **Efficiency and Returns on Investment:** Higher R-squared values indicate a more predictable relationship, and countries with high slopes indicate a greater return on investment.
* **Potential for Improvement:** Countries with lower R-squared or steeper slopes may improve efficiency or target investments.
* **Comparative Analysis Value:** Side-by-side comparisons provide insights for benchmarking and best practices.
* **Investment Considerations:** The analysis highlights the potential for healthcare investments, but also the importance of country-specific factors.
""")

st.markdown("**Call to Action:**")

st.markdown("""
**Government Policymakers:**

* Utilize this comparative analysis to understand healthcare spending efficiency.
* Prioritize policies that optimize spending for maximum life expectancy gains.
* Investigate why countries with similar spending have different outcomes.
* Investigate why some countries have a greater return on investment for healthcare spending.

**Healthcare Investors:**

* Identify investment opportunities based on the relationship between spending and life expectancy.
* Consider risks associated with countries having moderate R-squared values.
* Consider investing in countries with high returns on investment.

**Public Health Organizations:**

* Research factors influencing variations across countries.
* Share best practices and lessons learned.
* Focus on improving outcomes in countries with low R-squared values.

**General Public:**

* Advocate for transparent and efficient healthcare spending.
* Support equitable access to quality healthcare.
* Demand data-driven methods for improving healthcare outcomes.

**Healthcare Administrators:**

* Benchmark your system's performance against other nations.
* Implement data-driven strategies to optimize resource allocation.
* Look at the healthcare spending of countries with high R squared values.
""")




st.markdown("---")
# START OF HEALTH EXPENDITURE VS LIFE EXPECTANCY BY INCOME GROUP






import pandas as pd
import plotly.express as px
import streamlit as st

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
df = pd.merge(df, metadata_df[["Country Code", "IncomeGroup"]], on="Country Code", how="left")
df.dropna(subset=["Health Expenditure", "Life Expectancy", "IncomeGroup"], inplace=True)
df["Year"] = df["Year"].astype(int)

# Calculate correlation per income group (all years)
correlation_data = []
for group in df["IncomeGroup"].unique():
    subset = df[df["IncomeGroup"] == group]
    if len(subset) > 2:
        r = subset["Health Expenditure"].corr(subset["Life Expectancy"])
        correlation_data.append({"IncomeGroup": group, "Correlation": r})

correlation_df = pd.DataFrame(correlation_data)

# Plot with trendlines (all years, grouped by income)
color_map = {
    'High income': '#006BA4',
    'Low income': '#A2C8EC',
    'Lower middle income': '#E3120B',
    'Upper middle income': '#FAC0BE'
}

fig_scatter = px.scatter(
    df,
    x="Health Expenditure",
    y="Life Expectancy",
    color="IncomeGroup",
    trendline="ols",
    hover_name="Country Name_x",
    title="Healthcare Spending and Life Expectancy by Income Level (2000-2022)",
    labels={
        "Health Expenditure": "Health Expenditure per Capita (USD)",
        "Life Expectancy": "Life Expectancy (Years)"
    },
    log_x=True,
    color_discrete_map=color_map
)

fig_scatter.update_layout(template="plotly_white")

# Plot correlation values
fig_corr = px.bar(
    correlation_df,
    x="IncomeGroup",
    y="Correlation",
    title="Correlation Strength: Income's Influence on Health Outcomes",
    labels={"Correlation": "Correlation (r)"},
    color="IncomeGroup",
    color_discrete_map=color_map
)

fig_corr.update_layout(template="plotly_white")

# Display plots in Streamlit (Scatter Plot first, then Bar Plot)
st.header("Income Disparities and Health Outcomes: The Chain from Expenditure "
             "to Life Expectancy")
st.markdown("""
**Overview:** This analysis examines how income level influences healthcare 
expenditure, and subsequently, life expectancy. It uses a scatter plot 
to visualize the direct relationship between expenditure and life expectancy, 
segmented by income groups, and a bar plot to quantify the strength of these relationships.

**Purpose:** To demonstrate the causal pathway from income disparities to 
variations in healthcare spending, and ultimately, to differences in life 
expectancy. This aims to highlight the systemic impact of economic status 
on health outcomes and to inform targeted interventions.
""")
st.plotly_chart(fig_scatter, use_container_width=True)
st.plotly_chart(fig_corr, use_container_width=True)

# Interpretation and Call to Actions
st.markdown("**Key Observations:**")

st.markdown("""
* **Scatter Plot:**
    * Clear stratification: Higher income groups consistently exhibit higher 
    healthcare expenditure and life expectancy.
    * Trendline variation: The slope and fit of trendlines differ across income 
    groups, suggesting varying impacts of expenditure on life expectancy.
    * Visual disparities: The plot vividly displays the health outcome gaps 
    between income levels.
* **Bar Plot:**
    * Correlation strength: High-income groups show the strongest correlation, 
    indicating a more direct link between expenditure and life expectancy.
    * Weakest link: Upper-middle income groups display the weakest correlation, 
    implying other factors may be at play.
    * Moderate links: Low and lower-middle income groups demonstrate moderate 
    correlations.
""")

st.markdown("**Interpretation:**")

st.markdown("""
* **Income as a Determinant:** Income level significantly influences healthcare 
spending, which in turn impacts life expectancy.
* **Systemic Inequalities:** The data underscores systemic inequalities in 
health outcomes, driven by economic disparities.
* **Efficiency Variations:** Variations in correlation suggest differences 
in healthcare system efficiency across income levels.
* **Causal Chain:** The plots highlight the causal pathway from income 
to expenditure to life expectancy.
""")

st.markdown("**Call to Action:**")

st.markdown("""
**Government Policymakers:**

Prioritize policies that address income inequality to improve health outcomes, 
especially in low- and middle-income countries, by strategically investing 
in healthcare systems that maximize the impact of expenditure on life expectancy; 
investigate and address the factors limiting correlation in upper-middle-income 
countries to optimize healthcare spending and outcomes.

**Healthcare Investors:**

Focus investments on enhancing healthcare efficiency and access, particularly 
in underserved communities, exploring innovative models that break the link 
between low income and poor health outcomes, and prioritize areas that 
demonstrate a high correlation between expenditure and life expectancy 
for better returns.

**Public Health Organizations:**

Develop and advocate for programs and policies that address the social 
determinants of health and ensure equitable access to quality healthcare, 
conducting further research to understand the variations in correlations 
across income groups to inform targeted interventions and improve health outcomes.

**Philanthropic Organizations & NGOs:**

Fund initiatives that directly address healthcare disparities in low-income 
communities, supporting programs that improve healthcare infrastructure 
and access to break the cycle of poverty and poor health, using correlation 
data to guide funding decisions and maximize impact.

**Researchers:**

Investigate the specific factors contributing to weaker correlations in 
upper-middle-income countries and explore the interaction between healthcare 
expenditure, socioeconomic factors, and life expectancy across different 
income groups, publishing findings to inform policy and practice.

**Healthcare Administrators:**

Implement data-driven strategies to improve healthcare efficiency and patient 
outcomes, particularly in low-income settings, benchmarking performance against 
global standards and focusing on optimizing the impact of healthcare spending 
while addressing health disparities.
""")


st.markdown("---")




import streamlit as st

st.title("Comprehensive Conclusion: Healthcare Expenditure and Life Expectancy Analysis")

st.markdown("""
**Comprehensive Conclusion Based on the Entire Analysis:**

This Streamlit application provides a multi-faceted analysis of the relationship between healthcare expenditure 
and life expectancy from 2000 to 2022, considering global, regional, and income-based perspectives.

**Global Trends:**

* The choropleth map reveals significant global disparities in life expectancy, highlighting geographic inequalities.
* The line plot shows a general improvement in life expectancy across all regions over time, but persistent gaps remain, particularly between high- and low-income regions.

**Income Group Analysis:**

* The animated bar chart demonstrates a strong correlation between income level and life expectancy, with high-income countries consistently showing better outcomes.
* The scatter plots and correlation bar charts further illustrate that the strength of the relationship between healthcare expenditure and life expectancy varies significantly across income groups.
* High-income groups have the highest correlation between healthcare expenditure and life expectancy.
* Upper-middle income groups have the lowest correlation between healthcare expenditure and life expectancy.
* There is a large disparity in the amount of healthcare expenditure between high-income and low-income countries.

**Healthcare Expenditure vs. Life Expectancy:**

* Regression analysis indicates a positive correlation between healthcare expenditure and life expectancy, though the relationship is non-linear, 
suggesting diminishing returns at higher spending levels.
* The analysis of selected countries shows that the relationship between healthcare expenditure and life expectancy is not uniform, suggesting influences 
from healthcare system efficiency, policies, and socioeconomic conditions.

Overall, the analysis underscores the complex interplay between healthcare spending, income disparities, and life expectancy. While increased healthcare 
expenditure generally leads to improved life expectancy, its effectiveness is influenced by various factors, including income level, regional differences, 
and healthcare system efficiency. The findings highlight the need for targeted interventions and policies that address socioeconomic inequalities 
and optimize healthcare resource allocation to improve global health outcomes.

**Key Questions Answered Across the Entire Analysis:**

**What are the global disparities in life expectancy?**

* The choropleth map and regional line plot illustrate significant geographic disparities.

**How does income level influence life expectancy?**

* The animated bar chart and correlation analysis demonstrate a strong positive correlation between income level and life expectancy.

**Does healthcare expenditure correlate with life expectancy, and how does this relationship vary across income groups and countries?**

* Yes, there is a positive correlation, but its strength varies significantly, with high-income countries showing the strongest correlation and upper-middle income countries the weakest.

**Are there disparities in healthcare expenditure between income groups?**

* Yes, High-income countries have a significantly higher healthcare expenditure than lower-income countries.

**What is the general trend of life expectancy over time, and how has it been affected by global events?**

* Life expectancy has generally improved, but global events like the COVID-19 pandemic have caused temporary setbacks.

**Does the country that the data is from affect the relationship between healthcare expenditure and life expectancy?**

* Yes, the country that the data is from has a large effect on the relationship between healthcare expenditure and life expectancy.
""")
