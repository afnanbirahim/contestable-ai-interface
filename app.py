# contestable_ai_final_mobile_saas.py
# Contestable AI Decision Interface
# Mobile-safe Streamlit MVP with SaaS-oriented upgrades
# Run locally with: streamlit run contestable_ai_final_mobile_saas.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
import json
from typing import Any

import pandas as pd
import streamlit as st


# =========================================================
# Page setup
# =========================================================
st.set_page_config(
    page_title="Contestable AI Decision Interface",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# =========================================================
# Mobile-first CSS
# Important design decision:
# - No selectbox/dropdown is used anywhere, because mobile Streamlit dropdowns
#   can become unreadable in browser dark mode.
# - No st.tabs() is used, because tab labels can become low contrast on phones.
# - No custom HTML progress bar is used, because malformed/nested HTML can render
#   black blocks on mobile.
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #f8fafc;
        --panel: #ffffff;
        --text: #0f172a;
        --muted: #475569;
        --soft: #64748b;
        --line: #dbe3ef;
        --blue: #2563eb;
        --blue-soft: #eff6ff;
        --red: #dc2626;
        --red-soft: #fef2f2;
        --orange: #ea580c;
        --orange-soft: #fff7ed;
        --green: #16a34a;
        --green-soft: #f0fdf4;
        --purple: #7c3aed;
        --purple-soft: #f5f3ff;
        --shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
        --radius: 24px;
    }

    /* Force readable light surface even when the phone/browser is in dark mode. */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"], header {
        background: transparent !important;
    }

    [data-testid="stToolbar"], #MainMenu, footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    .block-container {
        max-width: 920px !important;
        padding-top: 1.2rem !important;
        padding-left: 1.05rem !important;
        padding-right: 1.05rem !important;
        padding-bottom: 5rem !important;
    }

    h1, h2, h3, h4, h5, h6,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    label, [data-testid="stWidgetLabel"] p {
        color: var(--text) !important;
    }

    h1 {
        font-size: 2.2rem !important;
        line-height: 1.1 !important;
        letter-spacing: -0.04em !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.55rem !important;
        line-height: 1.18 !important;
        letter-spacing: -0.035em !important;
        margin-top: 1.3rem !important;
        margin-bottom: 0.9rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
        letter-spacing: -0.02em !important;
    }

    p, li {
        font-size: 1.03rem !important;
        line-height: 1.75 !important;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 60%, #3b82f6 100%);
        border-radius: 28px;
        color: white !important;
        padding: 1.35rem;
        margin: 0.5rem 0 1.1rem 0;
        box-shadow: var(--shadow);
    }

    .hero * {
        color: white !important;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1.08;
        margin-bottom: 0.65rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        line-height: 1.65;
        opacity: 0.94;
        margin-bottom: 1rem;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 0.5rem;
    }

    .chip {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.45rem 0.75rem;
        font-size: 0.84rem;
        font-weight: 800;
        border: 1px solid rgba(255,255,255,0.28);
        background: rgba(255,255,255,0.12);
        white-space: nowrap;
    }

    .section-label {
        color: var(--blue) !important;
        font-size: 0.88rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 900;
        margin: 1.4rem 0 0.55rem 0;
    }

    .ui-card {
        background: var(--panel);
        border: 1px solid var(--line);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        padding: 1.2rem;
        margin: 0.8rem 0;
        overflow-wrap: anywhere;
        color: var(--text) !important;
    }

    .ui-card * {
        color: inherit;
    }

    .card-red { background: var(--red-soft); border-color: #fecaca; border-left: 8px solid var(--red); }
    .card-blue { background: var(--blue-soft); border-color: #bfdbfe; border-left: 8px solid var(--blue); }
    .card-orange { background: var(--orange-soft); border-color: #fed7aa; border-left: 8px solid var(--orange); }
    .card-green { background: var(--green-soft); border-color: #bbf7d0; border-left: 8px solid var(--green); }
    .card-purple { background: var(--purple-soft); border-color: #ddd6fe; border-left: 8px solid var(--purple); }
    .card-white { background: #ffffff; border-color: var(--line); border-left: 8px solid #cbd5e1; }

    .card-eyebrow {
        color: var(--soft) !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 900;
        margin-bottom: 0.65rem;
    }

    .card-title {
        color: var(--text) !important;
        font-size: 1.65rem;
        line-height: 1.15;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 0.7rem;
    }

    .card-body {
        color: var(--text) !important;
        font-size: 1.03rem;
        line-height: 1.75;
    }

    .muted {
        color: var(--muted) !important;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 0.75rem 0 1rem 0;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.06);
    }

    .metric-kicker {
        color: var(--soft) !important;
        text-transform: uppercase;
        font-weight: 900;
        letter-spacing: 0.1em;
        font-size: 0.72rem;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        color: var(--text) !important;
        font-weight: 950;
        font-size: 1.45rem;
        letter-spacing: -0.04em;
        line-height: 1.1;
    }

    .metric-note {
        color: var(--muted) !important;
        font-size: 0.86rem;
        margin-top: 0.35rem;
        line-height: 1.45;
    }

    /* Radio as visible mobile navigation instead of tabs/selectboxes. */
    div[role="radiogroup"] {
        gap: 0.5rem !important;
    }

    div[role="radiogroup"] label {
        background: #ffffff !important;
        border: 1px solid var(--line) !important;
        border-radius: 16px !important;
        padding: 0.7rem 0.85rem !important;
        margin-bottom: 0.45rem !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
    }

    div[role="radiogroup"] label p {
        color: var(--text) !important;
        font-weight: 750 !important;
        line-height: 1.25 !important;
    }

    /* Keep all inputs readable on phones/dark-mode browsers. */
    input, textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea {
        background: #ffffff !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        border-color: var(--line) !important;
        caret-color: var(--blue) !important;
    }

    textarea::placeholder, input::placeholder {
        color: #64748b !important;
        -webkit-text-fill-color: #64748b !important;
        opacity: 1 !important;
    }

    /* Streamlit generated components often inherit dark theme from browser. */
    .stCheckbox label p,
    .stSlider label p,
    .stFileUploader label p,
    .stDownloadButton,
    .stButton,
    .stFormSubmitButton,
    .stRadio label p {
        color: var(--text) !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        width: 100%;
        min-height: 3rem;
        border-radius: 16px !important;
        border: 1px solid #1d4ed8 !important;
        background: #2563eb !important;
        color: white !important;
        font-weight: 850 !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.22) !important;
    }

    .stButton > button * ,
    .stDownloadButton > button * ,
    .stFormSubmitButton > button * {
        color: white !important;
    }

    [data-testid="stFileUploader"] section {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px dashed #94a3b8 !important;
        border-radius: 18px !important;
    }

    [data-testid="stFileUploader"] section * {
        color: var(--text) !important;
    }

    /* Avoid black dataframe/table surfaces. */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background: #ffffff !important;
        color: var(--text) !important;
    }

    /* Native Streamlit alerts are not used much, but keep them readable. */
    [data-testid="stAlert"] {
        color: var(--text) !important;
        background: #ffffff !important;
        border: 1px solid var(--line) !important;
    }

    [data-testid="stAlert"] * {
        color: var(--text) !important;
    }

    .fine-print {
        color: var(--muted) !important;
        font-size: 0.88rem !important;
        line-height: 1.6 !important;
    }

    .divider {
        height: 1px;
        background: var(--line);
        margin: 1.2rem 0;
    }

    @media (max-width: 740px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }
        .hero {
            border-radius: 22px;
            padding: 1rem;
        }
        .hero-title {
            font-size: 1.55rem;
        }
        .hero-subtitle {
            font-size: 0.98rem;
        }
        .metric-grid {
            grid-template-columns: 1fr;
            gap: 0.6rem;
        }
        .ui-card {
            border-radius: 22px;
            padding: 1rem;
        }
        .card-title {
            font-size: 1.35rem;
        }
        .card-body {
            font-size: 0.99rem;
            line-height: 1.7;
        }
        h1 {
            font-size: 1.75rem !important;
        }
        h2 {
            font-size: 1.3rem !important;
        }
        p, li {
            font-size: 0.99rem !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Data structures and configuration
# =========================================================
@dataclass(frozen=True)
class LegalTemplate:
    title: str
    plain_notice: str
    consent_text: str
    appeal_timeline: str
    reviewer_note: str


LEGAL_TEMPLATES: dict[str, LegalTemplate] = {
    "Bangladesh": LegalTemplate(
        title="Bangladesh pilot notice",
        plain_notice=(
            "This notice uses plain-language review wording suitable for a Bangladesh pilot. "
            "The affected person may request human review, correct data, and submit relevant evidence for this case only."
        ),
        consent_text=(
            "I consent to share only the selected information for this specific review request."
        ),
        appeal_timeline="Suggested pilot timeline: acknowledge within 2 working days, review within 7 working days.",
        reviewer_note="Use plain Bangla/English explanation, avoid final legal language, and record reviewer reasoning.",
    ),
    "EU / UK": LegalTemplate(
        title="EU / UK rights-aware notice",
        plain_notice=(
            "This notice is framed for automated-decision contestability. It explains the recommendation, "
            "shows uncertainty, provides a route to meaningful human review, and records purpose-limited consent."
        ),
        consent_text=(
            "I consent to use the selected information only for this specific human review and data-correction request."
        ),
        appeal_timeline="Suggested compliance timeline: show acknowledgement immediately and route significant cases to human review.",
        reviewer_note="Record meaningful human intervention, not merely a rubber-stamp review.",
    ),
    "United States": LegalTemplate(
        title="US sector-aware notice",
        plain_notice=(
            "This notice is suitable for a US-style pilot where sector rules may vary. It emphasizes adverse-action clarity, "
            "error correction, fairness review, and documented escalation."
        ),
        consent_text="I consent to use the selected information only to review this case and correct possible errors.",
        appeal_timeline="Suggested operational timeline: acknowledge immediately and define review SLA by sector.",
        reviewer_note="Keep sector-specific wording separate for lending, hiring, insurance, and platform decisions.",
    ),
    "India": LegalTemplate(
        title="India digital-service notice",
        plain_notice=(
            "This notice is designed for digital lending, hiring, education, platform moderation, or service eligibility workflows. "
            "It keeps the explanation clear and gives a structured correction/review path."
        ),
        consent_text="I consent to use the selected information only for this case-specific review request.",
        appeal_timeline="Suggested pilot timeline: acknowledge within 48 hours and route high-impact cases to a reviewer.",
        reviewer_note="Use a simple multilingual explanation and keep consent tied to a narrow review purpose.",
    ),
    "Generic global": LegalTemplate(
        title="Generic global notice",
        plain_notice=(
            "This notice gives an affected person a clear explanation, uncertainty information, review triggers, "
            "and a structured way to contest an automated recommendation."
        ),
        consent_text="I consent to use the selected information only for this review request.",
        appeal_timeline="Suggested timeline: acknowledge immediately and review based on risk level.",
        reviewer_note="Adapt legal wording before production deployment in a specific jurisdiction.",
    ),
}

DOMAIN_GUIDANCE: dict[str, dict[str, str]] = {
    "Loan application": {
        "affected_person": "applicant",
        "decision_label": "approval recommendation",
        "evidence": "income statement, updated employment proof, debt correction, missing KYC document",
    },
    "Hiring shortlist": {
        "affected_person": "candidate",
        "decision_label": "shortlist recommendation",
        "evidence": "updated CV, certificate, portfolio, missing experience proof, correction of screening data",
    },
    "Insurance claim": {
        "affected_person": "claimant",
        "decision_label": "claim recommendation",
        "evidence": "medical or incident documents, policy clarification, photos, missing claim evidence",
    },
    "University admission": {
        "affected_person": "student/applicant",
        "decision_label": "admission recommendation",
        "evidence": "transcript, recommendation, corrected score, special-context document",
    },
    "Platform account restriction": {
        "affected_person": "platform user",
        "decision_label": "account restriction recommendation",
        "evidence": "identity proof, activity explanation, moderation-context correction, transaction evidence",
    },
    "NGO beneficiary selection": {
        "affected_person": "beneficiary/applicant",
        "decision_label": "eligibility recommendation",
        "evidence": "household information, income proof, location proof, vulnerability documentation",
    },
}

PRICING_PLANS = pd.DataFrame(
    [
        {
            "Plan": "Pilot",
            "Monthly price": "$99",
            "Best for": "1 small team",
            "Included cases": "250/month",
            "Key value": "Hosted appeal portal + audit export",
        },
        {
            "Plan": "Growth",
            "Monthly price": "$399",
            "Best for": "Fintech/HR startup",
            "Included cases": "1,500/month",
            "Key value": "Reviewer dashboard + templates + reports",
        },
        {
            "Plan": "Compliance",
            "Monthly price": "$999+",
            "Best for": "NBFI/insurer/platform",
            "Included cases": "5,000+/month",
            "Key value": "API, role controls, custom branding, SLA",
        },
        {
            "Plan": "Enterprise",
            "Monthly price": "Custom",
            "Best for": "Bank/public-sector/large platform",
            "Included cases": "Custom",
            "Key value": "SSO, data residency, legal templates, security review",
        },
    ]
)


# =========================================================
# Session state
# =========================================================
def init_state() -> None:
    defaults: dict[str, Any] = {
        "audit_log": [],
        "case_counter": 1,
        "appeal_submitted": False,
        "appeal_reasons": [],
        "appeal_text": "",
        "appeal_path": "Fast human review",
        "review_status": "Waiting for reviewer",
        "review_outcome": "Not reviewed yet",
        "reviewer_notes": "",
        "last_case_key": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# =========================================================
# Helper functions
# =========================================================
def safe_text(value: Any) -> str:
    return escape(str(value), quote=True)


def add_audit_event(event: str) -> None:
    st.session_state.audit_log.append(
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Event": event}
    )


def ui_card(title: str, body: str, tone: str = "white", eyebrow: str | None = None) -> None:
    tone_class = {
        "red": "card-red",
        "blue": "card-blue",
        "orange": "card-orange",
        "green": "card-green",
        "purple": "card-purple",
        "white": "card-white",
    }.get(tone, "card-white")

    eyebrow_html = ""
    if eyebrow:
        eyebrow_html = f'<div class="card-eyebrow">{safe_text(eyebrow)}</div>'

    body_html = safe_text(body).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="ui-card {tone_class}">
            {eyebrow_html}
            <div class="card-title">{safe_text(title)}</div>
            <div class="card-body">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_grid(items: list[tuple[str, str, str]]) -> None:
    cards = []
    for kicker, value, note in items:
        cards.append(
            f"""
            <div class="metric-card">
                <div class="metric-kicker">{safe_text(kicker)}</div>
                <div class="metric-value">{safe_text(value)}</div>
                <div class="metric-note">{safe_text(note)}</div>
            </div>
            """
        )
    st.markdown(f'<div class="metric-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def compute_decision(
    income: int,
    debt_ratio: float,
    employment_years: int,
    missing_docs: int,
    relevant_history: int,
    sensitive_context: bool,
) -> dict[str, Any]:
    """Transparent simulated model for the MVP. Not a real credit/hiring/insurance model."""
    score = 50.0
    score += min(income / 2000, 20)
    score -= debt_ratio * 35
    score += min(employment_years * 3, 15)
    score += relevant_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        recommendation = "Approve automatically"
        tone = "green"
        plain = "The automated system indicates approval. A human review path remains available if the affected person wants clarification."
    elif score >= 55:
        recommendation = "Send to conditional review"
        tone = "orange"
        plain = "The automated system is not confident enough for a final automatic decision. Extra information or human review is appropriate."
    else:
        recommendation = "Do not approve automatically"
        tone = "red"
        plain = "The automated system does not recommend automatic approval. This is not a final human decision."

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Income / capacity": min(income / 2000, 20),
        "Debt or burden ratio": -debt_ratio * 35,
        "Stable work/activity": min(employment_years * 3, 15),
        "Relevant history": relevant_history * 1.5,
        "Missing or unclear documents": -missing_docs * 8,
    }

    triggers: list[str] = []
    if uncertainty >= 60:
        triggers.append("The uncertainty level is high enough that automatic processing may be unsafe.")
    if missing_docs >= 2:
        triggers.append("Important documents may be missing, so the recommendation may be based on incomplete information.")
    if sensitive_context:
        triggers.append("The case includes sensitive context and should be checked by a human reviewer.")
    if recommendation == "Do not approve automatically" and score >= 45:
        triggers.append("The case is close enough to the boundary that a small data correction could change the outcome.")
    if not triggers:
        triggers.append("No mandatory trigger was detected, but the affected person may still ask for review or clarification.")

    if missing_docs >= 2:
        workflow = "Request missing or clearer documents before any final decision."
    elif uncertainty >= 60:
        workflow = "Route the case to fast human review before finalizing the outcome."
    elif recommendation == "Do not approve automatically":
        workflow = "Offer structured appeal, data correction, and evidence upload before final rejection."
    elif recommendation == "Send to conditional review":
        workflow = "Ask for limited extra evidence and assign a reviewer."
    else:
        workflow = "Proceed, but keep explanation, audit trail, and optional review access."

    risk_score = 0
    risk_score += 2 if uncertainty >= 60 else 1 if uncertainty >= 40 else 0
    risk_score += 2 if missing_docs >= 2 else 0
    risk_score += 2 if sensitive_context else 0
    risk_score += 1 if recommendation != "Approve automatically" else 0
    risk_level = "High" if risk_score >= 5 else "Elevated" if risk_score >= 3 else "Low"

    return {
        "score": score,
        "recommendation": recommendation,
        "tone": tone,
        "plain": plain,
        "uncertainty": uncertainty,
        "factors": factors,
        "triggers": triggers,
        "workflow": workflow,
        "risk_level": risk_level,
    }


def factor_explanation(factor: str, value: float) -> str:
    if factor == "Income / capacity":
        if value >= 15:
            return "Income or capacity information strongly supported the case."
        if value >= 8:
            return "Income or capacity information gave moderate support."
        return "Income or capacity information gave limited support."
    if factor == "Debt or burden ratio":
        if value <= -25:
            return "The burden ratio strongly reduced the recommendation score."
        if value <= -10:
            return "The burden ratio moderately reduced the recommendation score."
        return "The burden ratio had only a limited negative effect."
    if factor == "Stable work/activity":
        if value >= 12:
            return "Stable work or activity history improved confidence strongly."
        if value >= 6:
            return "Stable work or activity history gave moderate support."
        return "Stable work or activity history gave limited support."
    if factor == "Relevant history":
        if value >= 12:
            return "Relevant history strongly supported the case."
        if value >= 6:
            return "Relevant history gave moderate support."
        return "Relevant history gave limited support."
    if factor == "Missing or unclear documents":
        if value <= -24:
            return "Missing or unclear documents strongly reduced confidence."
        if value < 0:
            return "Missing or unclear documents reduced confidence."
        return "No missing document penalty was applied."
    return "This factor influenced the recommendation."


def build_case_report(case: dict[str, Any]) -> str:
    factors = case["decision"]["factors"]
    factor_lines = "\n".join(
        f"- {name}: {value:.2f} | {factor_explanation(name, value)}"
        for name, value in factors.items()
    )
    trigger_lines = "\n".join(f"- {item}" for item in case["decision"]["triggers"])
    appeal_lines = "\n".join(f"- {item}" for item in st.session_state.appeal_reasons) or "- No appeal submitted"
    audit_lines = "\n".join(
        f"- {row['Time']}: {row['Event']}" for row in st.session_state.audit_log
    ) or "- No audit events"

    return f"""# Contestable AI Case Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Case ID: {case['case_id']}
Country template: {case['country']}
Scenario: {case['scenario']}

## Automated Recommendation
Recommendation: {case['decision']['recommendation']}
Score: {case['decision']['score']:.1f}/100
Uncertainty: {case['decision']['uncertainty']:.1f}%
Review risk: {case['decision']['risk_level']}

Important notice: this is not a final human decision.

## Plain-language Notice
{case['decision']['plain']}

## Safer Workflow
{case['decision']['workflow']}

## Review Triggers
{trigger_lines}

## Factor Explanations
{factor_lines}

## Appeal / Contestation
Submitted: {st.session_state.appeal_submitted}
Review path: {st.session_state.appeal_path}
Reasons:
{appeal_lines}
Explanation:
{st.session_state.appeal_text or 'No explanation submitted'}

## Reviewer Status
Status: {st.session_state.review_status}
Outcome: {st.session_state.review_outcome}
Reviewer notes: {st.session_state.reviewer_notes or 'No reviewer notes yet'}

## Audit Trail
{audit_lines}

## SaaS Note
Production deployment should include authentication, tenant isolation, encrypted evidence storage, legal-template review, API access, role-based permissions, and data-retention settings.
"""


def download_json(label: str, obj: dict[str, Any], file_name: str) -> None:
    st.download_button(
        label,
        data=json.dumps(obj, indent=2, ensure_ascii=False),
        file_name=file_name,
        mime="application/json",
    )


def download_markdown(label: str, text: str, file_name: str) -> None:
    st.download_button(label, data=text, file_name=file_name, mime="text/markdown")


# =========================================================
# Header
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">Contestable AI Decision Interface</div>
        <div class="hero-subtitle">
            A mobile-safe MVP for explaining automated recommendations, routing human review,
            collecting evidence, recording consent, and producing audit-ready case reports.
        </div>
        <div class="chip-row">
            <span class="chip">Affected-person portal</span>
            <span class="chip">Human review</span>
            <span class="chip">Evidence upload</span>
            <span class="chip">Audit trail</span>
            <span class="chip">B2B SaaS-ready</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Configuration
# =========================================================
st.markdown('<div class="section-label">Configure demo case</div>', unsafe_allow_html=True)

country = st.radio(
    "Country / legal template",
    list(LEGAL_TEMPLATES.keys()),
    index=0,
)

scenario = st.radio(
    "Decision scenario",
    list(DOMAIN_GUIDANCE.keys()),
    index=0,
)

income = st.slider("Income / capacity indicator", 500, 10000, 2600, step=100)
debt_ratio = st.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
employment_years = st.slider("Years of stable work/activity", 0, 15, 2)
missing_docs = st.slider("Missing or unclear documents", 0, 5, 2)
relevant_history = st.slider("Relevant history score", 0, 10, 5)
sensitive_context = st.checkbox("Sensitive context may require human review", value=True)

case_key = f"{country}|{scenario}|{income}|{debt_ratio}|{employment_years}|{missing_docs}|{relevant_history}|{sensitive_context}"
if st.session_state.last_case_key != case_key:
    st.session_state.last_case_key = case_key
    add_audit_event("Case configuration viewed or changed")

legal = LEGAL_TEMPLATES[country]
domain = DOMAIN_GUIDANCE[scenario]
decision = compute_decision(
    income,
    debt_ratio,
    employment_years,
    missing_docs,
    relevant_history,
    sensitive_context,
)

case_id = f"CAI-{datetime.now().strftime('%Y%m%d')}-{st.session_state.case_counter:04d}"
case = {
    "case_id": case_id,
    "country": country,
    "scenario": scenario,
    "legal_template": legal.title,
    "affected_person_type": domain["affected_person"],
    "decision_label": domain["decision_label"],
    "evidence_guidance": domain["evidence"],
    "inputs": {
        "income_capacity": income,
        "debt_burden_ratio": debt_ratio,
        "stable_work_activity_years": employment_years,
        "missing_unclear_documents": missing_docs,
        "relevant_history_score": relevant_history,
        "sensitive_context": sensitive_context,
    },
    "decision": decision,
}

# =========================================================
# Top summary
# =========================================================
st.markdown('<div class="section-label">Case summary</div>', unsafe_allow_html=True)
metric_grid(
    [
        ("Recommendation", decision["recommendation"], "Automated recommendation only"),
        ("Uncertainty", f"{decision['uncertainty']:.0f}%", "Used to decide review caution"),
        ("Review risk", decision["risk_level"], "Based on uncertainty, missing data, and context"),
    ]
)

# Native progress bars are used to avoid black custom-HTML progress bugs.
st.write("Recommendation score")
st.progress(int(decision["score"]))
st.write("Uncertainty level")
st.progress(int(decision["uncertainty"]))


# =========================================================
# Main navigation: radio, not tabs/selectbox
# =========================================================
st.markdown('<div class="section-label">Choose workspace view</div>', unsafe_allow_html=True)
view = st.radio(
    "View",
    [
        "Affected-person portal",
        "Explanation and appeal",
        "Human reviewer dashboard",
        "SaaS admin and pricing",
        "Audit and exports",
        "Research framing",
    ],
    index=0,
)


# =========================================================
# View 1: Affected-person portal
# =========================================================
if view == "Affected-person portal":
    st.markdown('<div class="section-label">Affected-person view</div>', unsafe_allow_html=True)
    st.header("Your decision notice")

    ui_card(
        title=decision["recommendation"],
        body=(
            f"Scenario: {scenario}\n"
            f"Country template: {country}\n\n"
            f"{decision['plain']}\n\n"
            "This is not a final human decision. You can ask for explanation, correction, or review."
        ),
        tone=decision["tone"],
        eyebrow="Automated recommendation",
    )

    ui_card(
        title="What this means",
        body=legal.plain_notice,
        tone="blue",
        eyebrow=legal.title,
    )

    ui_card(
        title="Recommended safer workflow",
        body=decision["workflow"],
        tone="purple",
        eyebrow="Next safest step",
    )

    st.header("Why human review may be needed")
    for trigger in decision["triggers"]:
        tone = "orange" if "No mandatory" not in trigger else "green"
        ui_card(title="Review trigger", body=trigger, tone=tone)

    ui_card(
        title="Evidence that may help",
        body=(
            f"For this {scenario.lower()} case, useful evidence may include: {domain['evidence']}.\n\n"
            "Only submit information that is relevant to this specific review."
        ),
        tone="white",
        eyebrow="Data minimization",
    )


# =========================================================
# View 2: Explanation and appeal
# =========================================================
elif view == "Explanation and appeal":
    st.markdown('<div class="section-label">Plain-language explanation</div>', unsafe_allow_html=True)
    st.header("Why the system gave this recommendation")

    factors_sorted = sorted(decision["factors"].items(), key=lambda item: item[1])
    for name, value in factors_sorted:
        tone = "red" if value <= -10 else "green" if value >= 10 else "white"
        ui_card(
            title=name,
            body=f"Influence: {value:.1f}\n{factor_explanation(name, value)}",
            tone=tone,
        )

    factor_table = pd.DataFrame(
        {
            "Factor": [name for name, _ in factors_sorted],
            "Influence": [round(value, 2) for _, value in factors_sorted],
            "Plain-language meaning": [factor_explanation(name, value) for name, value in factors_sorted],
        }
    )

    st.download_button(
        "Download factor explanation as CSV",
        data=factor_table.to_csv(index=False),
        file_name="factor_explanation.csv",
        mime="text/csv",
    )

    st.markdown('<div class="section-label">Contest the recommendation</div>', unsafe_allow_html=True)
    st.header("Request review or correction")

    with st.form("appeal_form", clear_on_submit=False):
        reasons = st.multiselect(
            "What do you want to challenge?",
            [
                "Incorrect data was used",
                "Important document is missing",
                "The model misunderstood my context",
                "The recommendation may be unfair or biased",
                "The uncertainty is too high for automatic processing",
                "I want human review",
                "I only want a clearer explanation",
            ],
        )

        appeal_text = st.text_area(
            "Explain your challenge",
            placeholder="Example: My current income is higher than shown, and one employment document was missing.",
            height=140,
        )

        uploaded_file = st.file_uploader(
            "Upload optional evidence",
            type=["pdf", "png", "jpg", "jpeg", "docx", "txt"],
        )

        appeal_path = st.radio(
            "Choose review path",
            [
                "Fast human review",
                "Correct data and rerun recommendation",
                "Full appeal review",
                "Request explanation only",
            ],
            index=0,
        )

        consent = st.checkbox(legal.consent_text)
        submitted = st.form_submit_button("Submit review request")

    if submitted:
        if not reasons:
            ui_card("Cannot submit yet", "Please select at least one challenge reason.", tone="red")
        elif not consent:
            ui_card("Consent needed", "Please confirm purpose-limited consent before submitting.", tone="red")
        else:
            st.session_state.appeal_submitted = True
            st.session_state.appeal_reasons = reasons
            st.session_state.appeal_text = appeal_text
            st.session_state.appeal_path = appeal_path
            st.session_state.review_status = "Submitted to review queue"
            add_audit_event("Affected person submitted review request")
            if uploaded_file is not None:
                add_audit_event(f"Evidence uploaded: {uploaded_file.name}")

            ui_card(
                "Review request submitted",
                (
                    f"Review path: {appeal_path}\n"
                    f"Selected reasons: {', '.join(reasons)}\n\n"
                    "The submitted information is marked for this case-specific review purpose only."
                ),
                tone="green",
            )


# =========================================================
# View 3: Reviewer dashboard
# =========================================================
elif view == "Human reviewer dashboard":
    st.markdown('<div class="section-label">Company reviewer view</div>', unsafe_allow_html=True)
    st.header("Review queue")

    metric_grid(
        [
            ("Case ID", case_id, "Demo case identifier"),
            ("Status", st.session_state.review_status, "Current review state"),
            ("Timeline", legal.appeal_timeline, "Configurable by country/client"),
        ]
    )

    ui_card(
        "Reviewer guidance",
        legal.reviewer_note,
        tone="blue",
    )

    if st.session_state.appeal_submitted:
        ui_card(
            "Affected-person request",
            (
                f"Review path: {st.session_state.appeal_path}\n"
                f"Reasons: {', '.join(st.session_state.appeal_reasons)}\n\n"
                f"Explanation: {st.session_state.appeal_text or 'No written explanation submitted.'}"
            ),
            tone="purple",
        )
    else:
        ui_card(
            "No appeal submitted yet",
            "The reviewer can still inspect the automated recommendation and record an internal note.",
            tone="white",
        )

    st.header("Record human review")
    with st.form("reviewer_form", clear_on_submit=False):
        review_status = st.radio(
            "Reviewer status",
            [
                "Waiting for reviewer",
                "Under human review",
                "Waiting for additional evidence",
                "Resolved",
                "Escalated to senior reviewer",
            ],
            index=[
                "Waiting for reviewer",
                "Under human review",
                "Waiting for additional evidence",
                "Resolved",
                "Escalated to senior reviewer",
            ].index(st.session_state.review_status)
            if st.session_state.review_status
            in [
                "Waiting for reviewer",
                "Under human review",
                "Waiting for additional evidence",
                "Resolved",
                "Escalated to senior reviewer",
            ]
            else 0,
        )

        review_outcome = st.radio(
            "Reviewer outcome",
            [
                "Not reviewed yet",
                "Original recommendation upheld",
                "Recommendation changed after evidence",
                "Need more information",
                "Escalated",
            ],
            index=0,
        )

        reviewer_notes = st.text_area(
            "Reviewer notes",
            value=st.session_state.reviewer_notes,
            placeholder="Write the human reasoning here. Avoid vague statements such as 'system says no'.",
            height=150,
        )

        save_review = st.form_submit_button("Save reviewer decision")

    if save_review:
        st.session_state.review_status = review_status
        st.session_state.review_outcome = review_outcome
        st.session_state.reviewer_notes = reviewer_notes
        add_audit_event(f"Reviewer saved status: {review_status}; outcome: {review_outcome}")
        ui_card("Reviewer record saved", "The case audit trail has been updated.", tone="green")


# =========================================================
# View 4: SaaS admin and pricing
# =========================================================
elif view == "SaaS admin and pricing":
    st.markdown('<div class="section-label">SaaS profitability layer</div>', unsafe_allow_html=True)
    st.header("Company admin dashboard")

    ui_card(
        "What companies pay for",
        (
            "Companies do not pay for a generic AI dashboard. They pay for a workflow that reduces complaint chaos, "
            "standardizes appeal handling, produces audit records, supports reviewer accountability, and gives affected people a clearer route to correction."
        ),
        tone="blue",
    )

    st.header("Pricing model for pilots")
    for _, row in PRICING_PLANS.iterrows():
        ui_card(
            title=f"{row['Plan']} — {row['Monthly price']}",
            body=f"Best for: {row['Best for']}\nIncluded cases: {row['Included cases']}\nKey value: {row['Key value']}",
            tone="white",
        )

    st.header("ROI calculator for a potential client")
    monthly_cases = st.slider("Monthly automated decisions needing notice/review", 50, 10000, 1000, step=50)
    manual_minutes_saved = st.slider("Estimated support/review minutes saved per case", 1, 30, 8)
    staff_hourly_cost = st.slider("Reviewer/support cost per hour in USD", 2, 100, 12)
    subscription_price = st.slider("Proposed monthly subscription in USD", 50, 5000, 399, step=50)

    gross_time_saving = monthly_cases * manual_minutes_saved / 60 * staff_hourly_cost
    net_value = gross_time_saving - subscription_price
    roi_multiple = gross_time_saving / subscription_price if subscription_price else 0

    metric_grid(
        [
            ("Estimated monthly value", f"${gross_time_saving:,.0f}", "Support/review time saving only"),
            ("Net value after fee", f"${net_value:,.0f}", "Before legal/reputation benefits"),
            ("ROI multiple", f"{roi_multiple:.1f}x", "Estimated value divided by subscription"),
        ]
    )

    ui_card(
        "Best commercial upgrade",
        (
            "Add an API endpoint that lets a company create a case automatically from its own scoring system. "
            "Then your product becomes infrastructure, not just a form. The affected person receives a secure review link, "
            "while the company gets reviewer workflow, audit logs, and exportable reports."
        ),
        tone="purple",
    )

    api_payload = {
        "company_id": "demo_company_001",
        "country_template": country,
        "scenario": scenario,
        "external_person_id": "applicant_12345",
        "automated_recommendation": decision["recommendation"],
        "score": round(decision["score"], 2),
        "uncertainty": round(decision["uncertainty"], 2),
        "review_risk": decision["risk_level"],
        "review_triggers": decision["triggers"],
        "factor_influences": {k: round(v, 2) for k, v in decision["factors"].items()},
        "recommended_workflow": decision["workflow"],
    }

    st.header("API payload preview")
    st.text_area(
        "This is what a company could send to the SaaS backend",
        value=json.dumps(api_payload, indent=2, ensure_ascii=False),
        height=300,
    )
    download_json("Download API payload JSON", api_payload, "contestable_ai_api_payload.json")


# =========================================================
# View 5: Audit and exports
# =========================================================
elif view == "Audit and exports":
    st.markdown('<div class="section-label">Audit-ready records</div>', unsafe_allow_html=True)
    st.header("Audit trail")

    if st.session_state.audit_log:
        for row in st.session_state.audit_log:
            ui_card(row["Time"], row["Event"], tone="white")
    else:
        ui_card("No audit events", "No events have been recorded yet.", tone="white")

    audit_df = pd.DataFrame(st.session_state.audit_log)
    if not audit_df.empty:
        st.download_button(
            "Download audit log CSV",
            data=audit_df.to_csv(index=False),
            file_name="audit_log.csv",
            mime="text/csv",
        )

    st.header("Case report")
    report = build_case_report(case)
    download_markdown("Download case report", report, "contestable_ai_case_report.md")
    download_json("Download full case JSON", case, "contestable_ai_case.json")

    if st.button("Reset demo case"):
        st.session_state.audit_log = []
        st.session_state.appeal_submitted = False
        st.session_state.appeal_reasons = []
        st.session_state.appeal_text = ""
        st.session_state.appeal_path = "Fast human review"
        st.session_state.review_status = "Waiting for reviewer"
        st.session_state.review_outcome = "Not reviewed yet"
        st.session_state.reviewer_notes = ""
        st.session_state.case_counter += 1
        st.session_state.last_case_key = ""
        st.rerun()


# =========================================================
# View 6: Research framing
# =========================================================
elif view == "Research framing":
    st.markdown('<div class="section-label">Research and product framing</div>', unsafe_allow_html=True)
    st.header("Research contribution")

    ui_card(
        "From transparency to procedural empowerment",
        (
            "This MVP demonstrates actionable contestability. The affected person receives a plain-language explanation, "
            "uncertainty information, review triggers, a safer workflow recommendation, and a structured way to challenge the recommendation. "
            "The core design goal is to make the safe and fair path easier than a vague appeal process."
        ),
        tone="blue",
    )

    ui_card(
        "Suggested user study",
        (
            "Compare this interface against a standard automated rejection notice. Measure decision comprehension, error identification, "
            "correct review-path selection, data-minimization behavior, perceived procedural fairness, trust calibration, and appeal quality."
        ),
        tone="purple",
    )

    st.header("Production roadmap")
    roadmap = [
        ("1. Pilot-ready MVP", "Company workspace, affected-person portal, evidence upload, reviewer dashboard, audit export."),
        ("2. API-first SaaS", "Case creation API, webhooks, API keys, company branding, usage limits, paid plans."),
        ("3. Compliance layer", "Country templates, retention rules, consent records, role-based permissions, PDF reports."),
        ("4. Enterprise readiness", "SSO, encrypted storage, data residency, penetration testing, security documentation, SLA."),
    ]
    for title, body in roadmap:
        ui_card(title, body, tone="white")


# =========================================================
# Footer note
# =========================================================
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    """
    <p class="fine-print">
    Demo disclaimer: this app uses a transparent simulated decision model for interaction-design purposes only.
    It is not a real credit, hiring, insurance, education, moderation, or eligibility model. Legal wording should be reviewed before production use.
    </p>
    """,
    unsafe_allow_html=True,
)