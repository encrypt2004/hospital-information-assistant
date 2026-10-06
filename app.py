import os

import streamlit as st
from dotenv import load_dotenv

from src.data_loader import load_hospital_data
from src.structured_search import (
    structured_search,
    format_structured_context,
)
from src.router import route_question

from src.rag.vector_store import get_vectorstore
from src.rag.policy_search import (
    search_policy,
    format_policy_context,
)

from src.llm import get_llm
from src.prompt import build_prompt

from src.safety import (
    is_unsafe_query,
    safety_response,
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    st.error("GEMINI_API_KEY is missing. Please add it to your .env file.")
    st.stop()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VinCare Hospital Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        min-width: 260px;
        max-width: 280px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# LOAD RESOURCES
# ============================================================

@st.cache_resource
def load_resources():

    hospital_data = load_hospital_data()

    llm = get_llm()

    vectorstore = get_vectorstore()

    return hospital_data, llm, vectorstore


hospital_data, llm, vectorstore = load_resources()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🏥 VinCare")

    st.caption("Hospital Information Assistant")

    st.divider()

    st.markdown("### What can I help with?")

    with st.expander("🏥 Hospital", expanded=True):

        st.write("• Hospital timings")
        st.write("• Departments")
        st.write("• Hospital information")

    with st.expander("👨‍⚕️ Doctors", expanded=True):

        st.write("• Doctor discovery")
        st.write("• Specialization")
        st.write("• Room numbers")
        st.write("• Doctor schedules")

    with st.expander("📞 Services", expanded=True):

        st.write("• Appointments")
        st.write("• Pharmacy")
        st.write("• Laboratory")
        st.write("• Billing")
        st.write("• Emergency contacts")

    with st.expander("📋 Policies", expanded=True):

        st.write("• Appointment policies")
        st.write("• Hospital policies")
        st.write("• Room changes")
        st.write("• Privacy policies")

    st.divider()

    with st.expander("⚠️ Assistant limitations"):

        st.caption(
            "This assistant provides hospital information only."
        )

        st.caption(
            "It does not provide diagnosis, prescriptions, "
            "treatment recommendations, or medical test interpretation."
        )

    st.divider()

    st.caption("VinCare Hospital")
    st.caption("Fictional hospital dataset")


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🏥 VinCare Hospital Assistant")

st.caption(
    "Hospital information, doctor discovery & policy assistant"
)


# ============================================================
# ABOUT
# ============================================================

with st.expander("ℹ️ About this assistant"):

    st.write(
        """
        VinCare Hospital Assistant helps you find information from
        the hospital's structured records and official hospital policies.

        You can ask about doctors, departments, schedules, rooms,
        hospital timings, contact numbers, appointments and policies.
        """
    )


# ============================================================
# ASK ASSISTANT
# ============================================================

st.subheader("💬 Ask the Assistant")

question = st.chat_input(
    "Ask about doctors, departments, schedules, policies..."
)


# ============================================================
# SUGGESTIONS
# ============================================================

if not question:

    st.markdown("**Try asking:**")

    col1, col2 = st.columns(2)

    with col1:

        st.caption("👨‍⚕️ Doctor questions")

        st.write("• Who are the cardiologists?")
        st.write("• What is Dr. Arjun Mehta's schedule?")

    with col2:

        st.caption("📋 Hospital questions")

        st.write("• What is the appointment contact?")
        st.write("• What is the appointment policy?")


# ============================================================
# PROCESS QUESTION
# ============================================================

if question:

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    with st.chat_message("user"):

        st.write(question)


    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if is_unsafe_query(question):

        with st.chat_message("assistant"):

            st.warning(safety_response())

            st.caption("Source: Safety Policy")

        st.stop()


    # --------------------------------------------------------
    # Route question
    # --------------------------------------------------------

    route = route_question(question)


    # --------------------------------------------------------
    # Search information
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Searching hospital information..."):

            # =================================================
            # STRUCTURED DATA
            # =================================================

            if route == "structured":

                results = structured_search(
                    hospital_data,
                    question,
                )

                context = format_structured_context(
                    results
                )

                source = "Hospital Data"


            # =================================================
            # POLICY RAG
            # =================================================

            else:

                documents = search_policy(
                    vectorstore,
                    question,
                    k=4,
                )

                context = format_policy_context(
                    documents
                )

                source = "Hospital Policy PDF"


            # =================================================
            # GEMINI
            # =================================================

            prompt = build_prompt(
                question=question,
                context=context,
                source=source,
            )

            response = llm.invoke(prompt)


        # ----------------------------------------------------
        # Answer
        # ----------------------------------------------------

        st.write(response.content)

        st.caption(f"📚 Source: {source}")