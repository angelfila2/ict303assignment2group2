import streamlit as st

# Configure the page
st.set_page_config(
    page_title="GDP Dashboard",
    page_icon="🌍",
    layout="centered"
)

# Title
st.title("🌍 GDP Dashboard")
st.markdown("Welcome to the GDP Dashboard! Use the links below to navigate to different sections.")

# Create hyperlinks to different pages
st.markdown("""
### 📌 Navigate to Sections:
- [📊 GDP Data](pages/1_GDP_Data.py)
- [🌍 Select Countries & Years](pages/2_GDP_Selection.py)
- [📈 GDP Visualization](pages/3_GDP_Visualization.py)
- [📊 GDP Growth Comparison](pages/4_GDP_Comparison.py)

Or use the sidebar for navigation.
""")

st.info("Data Source: [World Bank Open Data](https://data.worldbank.org/)")

st.markdown("### Quick Start:")
st.markdown("""
1. Browse GDP data 📊
2. Select your countries & years 🌍
3. Visualize the trends 📈
4. Compare GDP growth 📊
""")

st.markdown("💡 *Click the links above or use the sidebar to explore!*")
