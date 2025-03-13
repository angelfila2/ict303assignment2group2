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
        st.error("Error: 'ASEAN pri sch enrolment rate.xlsx' not found. Did you upload it?")
        return None

df = load_data("data/ASEAN pri sch enrolment rate.xlsx")

if df is not None:
    # --- Website Content ---
    st.title("Primary School Enrolment and its Ripple Effects on ASEAN Health")
    st.write(
        """
        This section explores the crucial role of primary school enrolment in shaping the health and well-being of ASEAN nations. 
        We examine how access to basic education, as reflected in enrolment rates, contributes to improved health outcomes and overall life expectancy.
        """
    )

    st.write(
        """
        Primary education lays the foundation for health literacy. Enrolled children are more likely to learn about hygiene, nutrition, and disease prevention,
        leading to healthier lifestyles and informed healthcare decisions later in life. Furthermore, higher enrolment rates often indicate stronger educational systems,
        which can lead to better healthcare infrastructure and accessibility.
        """
    )

    st.write(
        """
        This analysis delves into the relationship between primary school enrolment rates and key health indicators in ASEAN, 
        highlighting the interconnectedness of education and health in building a healthier future for the region.
        """
    )

    # --- Graphs ---
    # Define row ranges and titles for each graph
    graph_info = [(1, 8, "Primary School Enrolment Rate (Total)"),
                  (10, 17, "Primary School Enrolment Rate (Male)"),
                  (18, 25, "Primary School Enrolment Rate (Female)")]

    for start_row, end_row, title in graph_info:
        df_subset = df.iloc[start_row - 1:end_row].copy()

        # Set column names (years)
        df_subset.columns = ['Country'] + [str(year) for year in range(2013, 2023)]

        # Melt the DataFrame
        df_melted = pd.melt(df_subset, id_vars=['Country'],
                            value_vars=[str(year) for year in range(2013, 2023)],
                            var_name='Year', value_name='Enrolment Rate')

        # Replace hyphens with NaN BEFORE converting to numeric
        df_melted['Enrolment Rate'] = df_melted['Enrolment Rate'].replace('-', pd.NA)

        # Convert Year and Enrolment Rate to numeric
        df_melted['Year'] = pd.to_numeric(df_melted['Year'])
        df_melted['Enrolment Rate'] = pd.to_numeric(df_melted['Enrolment Rate'])

        # Create the line plot
        fig = px.line(df_melted, x='Year', y='Enrolment Rate', color='Country',
                      title=title)  # Use dynamic title

        # Update layout
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Enrolment Rate",
            yaxis_range=[80, 100]  # Adjust range as needed
        )

        st.plotly_chart(fig) # Display the plot in Streamlit

        # --- Text Analysis below Graphs ---
    st.subheader("Analysis of Primary School Enrolment Trends")

    st.write(
        """
        **Overall Trends:**

        * **High Enrolment Rates:** All ASEAN countries generally maintain high primary school enrolment rates, mostly above 90%, indicating a strong commitment to basic education across the region.

        **Specific Observations:**

        * **Total Enrolment:** Brunei, Laos, Malaysia, Singapore, and Thailand consistently show enrolment rates close to or exceeding 100% for total primary school enrolment. This could potentially indicate that some students may be enrolled before reaching the official primary school age or that there are students repeating a grade. Cambodia shows a noticeable upward trend in total enrolment over the years.

        * **Male Enrolment:** Similar to total enrolment, most countries maintain high enrolment rates for males. Brunei and Singapore consistently show rates near or above 100%. Lao's male enrolment rate has been gradually increasing. There's a slight dip in male enrolment for Thailand around 2018, but it recovers in the following years.

        * **Female Enrolment:** The trends in female enrolment closely mirror those of male enrolment. Brunei and Singapore again show rates close to or above 100%. Laos demonstrates a consistent increase in female enrolment. Cambodia also shows a clear upward trend, suggesting efforts to improve female access to education. There is a slight decline for Thailand's female enrolment around 2018, mirroring the trend for males, but it recovers in subsequent years.

        **Potential Insights:**

        * **Gender Parity:** Generally, there seems to be a good balance between male and female enrolment rates across most countries, suggesting gender parity in primary education access.
        * **Focus on Education:** The high overall enrolment rates point to a strong emphasis on education within ASEAN countries.
        * **Improvements in Access:** Countries like Cambodia and Laos show significant improvements in enrolment rates over the years, indicating efforts to expand educational access to more children.

        **Analysis/Call to Action:**

        We can conclude that overall primary school enrolment rates are increasing. This is a good chance to better reach out to the public to better help them understand the importance of good healthcare and how it correlates to having better life expectancy over the long term with proper diseases prevention knowledge which can apply throughout their lives over the long term.

        This is an opportunity which the government can heavily capitalise on by educating people to prevent common diseases by teaching more than basic healthcare in school syllabuses which can indirectly help reduce expenditure in some healthcare areas as people can take action on their own to prevent common diseases and resources spent on combating this common diseases can be better used to be spent on more serious diseases or other aspects of healthcare which is still lacking. 
        """
    )


    if st.button("Go to Immunisation Page"):
        st.session_state.page = "immunisation"
        st.experimental_rerun()
