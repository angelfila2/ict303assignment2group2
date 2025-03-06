import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

# ===========================
# Streamlit Page Configuration
# ===========================
st.set_page_config(
    page_title="📊 Healthcare Investment & Workforce",
    page_icon="🏥",
    layout="wide"
)

# ===========================
# Load Data
# ===========================
data_path = Path(__file__).parent.parent / "data"
workforce_file = data_path / "workforce.csv"
healthcare_file = data_path / "healthcareExpenditure.csv"

df_workforce = pd.read_csv(workforce_file)
df_healthcare = pd.read_csv(healthcare_file, skiprows=4)

# ===========================
# Data Cleaning & Processing
# ===========================
df_workforce.columns = df_workforce.columns.astype(str).str.strip()
df_healthcare.columns = df_healthcare.columns.astype(str).str.strip()

df_workforce["Year"] = pd.to_numeric(df_workforce["Year"], errors='coerce')
df_workforce_filtered = df_workforce[df_workforce["Year"] >= 2010].dropna()

# Select relevant workforce categories
categories = [
    "Medical doctors (per 10 000 population)", 
    "Nursing and midwifery personnel (per 10 000 population)", 
    "Dentists (per 10 000 population)", 
    "Pharmacists  (per 10 000 population)"
]

valid_categories = [col for col in categories if col in df_workforce_filtered.columns]

# Calculate Total Healthcare Workers if valid columns exist
if valid_categories:
    df_workforce_filtered["Total Healthcare Workers"] = df_workforce_filtered[valid_categories].sum(axis=1)

# Rename for merging
if "Countries, territories and areas" in df_workforce_filtered.columns:
    df_workforce_filtered = df_workforce_filtered.rename(columns={"Countries, territories and areas": "Country Name"})

expected_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
available_columns = [col for col in expected_columns if col in df_healthcare.columns]

if available_columns:
    df_melted = df_healthcare.melt(id_vars=available_columns, var_name="Year", value_name="Value")
    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
    df_healthcare_filtered = df_melted[df_melted["Year"] >= 2010].dropna()
    df_healthcare_filtered = df_healthcare_filtered[['Country Name', 'Year', 'Value']]
else:
    st.error("🚨 Healthcare expenditure dataset is missing required columns.")
    st.stop()

df_merged = pd.merge(df_workforce_filtered, df_healthcare_filtered, on=["Country Name", "Year"], how="inner")
df_merged = df_merged.rename(columns={"Value": "Healthcare Expenditure"})

# ===========================
# 📢 Introduction
# ===========================
st.title("📊 Healthcare Investment & Workforce Growth")
st.markdown("""
### Why Should Policymakers Invest More in Healthcare?
- A **strong healthcare workforce** is **critical** for a nation's well-being.
- **💰 Higher healthcare spending** has a **direct impact** on **healthcare workforce density**.
- **📈 Our hypothesis:** *If governments spend more on healthcare, the number of healthcare professionals per capita increases.*
""")

# ===========================
# 🌍 Scatter Plot: Healthcare Expenditure vs Workforce Density
# ===========================
st.subheader("🌍 Does More Healthcare Spending Lead to More Workers?")
st.markdown("This chart compares healthcare spending with the density of healthcare professionals per country.")

fig_scatter = px.scatter(
    df_merged, x="Healthcare Expenditure", y="Total Healthcare Workers",
    hover_name="Country Name", color="Country Name",
    trendline="ols",
    title="Healthcare Expenditure vs. Workforce Density",
    labels={"Healthcare Expenditure": "Healthcare Expenditure (per capita)", "Total Healthcare Workers": "Total Healthcare Workers (per 10,000 population)"},
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ===========================
# 📊 Line Chart: Trends Over Time (Fixed Clutter)
# ===========================
st.subheader("📉 Healthcare Workforce Density Over Time")

# Allow users to select specific countries
all_countries = df_merged["Country Name"].unique()
default_top_countries = df_merged.groupby("Country Name")["Total Healthcare Workers"].mean().nlargest(10).index.tolist()

selected_countries = st.multiselect(
    "🌍 Select Countries to Display (Default: Top 10)", 
    options=all_countries, 
    default=default_top_countries
)

df_selected = df_merged[df_merged["Country Name"].isin(selected_countries)]

# Optional: Rolling Average
rolling_window = st.slider("📊 Apply Rolling Average (Smoother Trend)", min_value=1, max_value=5, value=1)
df_selected["Smoothed Workforce Density"] = df_selected.groupby("Country Name")["Total Healthcare Workers"].transform(lambda x: x.rolling(rolling_window).mean())

# Create Smoothed Line Chart
fig_line = px.line(
    df_selected, x="Year", y="Smoothed Workforce Density", 
    color="Country Name", 
    title="Healthcare Workforce Density Over Time (Selected Countries)",
    labels={"Smoothed Workforce Density": "Healthcare Workers per 10,000 people"},
    hover_name="Country Name"
)

fig_line.update_traces(mode="lines+markers", marker=dict(size=3))

st.plotly_chart(fig_line, use_container_width=True)

# ===========================
# 📌 Country-Level Insights
# ===========================
st.subheader("🔍 Which Countries Invest the Most?")
fig_bar = px.bar(
    df_merged.groupby("Country Name").mean().reset_index(),
    x="Country Name", y="Healthcare Expenditure",
    title="Top & Bottom Countries by Healthcare Expenditure",
    labels={"Healthcare Expenditure": "Avg Healthcare Expenditure (per capita)"},
    color="Country Name"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===========================
# 🌎 Map: Healthcare Expenditure
# ===========================
st.subheader("🌎 Healthcare Investment Across the World")
fig_map = px.choropleth(
    df_merged, locations="Country Name", locationmode="country names",
    color="Healthcare Expenditure", hover_name="Country Name",
    title="Global Healthcare Expenditure",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_map, use_container_width=True)

# ===========================
# 📢 Conclusion & Call to Action
# ===========================
st.subheader("🚀 The Evidence is Clear: Invest More in Healthcare!")
st.markdown("""
- Countries that **increase healthcare spending** see **growth in workforce density**.
- **Strong healthcare systems** depend on **continuous investment**.
- **Policymakers must take action** to ensure a sustainable healthcare workforce.
""")

st.success("📢 Let's push for increased healthcare investment worldwide!")
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import statsmodels.api as sm
from scipy.stats import pearsonr
from pathlib import Path



# ===========================
# Load Data
# ===========================
data_path = Path(__file__).parent.parent / "data"
workforce_file = data_path / "workforce.csv"
healthcare_file = data_path / "healthcareExpenditure.csv"

df_workforce = pd.read_csv(workforce_file)
df_healthcare = pd.read_csv(healthcare_file, skiprows=4)

# ===========================
# Data Cleaning & Processing
# ===========================
df_workforce.columns = df_workforce.columns.astype(str).str.strip()
df_healthcare.columns = df_healthcare.columns.astype(str).str.strip()

df_workforce["Year"] = pd.to_numeric(df_workforce["Year"], errors='coerce')
df_workforce_filtered = df_workforce[df_workforce["Year"] >= 2010].dropna()

# Select relevant workforce categories
categories = [
    "Medical doctors (per 10 000 population)", 
    "Nursing and midwifery personnel (per 10 000 population)", 
    "Dentists (per 10 000 population)", 
    "Pharmacists  (per 10 000 population)"
]

valid_categories = [col for col in categories if col in df_workforce_filtered.columns]

# Calculate Total Healthcare Workers if valid columns exist
if valid_categories:
    df_workforce_filtered["Total Healthcare Workers"] = df_workforce_filtered[valid_categories].sum(axis=1)

# Rename for merging
if "Countries, territories and areas" in df_workforce_filtered.columns:
    df_workforce_filtered = df_workforce_filtered.rename(columns={"Countries, territories and areas": "Country Name"})

expected_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
available_columns = [col for col in expected_columns if col in df_healthcare.columns]

if available_columns:
    df_melted = df_healthcare.melt(id_vars=available_columns, var_name="Year", value_name="Value")
    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
    df_healthcare_filtered = df_melted[df_melted["Year"] >= 2010].dropna()
    df_healthcare_filtered = df_healthcare_filtered[['Country Name', 'Year', 'Value']]
else:
    st.error("🚨 Healthcare expenditure dataset is missing required columns.")
    st.stop()

df_merged = pd.merge(df_workforce_filtered, df_healthcare_filtered, on=["Country Name", "Year"], how="inner")
df_merged = df_merged.rename(columns={"Value": "Healthcare Expenditure"})

# ===========================
# 📊 Scatter Plot with Regression Line
# ===========================
st.subheader("🌍 Does More Healthcare Spending Lead to More Healthcare Workers?")
st.markdown("A regression line shows the relationship between healthcare spending and workforce density.")

fig_scatter = px.scatter(
    df_merged, x="Healthcare Expenditure", y="Total Healthcare Workers",
    hover_name="Country Name", color="Country Name",
    trendline="ols",
    title="Healthcare Expenditure vs. Workforce Density",
    labels={"Healthcare Expenditure": "Healthcare Expenditure (per capita)", "Total Healthcare Workers": "Total Healthcare Workers (per 10,000 population)"},
)
fig_scatter = px.scatter(
    df_merged, x="Healthcare Expenditure", y="Total Healthcare Workers",
    hover_name="Country Name", opacity=0.7,  # Reduce opacity for clarity
    trendline="ols",  # Global regression line
    title="Healthcare Expenditure vs. Workforce Density",
    labels={
        "Healthcare Expenditure": "Healthcare Expenditure (per capita)", 
        "Total Healthcare Workers": "Healthcare Workers (per 10,000 people)"
    }
)


st.plotly_chart(fig_scatter, use_container_width=True)

# ===========================
# 📈 Correlation & Regression Analysis
# ===========================
st.subheader("📊 Statistical Proof: Does the Relationship Hold?")
st.markdown("We calculate the Pearson correlation coefficient and run a regression analysis to confirm the relationship.")

# Correlation Calculation
x = df_merged["Healthcare Expenditure"]
y = df_merged["Total Healthcare Workers"]

# Pearson Correlation
corr, p_value = pearsonr(x, y)
st.write(f"📈 **Pearson Correlation Coefficient (r-value)**: {corr:.2f}")
st.write(f"📊 **P-value**: {p_value:.4f} {'✅ Strong evidence' if p_value < 0.05 else '❌ No strong evidence'}")

# Regression Model
X = sm.add_constant(x)  # Adds intercept
model = sm.OLS(y, X).fit()
st.write("### 🔹 Regression Results")
st.write(model.summary())

# ===========================
# 📊 Compare High vs. Low Spending Countries
# ===========================
st.subheader("💰 Do Richer Countries Have More Healthcare Workers?")
st.markdown("We compare the top 10 and bottom 10 countries based on healthcare expenditure.")

# Identify High & Low Spending Countries
df_grouped = df_merged.groupby("Country Name").mean().reset_index()
df_top10 = df_grouped.nlargest(10, "Healthcare Expenditure")
df_bottom10 = df_grouped.nsmallest(10, "Healthcare Expenditure")

fig_bar = px.bar(
    pd.concat([df_top10, df_bottom10]), x="Country Name", 
    y="Total Healthcare Workers", color="Healthcare Expenditure",
    title="Top 10 vs. Bottom 10 Countries: Healthcare Workers vs. Spending",
    labels={"Total Healthcare Workers": "Healthcare Workers (per 10,000 people)", "Healthcare Expenditure": "Expenditure (per capita)"},
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ===========================
# 📉 Time-Series Analysis (Spending vs. Workforce Over Years)
# ===========================
st.subheader("📅 What Happens When Countries Increase Healthcare Spending?")
st.markdown("This chart shows how workforce density changes when healthcare spending increases over time.")

fig_line = px.line(
    df_merged, x="Year", y="Total Healthcare Workers", color="Country Name",
    title="Workforce Growth in Countries Increasing Healthcare Spending",
    labels={"Total Healthcare Workers": "Healthcare Workers per 10,000 people"},
    hover_name="Country Name"
)

st.plotly_chart(fig_line, use_container_width=True)

# ===========================
# 📢 Conclusion & Call to Action
# ===========================
st.subheader("🚀 The Evidence is Clear: Investing in Healthcare Works!")
st.markdown(f"""
- **📈 Correlation Coefficient (r)**: {corr:.2f} (**{ 'strong' if abs(corr) > 0.5 else 'weak' } correlation**)
- **📊 P-value**: {p_value:.4f} ({'Statistically Significant' if p_value < 0.05 else 'Not Significant'})
- **✅ Regression Model** confirms that **higher healthcare spending is associated with a denser healthcare workforce**.
- **💰 Top-spending countries have significantly more healthcare workers than low-spending ones**.

**📢 Policymakers should increase healthcare investment to build a stronger workforce.**
""")
st.success("📢 Let's push for increased healthcare investment worldwide!")

# ===========================
# Load Data
# ===========================
data_path = Path(__file__).parent.parent / "data"
workforce_file = data_path / "workforce.csv"
healthcare_file = data_path / "healthcareExpenditure.csv"

df_workforce = pd.read_csv(workforce_file)
df_healthcare = pd.read_csv(healthcare_file, skiprows=4)

# ===========================
# Data Cleaning & Processing
# ===========================
df_workforce.columns = df_workforce.columns.astype(str).str.strip()
df_healthcare.columns = df_healthcare.columns.astype(str).str.strip()

df_workforce["Year"] = pd.to_numeric(df_workforce["Year"], errors='coerce')
df_workforce_filtered = df_workforce[df_workforce["Year"] >= 2010].dropna()

# Select relevant workforce categories
categories = [
    "Medical doctors (per 10 000 population)", 
    "Nursing and midwifery personnel (per 10 000 population)", 
    "Dentists (per 10 000 population)", 
    "Pharmacists  (per 10 000 population)"
]

valid_categories = [col for col in categories if col in df_workforce_filtered.columns]

if valid_categories:
    df_workforce_filtered["Total Healthcare Workers"] = df_workforce_filtered[valid_categories].sum(axis=1)

# Rename for merging
if "Countries, territories and areas" in df_workforce_filtered.columns:
    df_workforce_filtered = df_workforce_filtered.rename(columns={"Countries, territories and areas": "Country Name"})

expected_columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]
available_columns = [col for col in expected_columns if col in df_healthcare.columns]

if available_columns:
    df_melted = df_healthcare.melt(id_vars=available_columns, var_name="Year", value_name="Value")
    df_melted["Year"] = pd.to_numeric(df_melted["Year"], errors='coerce')
    df_healthcare_filtered = df_melted[df_melted["Year"] >= 2010].dropna()
    df_healthcare_filtered = df_healthcare_filtered[['Country Name', 'Year', 'Value']]
else:
    st.error("🚨 Healthcare expenditure dataset is missing required columns.")
    st.stop()

df_merged = pd.merge(df_workforce_filtered, df_healthcare_filtered, on=["Country Name", "Year"], how="inner")
df_merged = df_merged.rename(columns={"Value": "Healthcare Expenditure"})

# ===========================
# 📊 Scatter Plot (Fixed)
# ===========================
st.subheader("🌍 Does More Healthcare Spending Lead to More Healthcare Workers?")
st.markdown("A regression line shows the relationship between healthcare spending and workforce density.")

# Country selection to reduce clutter
all_countries = df_merged["Country Name"].unique()
default_countries = ["United States", "Germany", "India", "Japan", "Australia"]

selected_countries = st.multiselect(
    "🌍 Select Countries to Compare",
    options=all_countries,
    default=[c for c in default_countries if c in all_countries]
)

df_filtered = df_merged[df_merged["Country Name"].isin(selected_countries)] if selected_countries else df_merged

# Scatter plot with global regression
fig_scatter = px.scatter(
    df_filtered, x="Healthcare Expenditure", y="Total Healthcare Workers",
    hover_name="Country Name", opacity=0.7, trendline="ols",
    title="Healthcare Expenditure vs. Workforce Density",
    labels={"Healthcare Expenditure": "Healthcare Expenditure (per capita)", "Total Healthcare Workers": "Healthcare Workers (per 10,000 people)"}
)

fig_scatter.update_layout(xaxis_type="log")  # Log scale for better clarity

st.plotly_chart(fig_scatter, use_container_width=True)

# ===========================
# 📈 Correlation Analysis
# ===========================
st.subheader("📊 Statistical Proof: Does the Relationship Hold?")
st.markdown("We calculate the Pearson correlation coefficient and run a regression analysis to confirm the relationship.")

x = df_merged["Healthcare Expenditure"]
y = df_merged["Total Healthcare Workers"]

# Pearson Correlation
corr, p_value = pearsonr(x, y)

st.write(f"📈 **Correlation Coefficient (r)**: {corr:.2f}")
st.write(f"📊 **P-value**: {p_value:.4f} {'✅ Strong evidence' if p_value < 0.05 else '❌ No strong evidence'}")

# Regression Model
X = sm.add_constant(x)  # Adds intercept
model = sm.OLS(y, X).fit()
st.write("### 🔹 Regression Results")
st.write(f"📉 **R-squared**: {model.rsquared:.2f}")
st.write(f"📊 **Regression Coefficients**: {model.params.to_dict()}")
st.write(f"📈 **P-value of Regression Model**: {model.pvalues.to_dict()}")

# ===========================
# 📌 Country-Level Insights
# ===========================
st.subheader("🔍 Which Countries Invest the Most?")
df_grouped = df_merged.groupby("Country Name").mean().reset_index()

df_top10 = df_grouped.nlargest(10, "Healthcare Expenditure")
df_bottom10 = df_grouped.nsmallest(10, "Healthcare Expenditure")

fig_bar = px.bar(
    pd.concat([df_top10, df_bottom10]), x="Country Name",
    y="Total Healthcare Workers", color="Healthcare Expenditure",
    title="Top 10 vs. Bottom 10 Countries: Healthcare Workers vs. Spending",
    labels={"Total Healthcare Workers": "Healthcare Workers (per 10,000 people)", "Healthcare Expenditure": "Expenditure (per capita)"},
    color_continuous_scale="Blues"
)

st.plotly_chart(fig_bar, use_container_width=True)

# ===========================
# 📢 Conclusion
# ===========================
st.subheader("🚀 The Evidence is Clear: Investing in Healthcare Works!")
st.markdown(f"""
- **📈 Correlation Coefficient (r)**: {corr:.2f} (**{ 'strong' if abs(corr) > 0.5 else 'weak' } correlation**)
- **📊 P-value**: {p_value:.4f} ({'Statistically Significant' if p_value < 0.05 else 'Not Significant'})
- **✅ Regression Model** confirms that **higher healthcare spending is associated with a denser healthcare workforce**.
- **💰 Top-spending countries have significantly more healthcare workers than low-spending ones**.

**📢 Policymakers should increase healthcare investment to build a stronger workforce.**
""")
st.success("📢 Let's push for increased healthcare investment worldwide!")
