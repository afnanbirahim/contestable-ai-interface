# app.py
# Contestable AI Decision Interface
# Final Streamlit MVP for a usable-security / AI-contestability prototype
# Run locally with: streamlit run app.py

from datetime import datetime

import pandas as pd
import streamlit as st


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Contestable AI Decision Interface",
    page_icon="🛡️",
    layout="wide",
)


# -----------------------------
# Lightweight CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        line-height: 1.15;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #4b5563;
        margin-bottom: 1.4rem;
    }
    .card {
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 1rem;
        background: #ffffff;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
        margin-bottom: 1rem;
    }
    .good-card {
        border-left: 6px solid #22c55e;
        background: #f0fdf4;
    }
    .warn-card {
        border-left: 6px solid #f59e0b;
        background: #fffbeb;
    }
    .bad-card {
        border-left: 6px solid #ef4444;
        background: #fef2f2;
    }
    .info-card {
        border-left: 6px solid #3b82f6;
        background: #eff6ff;
    }
    .small-text {
        color: #6b7280;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Session state
# -----------------------------
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if "contestation_submitted" not in st.session_state:
    st.session_state.contestation_submitted = False

if "decision_logged" not in st.session_state:
    st.session_state.decision_logged = False


# -----------------------------
# Helper functions
# -----------------------------
def add_audit_event(event: str) -> None:
    """Add a timestamped event to the audit trail."""
    st.session_state.audit_log.append(
        {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Event": event,
        }
    )


def compute_decision(
    income: int,
    debt_ratio: float,
    employment_years: int,
    missing_docs: int,
    credit_history: int,
    sensitive_context: bool,
):
    """
    Transparent simulated decision model.

    This is not a real credit, hiring, insurance, admission, or moderation model.
    It is only a demonstration model for interaction design and contestability.
    """
    score = 50
    score += min(income / 2000, 20)
    score -= debt_ratio * 35
    score += min(employment_years * 3, 15)
    score += credit_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        decision = "Approved"
        decision_status = "good-card"
    elif score >= 55:
        decision = "Conditional Review"
        decision_status = "warn-card"
    else:
        decision = "Rejected"
        decision_status = "bad-card"

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Income stability": min(income / 2000, 20),
        "Debt burden": -debt_ratio * 35,
        "Employment history": min(employment_years * 3, 15),
        "Relevant history": credit_history * 1.5,
        "Missing documents": -missing_docs * 8,
    }

    review_triggers = []

    if uncertainty >= 60:
        review_triggers.append(
            "The model uncertainty is high enough that automatic processing may be unsafe."
        )

    if missing_docs >= 2:
        review_triggers.append(
            "Important documents may be missing, so the decision may be based on incomplete information."
        )

    if sensitive_context:
        review_triggers.append(
            "The case includes sensitive context and should be checked by a human reviewer."
        )

    if decision == "Rejected" and score >= 45:
        review_triggers.append(
            "The case is near the rejection boundary, so a small correction could change the outcome."
        )

    return score, decision, decision_status, uncertainty, factors, review_triggers


def factor_explanation(factor: str, value: float) -> str:
    """Convert numerical factor influence into plain language."""
    if factor == "Income stability":
        if value >= 15:
            return "Income strongly supported the application."
        if value >= 8:
            return "Income moderately supported the application."
        return "Income gave limited support to the application."

    if factor == "Debt burden":
        if value <= -25:
            return "Debt burden strongly reduced the decision score."
        if value <= -10:
            return "Debt burden moderately reduced the decision score."
        return "Debt burden had only a limited negative effect."

    if factor == "Employment history":
        if value >= 12:
            return "Stable employment or activity history improved confidence."
        if value >= 6:
            return "Employment or activity history gave moderate support."
        return "Employment or activity history gave limited support."

    if factor == "Relevant history":
        if value >= 12:
            return "Relevant history strongly supported the application."
        if value >= 6:
            return "Relevant history moderately supported the application."
        return "Relevant history gave limited support."

    if factor == "Missing documents":
        if value <= -24:
            return "Missing documents strongly reduced confidence in the decision."
        if value < 0:
            return "Missing documents reduced confidence in the decision."
        return "No missing documents reduced the score."

    return "This factor influenced the decision."


def safer_workflow_recommendation(
    decision: str,
    missing_docs: int,
    uncertainty: float,
    review_triggers: list[str],
) -> str:
    """Recommend a safer next step based on the decision context."""
    if missing_docs >= 2:
        return "Request missing documents before making a final decision."

    if uncertainty >= 60:
        return "Send the case to fast human review instead of relying only on automation."

    if decision == "Rejected" and review_triggers:
        return "Allow structured appeal and data correction before final rejection."

    if decision == "Conditional Review":
        return "Use conditional review with limited additional evidence."

    if decision == "Approved":
        return "Proceed, but keep an audit trail and purpose limitation."

    return "Offer explanation and a clear review path."


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-title">🛡️ Contestable AI Decision Interface</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">A working MVP showing how automated decisions can become explainable, contestable, and safer for users.</div>',
    unsafe_allow_html=True,
)

with st.expander("Purpose of this prototype"):
    st.write(
        """
        This prototype demonstrates a human-centered workflow for AI decisions. Instead of showing only an automated outcome,
        it helps users understand the decision, see uncertainty, identify possible errors, submit evidence, request human review,
        and share information only for a specific review purpose.
        """
    )


# -----------------------------
# Sidebar inputs
# -----------------------------
st.sidebar.header("Input Data")

scenario = st.sidebar.selectbox(
    "Decision scenario",
    [
        "Loan application",
        "Hiring shortlist",
        "Insurance claim",
        "University admission",
        "Content moderation appeal",
    ],
)

income = st.sidebar.slider("Monthly income / capacity indicator", 500, 10000, 2600, step=100)
debt_ratio = st.sidebar.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
employment_years = st.sidebar.slider("Years of stable work/activity", 0, 15, 2)
missing_docs = st.sidebar.slider("Missing or unclear documents", 0, 5, 2)
credit_history = st.sidebar.slider("Relevant history score", 0, 10, 5)
sensitive_context = st.sidebar.checkbox("Sensitive context may require human review", value=True)

score, decision, decision_status, uncertainty, factors, review_triggers = compute_decision(
    income,
    debt_ratio,
    employment_years,
    missing_docs,
    credit_history,
    sensitive_context,
)

recommended_workflow = safer_workflow_recommendation(
    decision,
    missing_docs,
    uncertainty,
    review_triggers,
)

if not st.session_state.decision_logged:
    add_audit_event("Decision viewed")
    st.session_state.decision_logged = True


# -----------------------------
# Decision summary
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("AI Decision")
    st.markdown(
        f"""
        <div class="card {decision_status}">
            <b>Scenario:</b> {scenario}<br>
            <b>Decision:</b> {decision}<br>
            <b>Score:</b> {score:.1f}/100
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(int(score))

with col2:
    st.subheader("Uncertainty")
    st.markdown(
        f"""
        <div class="card info-card">
            <b>Estimated uncertainty:</b> {uncertainty:.1f}%<br>
            <span class="small-text">Higher uncertainty means the system should be more careful before finalizing the decision.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(int(uncertainty))


# -----------------------------
# Review triggers and safer workflow
# -----------------------------
st.subheader("Why Human Review May Be Needed")

if review_triggers:
    for trigger in review_triggers:
        st.warning(trigger)
else:
    st.success("No automatic human-review trigger was detected, but the user can still contest the decision.")

st.info(f"Recommended safer workflow: {recommended_workflow}")


# -----------------------------
# Explanation
# -----------------------------
st.subheader("Human-Readable Explanation")

factor_df = pd.DataFrame(
    {
        "Factor": list(factors.keys()),
        "Influence": list(factors.values()),
        "Plain-language meaning": [factor_explanation(k, v) for k, v in factors.items()],
    }
).sort_values("Influence")

st.dataframe(factor_df, use_container_width=True, hide_index=True)

st.write("Key explanation:")
important_factors = factor_df[abs(factor_df["Influence"]) >= 10]

if important_factors.empty:
    st.write("- No single factor strongly dominated the decision.")
else:
    for _, row in important_factors.iterrows():
        st.write(f"- **{row['Factor']}**: {row['Plain-language meaning']}")


# -----------------------------
# Traditional vs contestable comparison
# -----------------------------
st.subheader("Why This Interface Is Different")

compare_col1, compare_col2 = st.columns(2)

with compare_col1:
    st.markdown(
        """
        <div class="card bad-card">
        <b>Traditional AI Notice</b><br><br>
        • Shows a decision only<br>
        • Gives vague explanation<br>
        • Provides generic appeal button<br>
        • User may not know what to challenge<br>
        • User may overshare unnecessary data
        </div>
        """,
        unsafe_allow_html=True,
    )

with compare_col2:
    st.markdown(
        """
        <div class="card good-card">
        <b>Contestable AI Interface</b><br><br>
        • Shows decision and uncertainty<br>
        • Explains important factors in plain language<br>
        • Guides the user to challenge specific issues<br>
        • Supports human review and evidence upload<br>
        • Uses purpose-limited consent
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# Contestation workflow
# -----------------------------
st.subheader("Contest the Decision")

with st.form("contest_form"):
    reasons = st.multiselect(
        "What do you want to challenge?",
        [
            "Incorrect data was used",
            "Important document is missing",
            "The model misunderstood my context",
            "The decision may be unfair or biased",
            "The decision is too uncertain for automatic processing",
            "I want human review",
        ],
    )

    explanation = st.text_area(
        "Explain your challenge",
        placeholder="Example: My current income is higher than shown, and one employment document was missing.",
    )

    uploaded_file = st.file_uploader(
        "Upload optional evidence",
        type=["pdf", "png", "jpg", "jpeg", "docx"],
    )

    review_path = st.radio(
        "Choose review path",
        [
            "Fast human review",
            "Correct data and rerun decision",
            "Full appeal review",
            "Request explanation only",
        ],
    )

    consent = st.checkbox(
        "I consent to share only the selected information for this specific human review purpose."
    )

    submitted = st.form_submit_button("Submit Contestation Request")

if submitted:
    if not reasons:
        st.error("Please select at least one reason for contesting the decision.")
    elif not consent:
        st.error("Please give purpose-limited consent before submitting.")
    else:
        st.session_state.contestation_submitted = True
        add_audit_event("Contestation request submitted")
        st.success("Contestation request submitted successfully.")

        st.markdown("### Contestation Receipt")
        st.markdown(
            f"""
            <div class="card good-card">
            <b>Original decision:</b> {decision}<br>
            <b>Review path:</b> {review_path}<br>
            <b>Purpose limitation:</b> Submitted information may be used only to evaluate this contestation request.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("**Selected challenge reasons:**")
        for reason in reasons:
            st.write(f"- {reason}")

        if explanation:
            st.write("**User explanation:**")
            st.write(explanation)

        if uploaded_file is not None:
            st.write(f"**Uploaded evidence:** {uploaded_file.name}")


# -----------------------------
# Audit trail
# -----------------------------
st.subheader("Audit Trail")
st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True, hide_index=True)


# -----------------------------
# Research framing
# -----------------------------
st.divider()
st.subheader("Research Framing")
st.write(
    """
    This MVP demonstrates actionable contestability. The user does not only receive an automated decision.
    They receive an explanation, uncertainty information, review triggers, a safer workflow recommendation,
    and a structured way to challenge the decision. The goal is to make the safe and fair path easier than a vague appeal process.
    """
)

st.subheader("Suggested User Study")
st.write(
    """
    Compare this interface with a standard AI rejection notice. Measure whether users can understand the decision,
    identify possible errors, choose an appropriate review path, avoid unnecessary data sharing, and feel that the process is fair.
    """
)
