import streamlit as st

st.title("Conclusion: Empowering Futures Through Education")

st.write(
    """
    The data presented in this analysis underscores the undeniable role of education as a cornerstone for a healthier and more prosperous ASEAN.
    We've seen how education, starting from primary school, empowers individuals with the knowledge and skills to make informed choices about their health,
    leading to better health outcomes and longer life expectancy.
    """
)

st.write(
    """
    **Key Takeaways:**

    * **Health Literacy:** Education fosters health literacy, enabling individuals to understand and access healthcare information and services effectively.
    * **Disease Prevention:** Education promotes awareness of disease prevention strategies, including immunization, hygiene, and nutrition, leading to healthier lifestyles.
    * **Empowered Choices:** Educated individuals are more likely to make informed decisions about their health, seek timely medical care, and adhere to treatment plans.
    * **Stronger Systems:** Higher education levels often correlate with better healthcare infrastructure and accessibility, further improving health outcomes.
    """
)

st.header("The Way Forward: A Collaborative Approach")

st.write(
    """
    To fully harness the potential of education in improving health and well-being in ASEAN, a collaborative approach is essential.
    This involves the active participation of:
    """
)

st.subheader("Policy Makers")

st.write(
    """
    * **Prioritize Education:** Invest in quality education systems, ensuring accessibility and affordability for all, especially at the primary school level.
    * **Integrate Health Education:** Incorporate comprehensive health education into curricula, covering topics like hygiene, nutrition, disease prevention, and sexual health.
    * **Support Teacher Training:** Provide teachers with adequate training and resources to effectively deliver health education.
    * **Promote Health Literacy Campaigns:** Launch public awareness campaigns to promote health literacy and encourage healthy behaviors.
    """
)

st.subheader("Healthcare Professionals")

st.write(
    """
    * **Partner with Schools:** Collaborate with schools to provide health screenings, vaccinations, and health education programs.
    * **Engage with Communities:** Conduct outreach programs to educate communities about health issues and available services.
    * **Advocate for Health Policies:** Advocate for policies that support health education and access to healthcare.
    """
)

st.subheader("Private Sector and Investors")

st.write(
    """
    * **Support Educational Initiatives:** Invest in educational programs, scholarships, and infrastructure development.
    * **Fund Health Research:** Support research on health issues prevalent in ASEAN and develop innovative solutions.
    * **Promote Corporate Social Responsibility:** Implement health-focused CSR initiatives to improve community health and well-being.
    """
)

st.subheader("Communities and Individuals")

st.write(
    """
    * **Value Education:** Recognize the importance of education and actively participate in learning opportunities.
    * **Embrace Healthy Lifestyles:** Adopt healthy habits, including regular exercise, balanced nutrition, and preventive healthcare.
    * **Support Health Initiatives:** Engage in community health programs and advocate for improved health policies.
    """
)

st.write(
    """
    By fostering a collaborative ecosystem that values and invests in education, ASEAN can pave the way for a future where health and well-being are accessible to all.
    """
)

if st.button("Go back to Main Page"):  # Optional: Link back to the start
    st.session_state.page = "main"