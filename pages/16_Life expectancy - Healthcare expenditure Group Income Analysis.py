
import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
health_exp_df = pd.read_csv('data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv', skiprows=4)
life_exp_df = pd.read_csv('data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv', skiprows=4)
metadata_df = pd.read_csv('data/Metadata_Country_API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv')

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
