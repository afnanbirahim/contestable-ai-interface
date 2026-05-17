import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Contestable AI Interface", page_icon="🛡️", layout="wide")

st.title("🛡️ Contestable AI Decision Interface")
st.write("A simple MVP showing how AI decisions can become explainable and contestable.")

def compute_decision(income, debt_ratio, employment_years, missing_docs, credit_history):
    score = 50
    score += min(income / 2000, 20)
    score -= debt_ratio * 35
    score += min(employment_years * 3, 15)
    score += credit_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        decision = "Approved"
    elif score >= 55:
        decision = "Conditional Review"
    else:
        decision = "Rejected"

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Income stability": min(income / 2000, 20),
        "Debt burden": -debt_ratio * 35,
        "Employment history": min(employment_years * 3, 15),
        "Credit history": credit_history * 1.5,
        "Missing documents": -missing_docs * 8,
    }

    return score, decision, uncertainty, factors

st.sidebar.header("Input Data")

income = st.sidebar.slider("Monthly income", 500, 10000, 2600, step=100)
debt_ratio = st.sidebar.slider("Debt ratio", 0.0, 1.0, 0.42, step=0.01)
employment_years = st.sidebar.slider("Employment years", 0, 15, 2)
missing_docs = st.sidebar.slider("Missing documents", 0, 5, 2)
credit_history = st.sidebar.slider("Credit history score", 0, 10, 5)

score, decision, uncertainty, factors = compute_decision(
    income, debt_ratio, employment_years, missing_docs, credit_history
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("AI Decision")
    st.metric("Decision", decision)
    st.metric("Score", f"{score:.1f}/100")
    st.progress(int(score))

with col2:
    st.subheader("Uncertainty")
    st.metric("Uncertainty", f"{uncertainty:.1f}%")
    st.progress(int(uncertainty))

st.subheader("Explanation")

factor_df = pd.DataFrame({
    "Factor": list(factors.keys()),
    "Influence": list(factors.values())
})

st.dataframe(factor_df, use_container_width=True)

st.subheader("Contest the Decision")

reasons = st.multiselect(
    "What do you want to challenge?",
    [
        "Incorrect data was used",
        "Important document is missing",
        "The model misunderstood my context",
        "The decision may be unfair",
        "I want human review"
    ]
)

explanation = st.text_area("Explain your challenge")

uploaded_file = st.file_uploader("Upload optional evidence", type=["pdf", "png", "jpg", "jpeg"])

consent = st.checkbox("I consent to share this information only for human review.")

if st.button("Submit Contestation Request"):
    if not reasons:
        st.error("Please select at least one reason.")
    elif not consent:
        st.error("Please give purpose-limited consent.")
    else:
        st.success("Contestation request submitted.")
        st.write("Submitted at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        st.write("Reasons:", reasons)
        if explanation:
            st.write("Explanation:", explanation)
        if uploaded_file:
            st.write("Uploaded file:", uploaded_file.name)

st.divider()

st.subheader("Research Framing")
st.write(
    "This MVP shows how explainability can become actionable contestability. "
    "Instead of only showing an AI decision, the interface lets users understand, challenge, "
    "correct, and escalate the decision safely."
)
