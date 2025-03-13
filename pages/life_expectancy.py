import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("Error: 'ASEAN average life expectancy.xlsx' not found. Did you upload it?")
        return None

df = load_data("data/ASEAN average life expectancy.xlsx")

if df is not None:
    # --- Website Content ---
    st.title("Life Expectancy in ASEAN")

    st.write(
        """
        Life expectancy is a crucial indicator of a population's overall health and well-being. It reflects the quality of healthcare, socioeconomic conditions, and lifestyle factors within a society. This section explores trends in life expectancy across ASEAN countries, highlighting disparities and potential areas for improvement.
        """
    )

    # --- Graph 1: Overall Literacy Rates ---
    st.header("Combined average life expectancy in ASEAN Countries (2013-2022)")

    # 2. Select Combined Data (Rows 0 to 6)
    df_combined = df.iloc[0:6].copy()

    # 3. Clean the data (replace hyphens with NaN)
    df_combined.replace({"-": pd.NA, "-.0": pd.NA}, inplace=True)  # Replace both "-" and "-.0"

    # 4. Melt the DataFrame to long format for easier plotting
    df_melted = pd.melt(df_combined, id_vars='Country', value_vars=df_combined.columns[1:],
                        var_name='Year', value_name='Life Expectancy')

    # 5. Convert 'Year' and 'Life Expectancy' to numeric
    df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')
    df_melted['Life Expectancy'] = pd.to_numeric(df_melted['Life Expectancy'], errors='coerce')

    # 6. Remove rows with NaN values (optional, but good practice)
    df_melted.dropna(subset=['Life Expectancy'], inplace=True)

    # 7. Create the line graph
    fig = px.line(df_melted, x='Year', y='Life Expectancy', color='Country',
                    title='Life Expectancy by Country (Combined Data)')

    # 8. Customize the layout (optional)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Life Expectancy",
        yaxis_range=[60, 90]  # Or a more appropriate range for your data
    )

    # 9. Display the Plotly figure in Streamlit
    st.plotly_chart(fig)

    # --- Graph 2: Individual Country Life Expectancy Trends ---
    st.header("Life Expectancy Trends in Individual ASEAN Countries (2013-2022)")

    # 1. Select Individual Country Data (Rows 7 onwards)
    df_individual = df.iloc[7:14].copy() #changed the rows to 7:15 to match the original data

    # 2. Clean the data (replace hyphens with NaN)
    df_individual.replace({"-": pd.NA, "-.0": pd.NA}, inplace=True)

    # 3. Melt the DataFrame to long format for easier plotting
    df_melted_individual = pd.melt(df_individual, id_vars='Country', value_vars=df_individual.columns[1:],
                                    var_name='Year', value_name='Life Expectancy')

    # 4. Convert 'Year' and 'Life Expectancy' to numeric
    df_melted_individual['Year'] = pd.to_numeric(df_melted_individual['Year'], errors='coerce')
    df_melted_individual['Life Expectancy'] = pd.to_numeric(df_melted_individual['Life Expectancy'], errors='coerce')

    # 5. Remove rows with NaN values (optional, but good practice)
    df_melted_individual.dropna(subset=['Life Expectancy'], inplace=True)

    # 6. Create the line graph
    fig_individual = px.line(df_melted_individual, x='Year', y='Life Expectancy', color='Country',
                                title='Life Expectancy by Country (Individual Data)')

    # 7. Customize the layout (optional)
    fig_individual.update_layout(
        xaxis_title="Year",
        yaxis_title="Life Expectancy",
        yaxis_range=[60, 90]  # Or a more appropriate range for your data
    )

    # 8. Display the Plotly figure in Streamlit
    st.plotly_chart(fig_individual)

    # --- Graph 3: Female Life Expectancy ---
    st.header("Female Life Expectancy by Country (Combined Data)")

    # 2. Select Combined Data (Rows 15 to 22)
    df_combined_female = df.iloc[15:22].copy()

    # 3. Clean the data (replace hyphens with NaN)
    df_combined_female.replace({"-": pd.NA, "-.0": pd.NA}, inplace=True)

    # 4. Melt the DataFrame to long format for easier plotting
    df_melted_female = pd.melt(df_combined_female, id_vars='Country', value_vars=df_combined_female.columns[1:],
                                var_name='Year', value_name='Life Expectancy')

    # 5. Convert 'Year' and 'Life Expectancy' to numeric
    df_melted_female['Year'] = pd.to_numeric(df_melted_female['Year'], errors='coerce')
    df_melted_female['Life Expectancy'] = pd.to_numeric(df_melted_female['Life Expectancy'], errors='coerce')

    # 6. Remove rows with NaN values (optional, but good practice)
    df_melted_female.dropna(subset=['Life Expectancy'], inplace=True)

    # 7. Create the line graph
    fig_female = px.line(df_melted_female, x='Year', y='Life Expectancy', color='Country',
                            title='Female Life Expectancy by Country (Combined Data)')

    # 8. Customize the layout (optional)
    fig_female.update_layout(
        xaxis_title="Year",
        yaxis_title="Life Expectancy",
        yaxis_range=[60, 90]  # Or a more appropriate range for your data
    )

    # 9. Display the Plotly figure in Streamlit
    st.plotly_chart(fig_female)

    # --- Graph Analysis ---
    st.header("Graph Analysis")

    st.subheader("Overall Life Expectancy Trends (Graph 1)")
    st.write("""
     * **General upward trend:** Most ASEAN countries have experienced a steady increase in life expectancy over the years, reflecting improvements in healthcare, sanitation, and living standards.
     * **Singapore as an outlier:** Singapore consistently demonstrates the highest life expectancy among ASEAN nations, significantly exceeding the regional average.
     * **Variations in growth:** While most countries exhibit an upward trend, the rate of increase varies. Some countries, like Brunei, show more rapid progress compared to others.
     * **Data gaps:** There might be some periods with missing data for certain countries, which could affect the interpretation of trends.
    """)

    st.subheader("Male Life Expectancy Trends (Graph 2)")
    st.write("""
     * **Similar upward trend:** Similar to the overall trend, male life expectancy has also increased across most ASEAN countries.
     * **Lower than overall:** Male life expectancy generally appears to be slightly lower compared to the overall average in most countries, potentially due to factors such as higher occupational risks and lifestyle choices.
     * **Country-specific variations:** Again, variations in the rate of increase are evident among countries, highlighting potential differences in healthcare access and lifestyle factors affecting male populations.
    """)

    st.subheader("Female Life Expectancy Trends (Graph 3)")
    st.write("""
     * **Highest life expectancy:** Female life expectancy consistently surpasses both overall and male life expectancy in most ASEAN countries, reflecting a global trend attributed to biological and social factors.
     * **Steeper increase:** In some cases, the increase in female life expectancy appears to be steeper compared to male life expectancy, indicating potential improvements in maternal healthcare and overall well-being for women.
     * **Singapore maintains lead:** Similar to the overall trend, Singapore leads in female life expectancy, showcasing advanced healthcare infrastructure and public health initiatives.
    """)

    st.subheader("Overall Observations and Insights")
    st.write("""
     * **Life expectancy is improving in ASEAN:** The data shows a positive trajectory for life expectancy in the region, indicating overall progress in health and well-being.
     * **Gender differences exist:** There are noticeable differences between male and female life expectancies, suggesting the need for targeted interventions to address specific health needs for each gender.
     * **Singapore's exceptional performance:** Singapore stands out as a model for achieving high life expectancy, potentially due to its strong healthcare system and socioeconomic factors.
    """)

    st.subheader("Analysis/Call to action")
    st.write("""
    While we can see that generally there are higher life expectancy for females over males, males have started to have increased life expectancy, and we should further explore into potential reasons why such as safety in more dangerous job environments can also be a health risk especially in hazardous environment. While individuals are responsible for their own lifestyles which contributes to their health and better awareness of this should be promoted, the government policy makers from various aspects of not just health, but also in areas such as manpower management should also have higher awareness to safety aspects which can also affect healthcare.
    """)

    # Navigation button to go to the next page
    if st.button("Go to Primary School Enrolment Page"):
        st.session_state.page = "prisch_enrolment"
