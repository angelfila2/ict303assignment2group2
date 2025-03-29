import pandas as pd
import plotly.express as px
import streamlit as st
import statsmodels.api as sm

# --- Load Datasets ---
health_exp_df = pd.read_csv("data/API_SH.XPD.CHEX.PC.CD_DS2_en_csv_v2_75935.csv", skiprows=4)
life_expectancy_df = pd.read_csv("data/API_SP.DYN.LE00.IN_DS2_en_CSV_v2_76065.csv", skiprows=4)

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
The rate of increase in life expectancy remains positive even at higher levels of healthcare expenditure. This suggests that significantly more healthcare spending can indeed continue to improve life expectancy.
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
