# app.py
# Contestable AI Decision Interface
# UI/UX-polished Streamlit MVP for AI contestability / human-review workflow
# Run locally with: streamlit run app.py

from __future__ import annotations

from datetime import datetime
from hashlib import sha1
from typing import Dict, List, Tuple
import json

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
# UI helpers and styling
# ============================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #f8fafc;
        --card: #ffffff;
        --text: #111827;
        --muted: #4b5563;
        --line: #e5e7eb;
        --soft-line: #f1f5f9;
        --blue: #2563eb;
        --blue-soft: #dbeafe;
        --green: #16a34a;
        --green-soft: #dcfce7;
        --amber: #d97706;
        --amber-soft: #fef3c7;
        --red: #dc2626;
        --red-soft: #fee2e2;
        --purple: #7c3aed;
        --purple-soft: #ede9fe;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    .hero {
        border: 1px solid var(--line);
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 34%),
            linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 24px;
        padding: 1.45rem 1.55rem;
        box-shadow: 0 12px 34px rgba(15, 23, 42, 0.07);
        margin-bottom: 1.15rem;
    }

    .main-title {
        font-size: clamp(1.8rem, 3vw, 2.55rem);
        font-weight: 850;
        letter-spacing: -0.04em;
        color: var(--text);
        line-height: 1.05;
        margin: 0 0 0.45rem 0;
    }

    .subtitle {
        font-size: 1.02rem;
        color: var(--muted);
        max-width: 860px;
        line-height: 1.55;
        margin: 0;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text);
        margin: 1.1rem 0 0.55rem 0;
        letter-spacing: -0.015em;
    }

    .section-help {
        color: var(--muted);
        line-height: 1.5;
        margin-top: -0.25rem;
        margin-bottom: 0.75rem;
        font-size: 0.95rem;
    }

    .card {
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 1rem 1.05rem;
        background: var(--card);
        box-shadow: 0 4px 16px rgba(15, 23, 42, 0.045);
        margin-bottom: 0.85rem;
        color: var(--text);
    }

    .compact-card {
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 0.85rem 0.95rem;
        background: var(--card);
        margin-bottom: 0.7rem;
        color: var(--text);
    }

    .decision-card {
        border-radius: 22px;
        padding: 1.2rem;
        box-shadow: 0 10px 26px rgba(15, 23, 42, 0.07);
        margin-bottom: 0.85rem;
        color: var(--text);
    }

    .status-approved {
        border: 1px solid #bbf7d0;
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    }

    .status-review {
        border: 1px solid #fde68a;
        background: linear-gradient(135deg, #fffbeb 0%, #ffffff 100%);
    }

    .status-rejected {
        border: 1px solid #fecaca;
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
    }

    .status-info {
        border: 1px solid #bfdbfe;
        background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        border-radius: 999px;
        padding: 0.28rem 0.68rem;
        font-size: 0.78rem;
        font-weight: 750;
        border: 1px solid transparent;
        margin-bottom: 0.55rem;
    }

    .badge-green {
        color: #166534;
        background: var(--green-soft);
        border-color: #bbf7d0;
    }

    .badge-amber {
        color: #92400e;
        background: var(--amber-soft);
        border-color: #fde68a;
    }

    .badge-red {
        color: #991b1b;
        background: var(--red-soft);
        border-color: #fecaca;
    }

    .badge-blue {
        color: #1e40af;
        background: var(--blue-soft);
        border-color: #bfdbfe;
    }

    .badge-purple {
        color: #5b21b6;
        background: var(--purple-soft);
        border-color: #ddd6fe;
    }

    .kpi-label {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.2rem;
    }

    .kpi-value {
        color: var(--text);
        font-size: 1.55rem;
        font-weight: 850;
        letter-spacing: -0.035em;
        line-height: 1.05;
    }

    .kpi-help {
        color: var(--muted);
        font-size: 0.88rem;
        margin-top: 0.35rem;
        line-height: 1.4;
    }

    .factor-card {
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 0.95rem;
        background: #ffffff;
        margin-bottom: 0.72rem;
        color: var(--text);
    }

    .factor-head {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        align-items: flex-start;
        margin-bottom: 0.45rem;
    }

    .factor-name {
        font-weight: 800;
        color: var(--text);
    }

    .factor-score-pos {
        color: var(--green);
        font-weight: 850;
        white-space: nowrap;
    }

    .factor-score-neg {
        color: var(--red);
        font-weight: 850;
        white-space: nowrap;
    }

    .factor-score-neu {
        color: var(--muted);
        font-weight: 850;
        white-space: nowrap;
    }

    .factor-text {
        color: var(--muted);
        line-height: 1.45;
        font-size: 0.94rem;
    }

    .timeline-item {
        border-left: 3px solid #bfdbfe;
        padding: 0.1rem 0 0.75rem 0.9rem;
        margin-left: 0.2rem;
    }

    .timeline-time {
        color: var(--muted);
        font-size: 0.82rem;
        font-weight: 650;
    }

    .timeline-event {
        color: var(--text);
        font-weight: 700;
        margin-top: 0.12rem;
    }

    .callout {
        border-radius: 16px;
        padding: 0.9rem 1rem;
        border: 1px solid var(--line);
        background: #f8fafc;
        margin-bottom: 0.85rem;
        color: var(--text);
        line-height: 1.48;
    }

    .callout strong {
        color: var(--text);
    }

    .small-text {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.45;
    }

    .muted {
        color: var(--muted);
    }

    .divider-soft {
        height: 1px;
        background: var(--line);
        margin: 0.75rem 0;
    }

    .step-number {
        width: 1.55rem;
        height: 1.55rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: #111827;
        color: #ffffff;
        border-radius: 999px;
        font-size: 0.82rem;
        font-weight: 800;
        margin-right: 0.4rem;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.4rem;
        background: #f1f5f9;
        padding: 0.35rem;
        border-radius: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 0.55rem 0.85rem;
        font-weight: 750;
    }

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    @media (max-width: 760px) {
        .block-container {
            padding-left: 0.85rem;
            padding-right: 0.85rem;
            padding-top: 0.9rem;
        }

        .hero {
            padding: 1.05rem;
            border-radius: 18px;
        }

        .main-title {
            font-size: 1.75rem;
        }

        .subtitle {
            font-size: 0.95rem;
        }

        .card, .compact-card, .decision-card, .factor-card {
            padding: 0.88rem;
            border-radius: 15px;
        }

        .kpi-value {
            font-size: 1.28rem;
        }

        .section-title {
            font-size: 1.12rem;
        }

        .factor-head {
            flex-direction: column;
            gap: 0.2rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def html_card(body: str, class_name: str = "card") -> None:
    st.markdown(f'<div class="{class_name}">{body}</div>', unsafe_allow_html=True)


def badge(text: str, variant: str = "blue") -> str:
    return f'<span class="badge badge-{variant}">{text}</span>'


def section_title(title: str, help_text: str | None = None) -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if help_text:
        st.markdown(f'<div class="section-help">{help_text}</div>', unsafe_allow_html=True)


def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================
# Session state
# ============================================================
DEFAULTS = {
    "audit_log": [],
    "contestation_submitted": False,
    "contest_receipt": None,
    "review_status": "Not submitted",
    "reviewer_notes": "",
    "final_reviewer_outcome": "Pending",
    "case_counter": 1,
    "last_case_signature": "",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def add_audit_event(event: str, actor: str = "System") -> None:
    st.session_state.audit_log.append(
        {
            "Time": now_str(),
            "Actor": actor,
            "Event": event,
        }
    )


def reset_case_state() -> None:
    st.session_state.audit_log = []
    st.session_state.contestation_submitted = False
    st.session_state.contest_receipt = None
    st.session_state.review_status = "Not submitted"
    st.session_state.reviewer_notes = ""
    st.session_state.final_reviewer_outcome = "Pending"
    st.session_state.case_counter += 1
    st.session_state.last_case_signature = ""
    st.rerun()


# ============================================================
# Country and domain templates
# ============================================================
COUNTRY_TEMPLATES: Dict[str, Dict[str, str]] = {
    "Bangladesh": {
        "language_note": "Plain Bangla/English wording, clear company review route, and simple evidence guidance.",
        "rights_text": "You can request human review, correct incomplete information, and submit relevant evidence for this specific review.",
        "timeline": "Suggested review timeline: 3–7 working days.",
        "consent": "I consent to share only the selected information for this specific human review purpose.",
        "regulatory_style": "Practical trust, grievance handling, and internal review readiness.",
    },
    "UK/EU-style": {
        "language_note": "GDPR-style wording with human intervention, contestation, and explanation rights.",
        "rights_text": "You can request meaningful human intervention, express your point of view, and contest the automated recommendation.",
        "timeline": "Suggested review timeline: defined by organizational policy and applicable data-rights procedures.",
        "consent": "I consent to this information being used only for the review of this decision and related audit record.",
        "regulatory_style": "Automated decision contestability, meaningful human review, and audit-readiness.",
    },
    "US-style": {
        "language_note": "Sector-specific adverse-action or fairness-oriented notice style.",
        "rights_text": "You can ask for the main reasons, correct inaccurate information, and request review according to the company policy.",
        "timeline": "Suggested review timeline: policy-dependent, usually shown clearly in the notice.",
        "consent": "I authorize this information to be used only for this review request.",
        "regulatory_style": "Adverse-action style explanation and case documentation.",
    },
    "India-style": {
        "language_note": "Plain-language notice with grievance route, digital lending/HR/consumer review adaptation.",
        "rights_text": "You can request review, submit correction evidence, and ask for the decision basis in simple language.",
        "timeline": "Suggested review timeline: 3–10 working days depending on sector.",
        "consent": "I agree that the submitted information will be used only for this review request.",
        "regulatory_style": "Digital service grievance, transparency, and internal escalation readiness.",
    },
}

DOMAIN_TEMPLATES: Dict[str, Dict[str, str]] = {
    "Loan application": {
        "affected_person": "Applicant",
        "company_team": "Credit/risk review team",
        "decision_label": "Automated credit recommendation",
        "evidence_examples": "Updated income proof, employment document, repayment record, corrected debt information.",
    },
    "Hiring shortlist": {
        "affected_person": "Candidate",
        "company_team": "HR/recruitment review team",
        "decision_label": "Automated shortlisting recommendation",
        "evidence_examples": "Updated CV, missing experience record, portfolio, certification, corrected eligibility information.",
    },
    "Insurance claim": {
        "affected_person": "Claimant",
        "company_team": "Claims review team",
        "decision_label": "Automated claim recommendation",
        "evidence_examples": "Medical or repair documents, claim photos, policy document, corrected incident details.",
    },
    "University admission": {
        "affected_person": "Applicant",
        "company_team": "Admissions review team",
        "decision_label": "Automated admissions recommendation",
        "evidence_examples": "Transcript correction, test score, recommendation letter, missing eligibility document.",
    },
    "Content moderation appeal": {
        "affected_person": "Account holder",
        "company_team": "Trust and safety review team",
        "decision_label": "Automated moderation recommendation",
        "evidence_examples": "Context explanation, ownership proof, screenshot, corrected account activity information.",
    },
    "NGO beneficiary selection": {
        "affected_person": "Beneficiary applicant",
        "company_team": "Program eligibility review team",
        "decision_label": "Automated eligibility recommendation",
        "evidence_examples": "Household information, income correction, location proof, vulnerability documentation.",
    },
}


# ============================================================
# Model and explanation logic
# ============================================================
def compute_decision(
    capacity_indicator: int,
    burden_ratio: float,
    stable_activity_years: int,
    missing_docs: int,
    relevant_history: int,
    sensitive_context: bool,
) -> Tuple[float, str, str, float, Dict[str, float], List[str], str]:
    """
    Transparent simulated decision model.

    This is not a real credit, hiring, insurance, admission, or moderation model.
    It is only a demonstration model for interaction design and contestability.
    """
    score = 50
    score += min(capacity_indicator / 2000, 20)
    score -= burden_ratio * 35
    score += min(stable_activity_years * 3, 15)
    score += relevant_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        decision = "Approve"
        status_class = "status-approved"
    elif score >= 55:
        decision = "Send to conditional review"
        status_class = "status-review"
    else:
        decision = "Do not approve automatically"
        status_class = "status-rejected"

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Capacity indicator": min(capacity_indicator / 2000, 20),
        "Burden or risk ratio": -burden_ratio * 35,
        "Stable activity history": min(stable_activity_years * 3, 15),
        "Relevant history": relevant_history * 1.5,
        "Missing or unclear documents": -missing_docs * 8,
    }

    review_triggers: List[str] = []

    if uncertainty >= 60:
        review_triggers.append(
            "The model uncertainty is high enough that automatic finalization may be unsafe."
        )

    if missing_docs >= 2:
        review_triggers.append(
            "Important documents may be missing, so the recommendation may be based on incomplete information."
        )

    if sensitive_context:
        review_triggers.append(
            "The case includes sensitive context and should be checked by a human reviewer."
        )

    if decision == "Do not approve automatically" and score >= 45:
        review_triggers.append(
            "The case is near the decision boundary, so a small correction could change the outcome."
        )

    if score >= 70 and not review_triggers:
        risk_level = "Low"
    elif uncertainty >= 60 or missing_docs >= 2 or sensitive_context:
        risk_level = "Elevated"
    else:
        risk_level = "Moderate"

    return score, decision, status_class, uncertainty, factors, review_triggers, risk_level


def uncertainty_label(uncertainty: float) -> Tuple[str, str]:
    if uncertainty >= 65:
        return "High uncertainty", "red"
    if uncertainty >= 45:
        return "Medium uncertainty", "amber"
    return "Low uncertainty", "green"


def risk_badge_variant(risk_level: str) -> str:
    if risk_level == "Low":
        return "green"
    if risk_level == "Moderate":
        return "amber"
    return "red"


def factor_explanation(factor: str, value: float) -> str:
    """Convert numerical factor influence into plain language."""
    if factor == "Capacity indicator":
        if value >= 15:
            return "This strongly supported the application or request."
        if value >= 8:
            return "This moderately supported the application or request."
        return "This gave limited support to the application or request."

    if factor == "Burden or risk ratio":
        if value <= -25:
            return "This strongly reduced the automated score."
        if value <= -10:
            return "This moderately reduced the automated score."
        return "This had only a limited negative effect."

    if factor == "Stable activity history":
        if value >= 12:
            return "Stable history improved confidence in the recommendation."
        if value >= 6:
            return "This gave moderate support."
        return "This gave limited support."

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

    return "This factor influenced the recommendation."


def correction_hint(factor: str, value: float, domain: str) -> str:
    examples = DOMAIN_TEMPLATES[domain]["evidence_examples"]
    if factor == "Missing or unclear documents" and value < 0:
        return f"Upload or clarify missing documents. Examples: {examples}"
    if factor == "Burden or risk ratio" and value <= -10:
        return "Check whether this value is current and whether the underlying data is complete."
    if factor == "Capacity indicator" and value < 8:
        return "Submit updated information if the current capacity indicator is inaccurate or incomplete."
    if factor == "Stable activity history" and value < 6:
        return "Add missing work, activity, education, or eligibility history if relevant."
    if factor == "Relevant history" and value < 6:
        return "Add missing positive history or correction evidence if the record is incomplete."
    return "No immediate correction is suggested, but the person can still request human review."


def safer_workflow_recommendation(
    decision: str,
    missing_docs: int,
    uncertainty: float,
    review_triggers: List[str],
) -> str:
    """Recommend a safer next step based on the decision context."""
    if missing_docs >= 2:
        return "Request missing documents before making a final decision."

    if uncertainty >= 60:
        return "Send the case to fast human review instead of relying only on automation."

    if decision == "Do not approve automatically" and review_triggers:
        return "Allow structured appeal and data correction before final rejection."

    if decision == "Send to conditional review":
        return "Use conditional review with limited additional evidence."

    if decision == "Approve":
        return "Proceed, but keep an audit trail and purpose limitation."

    return "Offer explanation and a clear review path."


def make_case_id(signature: str, counter: int) -> str:
    digest = sha1(signature.encode("utf-8")).hexdigest()[:7].upper()
    return f"CAI-{counter:04d}-{digest}"


def make_case_signature(values: Dict[str, object]) -> str:
    return json.dumps(values, sort_keys=True, default=str)


def build_report(
    case_id: str,
    country: str,
    scenario: str,
    score: float,
    decision: str,
    uncertainty: float,
    risk_level: str,
    recommended_workflow: str,
    factors: Dict[str, float],
    review_triggers: List[str],
) -> str:
    factor_lines = "\n".join(
        f"- {name}: {value:.2f} | {factor_explanation(name, value)}"
        for name, value in factors.items()
    )
    trigger_lines = "\n".join(f"- {trigger}" for trigger in review_triggers) if review_triggers else "- No automatic trigger detected."
    audit_lines = "\n".join(
        f"- {row['Time']} | {row['Actor']} | {row['Event']}"
        for row in st.session_state.audit_log
    )

    contest = st.session_state.contest_receipt or {}
    contest_lines = json.dumps(contest, indent=2, ensure_ascii=False) if contest else "No contestation submitted."

    return f"""Contestable AI Decision Case Report

Case ID: {case_id}
Generated: {now_str()}

Country template: {country}
Scenario: {scenario}
Automated recommendation: {decision}
Score: {score:.1f}/100
Uncertainty: {uncertainty:.1f}%
Risk level: {risk_level}

Recommended safer workflow:
{recommended_workflow}

Review triggers:
{trigger_lines}

Factor explanations:
{factor_lines}

Contestation receipt:
{contest_lines}

Reviewer status:
- Review status: {st.session_state.review_status}
- Final reviewer outcome: {st.session_state.final_reviewer_outcome}
- Reviewer notes: {st.session_state.reviewer_notes or "No reviewer notes yet."}

Audit trail:
{audit_lines}
"""


# ============================================================
# Header
# ============================================================
st.markdown(
    """
    <div class="hero">
        <div class="main-title">🛡️ Contestable AI Decision Interface</div>
        <p class="subtitle">
            A UI/UX-polished MVP showing how automated recommendations can become understandable, contestable,
            purpose-limited, and reviewable by humans. Built as a prototype for affected people and company reviewers.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# Sidebar inputs
# ============================================================
with st.sidebar:
    st.header("Case setup")

    country = st.selectbox(
        "Country / legal style",
        list(COUNTRY_TEMPLATES.keys()),
        help="This changes the wording, rights notice, timeline, and consent text.",
    )

    scenario = st.selectbox(
        "Decision scenario",
        list(DOMAIN_TEMPLATES.keys()),
    )

    st.divider()
    st.subheader("Simulated input data")

    capacity_indicator = st.slider(
        "Capacity indicator",
        500,
        10000,
        2600,
        step=100,
        help="For a loan this can represent income. For other domains, treat it as a general capacity/eligibility signal.",
    )

    burden_ratio = st.slider(
        "Burden or risk ratio",
        0.0,
        1.0,
        0.42,
        step=0.01,
        help="Higher values reduce the automated score.",
    )

    stable_activity_years = st.slider(
        "Years of stable activity",
        0,
        15,
        2,
        help="Work, education, platform, or relevant activity history depending on the domain.",
    )

    missing_docs = st.slider(
        "Missing or unclear documents",
        0,
        5,
        2,
    )

    relevant_history = st.slider(
        "Relevant history score",
        0,
        10,
        5,
    )

    sensitive_context = st.checkbox(
        "Sensitive context may require human review",
        value=True,
    )

    st.divider()
    if st.button("Start new simulated case", use_container_width=True):
        reset_case_state()


case_values = {
    "country": country,
    "scenario": scenario,
    "capacity_indicator": capacity_indicator,
    "burden_ratio": burden_ratio,
    "stable_activity_years": stable_activity_years,
    "missing_docs": missing_docs,
    "relevant_history": relevant_history,
    "sensitive_context": sensitive_context,
    "case_counter": st.session_state.case_counter,
}
case_signature = make_case_signature(case_values)
case_id = make_case_id(case_signature, st.session_state.case_counter)

if case_signature != st.session_state.last_case_signature:
    add_audit_event(f"Case inputs viewed or changed for {case_id}", actor="System")
    st.session_state.last_case_signature = case_signature


score, decision, status_class, uncertainty, factors, review_triggers, risk_level = compute_decision(
    capacity_indicator,
    burden_ratio,
    stable_activity_years,
    missing_docs,
    relevant_history,
    sensitive_context,
)

recommended_workflow = safer_workflow_recommendation(
    decision,
    missing_docs,
    uncertainty,
    review_triggers,
)

uncertainty_text, uncertainty_variant = uncertainty_label(uncertainty)
country_template = COUNTRY_TEMPLATES[country]
domain_template = DOMAIN_TEMPLATES[scenario]

factor_df = pd.DataFrame(
    {
        "Factor": list(factors.keys()),
        "Influence": list(factors.values()),
        "Plain-language meaning": [factor_explanation(k, v) for k, v in factors.items()],
        "Suggested correction route": [correction_hint(k, v, scenario) for k, v in factors.items()],
    }
).sort_values("Influence")


# ============================================================
# Top summary row
# ============================================================
top_cols = st.columns([1.15, 1, 1, 1])

with top_cols[0]:
    html_card(
        f"""
        <div class="kpi-label">Case ID</div>
        <div class="kpi-value">{case_id}</div>
        <div class="kpi-help">{country} · {scenario}</div>
        """,
        "compact-card",
    )

with top_cols[1]:
    html_card(
        f"""
        <div class="kpi-label">Recommendation</div>
        <div class="kpi-value" style="font-size:1.18rem;">{decision}</div>
        <div class="kpi-help">Not a final human decision</div>
        """,
        f"compact-card {status_class}",
    )

with top_cols[2]:
    html_card(
        f"""
        <div class="kpi-label">Uncertainty</div>
        <div class="kpi-value">{uncertainty:.0f}%</div>
        <div class="kpi-help">{uncertainty_text}</div>
        """,
        "compact-card status-info",
    )

with top_cols[3]:
    html_card(
        f"""
        <div class="kpi-label">Review risk</div>
        <div class="kpi-value">{risk_level}</div>
        <div class="kpi-help">Based on triggers and uncertainty</div>
        """,
        "compact-card",
    )


# ============================================================
# Tabs
# ============================================================
tab_user, tab_review, tab_audit, tab_research = st.tabs(
    [
        "👤 Affected-person portal",
        "🏢 Company review dashboard",
        "📋 Audit & export",
        "🔬 Research framing",
    ]
)


# ============================================================
# Affected-person portal
# ============================================================
with tab_user:
    left, right = st.columns([1.25, 0.85])

    with left:
        section_title(
            "Your decision notice",
            "This is the version an affected person would see. It avoids saying the AI made a final decision.",
        )

        decision_badge = "green" if decision == "Approve" else "amber" if decision == "Send to conditional review" else "red"
        html_card(
            f"""
            {badge(domain_template["decision_label"], "blue")}
            {badge(decision, decision_badge)}
            {badge(risk_level + " review risk", risk_badge_variant(risk_level))}
            <h3 style="margin:0.2rem 0 0.4rem 0;color:#111827;">Automated recommendation: {decision}</h3>
            <p class="small-text">
                This is an automated recommendation, not the end of the process. You may request human review,
                correct information, or submit evidence if something is missing or misunderstood.
            </p>
            <div class="divider-soft"></div>
            <div class="small-text"><strong>Country template:</strong> {country}</div>
            <div class="small-text"><strong>Expected route:</strong> {country_template["timeline"]}</div>
            """,
            f"decision-card {status_class}",
        )

        st.progress(int(score), text=f"Automated score: {score:.1f}/100")
        st.progress(int(uncertainty), text=f"Estimated uncertainty: {uncertainty:.1f}%")

        section_title("Why review may be needed")
        if review_triggers:
            for idx, trigger in enumerate(review_triggers, start=1):
                html_card(
                    f"""
                    <span class="step-number">{idx}</span>
                    <strong>{trigger}</strong>
                    """,
                    "callout",
                )
        else:
            html_card(
                "No automatic human-review trigger was detected, but you can still request review if you believe the decision is wrong.",
                "callout",
            )

        html_card(
            f"""
            <strong>Recommended safer workflow:</strong><br>
            {recommended_workflow}
            """,
            "callout",
        )

    with right:
        section_title("Your rights and options")
        html_card(
            f"""
            {badge(country, "purple")}
            <p><strong>Plain-language notice</strong></p>
            <p class="small-text">{country_template["language_note"]}</p>
            <div class="divider-soft"></div>
            <p><strong>What you can do</strong></p>
            <p class="small-text">{country_template["rights_text"]}</p>
            """,
            "card",
        )

        html_card(
            f"""
            <p><strong>Evidence examples for this case</strong></p>
            <p class="small-text">{domain_template["evidence_examples"]}</p>
            """,
            "card",
        )

    section_title(
        "Plain-language factor explanation",
        "The mobile-friendly card layout is used instead of only showing a table.",
    )

    for _, row in factor_df.iterrows():
        value = float(row["Influence"])
        if value > 2:
            score_class = "factor-score-pos"
            sign = "+"
        elif value < -2:
            score_class = "factor-score-neg"
            sign = ""
        else:
            score_class = "factor-score-neu"
            sign = ""

        html_card(
            f"""
            <div class="factor-head">
                <div class="factor-name">{row["Factor"]}</div>
                <div class="{score_class}">{sign}{value:.1f}</div>
            </div>
            <div class="factor-text">{row["Plain-language meaning"]}</div>
            <div class="divider-soft"></div>
            <div class="factor-text"><strong>Possible action:</strong> {row["Suggested correction route"]}</div>
            """,
            "factor-card",
        )

    with st.expander("Show detailed factor table"):
        st.dataframe(factor_df, use_container_width=True, hide_index=True)

    section_title(
        "Contest or request review",
        "The form guides the person to challenge specific issues rather than writing a vague appeal.",
    )

    with st.form("contest_form", clear_on_submit=False):
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
            default=["Important document is missing"] if missing_docs >= 2 else [],
        )

        explanation = st.text_area(
            "Explain your challenge",
            placeholder="Example: My current information is higher than shown, and one document was missing.",
            height=120,
        )

        uploaded_file = st.file_uploader(
            "Upload optional evidence",
            type=["pdf", "png", "jpg", "jpeg", "docx"],
            help="In a full SaaS version, this would be stored securely with access control.",
        )

        review_path_options = [
            "Fast human review",
            "Correct data and rerun recommendation",
            "Full appeal review",
            "Request explanation only",
        ]

        suggested_index = 0
        if missing_docs >= 2:
            suggested_index = 1
        elif decision == "Do not approve automatically":
            suggested_index = 2

        review_path = st.radio(
            "Choose review path",
            review_path_options,
            index=suggested_index,
        )

        consent = st.checkbox(country_template["consent"])

        submitted = st.form_submit_button("Submit review request", use_container_width=True)

    if submitted:
        if not reasons:
            st.error("Please select at least one reason for requesting review.")
        elif not consent:
            st.error("Please give purpose-limited consent before submitting.")
        else:
            st.session_state.contestation_submitted = True
            st.session_state.review_status = "Submitted"
            st.session_state.contest_receipt = {
                "case_id": case_id,
                "submitted_at": now_str(),
                "original_recommendation": decision,
                "review_path": review_path,
                "selected_reasons": reasons,
                "user_explanation": explanation,
                "uploaded_evidence": uploaded_file.name if uploaded_file is not None else None,
                "purpose_limitation": country_template["consent"],
            }
            add_audit_event("Review request submitted by affected person", actor=domain_template["affected_person"])
            st.success("Review request submitted successfully.")

    if st.session_state.contest_receipt:
        section_title("Review request receipt")
        receipt = st.session_state.contest_receipt
        html_card(
            f"""
            {badge("Submitted", "green")}
            <p><strong>Case:</strong> {receipt["case_id"]}</p>
            <p><strong>Original recommendation:</strong> {receipt["original_recommendation"]}</p>
            <p><strong>Review path:</strong> {receipt["review_path"]}</p>
            <p><strong>Submitted:</strong> {receipt["submitted_at"]}</p>
            <p class="small-text"><strong>Purpose limitation:</strong> {receipt["purpose_limitation"]}</p>
            """,
            "card status-approved",
        )


# ============================================================
# Company reviewer dashboard
# ============================================================
with tab_review:
    section_title(
        "Company review dashboard",
        "This is the internal side used by the company team that pays for the product.",
    )

    review_cols = st.columns([1, 1, 1])

    with review_cols[0]:
        html_card(
            f"""
            <div class="kpi-label">Assigned team</div>
            <div class="kpi-value" style="font-size:1.15rem;">{domain_template["company_team"]}</div>
            <div class="kpi-help">Role-based reviewer queue in full SaaS</div>
            """,
            "compact-card",
        )

    with review_cols[1]:
        html_card(
            f"""
            <div class="kpi-label">Review status</div>
            <div class="kpi-value" style="font-size:1.15rem;">{st.session_state.review_status}</div>
            <div class="kpi-help">Changes after user submission</div>
            """,
            "compact-card status-info",
        )

    with review_cols[2]:
        html_card(
            f"""
            <div class="kpi-label">Suggested action</div>
            <div class="kpi-value" style="font-size:1.02rem;">{recommended_workflow}</div>
            <div class="kpi-help">Generated from triggers</div>
            """,
            "compact-card",
        )

    left, right = st.columns([1.1, 0.9])

    with left:
        section_title("Case triage")
        trigger_text = "<br>".join(f"• {trigger}" for trigger in review_triggers) if review_triggers else "No automatic trigger detected."
        html_card(
            f"""
            <p><strong>Case ID:</strong> {case_id}</p>
            <p><strong>Scenario:</strong> {scenario}</p>
            <p><strong>Automated recommendation:</strong> {decision}</p>
            <p><strong>Score:</strong> {score:.1f}/100</p>
            <p><strong>Uncertainty:</strong> {uncertainty:.1f}%</p>
            <p><strong>Review risk:</strong> {risk_level}</p>
            <div class="divider-soft"></div>
            <p><strong>Review triggers</strong></p>
            <p class="small-text">{trigger_text}</p>
            """,
            "card",
        )

        if st.session_state.contest_receipt:
            section_title("Affected-person submission")
            receipt = st.session_state.contest_receipt
            st.json(receipt)
        else:
            st.info("No review request has been submitted yet.")

    with right:
        section_title("Reviewer action")
        with st.form("reviewer_form"):
            new_status = st.selectbox(
                "Review status",
                [
                    "Not submitted",
                    "Submitted",
                    "In human review",
                    "Waiting for more evidence",
                    "Resolved",
                ],
                index=[
                    "Not submitted",
                    "Submitted",
                    "In human review",
                    "Waiting for more evidence",
                    "Resolved",
                ].index(st.session_state.review_status)
                if st.session_state.review_status
                in [
                    "Not submitted",
                    "Submitted",
                    "In human review",
                    "Waiting for more evidence",
                    "Resolved",
                ]
                else 0,
            )

            outcome = st.selectbox(
                "Final reviewer outcome",
                [
                    "Pending",
                    "Original recommendation upheld",
                    "Recommendation changed",
                    "More information required",
                    "Escalated to senior reviewer",
                ],
                index=[
                    "Pending",
                    "Original recommendation upheld",
                    "Recommendation changed",
                    "More information required",
                    "Escalated to senior reviewer",
                ].index(st.session_state.final_reviewer_outcome)
                if st.session_state.final_reviewer_outcome
                in [
                    "Pending",
                    "Original recommendation upheld",
                    "Recommendation changed",
                    "More information required",
                    "Escalated to senior reviewer",
                ]
                else 0,
            )

            notes = st.text_area(
                "Reviewer notes",
                value=st.session_state.reviewer_notes,
                height=150,
                placeholder="Write what was checked, what evidence was considered, and why the final decision is justified.",
            )

            reviewer_submitted = st.form_submit_button("Save reviewer update", use_container_width=True)

        if reviewer_submitted:
            st.session_state.review_status = new_status
            st.session_state.final_reviewer_outcome = outcome
            st.session_state.reviewer_notes = notes
            add_audit_event(f"Reviewer updated status to '{new_status}' and outcome to '{outcome}'", actor="Company reviewer")
            st.success("Reviewer update saved.")

    section_title("Traditional notice vs contestable workflow")
    c1, c2 = st.columns(2)

    with c1:
        html_card(
            """
            <h4 style="margin-top:0;color:#111827;">Traditional automated notice</h4>
            <p class="small-text">
            • Shows only a decision<br>
            • Gives vague reasons<br>
            • Provides generic appeal route<br>
            • User may not know what to challenge<br>
            • Organization gets unstructured complaints
            </p>
            """,
            "card status-rejected",
        )

    with c2:
        html_card(
            """
            <h4 style="margin-top:0;color:#111827;">Contestable workflow</h4>
            <p class="small-text">
            • Shows recommendation, uncertainty, and triggers<br>
            • Explains factors in plain language<br>
            • Guides focused evidence submission<br>
            • Routes the case to human review<br>
            • Creates an audit-ready record
            </p>
            """,
            "card status-approved",
        )


# ============================================================
# Audit and export
# ============================================================
with tab_audit:
    section_title(
        "Audit trail",
        "Every important step should be recorded. In a full SaaS version this must be immutable or tamper-evident.",
    )

    if st.session_state.audit_log:
        audit_df = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(audit_df, use_container_width=True, hide_index=True)

        section_title("Timeline view")
        for row in reversed(st.session_state.audit_log[-8:]):
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">{row["Time"]} · {row["Actor"]}</div>
                    <div class="timeline-event">{row["Event"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No audit events yet.")

    report_text = build_report(
        case_id,
        country,
        scenario,
        score,
        decision,
        uncertainty,
        risk_level,
        recommended_workflow,
        factors,
        review_triggers,
    )

    export_cols = st.columns(2)
    with export_cols[0]:
        st.download_button(
            "Download case report (.txt)",
            data=report_text,
            file_name=f"{case_id}_contestable_ai_report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with export_cols[1]:
        audit_json = json.dumps(st.session_state.audit_log, indent=2, ensure_ascii=False)
        st.download_button(
            "Download audit log (.json)",
            data=audit_json,
            file_name=f"{case_id}_audit_log.json",
            mime="application/json",
            use_container_width=True,
        )

    with st.expander("Preview case report"):
        st.text(report_text)


# ============================================================
# Research framing
# ============================================================
with tab_research:
    section_title("Research contribution")
    html_card(
        """
        <p>
        This MVP demonstrates <strong>actionable contestability</strong>. The affected person does not only receive
        an automated recommendation. They receive a plain-language explanation, uncertainty information, review triggers,
        a safer workflow recommendation, and a structured way to challenge the decision.
        </p>
        <p class="small-text">
        The central design shift is from transparency alone to procedural empowerment: the interface makes the safe and fair
        path easier than a vague appeal process.
        </p>
        """,
        "card",
    )

    section_title("Suggested user study")
    html_card(
        """
        <p><strong>Study design:</strong> Compare this interface against a standard automated rejection notice.</p>
        <p class="small-text">
        Measure whether users can understand the decision, identify possible errors, choose an appropriate review path,
        avoid unnecessary data sharing, and feel that the process is fair.
        </p>
        <div class="divider-soft"></div>
        <p><strong>Possible outcome measures</strong></p>
        <p class="small-text">
        • Decision comprehension<br>
        • Error identification accuracy<br>
        • Correct review-path selection<br>
        • Data minimization behavior<br>
        • Perceived procedural fairness<br>
        • Trust calibration<br>
        • Appeal quality
        </p>
        """,
        "card",
    )

    section_title("How this would become a real SaaS")
    html_card(
        """
        <p><strong>Next.js frontend</strong> for the public portal and company dashboard.</p>
        <p><strong>FastAPI or Django backend</strong> for case creation, review workflow, and API integrations.</p>
        <p><strong>PostgreSQL</strong> for companies, users, decision cases, appeals, audit logs, templates, and subscriptions.</p>
        <p><strong>S3/Supabase Storage</strong> for encrypted evidence files.</p>
        <p><strong>Auth0/Clerk/Supabase Auth</strong> for company login, reviewer roles, and secure access.</p>
        <p><strong>Stripe</strong> for company subscriptions.</p>
        """,
        "card",
    )

    section_title("UI/UX corrections made in this version")
    html_card(
        """
        <p class="small-text">
        • Replaced one long page with tabbed navigation<br>
        • Replaced pale low-contrast cards with higher-contrast cards<br>
        • Changed “Decision: Rejected” into “Automated recommendation” wording<br>
        • Added mobile-friendly factor cards instead of relying only on a table<br>
        • Added top summary cards for faster scanning<br>
        • Added country-aware wording and consent text<br>
        • Separated affected-person portal from company reviewer dashboard<br>
        • Added reviewer status, notes, and outcome fields<br>
        • Added report and audit-log downloads<br>
        • Added reset/new-case flow
        </p>
        """,
        "card status-info",
    )
