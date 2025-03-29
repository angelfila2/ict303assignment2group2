import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm





# --- Load Datasets ---
health_exp_df = pd.read_csv('data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv', skiprows=4)
life_expectancy_df = pd.read_csv('data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)

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
