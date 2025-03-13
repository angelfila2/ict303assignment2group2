import streamlit as st

st.title("Education: The Cornerstone of a Healthy individual")

st.write(
    """
    Welcome to an exploration of how education shapes the health and well-being of ASEAN nations. This project delves into the intricate connections between education,
    healthcare, and life expectancy, highlighting the transformative power of investing in human capital.

    We examine key indicators such as literacy rates, primary school enrolment, and immunization coverage, and analyze their impact on health outcomes.
    Through data-driven insights, we aim to demonstrate the importance of education in empowering individuals, strengthening healthcare systems, and building a healthier future for the ASEAN region.
    """
)

st.write(
    """
    Join us on a journey through the following sections:

    * **Literacy Rates:** Discover how literacy empowers individuals and strengthens communities.
    * **Life Expectancy:** Explore the relationship between education and life expectancy, and uncover factors that contribute to longer, healthier lives.
    * **Primary School Enrolment:** Understand the crucial role of primary education in laying the foundation for health literacy and better healthcare access.
    * **Immunization:** Examine the link between education and immunization rates, and how they collectively contribute to healthier communities.
    * **Conclusion:** Reflect on the key findings and the transformative power of education in shaping a healthier future for ASEAN.

    Let's embark on this exploration together and discover how education can pave the way for a healthier, more prosperous ASEAN.
    """
)

# if 'page' not in st.session_state:
#     st.session_state.page = "literacy_rate"  # Start with the first page

# if st.session_state.page == "literacy_rate":
#     import literacy_rate
# elif st.session_state.page == "life_expectancy":
#     import life_expectancy
# elif st.session_state.page == "prisch_enrolment":
#     import prisch_enrolment
# elif st.session_state.page == "immunisation":
#     import immunisation
# elif st.session_state.page == "conclusion":
#     import conclusion
