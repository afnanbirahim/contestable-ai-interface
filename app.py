# contestabilitylayer_native_streamlit_final.py
# ContestabilityLayer: Native Streamlit MVP
# Mobile-safe version: no custom HTML, no unsafe_allow_html, no CSS, no tabs, no expanders.
# Run locally with: streamlit run contestabilitylayer_native_streamlit_final.py

from __future__ import annotations

from datetime import datetime
import json
import uuid

import pandas as pd
import streamlit as st


# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="ContestabilityLayer MVP",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ------------------------------------------------------------
# Static content and templates
# ------------------------------------------------------------
COUNTRY_TEMPLATES = {
    "Bangladesh": {
        "notice": "Plain-language review wording suitable for a Bangladesh pilot. The affected person may request human review, correct data, and submit relevant evidence for this case only.",
        "consent": "I consent to share only the selected information for this specific human review purpose.",
        "retention": "Suggested pilot retention: 90 to 180 days unless the company needs a longer legally justified retention period.",
        "review_sla": "Suggested review target: 3 to 7 working days.",
    },
    "EU / UK": {
        "notice": "GDPR-style wording emphasizing meaningful information, human intervention, contestation, and review of significant automated decisions.",
        "consent": "I consent to submit this evidence for the limited purpose of reviewing this automated decision notice.",
        "retention": "Retention should follow purpose limitation, data minimization, and documented lawful-basis requirements.",
        "review_sla": "Suggested review target: 7 to 14 days, depending on sector policy.",
    },
    "United States": {
        "notice": "Adverse-action-style wording suitable for lending, hiring, insurance, or platform decisions, adapted to the company and sector.",
        "consent": "I consent to submit this information for review of this decision only.",
        "retention": "Retention should follow sector, state, and company policy requirements.",
        "review_sla": "Suggested review target: 5 to 10 working days.",
    },
    "India": {
        "notice": "Plain-language review wording for digital lending, HR screening, insurance, education, or platform decisions, configurable by sector.",
        "consent": "I consent to share the selected information only for this review request.",
        "retention": "Retention should follow company policy and applicable digital personal-data requirements.",
        "review_sla": "Suggested review target: 3 to 10 working days.",
    },
    "Generic global": {
        "notice": "General contestability notice for automated or AI-assisted decisions. The person can see the reason, submit evidence, and request human review.",
        "consent": "I consent to use the submitted information only for this specific review.",
        "retention": "Retention should be configured by country, sector, and company policy.",
        "review_sla": "Suggested review target: configured by company policy.",
    },
}

SCENARIO_EVIDENCE = {
    "Loan application": "income statement, updated employment proof, debt correction, missing KYC document",
    "Hiring shortlist": "updated CV, work sample, certificate, corrected experience record, accommodation/context note",
    "Insurance claim": "medical or repair document, claim photos, invoice, missing policy information, clarification letter",
    "University admission": "transcript, corrected grade record, recommendation, portfolio, special-circumstance note",
    "Platform account restriction": "identity clarification, transaction evidence, explanation of activity, corrected account information",
    "NGO beneficiary selection": "household information, vulnerability evidence, location correction, income clarification, supporting document",
}

SCENARIO_FIELDS = {
    "Loan application": ["income", "debt_ratio", "employment_years", "missing_documents", "relevant_history"],
    "Hiring shortlist": ["capacity_indicator", "burden_or_gap_ratio", "experience_years", "missing_documents", "relevant_history"],
    "Insurance claim": ["claim_support_indicator", "risk_or_burden_ratio", "policy_years", "missing_documents", "relevant_history"],
    "University admission": ["academic_capacity_indicator", "constraint_ratio", "preparation_years", "missing_documents", "relevant_history"],
    "Platform account restriction": ["positive_activity_indicator", "risk_signal_ratio", "account_age_years", "missing_documents", "relevant_history"],
    "NGO beneficiary selection": ["need_capacity_indicator", "vulnerability_ratio", "community_history_years", "missing_documents", "relevant_history"],
}

PRICING_ROWS = [
    {"Plan": "Pilot", "Best for": "first local pilots", "Monthly price": "$49 to $99", "Includes": "1 workspace, 2 reviewers, 100 cases"},
    {"Plan": "Growth", "Best for": "fintech/HR/insurance startups", "Monthly price": "$199 to $499", "Includes": "5 to 15 reviewers, 1,000 cases, exports"},
    {"Plan": "Business", "Best for": "NBFI, larger HR, platform teams", "Monthly price": "$799 to $2,500", "Includes": "API, branding, analytics, audit exports"},
    {"Plan": "Enterprise", "Best for": "banks, insurers, public-sector vendors", "Monthly price": "Custom", "Includes": "SSO, data residency, SLA, integrations"},
]


# ------------------------------------------------------------
# State
# ------------------------------------------------------------
if "case_id" not in st.session_state:
    st.session_state.case_id = "CASE-" + uuid.uuid4().hex[:8].upper()

if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

if "appeal_submitted" not in st.session_state:
    st.session_state.appeal_submitted = False

if "review_status" not in st.session_state:
    st.session_state.review_status = "Not started"

if "review_outcome" not in st.session_state:
    st.session_state.review_outcome = "Pending"


def log_event(event: str) -> None:
    st.session_state.audit_log.append(
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": event,
        }
    )


if not st.session_state.audit_log:
    log_event("Case opened")


# ------------------------------------------------------------
# Decision logic
# ------------------------------------------------------------
def compute_decision(
    income: int,
    debt_ratio: float,
    employment_years: int,
    missing_docs: int,
    relevant_history: int,
    sensitive_context: bool,
) -> dict:
    """Transparent demonstration model for the prototype only."""
    score = 50.0
    score += min(income / 2000, 20)
    score -= debt_ratio * 35
    score += min(employment_years * 3, 15)
    score += relevant_history * 1.5
    score -= missing_docs * 8
    score = max(0.0, min(100.0, score))

    if score >= 70:
        recommendation = "Approve automatically"
        recommendation_note = "Low-risk automated approval recommendation."
    elif score >= 55:
        recommendation = "Send to conditional review"
        recommendation_note = "The case should be checked before a final decision."
    else:
        recommendation = "Do not approve automatically"
        recommendation_note = "The automated system does not recommend automatic approval. This is not a final human decision."

    uncertainty = max(15.0, min(85.0, 100 - abs(score - 55) * 1.5))

    factors = [
        {"factor": "Capacity / income information", "influence": round(min(income / 2000, 20), 1)},
        {"factor": "Debt or burden ratio", "influence": round(-debt_ratio * 35, 1)},
        {"factor": "Stable work / activity history", "influence": round(min(employment_years * 3, 15), 1)},
        {"factor": "Relevant history", "influence": round(relevant_history * 1.5, 1)},
        {"factor": "Missing or unclear documents", "influence": round(-missing_docs * 8, 1)},
    ]

    triggers: list[str] = []
    if uncertainty >= 60:
        triggers.append("The uncertainty is high enough that automatic processing may be unsafe.")
    if missing_docs >= 1:
        triggers.append("Important documents may be missing or unclear, so the decision may be incomplete.")
    if sensitive_context:
        triggers.append("The case includes sensitive context and should be checked by a human reviewer.")
    if recommendation == "Do not approve automatically" and score >= 45:
        triggers.append("The case is near the rejection boundary, so a correction could change the outcome.")

    if missing_docs >= 1:
        safer = "Request missing or clearer documents before any final decision."
    elif uncertainty >= 60:
        safer = "Send the case to fast human review instead of relying only on automation."
    elif recommendation == "Send to conditional review":
        safer = "Use conditional review with limited additional evidence."
    elif recommendation == "Approve automatically":
        safer = "Proceed with approval, but keep an audit trail and review option."
    else:
        safer = "Allow structured appeal and data correction before any final rejection."

    if uncertainty >= 60 or sensitive_context or missing_docs >= 2:
        risk = "High"
    elif triggers:
        risk = "Elevated"
    else:
        risk = "Low"

    return {
        "score": round(score, 1),
        "recommendation": recommendation,
        "recommendation_note": recommendation_note,
        "uncertainty": round(uncertainty, 1),
        "risk": risk,
        "factors": factors,
        "triggers": triggers,
        "safer_workflow": safer,
    }


def factor_meaning(factor: str, influence: float) -> str:
    if "income" in factor.lower() or "capacity" in factor.lower():
        if influence >= 15:
            return "This information strongly supported the case."
        if influence >= 8:
            return "This information moderately supported the case."
        return "This information gave limited support."

    if "debt" in factor.lower() or "burden" in factor.lower():
        if influence <= -25:
            return "This strongly reduced the recommendation score."
        if influence <= -10:
            return "This moderately reduced the recommendation score."
        return "This had a limited negative effect."

    if "work" in factor.lower() or "activity" in factor.lower():
        if influence >= 12:
            return "Stable work or activity history improved confidence."
        if influence >= 6:
            return "Stable work or activity history gave moderate support."
        return "Stable work or activity history gave limited support."

    if "relevant" in factor.lower():
        if influence >= 12:
            return "Relevant history strongly supported the case."
        if influence >= 6:
            return "Relevant history moderately supported the case."
        return "Relevant history gave limited support."

    if "missing" in factor.lower() or "unclear" in factor.lower():
        if influence <= -16:
            return "Missing or unclear documents strongly reduced confidence."
        if influence < 0:
            return "Missing or unclear documents reduced confidence."
        return "No document issue reduced the score."

    return "This factor influenced the recommendation."


def make_case_report(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.title("🛡️ ContestabilityLayer MVP")
st.caption("A mobile-safe prototype for explainable, contestable, human-reviewable automated decisions.")

st.info(
    "This version intentionally uses only native Streamlit components. It contains no custom HTML, no CSS, "
    "no unsafe rendering, no tabs, no expanders, and no dropdowns. This avoids the black raw-HTML blocks on mobile."
)


# ------------------------------------------------------------
# Navigation and configuration
# ------------------------------------------------------------
view = st.radio(
    "Choose view",
    [
        "Affected-person notice",
        "Contest or appeal",
        "Company reviewer dashboard",
        "Audit and exports",
        "SaaS business model",
        "API and product roadmap",
    ],
    horizontal=False,
)

st.divider()
st.subheader("Configure demo case")

country = st.radio(
    "Country / legal template",
    list(COUNTRY_TEMPLATES.keys()),
    index=0,
    horizontal=False,
)

scenario = st.radio(
    "Decision scenario",
    list(SCENARIO_EVIDENCE.keys()),
    index=0,
    horizontal=False,
)

income = st.slider("Capacity / income indicator", 500, 10000, 2600, step=100)
debt_ratio = st.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
employment_years = st.slider("Years of stable work/activity", 0, 15, 2)
missing_docs = st.slider("Missing or unclear documents", 0, 5, 2)
relevant_history = st.slider("Relevant history score", 0, 10, 5)
sensitive_context = st.checkbox("Sensitive context may require human review", value=True)

result = compute_decision(
    income=income,
    debt_ratio=debt_ratio,
    employment_years=employment_years,
    missing_docs=missing_docs,
    relevant_history=relevant_history,
    sensitive_context=sensitive_context,
)

template = COUNTRY_TEMPLATES[country]

case_data = {
    "case_id": st.session_state.case_id,
    "country_template": country,
    "scenario": scenario,
    "recommendation": result["recommendation"],
    "score": result["score"],
    "uncertainty": result["uncertainty"],
    "review_risk": result["risk"],
    "safer_workflow": result["safer_workflow"],
    "review_triggers": result["triggers"],
    "factors": result["factors"],
    "review_status": st.session_state.review_status,
    "review_outcome": st.session_state.review_outcome,
}

st.divider()


# ------------------------------------------------------------
# Affected-person notice
# ------------------------------------------------------------
if view == "Affected-person notice":
    st.subheader("Your decision notice")

    with st.container(border=True):
        st.caption(f"Case ID: {st.session_state.case_id}")
        st.write(f"**Scenario:** {scenario}")
        st.write(f"**Country template:** {country}")
        st.write(f"**Automated recommendation:** {result['recommendation']}")
        st.write(result["recommendation_note"])
        st.write("This is an automated recommendation, not a final human decision.")

    st.metric("Recommendation score", f"{result['score']}/100")
    st.progress(int(result["score"]))

    st.metric("Estimated uncertainty", f"{result['uncertainty']}%")
    st.progress(int(result["uncertainty"]))

    st.metric("Review risk", result["risk"])

    with st.container(border=True):
        st.subheader("What this means")
        st.write(template["notice"])
        st.write(f"**Suggested review timeline:** {template['review_sla']}")

    with st.container(border=True):
        st.subheader("Recommended safer workflow")
        st.write(result["safer_workflow"])

    st.subheader("Why human review may be needed")
    if result["triggers"]:
        for item in result["triggers"]:
            st.warning(item)
    else:
        st.success("No automatic human-review trigger was detected, but the affected person may still request review.")

    st.subheader("Plain-language explanation")
    factor_rows = []
    for factor in sorted(result["factors"], key=lambda x: x["influence"]):
        factor_rows.append(
            {
                "Factor": factor["factor"],
                "Influence": factor["influence"],
                "Meaning": factor_meaning(factor["factor"], factor["influence"]),
            }
        )

    for row in factor_rows:
        with st.container(border=True):
            st.write(f"**{row['Factor']}**")
            st.write(f"Influence: {row['Influence']}")
            st.write(row["Meaning"])

    with st.container(border=True):
        st.subheader("Evidence that may help")
        st.write(f"For this {scenario.lower()} case, useful evidence may include: {SCENARIO_EVIDENCE[scenario]}.")
        st.caption("Data minimization: submit only evidence related to this review request.")


# ------------------------------------------------------------
# Contestation form
# ------------------------------------------------------------
elif view == "Contest or appeal":
    st.subheader("Contest the decision")
    st.write("The affected person can challenge specific issues instead of submitting a vague appeal.")

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
        height=140,
    )

    uploaded_file = st.file_uploader(
        "Upload optional evidence",
        type=["pdf", "png", "jpg", "jpeg", "docx"],
    )

    review_path = st.radio(
        "Choose review path",
        [
            "Fast human review",
            "Correct data and rerun recommendation",
            "Full appeal review",
            "Request explanation only",
        ],
        horizontal=False,
    )

    consent = st.checkbox(template["consent"])

    if st.button("Submit contestation request", type="primary"):
        if not reasons:
            st.error("Please select at least one reason for contesting the decision.")
        elif not consent:
            st.error("Please give purpose-limited consent before submitting.")
        else:
            st.session_state.appeal_submitted = True
            st.session_state.review_status = "Submitted"
            log_event("Contestation request submitted")
            st.success("Contestation request submitted successfully.")

    if st.session_state.appeal_submitted:
        with st.container(border=True):
            st.subheader("Contestation receipt")
            st.write(f"**Original automated recommendation:** {result['recommendation']}")
            st.write(f"**Review path:** {review_path}")
            st.write("**Purpose limitation:** Submitted information may be used only to evaluate this contestation request.")
            st.write("**Selected reasons:**")
            if reasons:
                for reason in reasons:
                    st.write(f"- {reason}")
            if explanation:
                st.write("**User explanation:**")
                st.write(explanation)
            if uploaded_file is not None:
                st.write(f"**Uploaded evidence:** {uploaded_file.name}")


# ------------------------------------------------------------
# Company reviewer dashboard
# ------------------------------------------------------------
elif view == "Company reviewer dashboard":
    st.subheader("Company reviewer dashboard")
    st.write("This is the paid B2B side of the product. Companies subscribe; affected people use the portal for free.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Open case", st.session_state.case_id)
        st.metric("Review risk", result["risk"])
    with col2:
        st.metric("Uncertainty", f"{result['uncertainty']}%")
        st.metric("Current status", st.session_state.review_status)

    with st.container(border=True):
        st.subheader("Case triage")
        st.write(f"**Scenario:** {scenario}")
        st.write(f"**Country template:** {country}")
        st.write(f"**Automated recommendation:** {result['recommendation']}")
        st.write(f"**Safer workflow:** {result['safer_workflow']}")
        st.write(f"**Review SLA:** {template['review_sla']}")
        st.write(f"**Retention guidance:** {template['retention']}")

    st.subheader("Reviewer action")
    reviewer_status = st.radio(
        "Reviewer status",
        ["Not started", "Submitted", "Under review", "Waiting for documents", "Escalated", "Closed"],
        index=["Not started", "Submitted", "Under review", "Waiting for documents", "Escalated", "Closed"].index(st.session_state.review_status)
        if st.session_state.review_status in ["Not started", "Submitted", "Under review", "Waiting for documents", "Escalated", "Closed"]
        else 0,
        horizontal=False,
    )

    review_outcome = st.radio(
        "Review outcome",
        [
            "Pending",
            "Original recommendation confirmed",
            "Data corrected and rerun required",
            "Recommendation overturned",
            "More evidence required",
            "Escalated to senior reviewer",
        ],
        index=[
            "Pending",
            "Original recommendation confirmed",
            "Data corrected and rerun required",
            "Recommendation overturned",
            "More evidence required",
            "Escalated to senior reviewer",
        ].index(st.session_state.review_outcome)
        if st.session_state.review_outcome in [
            "Pending",
            "Original recommendation confirmed",
            "Data corrected and rerun required",
            "Recommendation overturned",
            "More evidence required",
            "Escalated to senior reviewer",
        ]
        else 0,
        horizontal=False,
    )

    reviewer_note = st.text_area(
        "Reviewer note",
        placeholder="Example: Request updated income document and rerun recommendation before final decision.",
        height=140,
    )

    if st.button("Save reviewer update", type="primary"):
        st.session_state.review_status = reviewer_status
        st.session_state.review_outcome = review_outcome
        log_event(f"Reviewer update saved: {reviewer_status}; {review_outcome}")
        st.success("Reviewer update saved.")

    st.subheader("Company value")
    st.write("The company uses this dashboard to reduce support chaos, standardize appeals, prove human oversight, and export audit evidence.")


# ------------------------------------------------------------
# Audit and exports
# ------------------------------------------------------------
elif view == "Audit and exports":
    st.subheader("Audit trail")
    audit_df = pd.DataFrame(st.session_state.audit_log)
    st.dataframe(audit_df, use_container_width=True, hide_index=True)

    report = make_case_report(case_data)

    st.download_button(
        "Download case report JSON",
        data=report,
        file_name=f"{st.session_state.case_id}_case_report.json",
        mime="application/json",
    )

    st.download_button(
        "Download audit log CSV",
        data=audit_df.to_csv(index=False),
        file_name=f"{st.session_state.case_id}_audit_log.csv",
        mime="text/csv",
    )

    if st.button("Reset demo case"):
        st.session_state.case_id = "CASE-" + uuid.uuid4().hex[:8].upper()
        st.session_state.audit_log = []
        st.session_state.appeal_submitted = False
        st.session_state.review_status = "Not started"
        st.session_state.review_outcome = "Pending"
        log_event("New case opened")
        st.rerun()

    st.subheader("Case report preview")
    report_rows = pd.DataFrame(
        [
            {"Field": "Case ID", "Value": st.session_state.case_id},
            {"Field": "Country", "Value": country},
            {"Field": "Scenario", "Value": scenario},
            {"Field": "Recommendation", "Value": result["recommendation"]},
            {"Field": "Score", "Value": result["score"]},
            {"Field": "Uncertainty", "Value": result["uncertainty"]},
            {"Field": "Review risk", "Value": result["risk"]},
            {"Field": "Safer workflow", "Value": result["safer_workflow"]},
        ]
    )
    st.dataframe(report_rows, use_container_width=True, hide_index=True)


# ------------------------------------------------------------
# SaaS business model
# ------------------------------------------------------------
elif view == "SaaS business model":
    st.subheader("SaaS business model")
    st.write("Best positioning: companies pay for a contestability and human-review layer; affected people use the portal for free.")

    st.dataframe(pd.DataFrame(PRICING_ROWS), use_container_width=True, hide_index=True)

    st.subheader("ROI calculator for a client")
    monthly_cases = st.slider("Monthly automated decision cases", 100, 100000, 5000, step=100)
    appeal_rate = st.slider("Expected review/appeal rate", 0.01, 0.50, 0.08, step=0.01)
    minutes_saved = st.slider("Support minutes saved per appeal", 1, 60, 12)
    staff_hourly_cost = st.slider("Support/reviewer hourly cost in USD", 2, 100, 12)

    monthly_appeals = monthly_cases * appeal_rate
    hours_saved = monthly_appeals * minutes_saved / 60
    support_savings = hours_saved * staff_hourly_cost

    st.metric("Estimated monthly review cases", f"{monthly_appeals:,.0f}")
    st.metric("Estimated support hours saved", f"{hours_saved:,.1f}")
    st.metric("Estimated monthly operational value", f"${support_savings:,.0f}")

    st.write(
        "This does not include reputational benefit, regulatory preparedness, reduced complaint escalation, or better audit readiness."
    )

    st.subheader("Best first paying niches")
    for niche in [
        "Fintech and digital lending",
        "HR-tech screening platforms",
        "Insurance claim review",
        "University or scholarship selection systems",
        "Platform account restriction workflows",
        "NGO beneficiary-selection projects",
    ]:
        st.write(f"- {niche}")


# ------------------------------------------------------------
# API and roadmap
# ------------------------------------------------------------
elif view == "API and product roadmap":
    st.subheader("API-first SaaS design")
    st.write("A real SaaS version should let companies create cases through API, CSV upload, or dashboard entry.")

    api_fields = pd.DataFrame(
        [
            {"Field": "company_id", "Purpose": "Identifies the company workspace"},
            {"Field": "country_template", "Purpose": "Selects local legal/review wording"},
            {"Field": "scenario", "Purpose": "Loan, HR, insurance, admission, platform, NGO"},
            {"Field": "person_reference", "Purpose": "Pseudonymous user or applicant reference"},
            {"Field": "decision_outcome", "Purpose": "Automated recommendation/outcome"},
            {"Field": "score", "Purpose": "Transparent score if the company chooses to show it"},
            {"Field": "uncertainty", "Purpose": "Triggers review escalation"},
            {"Field": "reasons", "Purpose": "Plain-language factor explanations"},
            {"Field": "review_policy", "Purpose": "Fast review, rerun, full appeal, explanation only"},
            {"Field": "retention_policy", "Purpose": "Country/company retention rule"},
        ]
    )
    st.dataframe(api_fields, use_container_width=True, hide_index=True)

    st.subheader("Roadmap from Streamlit to real SaaS")
    roadmap = pd.DataFrame(
        [
            {"Phase": "1. Pilot MVP", "Build": "Company dashboard, affected-person portal, appeal form, audit export", "Target": "1 to 3 pilot clients"},
            {"Phase": "2. SaaS core", "Build": "Auth, workspaces, reviewer roles, subscriptions, email notifications", "Target": "Recurring B2B revenue"},
            {"Phase": "3. API product", "Build": "API keys, webhooks, CSV upload, custom templates, branded portal", "Target": "Fintech/HR/insurance integrations"},
            {"Phase": "4. Enterprise", "Build": "SSO, data residency, advanced audit, SLA, security review", "Target": "Banks, insurers, public vendors"},
        ]
    )
    st.dataframe(roadmap, use_container_width=True, hide_index=True)

    st.subheader("Recommended real stack")
    for item in [
        "Next.js frontend for public portal and company dashboard",
        "FastAPI or Django backend for cases, review workflow, and API integrations",
        "PostgreSQL for companies, users, cases, appeals, templates, and subscriptions",
        "S3 or Supabase Storage for encrypted evidence files",
        "Auth0, Clerk, or Supabase Auth for secure company login",
        "Stripe for subscriptions and usage-based billing",
        "Sentry and PostHog for monitoring and product analytics",
    ]:
        st.write(f"- {item}")


st.divider()
st.caption("Prototype note: this is not a real credit, hiring, insurance, admission, moderation, or aid-selection model. It is a contestability workflow demonstration.")
