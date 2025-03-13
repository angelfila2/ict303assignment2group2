import streamlit as st
import pandas as pd
import plotly.express as px

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("Error: 'ASEAN immunisation against measles and DPT.xlsx' not found. Did you upload it?")
        return None

df = load_data("data/ASEAN immunisation against measles and DPT.xlsx")

if df is not None:
    # --- Website Content ---
    st.title("Education, Immunization, and Healthy Futures in ASEAN")
    st.write(
        """
        This section explores the powerful link between education and immunization rates in ASEAN, and how they collectively contribute to healthier futures.
        We delve into how education empowers communities to embrace immunization, leading to improved public health outcomes.
        """
    )

    st.write(
        """
        Education plays a vital role in dispelling myths and misconceptions surrounding vaccines. Educated populations are more likely to understand the
        importance of immunization, leading to higher vaccination rates. Furthermore, education often improves access to healthcare information and services,
        ensuring that children receive timely vaccinations against preventable diseases like measles and DPT.
        """
    )

    st.write(
        """
        By examining the correlation between educational attainment and immunization coverage in ASEAN, we highlight the synergistic impact of
        investing in both education and public health to build resilient and thriving communities.
        """
    )

    # --- Graphs ---
    # Define row ranges for each graph and their titles
    graph_info = [(1,8 , "Measles"), (9, 17, "DPT")]  # (start_row, end_row, title)

    for start_row, end_row, title in graph_info:  # Iterate with title
        # Select data for the current graph
        df_subset = df.iloc[start_row - 1:end_row].copy()

        # Extract Vaccine type (now unused, but kept for consistency)
        vaccine_type = df_subset.iloc[0, 0]

        # Set column names (years) from the second row onwards
        df_subset.columns = ['Country'] + [str(year) for year in range(2013, 2020)]

        # Melt the DataFrame for Plotly
        df_melted = pd.melt(df_subset, id_vars=['Country'],
                            value_vars=[str(year) for year in range(2013, 2020)],
                            var_name='Year', value_name='Percentage')

        # Add Vaccine column (now unused, but kept for consistency)
        df_melted['Vaccine'] = vaccine_type

        # Replace hyphens with NaN BEFORE converting to numeric
        df_melted['Percentage'] = df_melted['Percentage'].replace('-', pd.NA)

        # Convert Year and Percentage to numeric
        df_melted['Year'] = pd.to_numeric(df_melted['Year'])
        df_melted['Percentage'] = pd.to_numeric(df_melted['Percentage'])

        # Create the line plot
        fig = px.line(df_melted, x='Year', y='Percentage', color='Country',
                      title=f'Immunisation Rates Over Time by Country ({title})')  # Use title variable

        # Update layout for better readability
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Percentage",
            yaxis_range=[60, 100]  # Set y-axis range from 70 to 100
        )

        st.plotly_chart(fig)

        # --- Graph Analysis ---
    st.header("Graph Analysis")

    st.subheader("Graph 1: Immunisation Rates Over Time by Country (Measles)")
    st.write("""
        * **Overall Trend:** Most ASEAN countries have maintained or slightly increased their measles immunization rates between 2013 and 2019.
        * **High Performers:** Singapore, Brunei, and Malaysia consistently show high immunization rates, generally above 90%.
        * **Low Performers:** Lao PDR and Myanmar have the lowest immunization rates, with noticeable fluctuations over the years.
        * **Potential Outliers:** There might be specific years or countries with unusually high or low rates that warrant further investigation. For example, the Philippines experienced a dip in 2018.
    """)

    st.subheader("Graph 2: Immunisation Rates Over Time by Country (DPT)")
    st.write("""
        * **Overall Trend:** Like measles, DPT immunization rates have remained stable or improved for most countries.
        * **High Performers:** Brunei and Singapore maintain consistently high DPT immunization rates, often close to 100%.
        * **Low Performers:** Lao PDR and Myanmar again have the lowest rates, with some improvements over time.
        * **Variations:** Some countries, such as Cambodia and Vietnam, show more variability in their DPT immunization rates compared to measles.
    """)

    st.subheader("Insights and Observations")
    st.write("""
        * **Regional Progress:** While most ASEAN countries demonstrate progress in measles and DPT immunization, disparities exist between countries.
        * **Focus Areas:** Lao PDR and Myanmar require targeted interventions to improve their immunization coverage for both vaccines.
        * **Potential Outbreaks:** Fluctuations in immunization rates, such as the dip in the Philippines' measles rate in 2018, could indicate vulnerability to outbreaks.
        * **Data Limitations:** The graphs show overall immunization rates but don't reveal underlying factors like access to healthcare or vaccine hesitancy. Further research is needed to understand these factors.
        * **Success Factors:** Analysing the strategies of high-performing countries like Singapore and Brunei could provide valuable insights for other nations.
    """)

    st.subheader("Analysis/Call to Action")
    st.write("""
        Countries that are more wealthy spend more in healthcare such as Brunei and Singapore being a consistent outlier have higher immunisation rates which prevent potential causes of early death such from common diseases such as Measles and DPT. We want to promote more expenditure in educating the general public and the government about the seriousness of such common diseases and improve the fatality rate from common diseases and how it leads to a long term investment in results such as having higher workforce in the future if people do not unnecessarily die from such diseases which can potentially help the economy as a future investment.
    """)

    if st.button("Go to Conclusion Page"):
        st.session_state.page = "conclusion"
        st.experimental_rerun()
