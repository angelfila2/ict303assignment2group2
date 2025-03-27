import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="Manpower costs",
   # page_icon="💰",
    layout="centered"
)
# Load the dataset
@st.cache_data
def load_data():
    file_path = "data/workforce_expenditure.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Title
st.title("Healthcare Expenditure vs Workforce Analysis (ASEAN/Asia)")
st.markdown("""
A well-funded healthcare system plays a crucial role in ensuring accessibility and quality of care. One of the key areas of investment is manpower costs, which directly impact the number of doctors, nurses, and medical staff available per capita.

In this section, we analyze how higher healthcare spending contributes to an improved patient-to-doctor ratio, exploring its significance in enhancing healthcare delivery and, ultimately, improving health outcomes across ASEAN and Asia.
                     
            """)


# Filters (On Main Page)
countries = df["Country"].unique()
years = sorted(df["Year"].unique())

st.header("Analysis of the correlations between healthcare expenditure and manpower in healthcare")

selected_countries = st.multiselect("Select Country/Countries", countries, default=["Singapore", "Malaysia"])
selected_years = st.slider("Select Year Range", min(years), max(years), (min(years), max(years)))

# Filter data based on selection
df_filtered = df[(df["Country"].isin(selected_countries)) & (df["Year"].between(*selected_years))]

fig1 = px.scatter(
    df_filtered, x="Health Expenditure (% GDP)", y="Medical doctors (per 10 000 population)",
    color="Country", trendline="ols",
    title="Healthcare Expenditure vs Medical Doctors"
)
st.plotly_chart(fig1)
st.markdown("<p style='text-align: center; font-weight: bold;'>Source: Graph showing relationship between health expenditure and medical doctors</p>", unsafe_allow_html=True)
 
st.subheader("🔍 Key Insights")

st.write("""
1. **Positive Relationship Between Healthcare Spending & Doctor Availability**  
   - The graph shows a **strong positive correlation** between **health expenditure (% of GDP)** and **the number of medical doctors per 10,000 people** in both Malaysia and Singapore.  
   - This indicates that as a country **allocates more funds to healthcare**, the **availability of doctors increases**, improving access to medical care.

2. **Singapore Has More Doctors per Capita for the Same Healthcare Spending**  
   - For **similar levels of healthcare expenditure (% of GDP)**, **Singapore consistently has more medical doctors per 10,000 people** compared to Malaysia.  
   - This suggests that Singapore's **healthcare system may be more efficient in workforce allocation** or that it invests more in medical education and infrastructure.
3. **Policy Implications: Balancing Growth & Efficiency**  
   - While **higher spending is linked to more doctors**, factors such as **workforce retention, training capacity, and distribution across rural and urban areas** may influence how effectively these investments translate into improved healthcare access.
""")

# Section: Recommendations
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
# Visualization 2: Medical Doctors Over Time
st.header("More Healthcare Workers → Better Patient Care")
st.write("""
         
         
         """)
# Define the available options for the y-axis
y_options = [
    "Medical doctors (per 10 000 population)",
    "Nursing and midwifery personnel (per 10 000 population)",
    "Dentists (per 10 000 population)",
    "Pharmacists (per 10 000 population)"
]

# Let users select the metric they want to visualize
selected_y = st.selectbox("Select a Healthcare Worker Type:", y_options)

chart_type = st.radio("Select Chart Type:", ["Line Chart", "Bar Chart"])
# Create the line chart based on the selected metric
if chart_type == "Line Chart":
    fig2 = px.line(
        df_filtered, x="Year", y=selected_y, color="Country",
        title=f"Trend of {selected_y} Over Time",
        markers=True  # Ensures data points are visible
    )
else:
    fig2 = px.bar(
        df_filtered, x="Year", y=selected_y, color="Country",
        title=f"{selected_y} Per 10,000 Population by Year",
        barmode="group"
    )
st.plotly_chart(fig2)
st.markdown("<p style='text-align: center; font-weight: bold;'>Source: Chart showing trend of  </p>", unsafe_allow_html=True)
 
st.write("""
### 🔍 Key Insights: More Healthcare Workers → Better Doctor-to-Patient Ratio
### Increasing Healthcare Workforce Leads to Improved Doctor-to-Patient Ratio
- The line chart consistently shows an upward trend, indicating that as the number of medical doctors per 10,000 population increases, the doctor-to-patient ratio improves.
This suggests that more healthcare workers allow for better patient distribution, reducing the workload per doctor and ensuring more efficient healthcare delivery.
### Lower Doctor-to-Patient Ratios Result in Higher Quality of Care
- Countries with more doctors per capita tend to have shorter patient wait times, better diagnosis rates, and improved treatment outcomes.
A lower doctor-to-patient ratio means that doctors can spend more time with each patient, leading to better medical assessments, more personalized treatments, and improved patient satisfaction.
Sustained Investment in Healthcare Workforce is Key to Improving Healthcare Access
""")

# Section: Recommendations
st.subheader("📌 Recommendations")

st.write("""
### Finance and Health Ministers
✅ Investing in the medical workforce improves doctor-to-patient ratios and healthcare outcomes
- The graph clearly demonstrates that an increase in the healthcare workforce—across all types of medical professionals—leads to better doctor-to-patient ratios.
- To sustain and enhance patient care quality, continued investment into expanding  healthcare workers should remain a priority in healthcare expenditure.

### General Public (Eligible Voters)
✅ To acquire better patient quality care
- With more healthcare workers, the public will be attended in a more timely manner at healthcare facilities
- Thus, it is in their best interests, to support politicians who are creating policies that support healthcare expenditure in manpower costs.
""")
# Correlation Analysis
st.write("### Correlation Between Healthcare Spending and Workforce")
correlation = df_filtered[["Health Expenditure (% GDP)", "Medical doctors (per 10 000 population)"]].corr().iloc[0,1]
st.write(f"**Correlation Coefficient:** {correlation:.2f} (Closer to 1 means strong positive correlation)")
