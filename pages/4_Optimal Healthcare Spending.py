import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
st.set_page_config(
    page_title="Healthcare Spending Breakdown",
   # page_icon="💰",
    layout="centered"
)
# Load the dataset
file_path = Path("data/merged_lifeBirth_spend.csv" ) # Ensure the file is in the correct directory
df = pd.read_csv(file_path)


# Streamlit Title & Description
st.title("📊 Optimal Healthcare Expenditure to Maximize Life Expectancy")
st.write(f"""
This visualization explores the relationship between **Healthcare Expenditure (% of GDP)** and **Life Expectancy at Birth (Years)**
for the selected year
- A **3rd-degree polynomial regression** curve is fitted to model the trend.
- The **optimal healthcare expenditure** level for **maximizing life expectancy** is highlighted.
""")
# Let user select the year dynamically
available_years = sorted(df["Year"].unique(), reverse=True)
selected_year = st.selectbox("📅 Select Year:", available_years, index=0)  # Default to latest year

# Filter data for the selected year
df_filtered = df[df["Year"] == selected_year]

# Ensure relevant columns are numeric
df_filtered["Healthcare Expenditure"] = pd.to_numeric(df_filtered["Healthcare Expenditure"], errors="coerce")
df_filtered["Life Expectancy at Birth"] = pd.to_numeric(df_filtered["Life Expectancy at Birth"], errors="coerce")
df_filtered = df_filtered[df_filtered["Gender"] == "Both sexes"]  # Filter for "Both sexes"

# Remove NaN values
df_filtered.dropna(subset=["Healthcare Expenditure", "Life Expectancy at Birth"], inplace=True)

# Fit a polynomial regression model to analyze the relationship
x = df_filtered["Healthcare Expenditure"].values
y = df_filtered["Life Expectancy at Birth"].values

# Fit a 3rd-degree polynomial regression curve
z = np.polyfit(x, y, 3)
p = np.poly1d(z)

# Generate smooth values for plotting the curve
x_vals = np.linspace(min(x), max(x), 100)
y_vals = p(x_vals)

# Find the optimal healthcare expenditure that maximizes life expectancy
optimal_expenditure = x_vals[np.argmax(y_vals)]
optimal_life_expectancy = max(y_vals)



# Create an interactive scatter plot
fig = px.scatter(
    df_filtered, x="Healthcare Expenditure", y="Life Expectancy at Birth", color="Location",
    hover_data={"Location": True, "Healthcare Expenditure": True, "Life Expectancy at Birth": True},
    title=f"Optimal Healthcare Expenditure to Maximize Life Expectancy ({selected_year})"
)

# Add the polynomial regression curve
fig.add_trace(
    go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Fitted Curve', line=dict(color='red', dash='dash'))
)

# Mark the optimal point
fig.add_trace(
    go.Scatter(
        x=[optimal_expenditure], y=[optimal_life_expectancy],
        mode='markers', name='Optimal Point',
        marker=dict(color='green', size=10)
    )
)

# Vertical line for optimal expenditure
fig.add_shape(
    go.layout.Shape(
        type="line", x0=optimal_expenditure, x1=optimal_expenditure,
        y0=min(y), y1=max(y_vals), line=dict(color="gray", dash="dot"),
    )
)

# Update labels and layout
fig.update_layout(
    xaxis_title="Healthcare Expenditure (% of GDP)",
    yaxis_title="Life Expectancy (Years)",
    hovermode="closest",
    legend_title="Legend"
)

# Display Plotly figure in Streamlit
st.plotly_chart(fig)

st.metric(label="Optimal Investment", value=f"${optimal_expenditure:.2f}")

# Display optimal healthcare expenditure point
st.subheader("📌 Key Insights : Optimal Healthcare Investment")
st.write(f"""
- The **optimal healthcare expenditure** to maximize life expectancy in **{selected_year}** is **{optimal_expenditure:.2f}% of GDP**.
- At this level of investment, the predicted **maximum life expectancy** is **{optimal_life_expectancy:.2f} years**.
""")
st.subheader("📌 Recommendations")

st.write("""
### **For Finance and Health Ministers**  
✅ **Increase Healthcare Spending to Expand Medical Workforce**  
   - The graph supports a **direct link between healthcare expenditure and the number of doctors**, reinforcing the need for **sustained or increased investments in healthcare.**  
   - Increasing the number of job opportunities for doctors and healthcare professionals not only strengthens the healthcare system but also makes the country more attractive to aspiring medical professionals. By allocating a larger portion of the budget to healthcare manpower, governments can enhance workforce retention, attract top talent, and ensure a steady pipeline of skilled medical personnel. This strategic investment fosters a more resilient healthcare system while contributing to economic growth through job creation in the healthcare sector.
### **For Healthcare Institutions & Hospital Administrators**  
✅ **Improve Efficiency in Doctor Utilization**  
   - The **Singapore model suggests** that a country can achieve **a higher doctor-to-patient ratio without extreme spending increases**—this could mean **optimizing training, digital healthcare solutions, or improving healthcare management.**  
✅ **Strengthen Doctor Retention Strategies**  
   - Increased spending on healthcare must be accompanied by **better working conditions, fair compensation, and incentives** to retain skilled medical professionals.

""")
