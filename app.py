# app.py
# ContestabilityLayer MVP
# Mobile-safe Streamlit prototype for contestable AI decisions.
# Run locally with: streamlit run app.py

from __future__ import annotations

from datetime import datetime, timedelta
import json
import uuid
from typing import Any, Dict, List, Tuple

import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Page configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ContestabilityLayer MVP",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# -----------------------------------------------------------------------------
# Country and domain templates
# These templates are deliberately data-driven so the future SaaS can replace
# them with database records instead of hardcoded text.
# -----------------------------------------------------------------------------
COUNTRY_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "Bangladesh": {
        "short_label": "BD",
        "notice_title": "Plain-language review notice",
        "affected_notice": (
            "This automated recommendation is not the final word. You may request "
            "human review, correct missing or inaccurate information, and submit "
            "evidence relevant to this case."
        ),
        "rights_summary": [
            "Right to receive a clear explanation in ordinary language.",
            "Right to request review by a responsible company officer or review team.",
            "Right to submit missing documents or correct inaccurate information.",
            "Right to know the expected review timeline and next step.",
        ],
        "consent_text": (
            "I consent to share the selected information only for this specific review request."
        ),
        "review_timeline": "3 to 7 working days",
        "retention_rule": "Keep appeal evidence only as long as needed for review and internal audit.",
        "escalation_route": "Company review desk or compliance/contact point.",
        "regulator_note": "Add sector-specific route later, for example central-bank, insurance, labour, or education channels.",
        "data_region_note": "Bangladesh-first deployment can use local or regional hosting depending on client need.",
        "required_disclosures": [
            "Reason for automated recommendation",
            "Important factors that affected the outcome",
            "Whether human review is available",
            "Expected response timeline",
            "How evidence will be used",
        ],
        "appeal_options": [
            "Correct inaccurate data",
            "Submit missing documents",
            "Request human review",
            "Ask for plain-language explanation",
            "Raise fairness or context concern",
        ],
    },
    "EU / UK": {
        "short_label": "EU/UK",
        "notice_title": "Automated decision and human-intervention notice",
        "affected_notice": (
            "This page explains an automated recommendation and gives you a structured way "
            "to request human intervention, contest the outcome, and provide additional information."
        ),
        "rights_summary": [
            "Right to meaningful information about the logic involved.",
            "Right to obtain human intervention where applicable.",
            "Right to express your point of view and contest the decision.",
            "Right to data minimisation and purpose-limited processing.",
        ],
        "consent_text": (
            "I agree that the selected information may be used only to assess this contestation or human-review request."
        ),
        "review_timeline": "Usually 5 to 15 working days, configurable by sector and policy.",
        "retention_rule": "Use purpose limitation, data minimisation, retention schedule, and deletion workflow.",
        "escalation_route": "Data protection officer, compliance team, or sector-specific complaints route.",
        "regulator_note": "Template should later map to GDPR, UK GDPR, AI Act, and sector rules.",
        "data_region_note": "Offer EU/UK data-residency option for production clients.",
        "required_disclosures": [
            "Meaningful information about logic involved",
            "Significance and likely consequences",
            "Human intervention route",
            "Contestation route",
            "Purpose and retention of submitted evidence",
        ],
        "appeal_options": [
            "Request human intervention",
            "Contest the automated recommendation",
            "Express my point of view",
            "Correct inaccurate personal data",
            "Request limited-purpose processing",
        ],
    },
    "United States": {
        "short_label": "US",
        "notice_title": "Decision notice and review request",
        "affected_notice": (
            "This page explains the main factors behind the automated recommendation and "
            "provides a route to request review, correction, or additional consideration."
        ),
        "rights_summary": [
            "Right to see key factors or reasons where sector rules require notice.",
            "Right to correct inaccurate information where supported by the company process.",
            "Right to submit additional information for review.",
            "Right to receive sector-specific disclosures where applicable.",
        ],
        "consent_text": (
            "I consent to use my submitted information only for this review and related audit record."
        ),
        "review_timeline": "Configurable by sector; start with 5 to 10 working days.",
        "retention_rule": "Follow sector and state retention rules; keep minimum necessary audit evidence.",
        "escalation_route": "Company support, compliance, fair-lending/fair-hiring, or sector complaints route.",
        "regulator_note": "Use sector-specific modules later, especially lending, employment, insurance, and platform moderation.",
        "data_region_note": "Production version can offer US-region hosting.",
        "required_disclosures": [
            "Key reasons or adverse factors",
            "Data correction channel",
            "Human review or reconsideration route",
            "Company contact point",
            "Sector-specific disclaimer",
        ],
        "appeal_options": [
            "Request reconsideration",
            "Correct incorrect data",
            "Submit additional documentation",
            "Ask for key reasons",
            "Raise fairness concern",
        ],
    },
    "India": {
        "short_label": "IN",
        "notice_title": "Digital decision review notice",
        "affected_notice": (
            "This page explains the automated recommendation and lets you request review, "
            "submit evidence, and limit the purpose for which your data is used."
        ),
        "rights_summary": [
            "Right to know what information is being used for this review.",
            "Right to submit correction or additional evidence.",
            "Right to request company-level review or grievance route.",
            "Right to purpose-limited use of review evidence.",
        ],
        "consent_text": (
            "I consent to use this information only for this review request and related recordkeeping."
        ),
        "review_timeline": "7 to 15 working days, configurable by company policy.",
        "retention_rule": "Use consent, purpose limitation, and a defined deletion/retention schedule.",
        "escalation_route": "Company grievance/review officer or sector-specific route.",
        "regulator_note": "Add sector modules later for lending, HR, insurance, education, and platforms.",
        "data_region_note": "Production version can offer India-region hosting.",
        "required_disclosures": [
            "Purpose of processing",
            "Main reason for recommendation",
            "Correction route",
            "Grievance/review route",
            "Retention and deletion note",
        ],
        "appeal_options": [
            "Request grievance review",
            "Correct personal data",
            "Submit missing evidence",
            "Ask for explanation",
            "Limit use to this review purpose",
        ],
    },
    "Global / Default": {
        "short_label": "Global",
        "notice_title": "General contestability notice",
        "affected_notice": (
            "This page explains an automated recommendation and provides a clear path to "
            "challenge, correct, or request human review."
        ),
        "rights_summary": [
            "Clear explanation of the recommendation.",
            "Structured route to submit corrections or evidence.",
            "Human review where the case is uncertain, sensitive, or high-impact.",
            "Purpose-limited use of submitted evidence.",
        ],
        "consent_text": (
            "I consent to use the selected information only for this review request."
        ),
        "review_timeline": "5 to 10 working days by default.",
        "retention_rule": "Minimum necessary retention with audit record and deletion option.",
        "escalation_route": "Company review desk or compliance route.",
        "regulator_note": "Add local legal references per country before production deployment.",
        "data_region_note": "Region-aware storage should be added for enterprise clients.",
        "required_disclosures": [
            "Main decision outcome",
            "Important reasons",
            "Review route",
            "Evidence use",
            "Expected timeline",
        ],
        "appeal_options": [
            "Correct data",
            "Submit evidence",
            "Request human review",
            "Ask for explanation",
            "Raise fairness concern",
        ],
    },
}

DOMAIN_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "Fintech / loan decision": {
        "industry": "Fintech, bank, NBFI, digital lending",
        "affected_person": "Applicant",
        "recommendation_label": "Loan recommendation",
        "case_goal": "Determine whether the applicant should be approved, rejected, or sent to review.",
        "factor_names": {
            "capacity": "Income or repayment capacity",
            "burden": "Debt or obligation burden",
            "stability": "Employment or activity stability",
            "history": "Credit or repayment history",
            "documents": "Document completeness",
        },
        "evidence_examples": [
            "Updated income statement or salary certificate",
            "Bank statement",
            "Employment or business proof",
            "Corrected credit information",
            "Explanation of temporary hardship",
        ],
        "review_paths": [
            "Fast human review",
            "Correct data and rerun scoring",
            "Full manual underwriting review",
            "Explanation only",
        ],
        "business_value": "Reduces complaint chaos, improves trust, and creates a repeatable review trail.",
        "pricing_anchor": "High willingness to pay if linked to compliance, customer trust, and loan-review efficiency.",
    },
    "HR / hiring shortlist": {
        "industry": "HR-tech, recruitment platform, employer ATS",
        "affected_person": "Candidate",
        "recommendation_label": "Shortlist recommendation",
        "case_goal": "Determine whether the candidate should be shortlisted, rejected, or reviewed by a recruiter.",
        "factor_names": {
            "capacity": "Role-fit evidence",
            "burden": "Skill or requirement gap",
            "stability": "Experience continuity",
            "history": "Relevant achievement history",
            "documents": "CV or document completeness",
        },
        "evidence_examples": [
            "Updated CV",
            "Portfolio link",
            "Certificate or transcript",
            "Work sample",
            "Explanation of career gap",
        ],
        "review_paths": [
            "Recruiter human review",
            "Correct profile data and rescreen",
            "Full appeal review",
            "Explanation only",
        ],
        "business_value": "Improves candidate trust, reduces opaque rejection complaints, and supports fair hiring documentation.",
        "pricing_anchor": "Useful for HR-tech firms and large employers using automated screening.",
    },
    "Insurance claim": {
        "industry": "Insurance, claims processing, health/vehicle/property claims",
        "affected_person": "Claimant",
        "recommendation_label": "Claim recommendation",
        "case_goal": "Determine whether the claim should be approved, denied, partially approved, or reviewed.",
        "factor_names": {
            "capacity": "Claim support strength",
            "burden": "Policy exclusion or risk conflict",
            "stability": "Policy and coverage continuity",
            "history": "Claim or policy history",
            "documents": "Evidence completeness",
        },
        "evidence_examples": [
            "Medical or repair report",
            "Invoice or receipt",
            "Policy document",
            "Photo evidence",
            "Explanation of disputed exclusion",
        ],
        "review_paths": [
            "Claims officer review",
            "Submit missing evidence",
            "Full appeal review",
            "Explanation only",
        ],
        "business_value": "Reduces disputes and creates explainable claim-denial records.",
        "pricing_anchor": "Good fit where claim volume and complaint risk are high.",
    },
    "University / scholarship": {
        "industry": "University, scholarship body, admission platform",
        "affected_person": "Applicant or student",
        "recommendation_label": "Admission or scholarship recommendation",
        "case_goal": "Determine whether the applicant should be accepted, waitlisted, rejected, or reviewed.",
        "factor_names": {
            "capacity": "Academic or eligibility strength",
            "burden": "Eligibility gap",
            "stability": "Academic continuity",
            "history": "Relevant achievement history",
            "documents": "Application completeness",
        },
        "evidence_examples": [
            "Transcript",
            "Recommendation letter",
            "Financial need document",
            "Updated test score",
            "Explanation of special circumstances",
        ],
        "review_paths": [
            "Admissions human review",
            "Correct application data",
            "Scholarship committee review",
            "Explanation only",
        ],
        "business_value": "Creates transparent and fair review for high-stakes education decisions.",
        "pricing_anchor": "Can be sold as a seasonal or annual admissions-review workflow.",
    },
    "Platform account moderation": {
        "industry": "Marketplace, gig platform, social platform, e-commerce",
        "affected_person": "User, seller, rider, creator, or customer",
        "recommendation_label": "Account action recommendation",
        "case_goal": "Determine whether restriction, warning, reinstatement, or human review is appropriate.",
        "factor_names": {
            "capacity": "Positive account evidence",
            "burden": "Policy-risk signals",
            "stability": "Account activity stability",
            "history": "Past account history",
            "documents": "Evidence completeness",
        },
        "evidence_examples": [
            "Identity or ownership proof",
            "Order or delivery evidence",
            "Screenshot or transaction proof",
            "Explanation of disputed incident",
            "Corrected account information",
        ],
        "review_paths": [
            "Trust and safety review",
            "Correct account data",
            "Full appeal review",
            "Explanation only",
        ],
        "business_value": "Reduces angry support tickets and gives users a fair path after automated restrictions.",
        "pricing_anchor": "High value for platforms with many account restrictions or fraud flags.",
    },
    "NGO / beneficiary selection": {
        "industry": "NGO, development programme, social protection, grant allocation",
        "affected_person": "Applicant or beneficiary",
        "recommendation_label": "Eligibility recommendation",
        "case_goal": "Determine whether the person should be selected, waitlisted, rejected, or reviewed.",
        "factor_names": {
            "capacity": "Eligibility evidence",
            "burden": "Eligibility conflict or risk",
            "stability": "Household or programme continuity",
            "history": "Prior programme history",
            "documents": "Document completeness",
        },
        "evidence_examples": [
            "Household information",
            "Income or vulnerability document",
            "Local verification letter",
            "Updated identity document",
            "Explanation of special circumstance",
        ],
        "review_paths": [
            "Programme officer review",
            "Correct beneficiary data",
            "Community/field verification",
            "Explanation only",
        ],
        "business_value": "Improves legitimacy, fairness, and auditability in beneficiary selection.",
        "pricing_anchor": "Strong fit for donor-funded pilots, dashboards, and field operations.",
    },
}

PLAN_TABLE = pd.DataFrame(
    [
        {
            "Plan": "Pilot",
            "Best for": "1 workflow, 1 team",
            "Monthly price idea": "$49-$99 or ৳10k-৳25k",
            "Includes": "Manual case entry, affected portal, appeal queue, exports",
        },
        {
            "Plan": "Growth",
            "Best for": "SME fintech/HR/NGO",
            "Monthly price idea": "$199-$499 or ৳30k-৳80k",
            "Includes": "API, templates, reviewer seats, analytics, branded portal",
        },
        {
            "Plan": "Enterprise",
            "Best for": "Bank, insurer, large platform",
            "Monthly price idea": "Custom $1k+ / month",
            "Includes": "SSO, region storage, advanced audit, SLA, custom legal templates",
        },
    ]
)


# -----------------------------------------------------------------------------
# Session state utilities
# -----------------------------------------------------------------------------
def now_string() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def generate_case_id() -> str:
    return "CASE-" + uuid.uuid4().hex[:8].upper()


def add_audit_event(event: str, actor: str = "System") -> None:
    st.session_state.audit_log.append(
        {
            "time": now_string(),
            "actor": actor,
            "event": event,
        }
    )


def init_state() -> None:
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []
    if "company_name" not in st.session_state:
        st.session_state.company_name = "Demo Financial Services"
    if "support_email" not in st.session_state:
        st.session_state.support_email = "review@example.com"
    if "case" not in st.session_state:
        st.session_state.case = None
    if "appeal" not in st.session_state:
        st.session_state.appeal = None
    if "review" not in st.session_state:
        st.session_state.review = {
            "status": "No reviewer action yet",
            "priority": "Not assigned",
            "outcome": "Pending",
            "notes": "",
            "assigned_to": "",
        }
    if not st.session_state.audit_log:
        add_audit_event("MVP opened", "System")


init_state()


# -----------------------------------------------------------------------------
# Decision model
# -----------------------------------------------------------------------------
def compute_decision(
    capacity: int,
    burden: float,
    stability_years: int,
    history: int,
    missing_docs: int,
    sensitive_context: bool,
    high_impact: bool,
) -> Tuple[float, str, str, float, Dict[str, float], List[str], List[str]]:
    """
    Transparent simulation model.
    This is not a real credit, hiring, insurance, admission, moderation, or welfare model.
    It is a demo model for contestability workflow design.
    """
    score = 50.0
    score += min(capacity / 2000, 20)
    score -= burden * 35
    score += min(stability_years * 3, 15)
    score += history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 72:
        recommendation = "Likely approve"
        tone = "success"
    elif score >= 56:
        recommendation = "Send to conditional review"
        tone = "warning"
    else:
        recommendation = "Likely reject unless corrected or reviewed"
        tone = "error"

    # Uncertainty rises near the review boundary and with missing data/sensitive context.
    uncertainty = 20 + max(0, 55 - abs(score - 56)) * 0.8
    uncertainty += missing_docs * 4
    if sensitive_context:
        uncertainty += 8
    if high_impact:
        uncertainty += 5
    uncertainty = max(10, min(90, uncertainty))

    factors = {
        "capacity": min(capacity / 2000, 20),
        "burden": -burden * 35,
        "stability": min(stability_years * 3, 15),
        "history": history * 1.5,
        "documents": -missing_docs * 8,
    }

    triggers: List[str] = []
    if uncertainty >= 60:
        triggers.append("Uncertainty is high, so automatic finalisation may be unsafe.")
    if missing_docs >= 2:
        triggers.append("Important evidence may be missing or unclear.")
    if sensitive_context:
        triggers.append("Sensitive context is present and should be reviewed by a human.")
    if high_impact:
        triggers.append("The decision may have a significant effect on the affected person.")
    if recommendation.startswith("Likely reject") and score >= 45:
        triggers.append("The case is near the rejection boundary and may change after correction.")

    improvement_actions: List[str] = []
    if missing_docs > 0:
        improvement_actions.append("Upload missing or clearer evidence.")
    if burden >= 0.45:
        improvement_actions.append("Explain or correct the debt, burden, or risk indicator.")
    if capacity < 2500:
        improvement_actions.append("Submit updated capacity, income, eligibility, or role-fit evidence.")
    if history <= 4:
        improvement_actions.append("Provide relevant history, past performance, or supporting documentation.")
    if sensitive_context:
        improvement_actions.append("Ask for human review so context is not judged only by automation.")
    if not improvement_actions:
        improvement_actions.append("Request explanation or human confirmation if the outcome still feels wrong.")

    return score, recommendation, tone, uncertainty, factors, triggers, improvement_actions


def factor_explanation(key: str, value: float, domain: str) -> str:
    names = DOMAIN_TEMPLATES[domain]["factor_names"]
    label = names[key]
    if key == "capacity":
        if value >= 15:
            return f"{label} strongly supported the case."
        if value >= 8:
            return f"{label} moderately supported the case."
        return f"{label} gave limited support."
    if key == "burden":
        if value <= -25:
            return f"{label} strongly reduced the score."
        if value <= -10:
            return f"{label} moderately reduced the score."
        return f"{label} had a limited negative effect."
    if key == "stability":
        if value >= 12:
            return f"{label} strongly improved confidence."
        if value >= 6:
            return f"{label} gave moderate support."
        return f"{label} gave limited support."
    if key == "history":
        if value >= 12:
            return f"{label} strongly supported the case."
        if value >= 6:
            return f"{label} moderately supported the case."
        return f"{label} gave limited support."
    if key == "documents":
        if value <= -24:
            return f"{label} strongly reduced confidence."
        if value < 0:
            return f"{label} reduced confidence."
        return f"{label} did not reduce the score."
    return f"{label} influenced the recommendation."


def safer_workflow(recommendation: str, uncertainty: float, missing_docs: int, triggers: List[str]) -> str:
    if missing_docs >= 2:
        return "Request missing evidence before any final outcome."
    if uncertainty >= 60:
        return "Route to human review before finalising the decision."
    if recommendation.startswith("Likely reject") and triggers:
        return "Allow structured correction or appeal before confirming rejection."
    if "conditional" in recommendation.lower():
        return "Use conditional review with focused evidence."
    return "Proceed, but keep explanation, consent, and audit records."


def recommendation_message(tone: str, recommendation: str) -> None:
    if tone == "success":
        st.success(f"Automated recommendation: {recommendation}")
    elif tone == "warning":
        st.warning(f"Automated recommendation: {recommendation}")
    else:
        st.error(f"Automated recommendation: {recommendation}")


def ensure_case_exists() -> None:
    if st.session_state.case is None:
        create_or_update_case(
            country="Bangladesh",
            domain="Fintech / loan decision",
            company_name=st.session_state.company_name,
            support_email=st.session_state.support_email,
            affected_reference="Applicant-001",
            capacity=2600,
            burden=0.42,
            stability_years=2,
            history=5,
            missing_docs=2,
            sensitive_context=True,
            high_impact=True,
        )


def create_or_update_case(
    country: str,
    domain: str,
    company_name: str,
    support_email: str,
    affected_reference: str,
    capacity: int,
    burden: float,
    stability_years: int,
    history: int,
    missing_docs: int,
    sensitive_context: bool,
    high_impact: bool,
) -> None:
    score, recommendation, tone, uncertainty, factors, triggers, improvement_actions = compute_decision(
        capacity=capacity,
        burden=burden,
        stability_years=stability_years,
        history=history,
        missing_docs=missing_docs,
        sensitive_context=sensitive_context,
        high_impact=high_impact,
    )
    case_id = st.session_state.case["case_id"] if st.session_state.case else generate_case_id()
    created_at = st.session_state.case["created_at"] if st.session_state.case else now_string()
    st.session_state.company_name = company_name
    st.session_state.support_email = support_email
    st.session_state.case = {
        "case_id": case_id,
        "created_at": created_at,
        "updated_at": now_string(),
        "country": country,
        "domain": domain,
        "company_name": company_name,
        "support_email": support_email,
        "affected_reference": affected_reference,
        "score": score,
        "recommendation": recommendation,
        "tone": tone,
        "uncertainty": uncertainty,
        "factors": factors,
        "triggers": triggers,
        "improvement_actions": improvement_actions,
        "safer_workflow": safer_workflow(recommendation, uncertainty, missing_docs, triggers),
        "inputs": {
            "capacity": capacity,
            "burden": burden,
            "stability_years": stability_years,
            "history": history,
            "missing_docs": missing_docs,
            "sensitive_context": sensitive_context,
            "high_impact": high_impact,
        },
    }
    add_audit_event(f"Case generated or updated: {case_id}", "Company admin")


def case_report_dict() -> Dict[str, Any]:
    ensure_case_exists()
    case = st.session_state.case
    country = COUNTRY_TEMPLATES[case["country"]]
    domain = DOMAIN_TEMPLATES[case["domain"]]
    return {
        "case": case,
        "country_template": {
            "notice_title": country["notice_title"],
            "review_timeline": country["review_timeline"],
            "retention_rule": country["retention_rule"],
            "escalation_route": country["escalation_route"],
            "required_disclosures": country["required_disclosures"],
        },
        "domain_template": {
            "industry": domain["industry"],
            "case_goal": domain["case_goal"],
            "evidence_examples": domain["evidence_examples"],
            "review_paths": domain["review_paths"],
        },
        "appeal": st.session_state.appeal,
        "review": st.session_state.review,
        "audit_log": st.session_state.audit_log,
    }


def json_download_data() -> str:
    return json.dumps(case_report_dict(), indent=2, ensure_ascii=False)


def audit_csv_data() -> str:
    return pd.DataFrame(st.session_state.audit_log).to_csv(index=False)


def factor_dataframe(case: Dict[str, Any]) -> pd.DataFrame:
    domain = case["domain"]
    names = DOMAIN_TEMPLATES[domain]["factor_names"]
    rows = []
    for key, value in case["factors"].items():
        rows.append(
            {
                "Factor": names[key],
                "Influence": round(value, 2),
                "Meaning": factor_explanation(key, value, domain),
            }
        )
    return pd.DataFrame(rows).sort_values("Influence")


# -----------------------------------------------------------------------------
# Reusable native UI helpers
# -----------------------------------------------------------------------------
def top_header() -> None:
    st.title("🛡️ ContestabilityLayer MVP")
    st.caption(
        "Mobile-safe prototype for explainable, contestable, human-reviewed automated decisions."
    )
    ensure_case_exists()
    case = st.session_state.case
    col1, col2, col3 = st.columns(3)
    col1.metric("Current case", case["case_id"])
    col2.metric("Country template", COUNTRY_TEMPLATES[case["country"]]["short_label"])
    col3.metric("Uncertainty", f"{case['uncertainty']:.0f}%")
    recommendation_message(case["tone"], case["recommendation"])


def render_case_metrics(case: Dict[str, Any]) -> None:
    col1, col2 = st.columns(2)
    col1.metric("Decision score", f"{case['score']:.1f}/100")
    col2.metric("Estimated uncertainty", f"{case['uncertainty']:.1f}%")
    st.progress(int(case["score"]))
    st.caption("Score is a demo value. In production, your client system would send its own outcome and reasons.")


def render_country_notice(country_name: str) -> None:
    country = COUNTRY_TEMPLATES[country_name]
    st.subheader(country["notice_title"])
    st.info(country["affected_notice"])
    with st.container(border=True):
        st.write("What this template gives the affected person:")
        for item in country["rights_summary"]:
            st.write(f"- {item}")
        st.write(f"Expected review timeline: **{country['review_timeline']}**")
        st.write(f"Escalation route: **{country['escalation_route']}**")


def render_status_steps() -> None:
    appeal = st.session_state.appeal
    review = st.session_state.review
    steps = [
        ("1", "Automated recommendation viewed", True),
        ("2", "Contestation submitted", appeal is not None),
        ("3", "Reviewer assigned", bool(review.get("assigned_to"))),
        ("4", "Human review outcome recorded", review.get("outcome") not in ["Pending", "No reviewer action yet"]),
    ]
    st.write("Review progress")
    for number, label, done in steps:
        symbol = "✅" if done else "⬜"
        st.write(f"{symbol} **Step {number}:** {label}")


# -----------------------------------------------------------------------------
# View 1: Setup
# -----------------------------------------------------------------------------
def view_setup() -> None:
    st.header("1. Create or update a decision case")
    st.write(
        "Use this screen as the company-side case creator. In the real SaaS, this can be manual entry, CSV upload, or API-based case creation."
    )

    case = st.session_state.case
    default_country = case["country"] if case else "Bangladesh"
    default_domain = case["domain"] if case else "Fintech / loan decision"
    default_inputs = case["inputs"] if case else {
        "capacity": 2600,
        "burden": 0.42,
        "stability_years": 2,
        "history": 5,
        "missing_docs": 2,
        "sensitive_context": True,
        "high_impact": True,
    }

    with st.form("case_setup_form"):
        st.subheader("Company and template")
        company_name = st.text_input("Company or project name", value=st.session_state.company_name)
        support_email = st.text_input("Review/contact email", value=st.session_state.support_email)
        affected_reference = st.text_input(
            "Affected person reference",
            value=case["affected_reference"] if case else "Applicant-001",
            help="Use a reference ID instead of sensitive personal data in the demo.",
        )

        country = st.radio(
            "Country/legal template",
            list(COUNTRY_TEMPLATES.keys()),
            index=list(COUNTRY_TEMPLATES.keys()).index(default_country),
            horizontal=False,
        )
        domain = st.radio(
            "Decision domain",
            list(DOMAIN_TEMPLATES.keys()),
            index=list(DOMAIN_TEMPLATES.keys()).index(default_domain),
            horizontal=False,
        )

        st.subheader("Demo decision inputs")
        st.caption("These are generic demo inputs. In production, the client's model sends the real factors.")
        capacity = st.slider(
            "Capacity / eligibility / role-fit indicator",
            min_value=500,
            max_value=10000,
            value=int(default_inputs["capacity"]),
            step=100,
        )
        burden = st.slider(
            "Burden / risk / gap indicator",
            min_value=0.0,
            max_value=1.0,
            value=float(default_inputs["burden"]),
            step=0.01,
        )
        stability_years = st.slider(
            "Years of stability / relevant activity",
            min_value=0,
            max_value=15,
            value=int(default_inputs["stability_years"]),
        )
        history = st.slider(
            "Relevant history score",
            min_value=0,
            max_value=10,
            value=int(default_inputs["history"]),
        )
        missing_docs = st.slider(
            "Missing or unclear documents",
            min_value=0,
            max_value=5,
            value=int(default_inputs["missing_docs"]),
        )
        sensitive_context = st.checkbox(
            "Sensitive context may require human review",
            value=bool(default_inputs["sensitive_context"]),
        )
        high_impact = st.checkbox(
            "This decision may significantly affect the person",
            value=bool(default_inputs["high_impact"]),
        )

        submitted = st.form_submit_button("Generate / update case")

    if submitted:
        create_or_update_case(
            country=country,
            domain=domain,
            company_name=company_name,
            support_email=support_email,
            affected_reference=affected_reference,
            capacity=capacity,
            burden=burden,
            stability_years=stability_years,
            history=history,
            missing_docs=missing_docs,
            sensitive_context=sensitive_context,
            high_impact=high_impact,
        )
        st.success("Case updated. Open the affected-person portal or reviewer dashboard next.")

    st.subheader("Current case preview")
    case = st.session_state.case
    with st.container(border=True):
        st.write(f"**Case ID:** {case['case_id']}")
        st.write(f"**Company:** {case['company_name']}")
        st.write(f"**Domain:** {case['domain']}")
        st.write(f"**Country template:** {case['country']}")
        render_case_metrics(case)
        st.write(f"**Recommended safer workflow:** {case['safer_workflow']}")


# -----------------------------------------------------------------------------
# View 2: Affected-person portal
# -----------------------------------------------------------------------------
def view_affected_portal() -> None:
    ensure_case_exists()
    case = st.session_state.case
    country = COUNTRY_TEMPLATES[case["country"]]
    domain = DOMAIN_TEMPLATES[case["domain"]]

    st.header("2. Affected-person portal")
    st.caption("This is what the applicant, candidate, claimant, user, or beneficiary would see.")

    with st.container(border=True):
        st.write(f"**{domain['affected_person']} reference:** {case['affected_reference']}")
        st.write(f"**Company:** {case['company_name']}")
        st.write(f"**Case type:** {case['domain']}")
        recommendation_message(case["tone"], case["recommendation"])
        render_case_metrics(case)

    render_country_notice(case["country"])

    st.subheader("Why human review may be needed")
    if case["triggers"]:
        for item in case["triggers"]:
            st.warning(item)
    else:
        st.success("No automatic escalation trigger was detected, but you may still ask for review.")
    st.info(f"Recommended safer workflow: {case['safer_workflow']}")

    st.subheader("Explanation")
    explanation_mode = st.radio(
        "Choose explanation detail",
        ["Simple", "Detailed", "Technical table"],
        horizontal=True,
    )
    factor_df = factor_dataframe(case)

    if explanation_mode == "Simple":
        strongest = factor_df.iloc[0]
        supportive = factor_df.iloc[-1]
        st.write("Main things to know:")
        st.write(f"- Biggest concern: **{strongest['Factor']}** — {strongest['Meaning']}")
        st.write(f"- Strongest support: **{supportive['Factor']}** — {supportive['Meaning']}")
        st.write("- The recommendation is not final if evidence is missing, context is sensitive, or uncertainty is high.")
    elif explanation_mode == "Detailed":
        for _, row in factor_df.iterrows():
            with st.container(border=True):
                st.write(f"**{row['Factor']}**")
                st.write(row["Meaning"])
                influence = float(row["Influence"])
                if influence >= 0:
                    st.write(f"Influence: +{influence:.1f}")
                else:
                    st.write(f"Influence: {influence:.1f}")
    else:
        st.dataframe(factor_df, use_container_width=True, hide_index=True)

    st.subheader("What could help change or clarify the outcome")
    for action in case["improvement_actions"]:
        st.write(f"- {action}")

    st.subheader("What-if correction simulator")
    st.caption("This lets the affected person see whether corrections may matter before submitting evidence.")
    with st.form("what_if_form"):
        wi_capacity = st.slider(
            "Corrected capacity / eligibility / role-fit indicator",
            500,
            10000,
            int(case["inputs"]["capacity"]),
            step=100,
        )
        wi_burden = st.slider(
            "Corrected burden / risk / gap indicator",
            0.0,
            1.0,
            float(case["inputs"]["burden"]),
            step=0.01,
        )
        wi_missing = st.slider(
            "Corrected missing documents count",
            0,
            5,
            int(case["inputs"]["missing_docs"]),
        )
        wi_submit = st.form_submit_button("Preview corrected outcome")

    if wi_submit:
        wi_score, wi_rec, wi_tone, wi_uncertainty, *_ = compute_decision(
            capacity=wi_capacity,
            burden=wi_burden,
            stability_years=int(case["inputs"]["stability_years"]),
            history=int(case["inputs"]["history"]),
            missing_docs=wi_missing,
            sensitive_context=bool(case["inputs"]["sensitive_context"]),
            high_impact=bool(case["inputs"]["high_impact"]),
        )
        with st.container(border=True):
            st.write("Corrected-outcome preview")
            if wi_tone == "success":
                st.success(f"Preview recommendation: {wi_rec}")
            elif wi_tone == "warning":
                st.warning(f"Preview recommendation: {wi_rec}")
            else:
                st.error(f"Preview recommendation: {wi_rec}")
            st.metric("Preview score", f"{wi_score:.1f}/100", delta=f"{wi_score - case['score']:.1f}")
            st.metric("Preview uncertainty", f"{wi_uncertainty:.1f}%", delta=f"{wi_uncertainty - case['uncertainty']:.1f}%")

    st.subheader("Submit contestation or review request")
    with st.form("appeal_form"):
        st.write("Select reasons for review")
        selected_reasons: List[str] = []
        for option in country["appeal_options"]:
            if st.checkbox(option, key=f"reason_{option}"):
                selected_reasons.append(option)
        extra_reason = st.text_input("Other reason, if any")
        explanation = st.text_area(
            "Explain what should be reviewed",
            placeholder="Example: One document was missing, and my current income/experience/evidence is higher than shown.",
        )
        review_path = st.radio("Preferred review path", domain["review_paths"], horizontal=False)
        uploaded = st.file_uploader(
            "Upload evidence, if needed",
            type=["pdf", "png", "jpg", "jpeg", "docx", "txt", "csv"],
            accept_multiple_files=True,
        )
        consent = st.checkbox(country["consent_text"])
        appeal_submit = st.form_submit_button("Submit review request")

    if appeal_submit:
        if extra_reason.strip():
            selected_reasons.append(extra_reason.strip())
        if not selected_reasons:
            st.error("Please select at least one reason or write another reason.")
        elif not consent:
            st.error("Please confirm purpose-limited consent before submitting.")
        else:
            st.session_state.appeal = {
                "submitted_at": now_string(),
                "reasons": selected_reasons,
                "explanation": explanation,
                "review_path": review_path,
                "uploaded_files": [f.name for f in uploaded] if uploaded else [],
                "consent_text": country["consent_text"],
            }
            st.session_state.review["status"] = "Appeal received, awaiting reviewer"
            add_audit_event("Affected person submitted contestation request", "Affected person")
            st.success("Review request submitted successfully.")
            st.balloons()

    st.subheader("Appeal status")
    with st.container(border=True):
        render_status_steps()
        if st.session_state.appeal:
            st.write(f"Submitted at: **{st.session_state.appeal['submitted_at']}**")
            st.write(f"Current review status: **{st.session_state.review['status']}**")
            st.write(f"Expected timeline: **{country['review_timeline']}**")
        else:
            st.write("No contestation has been submitted yet.")


# -----------------------------------------------------------------------------
# View 3: Reviewer dashboard
# -----------------------------------------------------------------------------
def view_reviewer_dashboard() -> None:
    ensure_case_exists()
    case = st.session_state.case
    country = COUNTRY_TEMPLATES[case["country"]]
    domain = DOMAIN_TEMPLATES[case["domain"]]

    st.header("3. Company reviewer dashboard")
    st.caption("This is the paid company-side workflow: receive appeals, review evidence, record outcomes, and export audit evidence.")

    with st.container(border=True):
        st.write("Case summary")
        col1, col2 = st.columns(2)
        col1.metric("Case ID", case["case_id"])
        col2.metric("Uncertainty", f"{case['uncertainty']:.1f}%")
        st.write(f"**Affected reference:** {case['affected_reference']}")
        st.write(f"**Domain:** {case['domain']}")
        st.write(f"**Country template:** {case['country']}")
        recommendation_message(case["tone"], case["recommendation"])
        st.write(f"**Safer workflow:** {case['safer_workflow']}")

    st.subheader("Reviewer checklist")
    for item in country["required_disclosures"]:
        st.write(f"- {item}")
    st.info(f"Retention rule: {country['retention_rule']}")
    st.info(f"Regulatory/template note: {country['regulator_note']}")

    st.subheader("Appeal received")
    if st.session_state.appeal:
        appeal = st.session_state.appeal
        with st.container(border=True):
            st.write(f"**Submitted:** {appeal['submitted_at']}")
            st.write(f"**Preferred path:** {appeal['review_path']}")
            st.write("**Reasons:**")
            for reason in appeal["reasons"]:
                st.write(f"- {reason}")
            if appeal["explanation"]:
                st.write("**Affected-person explanation:**")
                st.write(appeal["explanation"])
            if appeal["uploaded_files"]:
                st.write("**Uploaded evidence:**")
                for file_name in appeal["uploaded_files"]:
                    st.write(f"- {file_name}")
            else:
                st.write("No evidence file uploaded yet.")
    else:
        st.warning("No appeal submitted yet. Use the affected-person portal to submit one.")

    st.subheader("Record human review")
    with st.form("reviewer_form"):
        assigned_to = st.text_input("Assigned reviewer", value=st.session_state.review.get("assigned_to", ""))
        priority = st.radio(
            "Priority",
            ["Low", "Normal", "High", "Urgent"],
            index=["Low", "Normal", "High", "Urgent"].index(st.session_state.review.get("priority", "Normal") if st.session_state.review.get("priority") in ["Low", "Normal", "High", "Urgent"] else "Normal"),
            horizontal=True,
        )
        status = st.radio(
            "Review status",
            ["Appeal received, awaiting reviewer", "In review", "Need more evidence", "Ready for final outcome", "Closed"],
            horizontal=False,
        )
        outcome = st.radio(
            "Human-review outcome",
            ["Pending", "Original recommendation upheld", "Recommendation changed", "More evidence required", "Escalated to senior review"],
            horizontal=False,
        )
        reviewer_notes = st.text_area(
            "Reviewer notes",
            value=st.session_state.review.get("notes", ""),
            placeholder="Record what was checked, what evidence was considered, and why the outcome is fair or needs correction.",
        )
        internal_flag = st.checkbox("Flag for compliance/legal audit")
        submit_review = st.form_submit_button("Save reviewer decision")

    if submit_review:
        st.session_state.review = {
            "status": status,
            "priority": priority,
            "outcome": outcome,
            "notes": reviewer_notes,
            "assigned_to": assigned_to,
            "internal_flag": internal_flag,
            "updated_at": now_string(),
        }
        add_audit_event(f"Reviewer saved status: {status}; outcome: {outcome}", "Reviewer")
        st.success("Reviewer decision saved.")

    st.subheader("Evidence examples for this domain")
    for item in domain["evidence_examples"]:
        st.write(f"- {item}")


# -----------------------------------------------------------------------------
# View 4: Admin and SaaS business layer
# -----------------------------------------------------------------------------
def view_admin_saas() -> None:
    ensure_case_exists()
    case = st.session_state.case
    country = COUNTRY_TEMPLATES[case["country"]]
    domain = DOMAIN_TEMPLATES[case["domain"]]

    st.header("4. SaaS admin and profitability layer")
    st.write(
        "This section turns the prototype into a sellable B2B product idea: templates, pricing, ROI, and deployment readiness."
    )

    st.subheader("Why the company would pay")
    with st.container(border=True):
        st.write(f"**Domain:** {case['domain']}")
        st.write(f"**Business value:** {domain['business_value']}")
        st.write(f"**Pricing anchor:** {domain['pricing_anchor']}")
        st.write(f"**Data-region note:** {country['data_region_note']}")

    st.subheader("Suggested pricing tiers")
    st.dataframe(PLAN_TABLE, use_container_width=True, hide_index=True)

    st.subheader("ROI calculator")
    st.caption("This helps sell the SaaS by showing how appeal standardisation can save support and compliance cost.")
    with st.form("roi_form"):
        cases_per_month = st.slider("Automated decision cases per month", 50, 100000, 2000, step=50)
        appeal_rate = st.slider("Expected appeal/review rate", 0.0, 30.0, 5.0, step=0.5)
        current_minutes_per_appeal = st.slider("Current manual support minutes per appeal", 5, 180, 35, step=5)
        improved_minutes_per_appeal = st.slider("Minutes per appeal after using this system", 3, 120, 18, step=3)
        staff_cost_per_hour = st.slider("Support/compliance cost per hour", 2, 150, 15, step=1)
        monthly_saas_price = st.slider("Proposed monthly SaaS price", 20, 5000, 299, step=10)
        roi_submit = st.form_submit_button("Calculate ROI")

    if roi_submit:
        appeals = cases_per_month * appeal_rate / 100
        current_cost = appeals * (current_minutes_per_appeal / 60) * staff_cost_per_hour
        improved_cost = appeals * (improved_minutes_per_appeal / 60) * staff_cost_per_hour
        savings = max(0, current_cost - improved_cost)
        net_value = savings - monthly_saas_price
        col1, col2 = st.columns(2)
        col1.metric("Estimated appeals/month", f"{appeals:.0f}")
        col2.metric("Estimated monthly savings", f"${savings:,.0f}")
        col3, col4 = st.columns(2)
        col3.metric("SaaS price", f"${monthly_saas_price:,.0f}")
        col4.metric("Net monthly value", f"${net_value:,.0f}")
        if net_value >= 0:
            st.success("The proposed price is defensible under this scenario.")
        else:
            st.warning("The proposed price may be too high unless compliance/risk value is also counted.")

    st.subheader("Best MVP feature set for paid pilots")
    pilot_features = [
        "Company workspace and reviewer login",
        "Manual and API-based case creation",
        "Affected-person portal link",
        "Plain-language explanation and uncertainty notice",
        "Evidence upload and purpose-limited consent",
        "Reviewer queue, notes, status, and outcome",
        "Country/domain templates",
        "Audit log export and case report export",
        "Company branding and email notifications",
    ]
    for feature in pilot_features:
        st.write(f"- {feature}")

    st.subheader("Country template currently active")
    with st.container(border=True):
        st.write(f"**Country:** {case['country']}")
        st.write(f"**Timeline:** {country['review_timeline']}")
        st.write(f"**Retention:** {country['retention_rule']}")
        st.write("**Required disclosures:**")
        for item in country["required_disclosures"]:
            st.write(f"- {item}")


# -----------------------------------------------------------------------------
# View 5: API, exports, and implementation handoff
# -----------------------------------------------------------------------------
def view_api_exports() -> None:
    ensure_case_exists()
    case = st.session_state.case
    country = COUNTRY_TEMPLATES[case["country"]]
    domain = DOMAIN_TEMPLATES[case["domain"]]

    st.header("5. API, exports, and SaaS handoff")
    st.write(
        "This section shows how the real SaaS would connect with client systems and generate audit evidence."
    )

    st.subheader("API payload preview")
    api_payload = {
        "external_case_id": case["case_id"],
        "country_template": case["country"],
        "domain_template": case["domain"],
        "affected_reference": case["affected_reference"],
        "automated_recommendation": case["recommendation"],
        "score": round(case["score"], 2),
        "uncertainty": round(case["uncertainty"], 2),
        "factors": [
            {
                "name": DOMAIN_TEMPLATES[case["domain"]]["factor_names"][key],
                "influence": round(value, 2),
                "plain_language": factor_explanation(key, value, case["domain"]),
            }
            for key, value in case["factors"].items()
        ],
        "review_triggers": case["triggers"],
        "recommended_workflow": case["safer_workflow"],
        "portal_callback_email": case["support_email"],
    }
    st.code(json.dumps(api_payload, indent=2, ensure_ascii=False), language="json")

    st.subheader("Required fields for this country/domain")
    required_fields = [
        "external_case_id",
        "affected_reference",
        "country_template",
        "domain_template",
        "automated_recommendation",
        "main_factors",
        "review_route",
        "support_contact",
    ]
    for field in required_fields:
        st.write(f"- `{field}`")

    st.subheader("Exports")
    st.download_button(
        "Download full case report as JSON",
        data=json_download_data(),
        file_name=f"{case['case_id']}_case_report.json",
        mime="application/json",
    )
    st.download_button(
        "Download audit log as CSV",
        data=audit_csv_data(),
        file_name=f"{case['case_id']}_audit_log.csv",
        mime="text/csv",
    )

    st.subheader("Audit timeline")
    st.dataframe(pd.DataFrame(st.session_state.audit_log), use_container_width=True, hide_index=True)

    st.subheader("CSV import simulator")
    st.caption("For paid pilots, let companies upload a CSV of decision cases before API integration.")
    uploaded_csv = st.file_uploader("Upload sample CSV", type=["csv"], key="csv_import")
    if uploaded_csv is not None:
        try:
            df = pd.read_csv(uploaded_csv)
            st.success("CSV loaded. In production, this would validate and create cases.")
            st.dataframe(df.head(20), use_container_width=True)
        except Exception as exc:
            st.error(f"Could not read CSV: {exc}")

    st.subheader("Final SaaS rebuild plan")
    roadmap = pd.DataFrame(
        [
            {"Phase": "Pilot SaaS", "Build": "Next.js + FastAPI/Django + PostgreSQL + file storage", "Goal": "Paid pilots"},
            {"Phase": "Growth SaaS", "Build": "Auth, billing, API keys, email, branding, analytics", "Goal": "Recurring subscription"},
            {"Phase": "Enterprise", "Build": "SSO, region storage, advanced audit, security review, SLA", "Goal": "Larger contracts"},
        ]
    )
    st.dataframe(roadmap, use_container_width=True, hide_index=True)

    st.info(
        "The Streamlit MVP is for validation. The final product should be rebuilt as a real multi-tenant SaaS, not extended endlessly in Streamlit."
    )


# -----------------------------------------------------------------------------
# Main app
# -----------------------------------------------------------------------------
def main() -> None:
    top_header()

    st.write("Choose what you want to test:")
    view = st.radio(
        "Main navigation",
        [
            "1. Setup case",
            "2. Affected-person portal",
            "3. Company reviewer dashboard",
            "4. SaaS admin and ROI",
            "5. API and exports",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    if view == "1. Setup case":
        view_setup()
    elif view == "2. Affected-person portal":
        view_affected_portal()
    elif view == "3. Company reviewer dashboard":
        view_reviewer_dashboard()
    elif view == "4. SaaS admin and ROI":
        view_admin_saas()
    else:
        view_api_exports()

    st.divider()
    st.caption(
        "Prototype note: This app demonstrates contestability workflow design. It is not legal, financial, hiring, insurance, or admissions advice."
    )


if __name__ == "__main__":
    main()
