import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Data Loading ---
@st.cache_data
def load_data(file_path):
    try:
        df = pd.read_excel(file_path)
        return df
    except FileNotFoundError:
        st.error("Error: 'ASEAN adult literacy rate.xlsx' not found. Did you upload it?")
        return None

df = load_data("ASEAN adult literacy rate.xlsx")

if df is not None:
    # --- Website Content ---
    st.title("The Impact of Educational Healthcare on Life Expectancy in ASEAN: A Data-Driven Exploration")
    st.write(
        """
        Education and healthcare investment are fundamental pillars of societal well-being. This analysis examines the intricate connection between healthcare spending directed towards education and its impact on life expectancy in ASEAN nations. Using data from the ASEAN Statistics World Book 2023, we delve into how education empowers individuals to make healthier choices and access better healthcare, ultimately contributing to longer lives. This investigation underscores the importance of integrated policies that prioritize both education and health for fostering prosperous and thriving societies.
        """
        """
A high literacy rate is foundational for individual empowerment and societal progress.

  Literacy enables individuals to access information, participate effectively in their communities, and pursue lifelong learning. Education systems play a crucial role in cultivating literacy skills, ensuring that every person has the tools they need to thrive. Investing in quality education directly translates to higher literacy rates, which in turn fosters economic development, improves health outcomes, and strengthens democratic participation. Simply put, literacy is the bridge that connects education to a brighter future
        """
    )

    # --- Graph 1: Overall Literacy Rates ---
    st.header("Overall Literacy Rates in ASEAN Countries (2013-2022)")

    df_countries1 = df.iloc[0:6].copy()
    df_countries1.replace("-", pd.NA, inplace=True)
    for col in df_countries1.columns[1:]:
        df_countries1[col] = pd.to_numeric(df_countries1[col], errors='coerce')
    df_long1 = pd.melt(df_countries1, id_vars=['Country'], value_vars=df_countries1.columns[1:], var_name='Year', value_name='Literacy Rate')
    df_long1.dropna(subset=['Literacy Rate'], inplace=True)
    df_long1['Year'] = df_long1['Year'].astype(str)
    year_order1 = sorted(df_long1['Year'].unique())
    df_long1['Year'] = pd.Categorical(df_long1['Year'], categories=year_order1, ordered=True)
    fig1 = make_subplots(rows=2, cols=3, subplot_titles=df_long1['Country'].unique())
    row1 = 1
    col1 = 1
    for country in df_long1['Country'].unique():
        data1 = df_long1[df_long1['Country'] == country]
        fig1.add_trace(go.Scatter(x=data1['Year'], y=data1['Literacy Rate'], name=country, mode='lines+markers', hoverinfo='x+y', customdata=data1[['Country', 'Literacy Rate']].values, hovertemplate=None), row=row1, col=col1)
        col1 += 1
        if col1 > 3:
            col1 = 1
            row1 += 1
    fig1.update_layout(title_text="", yaxis_range=[75, 100], hovermode="x unified")
    st.plotly_chart(fig1)

    # --- Graph 2: Male Literacy Rates ---
    st.header("Male Literacy Rates in ASEAN Countries (2013-2022)")

    df_countries2 = df.iloc[8:14].copy()  # Select rows for Male data
    df_countries2.replace("-", pd.NA, inplace=True)
    for col in df_countries2.columns[1:]:
        df_countries2[col] = pd.to_numeric(df_countries2[col], errors='coerce')
    df_long2 = pd.melt(df_countries2, id_vars=['Country'], value_vars=df_countries2.columns[1:], var_name='Year', value_name='Literacy Rate')
    df_long2.dropna(subset=['Literacy Rate'], inplace=True)
    df_long2['Year'] = df_long2['Year'].astype(str)
    year_order2 = sorted(df_long2['Year'].unique())
    df_long2['Year'] = pd.Categorical(df_long2['Year'], categories=year_order2, ordered=True)
    fig2 = make_subplots(rows=2, cols=3, subplot_titles=df_long2['Country'].unique())
    row2 = 1
    col2 = 1
    for country in df_long2['Country'].unique():
        data2 = df_long2[df_long2['Country'] == country]
        fig2.add_trace(go.Scatter(x=data2['Year'], y=data2['Literacy Rate'], name=country, mode='lines+markers', hoverinfo='x+y', customdata=data2[['Country', 'Literacy Rate']].values, hovertemplate=None), row=row2, col=col2)
        col2 += 1
        if col2 > 3:
            col2 = 1
            row2 += 1
    fig2.update_layout(title_text="", yaxis_range=[75, 100], hovermode="x unified")
    st.plotly_chart(fig2)

        # --- Graph 3: Female Literacy Rates ---
    st.header("Female Literacy Rates in ASEAN Countries (2013-2022)")

    df_countries3 = df.iloc[16:22].copy()  # Select rows for Female data
    df_countries3.replace("-", pd.NA, inplace=True)
    for col in df_countries3.columns[1:]:
        df_countries3[col] = pd.to_numeric(df_countries3[col], errors='coerce')
    df_long3 = pd.melt(df_countries3, id_vars=['Country'], value_vars=df_countries3.columns[1:], var_name='Year', value_name='Literacy Rate')
    df_long3.dropna(subset=['Literacy Rate'], inplace=True)
    df_long3['Year'] = df_long3['Year'].astype(str)
    year_order3 = sorted(df_long3['Year'].unique())
    df_long3['Year'] = pd.Categorical(df_long3['Year'], categories=year_order3, ordered=True)
    fig3 = make_subplots(rows=2, cols=3, subplot_titles=df_long3['Country'].unique())
    row3 = 1
    col3 = 1
    for country in df_long3['Country'].unique():
        data3 = df_long3[df_long3['Country'] == country]
        fig3.add_trace(go.Scatter(x=data3['Year'], y=data3['Literacy Rate'], name=country, mode='lines+markers', hoverinfo='x+y', customdata=data3[['Country', 'Literacy Rate']].values, hovertemplate=None), row=row3, col=col3)
        col3 += 1
        if col3 > 3:
            col3 = 1
            row3 += 1
    fig3.update_layout(title_text="", yaxis_range=[75, 100], hovermode="x unified")
    st.plotly_chart(fig3)


    st.write(r"""
    **Overall Literacy Rates:**
    * Generally High: All three images show that literacy rates across ASEAN countries are generally high, with most countries exceeding 90% for both males and females. This suggests a strong foundation in basic education across the region.
    * Singapore and Brunei Darussalam consistently lead: These two countries maintain near-100% literacy rates across all categories (total, male, female) throughout the decade, indicating highly successful education systems.
    * Cambodia shows the most variation: Cambodia's literacy rates, especially for females, show the most fluctuation over the years, with some noticeable dips and rises. This suggests potential challenges in maintaining consistent educational progress.

    **Gender Disparities:**
    * Gaps exist but are generally narrowing: Comparing the male and female literacy rate images reveals some gender gaps, particularly in Cambodia and Viet Nam. However, the trends in these countries suggest that the gaps are gradually narrowing over time.
    * Indonesia shows significant improvement for females: The female literacy rate in Indonesia shows a marked increase over the decade, indicating successful efforts in improving girls' access to education.
    * Malaysia and Brunei Darussalam have near-parity: These countries show minimal differences between male and female literacy rates, suggesting equitable access to education for both genders.

    **Trends Over Time:**
    * Most countries show improvement or stability: The majority of countries exhibit either stable high literacy rates or upward trends, indicating continued progress in education.
    * Fluctuations in some countries: Cambodia and Viet Nam show some fluctuations in literacy rates, particularly for females. This could be due to various factors, including socioeconomic challenges, educational policy changes, or data collection inconsistencies.

    **Analysis:**
    *While we can conclude that generally there is an increase in the overall literacy rates with females having steady increase over time, there needs to be more gender specific diseases taught to the respective gender which can help to better improve their lifestyles with better diseases prevention awareness.
    Educational policymakers need to better consider what kind of knowledge should be taught as specific life phases especially in primary and secondary education levels.
    
    """)

    st.write(r"""
**Calls to Action Based on Audience:**

**For Patients and Individuals:**
* Ask your healthcare provider to explain things in simple terms. Don't be afraid to ask questions until you understand.
* Bring a friend or family member to appointments to help you understand and remember important information.
* Use visual aids, like pictures or diagrams, to help you understand health information.
* Seek out health literacy resources in your community, such as classes or workshops.
* Advocate for clear and accessible health information in your community.

**For Healthcare Providers (Doctors, Nurses, Pharmacists):**
* Use plain language and avoid medical jargon when communicating with patients.
* Use visual aids, teach-back methods, and other strategies to ensure patients understand their health information.
* Provide written materials in multiple languages and at appropriate reading levels.
* Offer health literacy training to staff to improve communication skills.
* Collaborate with community organizations to provide health literacy resources.

**For Public Health Organizations:**
* Develop public health campaigns that use clear and simple language, visuals, and culturally appropriate messaging.
* Partner with community leaders and organizations to reach populations with low literacy.
* Provide health information in multiple formats, such as videos, audio recordings, and infographics.
* Evaluate the effectiveness of health communication materials and strategies.
* Advocate for policies that promote health literacy.

**For Children and Families:**
* Parents: Read to your children every day to improve their literacy skills and health knowledge.
* Schools: Incorporate health education into the curriculum from an early age.
* Community organizations: Provide family literacy programs that include health information.
* Healthcare providers: Offer parenting education on health topics.
* Advocate for increased access to early childhood education and literacy programs.

**For Elderly Populations:**
* Healthcare providers: Provide clear and concise medication instructions and appointment reminders.
* Family members: Help elderly loved ones manage their medications and attend appointments.
* Community centers: Offer health literacy workshops and support groups for seniors.
* Advocate for senior-friendly health information and services.

**For Marginalized and Underserved Communities:**
* Community organizations: Provide culturally and linguistically appropriate health literacy resources.
* Healthcare providers: Offer interpreter services and culturally sensitive care.
* Advocate for policies that address health disparities and promote health equity.
* Support programs that improve access to education and healthcare in underserved communities.

**For Insurance Companies and Healthcare Systems:**
* Invest in health literacy training for staff and providers.
* Develop clear and easy-to-understand insurance and healthcare materials.
* Support community-based health literacy programs.
* Track and analyze data on health literacy and its impact on healthcare costs and outcomes.
* Advocate for policies that promote health literacy and reduce healthcare disparities.

**For Educational Institutions:**
* Incorporate health education into all levels of curriculum.
* Provide health literacy training to teachers and staff.
* Partner with healthcare providers to offer health screenings and education to students.
* Offer adult literacy programs that include health information.
* Advocate for policies that support comprehensive health education in schools.
""")



if st.button("Go to Primary School Enrolment Page"):
    st.session_state.page = "prisch_enrolment"
    st.experimental_rerun()






