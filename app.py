
# app.py
# Contestable AI Decision Interface
# Improved Streamlit MVP for AI contestability, human review, and auditability
# Run locally with: streamlit run app.py

from __future__ import annotations

from datetime import datetime, timedelta
from io import StringIO
from uuid import uuid4

import pandas as pd
import streamlit as st


# ============================================================
# Page configuration
# ============================================================
st.set_page_config(
    page_title="Contestable AI Decision Interface",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }
    .main-title {
        font-size: 2.25rem;
        font-weight: 850;
        margin-bottom: 0.25rem;
        line-height: 1.12;
        letter-spacing: -0.02em;
    }
    .subtitle {
        font-size: 1.02rem;
        color: #4b5563;
        margin-bottom: 1.1rem;
        max-width: 1000px;
    }
    .card {
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: #ffffff;
        box-shadow: 0 1px 5px rgba(0,0,0,0.045);
        margin-bottom: 1rem;
    }
    .good-card {
        border-left: 7px solid #16a34a;
        background: #f0fdf4;
    }
    .warn-card {
        border-left: 7px solid #d97706;
        background: #fffbeb;
    }
    .bad-card {
        border-left: 7px solid #dc2626;
        background: #fef2f2;
    }
    .info-card {
        border-left: 7px solid #2563eb;
        background: #eff6ff;
    }
    .neutral-card {
        border-left: 7px solid #6b7280;
        background: #f9fafb;
    }
    .purple-card {
        border-left: 7px solid #7c3aed;
        background: #f5f3ff;
    }
    .small-text {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.45;
    }
    .tiny-label {
        color: #6b7280;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.2rem;
    }
    .big-value {
        font-size: 1.45rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.2;
    }
    .receipt {
        border: 1px dashed #94a3b8;
        border-radius: 14px;
        padding: 1rem;
        background: #f8fafc;
    }
    .footer-note {
        color: #6b7280;
        font-size: 0.86rem;
        border-top: 1px solid #e5e7eb;
        margin-top: 1.2rem;
        padding-top: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Country and domain configuration
# ============================================================
COUNTRY_CONFIG = {
    "Bangladesh": {
        "short_label": "BD",
        "default_language": "English + Bangla-ready",
        "review_timeline": "3–7 working days",
        "rights_notice": (
            "You may request a human review, correct incomplete information, and submit evidence. "
            "This notice is written as a plain-language organizational review workflow and is not legal advice."
        ),
        "consent_notice": (
            "Submitted information should be used only for this review purpose and should not be reused for unrelated profiling."
        ),
        "retention_notice": "Suggested retention: keep appeal records only as long as needed for review, audit, and lawful dispute handling.",
        "tone": "Plain-language trust and complaint-resolution framing.",
    },
    "EU / UK": {
        "short_label": "EU/UK",
        "default_language": "English + local EU language-ready",
        "review_timeline": "Usually 7–30 days depending on organization policy",
        "rights_notice": (
            "Where a solely automated decision has legal or similarly significant effects, the affected person should be given "
            "meaningful information, a route to human intervention, and a way to contest the outcome."
        ),
        "consent_notice": (
            "Only information necessary for the review should be collected. The purpose and retention period should be clear."
        ),
        "retention_notice": "Suggested retention: align with GDPR/UK GDPR data minimization, purpose limitation, and retention policies.",
        "tone": "Rights-based automated-decision and contestability framing.",
    },
    "United States": {
        "short_label": "US",
        "default_language": "English",
        "review_timeline": "Usually 7–30 days depending on sector and company policy",
        "rights_notice": (
            "The notice should explain the key reasons for the decision and provide a route to correct data or request review. "
            "Sector-specific rules may apply, especially in lending, employment, insurance, and housing."
        ),
        "consent_notice": (
            "Collect only review-relevant information and avoid asking users to disclose unnecessary sensitive details."
        ),
        "retention_notice": "Suggested retention: align with sector rules, dispute handling, and company data-retention policy.",
        "tone": "Adverse-action, fairness, and dispute-resolution framing.",
    },
    "India": {
        "short_label": "IN",
        "default_language": "English + Indian language-ready",
        "review_timeline": "3–15 working days depending on organization policy",
        "rights_notice": (
            "The affected person should be able to understand the reason for the automated or AI-assisted decision, "
            "correct inaccurate data, and request human review."
        ),
        "consent_notice": (
            "Review evidence should be limited to the specific appeal or correction purpose."
        ),
        "retention_notice": "Suggested retention: align with applicable data protection, sector, and internal grievance policies.",
        "tone": "Grievance, review, and digital trust framing.",
    },
    "Generic Global": {
        "short_label": "GLOBAL",
        "default_language": "English",
        "review_timeline": "According to company policy",
        "rights_notice": (
            "This workflow gives the affected person a clear explanation, a correction route, and a human-review path."
        ),
        "consent_notice": (
            "Evidence should be used only for the selected review purpose."
        ),
        "retention_notice": "Suggested retention: keep only what is necessary for review, audit, and dispute handling.",
        "tone": "General contestability and trust framing.",
    },
}


DOMAIN_CONFIG = {
    "Loan application": {
        "affected_person": "Applicant",
        "company_team": "Credit / risk review team",
        "decision_word": "application",
        "evidence_examples": [
            "updated income document",
            "bank statement",
            "employment confirmation",
            "proof of corrected debt information",
        ],
        "sensitive_warning": "Financial hardship, disability, family circumstances, or unusual income patterns may require careful human review.",
    },
    "Hiring shortlist": {
        "affected_person": "Candidate",
        "company_team": "HR / recruitment review team",
        "decision_word": "shortlisting decision",
        "evidence_examples": [
            "updated CV",
            "portfolio link",
            "certificate",
            "work sample",
            "clarification of experience",
        ],
        "sensitive_warning": "Career gaps, disability accommodations, caregiving breaks, or non-standard experience may require human review.",
    },
    "Insurance claim": {
        "affected_person": "Claimant",
        "company_team": "Claims review team",
        "decision_word": "claim",
        "evidence_examples": [
            "medical or repair document",
            "photo evidence",
            "policy document",
            "missing invoice",
        ],
        "sensitive_warning": "Health, accident, disaster, or family circumstances may require careful human review.",
    },
    "University admission": {
        "affected_person": "Applicant",
        "company_team": "Admissions review team",
        "decision_word": "admission decision",
        "evidence_examples": [
            "updated transcript",
            "recommendation letter",
            "test score correction",
            "portfolio or statement",
        ],
        "sensitive_warning": "Interrupted education, disability accommodations, conflict/disaster context, or unusual grading systems may require human review.",
    },
    "Content moderation appeal": {
        "affected_person": "User / creator",
        "company_team": "Trust and safety review team",
        "decision_word": "moderation action",
        "evidence_examples": [
            "context explanation",
            "ownership proof",
            "translation clarification",
            "policy exception explanation",
        ],
        "sensitive_warning": "Journalistic, educational, political, artistic, or local-language context may require human review.",
    },
}


# ============================================================
# Session state
# ============================================================
def init_state() -> None:
    defaults = {
        "case_id": f"CASE-{uuid4().hex[:8].upper()}",
        "audit_log": [],
        "decision_logged": False,
        "contestation_submitted": False,
        "contestation_receipt": None,
        "appeal_payload": None,
        "review_status": "No contestation submitted",
        "reviewer_updates": [],
        "final_outcome": "Pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_case() -> None:
    for key in [
        "case_id",
        "audit_log",
        "decision_logged",
        "contestation_submitted",
        "contestation_receipt",
        "appeal_payload",
        "review_status",
        "reviewer_updates",
        "final_outcome",
        "created_at",
    ]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()
    add_audit_event("New case created", actor="System")


init_state()


# ============================================================
# Helper functions
# ============================================================
def add_audit_event(event: str, actor: str = "System") -> None:
    """Add a timestamped event to the audit trail."""
    st.session_state.audit_log.append(
        {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Actor": actor,
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
) -> tuple[float, str, str, float, dict[str, float], list[str]]:
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
        decision = "Approve / allow"
        decision_status = "good-card"
    elif score >= 55:
        decision = "Conditional human review"
        decision_status = "warn-card"
    else:
        decision = "Reject / restrict"
        decision_status = "bad-card"

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Income or capacity stability": min(income / 2000, 20),
        "Debt or burden ratio": -debt_ratio * 35,
        "Stable work/activity history": min(employment_years * 3, 15),
        "Relevant history": credit_history * 1.5,
        "Missing or unclear documents": -missing_docs * 8,
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

    if decision == "Reject / restrict" and score >= 45:
        review_triggers.append(
            "The case is near the rejection boundary, so a small correction could change the outcome."
        )

    return score, decision, decision_status, uncertainty, factors, review_triggers


def uncertainty_label(uncertainty: float) -> tuple[str, str]:
    if uncertainty >= 70:
        return "High", "bad-card"
    if uncertainty >= 45:
        return "Medium", "warn-card"
    return "Low", "good-card"


def impact_label(decision: str, scenario: str) -> tuple[str, str]:
    if decision == "Approve / allow":
        return "Lower immediate harm", "good-card"
    if scenario in ["Loan application", "Hiring shortlist", "Insurance claim", "University admission"]:
        return "Potentially significant effect", "bad-card"
    return "Potential account/content impact", "warn-card"


def factor_explanation(factor: str, value: float) -> str:
    """Convert numerical factor influence into plain language."""
    if factor == "Income or capacity stability":
        if value >= 15:
            return "Income or capacity information strongly supported the case."
        if value >= 8:
            return "Income or capacity information moderately supported the case."
        return "Income or capacity information gave limited support."

    if factor == "Debt or burden ratio":
        if value <= -25:
            return "Debt or burden information strongly reduced the score."
        if value <= -10:
            return "Debt or burden information moderately reduced the score."
        return "Debt or burden information had only a limited negative effect."

    if factor == "Stable work/activity history":
        if value >= 12:
            return "Stable work or activity history improved confidence."
        if value >= 6:
            return "Work or activity history gave moderate support."
        return "Work or activity history gave limited support."

    if factor == "Relevant history":
        if value >= 12:
            return "Relevant history strongly supported the case."
        if value >= 6:
            return "Relevant history moderately supported the case."
        return "Relevant history gave limited support."

    if factor == "Missing or unclear documents":
        if value <= -24:
            return "Missing or unclear documents strongly reduced confidence."
        if value < 0:
            return "Missing or unclear documents reduced confidence."
        return "No missing documents reduced the score."

    return "This factor influenced the decision."


def challenge_suggestion(factor: str, value: float) -> str:
    """Suggest a targeted contestation route based on a factor."""
    if "Missing" in factor and value < 0:
        return "Upload the missing document or explain why it is unavailable."
    if "Debt" in factor and value <= -10:
        return "Correct debt/burden data if it is outdated or wrongly measured."
    if "Income" in factor and value < 8:
        return "Provide updated income/capacity evidence if the old record is incomplete."
    if "work" in factor.lower() and value < 6:
        return "Clarify work, activity, study, caregiving, or non-standard experience."
    if "Relevant history" in factor and value < 6:
        return "Provide context that the available history does not capture."
    return "Review this factor and challenge it only if it is inaccurate or incomplete."


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

    if decision == "Reject / restrict" and review_triggers:
        return "Allow structured appeal and data correction before final rejection."

    if decision == "Conditional human review":
        return "Use conditional review with limited additional evidence."

    if decision == "Approve / allow":
        return "Proceed, but keep an audit trail and purpose limitation."

    return "Offer explanation and a clear review path."


def build_factor_df(factors: dict[str, float]) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "Factor": list(factors.keys()),
            "Influence": list(factors.values()),
            "Plain-language meaning": [factor_explanation(k, v) for k, v in factors.items()],
            "What the person can do": [challenge_suggestion(k, v) for k, v in factors.items()],
        }
    )
    return df.sort_values("Influence")


def make_audit_csv() -> str:
    df = pd.DataFrame(st.session_state.audit_log)
    return df.to_csv(index=False)


def make_case_report(
    scenario: str,
    country: str,
    score: float,
    decision: str,
    uncertainty: float,
    recommended_workflow: str,
    factor_df: pd.DataFrame,
) -> str:
    output = StringIO()
    output.write("# Contestable AI Decision Case Report\n\n")
    output.write(f"Case ID: {st.session_state.case_id}\n\n")
    output.write(f"Created at: {st.session_state.created_at}\n\n")
    output.write(f"Country template: {country}\n\n")
    output.write(f"Scenario: {scenario}\n\n")
    output.write(f"Automated recommendation: {decision}\n\n")
    output.write(f"Score: {score:.1f}/100\n\n")
    output.write(f"Uncertainty: {uncertainty:.1f}%\n\n")
    output.write(f"Recommended safer workflow: {recommended_workflow}\n\n")

    output.write("## Explanation factors\n\n")
    for _, row in factor_df.iterrows():
        output.write(
            f"- {row['Factor']}: influence {row['Influence']:.2f}. "
            f"{row['Plain-language meaning']} "
            f"Suggested contestation route: {row['What the person can do']}\n"
        )

    output.write("\n## Contestation status\n\n")
    output.write(f"{st.session_state.review_status}\n\n")

    if st.session_state.appeal_payload:
        payload = st.session_state.appeal_payload
        output.write("## Appeal payload\n\n")
        output.write(f"Review path: {payload.get('review_path')}\n\n")
        output.write(f"Reasons: {', '.join(payload.get('reasons', []))}\n\n")
        output.write(f"Explanation: {payload.get('explanation') or 'No explanation provided.'}\n\n")
        output.write(f"Uploaded file name: {payload.get('uploaded_file_name') or 'No file uploaded.'}\n\n")

    if st.session_state.reviewer_updates:
        output.write("## Reviewer updates\n\n")
        for update in st.session_state.reviewer_updates:
            output.write(
                f"- {update['Time']} | {update['Reviewer']} | {update['Outcome']} | {update['Note']}\n"
            )

    output.write("\n## Audit log\n\n")
    for event in st.session_state.audit_log:
        output.write(f"- {event['Time']} | {event['Actor']} | {event['Event']}\n")

    output.write("\n\nDisclaimer: This is a prototype report, not a legal compliance certificate.\n")
    return output.getvalue()


def card(title: str, value: str, note: str, style: str = "neutral-card") -> None:
    st.markdown(
        f"""
        <div class="card {style}">
            <div class="tiny-label">{title}</div>
            <div class="big-value">{value}</div>
            <div class="small-text">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# Header
# ============================================================
st.markdown(
    '<div class="main-title">🛡️ Contestable AI Decision Interface</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">A stronger Streamlit MVP for automated-decision explanation, affected-person contestation, human review, and audit reporting.</div>',
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar controls
# ============================================================
st.sidebar.header("Case Setup")

country = st.sidebar.selectbox(
    "Country / legal template",
    list(COUNTRY_CONFIG.keys()),
    index=0,
)

scenario = st.sidebar.selectbox(
    "Decision scenario",
    list(DOMAIN_CONFIG.keys()),
    index=0,
)

st.sidebar.divider()
st.sidebar.subheader("Simulated Decision Inputs")

income = st.sidebar.slider("Monthly income / capacity indicator", 500, 10000, 2600, step=100)
debt_ratio = st.sidebar.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
employment_years = st.sidebar.slider("Years of stable work/activity", 0, 15, 2)
missing_docs = st.sidebar.slider("Missing or unclear documents", 0, 5, 2)
credit_history = st.sidebar.slider("Relevant history score", 0, 10, 5)
sensitive_context = st.sidebar.checkbox("Sensitive context may require human review", value=True)

st.sidebar.divider()
if st.sidebar.button("Create new case / reset demo"):
    reset_case()

st.sidebar.caption(f"Current case: {st.session_state.case_id}")


# ============================================================
# Computation
# ============================================================
score, decision, decision_status, uncertainty, factors, review_triggers = compute_decision(
    income,
    debt_ratio,
    employment_years,
    missing_docs,
    credit_history,
    sensitive_context,
)
recommended_workflow = safer_workflow_recommendation(decision, missing_docs, uncertainty, review_triggers)
factor_df = build_factor_df(factors)
uncertainty_level, uncertainty_card = uncertainty_label(uncertainty)
impact_level, impact_card = impact_label(decision, scenario)
country_settings = COUNTRY_CONFIG[country]
domain_settings = DOMAIN_CONFIG[scenario]

if not st.session_state.decision_logged:
    add_audit_event("Decision page viewed", actor=domain_settings["affected_person"])
    st.session_state.decision_logged = True


# ============================================================
# Top summary cards
# ============================================================
top1, top2, top3, top4 = st.columns(4)
with top1:
    card("Case ID", st.session_state.case_id, f"Created {st.session_state.created_at}", "neutral-card")
with top2:
    card("Automated recommendation", decision, "This is not final until the workflow allows review where needed.", decision_status)
with top3:
    card("Uncertainty", f"{uncertainty_level} ({uncertainty:.1f}%)", "Higher uncertainty should trigger more care.", uncertainty_card)
with top4:
    card("Impact", impact_level, f"Scenario: {scenario}", impact_card)


# ============================================================
# Main tabs
# ============================================================
tab_user, tab_reviewer, tab_audit, tab_research = st.tabs(
    [
        "Affected-person portal",
        "Company review dashboard",
        "Audit and exports",
        "Research framing",
    ]
)


# ============================================================
# Affected-person portal
# ============================================================
with tab_user:
    st.subheader("1. Decision notice")

    notice_col1, notice_col2 = st.columns([1.2, 1])

    with notice_col1:
        st.markdown(
            f"""
            <div class="card {decision_status}">
                <b>Scenario:</b> {scenario}<br>
                <b>Affected person:</b> {domain_settings["affected_person"]}<br>
                <b>Automated recommendation:</b> {decision}<br>
                <b>Score:</b> {score:.1f}/100<br>
                <span class="small-text">This is a simulated model output for an interface prototype.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(int(score))

    with notice_col2:
        st.markdown(
            f"""
            <div class="card info-card">
                <b>Country template:</b> {country}<br>
                <b>Review timeline:</b> {country_settings["review_timeline"]}<br>
                <b>Interface tone:</b> {country_settings["tone"]}<br>
                <span class="small-text">{country_settings["rights_notice"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("2. Why human review may be needed")

    if review_triggers:
        for trigger in review_triggers:
            st.warning(trigger)
    else:
        st.success("No automatic human-review trigger was detected, but the person can still request review.")

    st.info(f"Recommended safer workflow: {recommended_workflow}")

    with st.expander("Sensitive-context note"):
        st.write(domain_settings["sensitive_warning"])

    st.subheader("3. Plain-language explanation")

    desktop_view, mobile_view = st.tabs(["Table view", "Card view"])

    with desktop_view:
        st.dataframe(
            factor_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Influence": st.column_config.NumberColumn(format="%.2f"),
            },
        )

    with mobile_view:
        for _, row in factor_df.iterrows():
            style = "good-card" if row["Influence"] > 0 else "bad-card" if row["Influence"] < -10 else "neutral-card"
            st.markdown(
                f"""
                <div class="card {style}">
                    <b>{row["Factor"]}</b><br>
                    Influence: {row["Influence"]:.2f}<br>
                    <span class="small-text">{row["Plain-language meaning"]}</span><br><br>
                    <b>Possible action:</b><br>
                    <span class="small-text">{row["What the person can do"]}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    important_factors = factor_df[abs(factor_df["Influence"]) >= 10]
    st.write("**Key explanation:**")
    if important_factors.empty:
        st.write("- No single factor strongly dominated the decision.")
    else:
        for _, row in important_factors.iterrows():
            st.write(f"- **{row['Factor']}**: {row['Plain-language meaning']}")

    st.subheader("4. Contest the decision")

    st.caption(
        "The form is structured so the affected person challenges specific issues instead of sending a vague complaint or oversharing data."
    )

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
                "I want an explanation only",
            ],
            default=["Important document is missing"] if missing_docs >= 2 else [],
        )

        explanation = st.text_area(
            "Explain your challenge",
            placeholder="Example: My current income is higher than shown, and one employment document was missing.",
            height=120,
        )

        correction_col1, correction_col2 = st.columns(2)
        with correction_col1:
            corrected_income = st.number_input(
                "Optional corrected income/capacity value",
                min_value=0,
                value=0,
                step=100,
                help="Leave as 0 if you are not correcting this field.",
            )
        with correction_col2:
            corrected_docs = st.number_input(
                "Optional number of documents you can now provide",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
            )

        uploaded_file = st.file_uploader(
            "Upload optional evidence",
            type=["pdf", "png", "jpg", "jpeg", "docx"],
            help="For this demo, only the file name is shown. A production version should use encrypted storage.",
        )

        st.write("Suggested evidence for this scenario:")
        for item in domain_settings["evidence_examples"]:
            st.write(f"- {item}")

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
            f"I consent to share only the selected information for this specific review purpose. {country_settings['consent_notice']}"
        )

        no_extra_data = st.checkbox(
            "I understand that I should not upload unrelated sensitive information unless it is necessary for this review."
        )

        submitted = st.form_submit_button("Submit contestation request")

    if submitted:
        if not reasons:
            st.error("Please select at least one reason for contesting the decision.")
        elif not consent:
            st.error("Please give purpose-limited consent before submitting.")
        elif not no_extra_data:
            st.error("Please confirm that unrelated extra data should not be uploaded.")
        else:
            receipt_id = f"RCPT-{uuid4().hex[:8].upper()}"
            st.session_state.contestation_submitted = True
            st.session_state.review_status = "Contestation submitted and waiting for company review"
            st.session_state.contestation_receipt = receipt_id
            st.session_state.appeal_payload = {
                "receipt_id": receipt_id,
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reasons": reasons,
                "explanation": explanation,
                "uploaded_file_name": uploaded_file.name if uploaded_file is not None else None,
                "review_path": review_path,
                "corrected_income": corrected_income if corrected_income > 0 else None,
                "corrected_docs": corrected_docs if corrected_docs > 0 else None,
            }
            add_audit_event("Contestation request submitted", actor=domain_settings["affected_person"])
            add_audit_event(f"Review path selected: {review_path}", actor=domain_settings["affected_person"])
            st.success("Contestation request submitted successfully.")

    if st.session_state.contestation_submitted and st.session_state.appeal_payload:
        payload = st.session_state.appeal_payload
        st.markdown("### Contestation receipt")
        st.markdown(
            f"""
            <div class="receipt">
                <b>Receipt ID:</b> {payload["receipt_id"]}<br>
                <b>Submitted at:</b> {payload["submitted_at"]}<br>
                <b>Original automated recommendation:</b> {decision}<br>
                <b>Review path:</b> {payload["review_path"]}<br>
                <b>Status:</b> {st.session_state.review_status}<br>
                <b>Expected timeline:</b> {country_settings["review_timeline"]}<br>
                <span class="small-text">{country_settings["retention_notice"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("**Selected challenge reasons:**")
        for reason in payload["reasons"]:
            st.write(f"- {reason}")

        if payload["explanation"]:
            st.write("**User explanation:**")
            st.write(payload["explanation"])

        if payload["uploaded_file_name"]:
            st.write(f"**Uploaded evidence:** {payload['uploaded_file_name']}")


# ============================================================
# Company reviewer dashboard
# ============================================================
with tab_reviewer:
    st.subheader("Company review dashboard")

    st.markdown(
        f"""
        <div class="card purple-card">
            <b>Internal team:</b> {domain_settings["company_team"]}<br>
            <b>Current status:</b> {st.session_state.review_status}<br>
            <b>Final outcome:</b> {st.session_state.final_outcome}<br>
            <span class="small-text">This dashboard is what the subscribing organization would use. The affected person should not see internal notes unless the company chooses to share them.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    reviewer_col1, reviewer_col2 = st.columns(2)

    with reviewer_col1:
        st.write("**Case summary**")
        st.write(f"- Country template: {country}")
        st.write(f"- Scenario: {scenario}")
        st.write(f"- Automated recommendation: {decision}")
        st.write(f"- Score: {score:.1f}/100")
        st.write(f"- Uncertainty: {uncertainty:.1f}%")
        st.write(f"- Recommended safer workflow: {recommended_workflow}")

    with reviewer_col2:
        st.write("**Review triggers**")
        if review_triggers:
            for trigger in review_triggers:
                st.write(f"- {trigger}")
        else:
            st.write("- No automatic trigger, but voluntary review remains available.")

    if st.session_state.appeal_payload:
        st.write("### Submitted appeal")
        payload = st.session_state.appeal_payload
        st.write(f"**Receipt:** {payload['receipt_id']}")
        st.write(f"**Review path:** {payload['review_path']}")
        st.write(f"**Reasons:** {', '.join(payload['reasons'])}")
        st.write(f"**Explanation:** {payload['explanation'] or 'No explanation provided.'}")
        st.write(f"**File:** {payload['uploaded_file_name'] or 'No file uploaded.'}")
        if payload["corrected_income"]:
            st.write(f"**Corrected income/capacity:** {payload['corrected_income']}")
        if payload["corrected_docs"]:
            st.write(f"**Additional documents available:** {payload['corrected_docs']}")
    else:
        st.info("No contestation has been submitted yet.")

    st.subheader("Reviewer action")

    with st.form("reviewer_form"):
        reviewer_name = st.text_input("Reviewer name or ID", value="Reviewer-1")
        priority = st.selectbox(
            "Queue priority",
            ["Normal", "High - near boundary", "High - sensitive context", "High - missing documents"],
            index=2 if sensitive_context else 0,
        )
        reviewer_outcome = st.selectbox(
            "Reviewer outcome",
            [
                "Pending",
                "Request more documents",
                "Correct data and rerun",
                "Escalate to senior reviewer",
                "Uphold automated recommendation",
                "Reverse automated recommendation",
                "Partially revise decision",
            ],
        )
        reviewer_note = st.text_area(
            "Internal reviewer note",
            placeholder="Example: Applicant provided updated income document. Recommend data correction and rerun.",
            height=110,
        )
        share_summary = st.text_area(
            "Plain-language summary to share with affected person",
            placeholder="Example: We are reviewing the updated document and will notify you after human assessment.",
            height=100,
        )
        save_review = st.form_submit_button("Save reviewer update")

    if save_review:
        update = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Reviewer": reviewer_name,
            "Priority": priority,
            "Outcome": reviewer_outcome,
            "Note": reviewer_note or "No internal note.",
            "Shared summary": share_summary or "No shared summary.",
        }
        st.session_state.reviewer_updates.append(update)
        st.session_state.review_status = reviewer_outcome
        st.session_state.final_outcome = reviewer_outcome
        add_audit_event(f"Reviewer update saved: {reviewer_outcome}", actor=reviewer_name)
        st.success("Reviewer update saved.")

    if st.session_state.reviewer_updates:
        st.write("### Reviewer update history")
        st.dataframe(pd.DataFrame(st.session_state.reviewer_updates), use_container_width=True, hide_index=True)


# ============================================================
# Audit and exports
# ============================================================
with tab_audit:
    st.subheader("Audit trail")

    if st.session_state.audit_log:
        st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True, hide_index=True)
    else:
        st.info("No audit events yet.")

    report_text = make_case_report(
        scenario=scenario,
        country=country,
        score=score,
        decision=decision,
        uncertainty=uncertainty,
        recommended_workflow=recommended_workflow,
        factor_df=factor_df,
    )

    export_col1, export_col2 = st.columns(2)

    with export_col1:
        st.download_button(
            "Download audit log as CSV",
            data=make_audit_csv(),
            file_name=f"{st.session_state.case_id}_audit_log.csv",
            mime="text/csv",
        )

    with export_col2:
        st.download_button(
            "Download case report as TXT/Markdown",
            data=report_text,
            file_name=f"{st.session_state.case_id}_case_report.md",
            mime="text/markdown",
        )

    st.subheader("Data minimization checklist")
    st.checkbox("Only necessary evidence is requested.", value=True, disabled=True)
    st.checkbox("Purpose-limited consent is recorded.", value=bool(st.session_state.appeal_payload), disabled=True)
    st.checkbox("Human-review route is available.", value=True, disabled=True)
    st.checkbox("Audit log is generated.", value=bool(st.session_state.audit_log), disabled=True)
    st.checkbox("Country-specific notice is shown.", value=True, disabled=True)


# ============================================================
# Research framing
# ============================================================
with tab_research:
    st.subheader("Why this interface is different")

    compare_col1, compare_col2 = st.columns(2)

    with compare_col1:
        st.markdown(
            """
            <div class="card bad-card">
            <b>Traditional AI notice</b><br><br>
            • Shows a decision only<br>
            • Gives vague explanation<br>
            • Provides generic appeal button<br>
            • User may not know what to challenge<br>
            • User may overshare unnecessary data<br>
            • No clear audit trail for the affected person
            </div>
            """,
            unsafe_allow_html=True,
        )

    with compare_col2:
        st.markdown(
            """
            <div class="card good-card">
            <b>Contestable AI interface</b><br><br>
            • Shows recommendation and uncertainty<br>
            • Explains important factors in plain language<br>
            • Guides specific challenges and corrections<br>
            • Supports human review and evidence upload<br>
            • Uses purpose-limited consent<br>
            • Produces audit and review records
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Research contribution")
    st.write(
        """
        This MVP demonstrates actionable contestability. The affected person does not only receive an automated result.
        They receive an explanation, uncertainty information, review triggers, a safer workflow recommendation,
        a structured challenge form, and a path to human review. The core idea is to make the safe and fair path easier than a vague appeal process.
        """
    )

    st.subheader("Suggested user study")
    study_df = pd.DataFrame(
        [
            {
                "Measure": "Decision understanding",
                "Question": "Can users explain why the decision happened?",
                "Possible metric": "Comprehension score",
            },
            {
                "Measure": "Error identification",
                "Question": "Can users identify what data may be wrong or missing?",
                "Possible metric": "Correct issue selection rate",
            },
            {
                "Measure": "Review-path choice",
                "Question": "Can users choose an appropriate contestation path?",
                "Possible metric": "Path-choice accuracy",
            },
            {
                "Measure": "Data minimization",
                "Question": "Do users avoid uploading unnecessary sensitive data?",
                "Possible metric": "Oversharing rate",
            },
            {
                "Measure": "Procedural fairness",
                "Question": "Do users feel the process is more fair and reviewable?",
                "Possible metric": "Likert-scale fairness score",
            },
        ]
    )
    st.dataframe(study_df, use_container_width=True, hide_index=True)

    st.subheader("Next product improvements after this Streamlit MVP")
    st.write(
        """
        1. Replace session state with a real database such as PostgreSQL.
        2. Add company accounts, reviewer roles, and affected-person secure links.
        3. Store evidence in encrypted object storage.
        4. Add API endpoints so companies can send decisions automatically.
        5. Add PDF audit reports and email notifications.
        6. Add country templates through an admin configuration panel.
        7. Add multilingual interface files instead of hardcoded strings.
        """
    )


# ============================================================
# Footer
# ============================================================
st.markdown(
    """
    <div class="footer-note">
    Prototype disclaimer: This app simulates decision logic for research and product-design purposes. 
    It is not a real credit, hiring, insurance, admission, moderation, or legal compliance system.
    </div>
    """,
    unsafe_allow_html=True,
)
