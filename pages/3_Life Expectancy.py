import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from pathlib import Path
st.set_page_config(
    page_title="Healthcare Spending Breakdown",
   # page_icon="💰",
    layout="centered"
)
# Sidebar: Select Dataset
dataset_choice = st.sidebar.radio(
    "📂 Select Dataset:",
    ["Life Expectancy at Birth", "Life Expectancy at 60"]
)

# Load the appropriate dataset
if dataset_choice == "Life Expectancy at Birth":
    file_path = Path("data/merged_life_work.csv")
    title = "📊 Healthcare Workforce vs Life Expectancy at Birth"
    ylabel = "Life Expectancy at Birth (Years)"
elif dataset_choice == "Life Expectancy at 60":
    file_path = Path("data/merged_life60_work.csv")
    title = "📊 Healthcare Workforce vs Life Expectancy at 60"
    ylabel = "Life Expectancy at 60 (Years)"

# Load the selected dataset
df = pd.read_csv(file_path)

# Ensure relevant columns are numeric
df["Total Healthcare Workers per 10,000 Population"] = pd.to_numeric(df["Total Healthcare Workers per 10,000 Population"], errors="coerce")
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")  # "Value" represents the chosen Life Expectancy metric

# Remove NaN values
df.dropna(subset=["Total Healthcare Workers per 10,000 Population", "Value", "Year"], inplace=True)

# Sidebar: Select Year
available_years = sorted(df["Year"].unique(), reverse=True)
selected_year = st.sidebar.selectbox("📅 Select Year:", available_years, index=0)

# Filter data for the selected year
df_filtered = df[df["Year"] == selected_year]

# Compute Correlation Coefficient
correlation, p_value = pearsonr(df_filtered["Total Healthcare Workers per 10,000 Population"], df_filtered["Value"])

# Streamlit Title & Introduction
st.title(title)
st.write(f"""
This scatter plot visualizes the relationship between **Total Healthcare Workers per 10,000 Population** 
and **{ylabel}** for the selected year **{selected_year}**.
- Each point represents a **country**.
- A **trendline** is added to show the overall pattern.
- A **confidence interval (CI)** is included to indicate the uncertainty in predictions.
- The **correlation coefficient (r)** quantifies the strength of the relationship.
""")

# Seaborn Scatter Plot with Regression Line and Confidence Interval
fig, ax = plt.subplots(figsize=(8, 6))
sns.regplot(
    data=df_filtered, 
    x="Total Healthcare Workers per 10,000 Population", 
    y="Value", 
    scatter_kws={"s": 50, "alpha": 0.7},  # Adjust point size and transparency
    line_kws={"color": "red"},             # Trendline color
    ci=95,                                 # 95% Confidence Interval
    ax=ax
)

ax.set_title(f"Healthcare Workforce vs {ylabel} ({selected_year})", fontsize=14)
ax.set_xlabel("Total Healthcare Workers per 10,000 Population", fontsize=12)
ax.set_ylabel(ylabel, fontsize=12)  # Dynamic label
ax.grid(True)

# Display the plot in Streamlit
st.pyplot(fig)

# Display correlation analysis
st.subheader("📌 Correlation Analysis")
st.write(f"""
- The **correlation coefficient (r) is {correlation:.2f}**, indicating a {"strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.4 else "weak"} relationship between healthcare workforce and life expectancy.
- A **positive correlation** means that **as the number of healthcare workers increases, {ylabel.lower()} also tends to rise**.
- The **p-value is {p_value:.4f}**, {"suggesting a statistically significant correlation" if p_value < 0.05 else "indicating no strong statistical significance"}.
""")

# Conclusion
st.markdown("### **🔍 Key Takeaways**")
st.write(f"""
✅ **A higher number of healthcare workers is generally associated with longer {ylabel.lower()}**, but the strength of this relationship varies by country.  
✅ **The correlation coefficient quantifies the relationship**, helping policymakers assess how effectively healthcare resources are distributed.  
✅ **Not just workforce size, but healthcare system efficiency matters**—countries should ensure that healthcare workers are well-trained and supported.  
""")
ss