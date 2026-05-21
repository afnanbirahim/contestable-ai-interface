# app.py
# ContestabilityLayer MVP — mobile-safe Streamlit prototype
# Run locally with: streamlit run app.py

from __future__ import annotations

from datetime import datetime
from html import escape
from textwrap import dedent
from typing import Dict, List, Tuple
import json

import pandas as pd
import streamlit as st


# ============================================================
# Page setup
# ============================================================
st.set_page_config(
    page_title="ContestabilityLayer MVP",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ============================================================
# Safe HTML renderer
# IMPORTANT: dedent prevents Streamlit/Markdown from showing HTML
# as black code blocks on mobile.
# ============================================================
def html(markup: str) -> None:
    st.markdown(dedent(markup).strip(), unsafe_allow_html=True)


def safe(value: object) -> str:
    return escape(str(value), quote=True).replace("\n", "<br>")


# ============================================================
# CSS: light, mobile-first, high contrast
# ============================================================
html(
    """
    <style>
    :root {
        --bg: #f8fafc;
        --surface: #ffffff;
        --text: #0f172a;
        --muted: #475569;
        --line: #d9e2ef;
        --blue: #2563eb;
        --green: #16a34a;
        --amber: #d97706;
        --red: #dc2626;
        --purple: #7c3aed;
        --slate: #64748b;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"] {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], footer {
        visibility: hidden !important;
        height: 0 !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-left: 0.95rem !important;
        padding-right: 0.95rem !important;
        max-width: 860px !important;
    }

    h1, h2, h3, h4, p, li, label, span, div {
        color: var(--text) !important;
    }

    h1 {
        font-size: clamp(2rem, 8vw, 3.25rem) !important;
        line-height: 1.03 !important;
        letter-spacing: -0.06em !important;
        font-weight: 950 !important;
        margin-bottom: 0.6rem !important;
    }

    h2 {
        font-size: clamp(1.35rem, 5.6vw, 2rem) !important;
        line-height: 1.15 !important;
        letter-spacing: -0.04em !important;
        font-weight: 900 !important;
        margin-top: 1.8rem !important;
        margin-bottom: 0.8rem !important;
    }

    h3 {
        font-size: clamp(1.05rem, 4.8vw, 1.35rem) !important;
        line-height: 1.18 !important;
        font-weight: 850 !important;
        margin-top: 1.2rem !important;
    }

    .hero {
        border-radius: 26px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        background: linear-gradient(135deg, #172554 0%, #1d4ed8 58%, #38bdf8 100%);
        box-shadow: 0 18px 48px rgba(37, 99, 235, 0.28);
        border: 1px solid rgba(255,255,255,0.28);
    }
    .hero h1, .hero p, .hero div, .hero span {
        color: #ffffff !important;
    }
    .hero .sub {
        color: #dbeafe !important;
        font-size: 1.02rem;
        line-height: 1.65;
        margin-top: 0.5rem;
    }

    .eyebrow {
        color: var(--blue) !important;
        font-size: 0.78rem;
        line-height: 1.1;
        font-weight: 950;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        margin: 0 0 0.8rem 0;
    }

    .pill-row {
        display: flex;
        gap: 0.55rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    .pill {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.55rem 0.78rem;
        font-size: 0.88rem;
        font-weight: 850;
        color: #ffffff !important;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.35);
    }

    .card {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 24px;
        padding: 1.15rem;
        margin: 0.85rem 0 1rem 0;
        box-shadow: 0 14px 32px rgba(15, 23, 42, 0.08);
        overflow-wrap: anywhere;
        word-break: normal;
    }
    .card p {
        font-size: 1.01rem;
        line-height: 1.72;
        margin: 0.4rem 0 0 0;
        color: var(--text) !important;
    }
    .card-title {
        font-size: clamp(1.2rem, 5.2vw, 1.65rem);
        line-height: 1.14;
        font-weight: 950;
        letter-spacing: -0.045em;
        color: var(--text) !important;
        margin: 0.18rem 0 0.4rem 0;
    }
    .kicker {
        color: #64748b !important;
        font-size: 0.76rem;
        line-height: 1.15;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 0.55rem;
    }
    .muted {
        color: var(--muted) !important;
    }

    .accent-blue { border-left: 10px solid var(--blue); background: #eff6ff; }
    .accent-green { border-left: 10px solid var(--green); background: #f0fdf4; }
    .accent-amber { border-left: 10px solid var(--amber); background: #fffbeb; }
    .accent-red { border-left: 10px solid var(--red); background: #fef2f2; }
    .accent-purple { border-left: 10px solid var(--purple); background: #f5f3ff; }
    .accent-slate { border-left: 10px solid #94a3b8; background: #ffffff; }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-bottom: 0.8rem;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.45rem 0.7rem;
        background: #ffffff;
        color: var(--text) !important;
        border: 1px solid var(--line);
        font-size: 0.86rem;
        font-weight: 850;
    }

    .metric-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.8rem 0 1rem 0;
    }
    .metric-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1.05rem;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06);
    }
    .metric-kicker {
        color: #64748b !important;
        font-size: 0.72rem;
        font-weight: 950;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        color: var(--text) !important;
        font-size: clamp(1.35rem, 7vw, 2.1rem);
        font-weight: 950;
        line-height: 1.04;
        letter-spacing: -0.055em;
    }
    .metric-note {
        color: var(--muted) !important;
        font-size: 0.9rem;
        line-height: 1.45;
        margin-top: 0.4rem;
    }

    .bar-shell {
        width: 100%;
        height: 15px;
        border-radius: 999px;
        background: #e2e8f0;
        overflow: hidden;
        margin-top: 0.7rem;
        border: 1px solid #dbe3ef;
    }
    .bar-fill {
        height: 100%;
        border-radius: 999px;
        min-width: 2%;
    }
    .bar-blue { background: var(--blue); }
    .bar-red { background: var(--red); }
    .bar-amber { background: var(--amber); }
    .bar-green { background: var(--green); }
    .bar-purple { background: var(--purple); }

    .list-card ul {
        padding-left: 1.1rem;
        margin-bottom: 0;
    }
    .list-card li {
        font-size: 1rem;
        line-height: 1.65;
        color: var(--text) !important;
        margin-bottom: 0.28rem;
    }

    /* Streamlit widgets: readable on phones, no dark dropdowns because we use radios/checks instead. */
    div[role="radiogroup"] label {
        background: #ffffff !important;
        border: 1px solid #dbe3ef !important;
        border-radius: 16px !important;
        padding: 0.44rem 0.58rem !important;
        margin-bottom: 0.34rem !important;
        color: var(--text) !important;
    }
    div[role="radiogroup"] label p,
    .stCheckbox label p,
    .stSlider label p,
    .stTextInput label p,
    .stTextArea label p,
    .stFileUploader label p,
    .stNumberInput label p {
        color: var(--text) !important;
        font-weight: 780 !important;
    }
    textarea, input {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid #cbd5e1 !important;
    }
    .stButton > button, .stDownloadButton > button, [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {
        border-radius: 16px !important;
        font-weight: 850 !important;
        min-height: 3rem !important;
        width: 100% !important;
    }

    @media (max-width: 640px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }
        .hero {
            border-radius: 22px;
            padding: 1.05rem;
        }
        .metric-grid {
            grid-template-columns: 1fr;
        }
        .card {
            border-radius: 22px;
            padding: 1.05rem;
        }
        .pill {
            font-size: 0.82rem;
            padding: 0.48rem 0.64rem;
        }
    }
    </style>
    """
)


# ============================================================
# Configuration
# ============================================================
COUNTRY_COPY: Dict[str, Dict[str, str]] = {
    "Bangladesh": {
        "notice": "Plain-language review wording suitable for a Bangladesh pilot. The affected person may request human review, correct data, and submit relevant evidence for this case only.",
        "rights": "This is a review pathway, not legal advice. The company should provide a clear contact route, reviewer accountability, and a written outcome.",
        "timeline": "3 to 7 working days",
    },
    "EU / UK": {
        "notice": "GDPR-style wording emphasizing meaningful information, human intervention, contestation, and the ability to express a point of view.",
        "rights": "The workflow should support meaningful human review, purpose limitation, data minimization, and audit evidence.",
        "timeline": "configurable by legal policy",
    },
    "United States": {
        "notice": "Adverse-action-style wording for sectors such as lending, employment, insurance, or platform decisions, with clear reasons and correction paths.",
        "rights": "The workflow should be adjusted by sector, state, and legal counsel before production use.",
        "timeline": "based on sector and company policy",
    },
    "India": {
        "notice": "Plain-language digital-service review wording suitable for fintech, hiring, insurance, education, and platform decisions.",
        "rights": "The workflow should include grievance routing, consent limits, and a clear human-review owner.",
        "timeline": "3 to 10 working days",
    },
    "Generic global": {
        "notice": "Generic contestability wording for automated or AI-assisted decisions where a person needs explanation, correction, and review.",
        "rights": "Use local legal review before production deployment.",
        "timeline": "configurable by country and domain",
    },
}

SCENARIO_EVIDENCE: Dict[str, str] = {
    "Loan application": "income statement, updated employment proof, debt correction, missing KYC document",
    "Hiring shortlist": "updated CV, missing qualification certificate, work sample, corrected experience record",
    "Insurance claim": "claim documents, medical or repair record, missing receipt, corrected incident description",
    "University admission": "transcript, recommendation letter, corrected grade record, missing portfolio evidence",
    "Platform account restriction": "identity confirmation, transaction context, explanation of suspicious activity, supporting screenshots",
    "NGO beneficiary selection": "household information, eligibility document, local verification, corrected income or vulnerability data",
}

COUNTRIES = list(COUNTRY_COPY.keys())
SCENARIOS = list(SCENARIO_EVIDENCE.keys())
REVIEW_STATUSES = [
    "Not started",
    "Submitted",
    "Under human review",
    "Need more evidence",
    "Data corrected and rerun needed",
    "Final decision issued",
]


# ============================================================
# Session state
# ============================================================
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []
if "submission" not in st.session_state:
    st.session_state.submission = None
if "review_status" not in st.session_state:
    st.session_state.review_status = "Not started"
if "reviewer_note" not in st.session_state:
    st.session_state.reviewer_note = ""
if "audit_started" not in st.session_state:
    st.session_state.audit_started = False


# ============================================================
# UI helpers
# ============================================================
def add_audit_event(event: str) -> None:
    st.session_state.audit_log.append(
        {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "event": event}
    )


def render_card(
    title: str,
    body: str,
    kicker: str = "",
    accent: str = "slate",
    badges: List[str] | None = None,
) -> None:
    badge_html = ""
    if badges:
        badge_html = '<div class="badge-row">' + "".join(
            f'<span class="badge">{safe(badge)}</span>' for badge in badges
        ) + "</div>"
    kicker_html = f'<div class="kicker">{safe(kicker)}</div>' if kicker else ""
    html(
        f"""
        <div class="card accent-{safe(accent)}">
            {badge_html}
            {kicker_html}
            <div class="card-title">{safe(title)}</div>
            <p>{safe(body)}</p>
        </div>
        """
    )


def render_list_card(title: str, items: List[str], kicker: str = "", accent: str = "slate") -> None:
    list_items = "".join(f"<li>{safe(item)}</li>" for item in items)
    kicker_html = f'<div class="kicker">{safe(kicker)}</div>' if kicker else ""
    html(
        f"""
        <div class="card accent-{safe(accent)} list-card">
            {kicker_html}
            <div class="card-title">{safe(title)}</div>
            <ul>{list_items}</ul>
        </div>
        """
    )


def render_metric_grid(metrics: List[Tuple[str, str, str]]) -> None:
    items = ""
    for kicker, value, note in metrics:
        items += f"""
        <div class="metric-card">
            <div class="metric-kicker">{safe(kicker)}</div>
            <div class="metric-value">{safe(value)}</div>
            <div class="metric-note">{safe(note)}</div>
        </div>
        """
    html(f'<div class="metric-grid">{items}</div>')


def render_bar(label: str, value: float, color: str = "blue") -> None:
    width = max(0.0, min(100.0, float(value)))
    html(
        f"""
        <div class="card accent-slate">
            <div class="kicker">{safe(label)}</div>
            <div class="metric-value">{width:.0f}%</div>
            <div class="bar-shell">
                <div class="bar-fill bar-{safe(color)}" style="width:{width:.1f}%"></div>
            </div>
        </div>
        """
    )


# ============================================================
# Decision logic
# ============================================================
def compute_decision(
    capacity: int,
    burden_ratio: float,
    stable_years: int,
    missing_docs: int,
    relevant_history: int,
    sensitive_context: bool,
) -> Tuple[float, str, str, float, Dict[str, float], List[str]]:
    score = 50.0
    score += min(capacity / 2000, 20)
    score -= burden_ratio * 35
    score += min(stable_years * 3, 15)
    score += relevant_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        recommendation = "Approve automatically"
        tone = "green"
    elif score >= 55:
        recommendation = "Send to conditional review"
        tone = "amber"
    else:
        recommendation = "Do not approve automatically"
        tone = "red"

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Capacity / income indicator": min(capacity / 2000, 20),
        "Debt or burden ratio": -burden_ratio * 35,
        "Stable work or activity": min(stable_years * 3, 15),
        "Relevant history": relevant_history * 1.5,
        "Missing or unclear documents": -missing_docs * 8,
    }

    triggers: List[str] = []
    if uncertainty >= 60:
        triggers.append("The uncertainty is high enough that automatic processing should not be the only step.")
    if missing_docs >= 1:
        triggers.append("Important documents may be missing or unclear, so the result may be based on incomplete information.")
    if sensitive_context:
        triggers.append("Sensitive context is present, so a human reviewer should check the case before final action.")
    if recommendation == "Do not approve automatically" and score >= 45:
        triggers.append("The case is close enough to the review boundary that corrected data could change the result.")

    return score, recommendation, tone, uncertainty, factors, triggers


def factor_text(factor: str, value: float) -> str:
    if "Capacity" in factor:
        if value >= 15:
            return "Capacity information strongly supports the case."
        if value >= 8:
            return "Capacity information gives moderate support."
        return "Capacity information gives limited support."
    if "Debt" in factor:
        if value <= -25:
            return "The burden ratio strongly reduces the score."
        if value <= -10:
            return "The burden ratio moderately reduces the score."
        return "The burden ratio has limited negative effect."
    if "Stable" in factor:
        if value >= 12:
            return "Stable work or activity history improves confidence."
        if value >= 6:
            return "Stable work or activity gives moderate support."
        return "Stable work or activity gives limited support."
    if "Relevant" in factor:
        if value >= 12:
            return "Relevant history strongly supports the case."
        if value >= 6:
            return "Relevant history moderately supports the case."
        return "Relevant history gives limited support."
    if "Missing" in factor:
        if value <= -16:
            return "Missing or unclear documents significantly reduce confidence."
        if value < 0:
            return "Missing or unclear documents reduce confidence."
        return "No missing-document penalty is applied."
    return "This factor influenced the recommendation."


def safer_workflow(recommendation: str, missing_docs: int, uncertainty: float, triggers: List[str]) -> str:
    if missing_docs >= 1:
        return "Request missing or clearer documents before any final decision."
    if uncertainty >= 60:
        return "Route the case to fast human review before finalizing."
    if recommendation == "Do not approve automatically" and triggers:
        return "Allow structured appeal and data correction before final rejection."
    if recommendation == "Send to conditional review":
        return "Ask for limited additional evidence and assign a reviewer."
    return "Proceed, but keep the audit trail and allow the person to request review."


def risk_level(uncertainty: float, triggers: List[str]) -> str:
    if uncertainty >= 70 or len(triggers) >= 3:
        return "High"
    if uncertainty >= 50 or len(triggers) >= 1:
        return "Elevated"
    return "Low"


def case_report(case: Dict[str, object]) -> str:
    return json.dumps(case, indent=2, ensure_ascii=False)


# ============================================================
# Header
# ============================================================
html(
    """
    <div class="hero">
        <div class="eyebrow" style="color:#bfdbfe !important;">ContestabilityLayer MVP</div>
        <h1>Contestable AI Decision Interface</h1>
        <div class="sub">
            A mobile-first prototype for explainable decisions, evidence submission,
            human review, audit trail, and SaaS-ready automated-decision governance.
        </div>
        <div class="pill-row">
            <span class="pill">Affected-person portal</span>
            <span class="pill">Human review</span>
            <span class="pill">Evidence upload</span>
            <span class="pill">Audit trail</span>
        </div>
    </div>
    """
)

if not st.session_state.audit_started:
    add_audit_event("Demo case opened")
    st.session_state.audit_started = True


# ============================================================
# Configuration controls: no selectbox, no tabs, no expander
# ============================================================
html('<div class="eyebrow">Configure demo case</div>')

country = st.radio("Country / legal template", COUNTRIES, index=0, horizontal=False)
scenario = st.radio("Decision scenario", SCENARIOS, index=0, horizontal=False)
capacity = st.slider("Capacity / income indicator", 500, 10000, 2600, step=100)
burden_ratio = st.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
stable_years = st.slider("Years of stable work/activity", 0, 15, 2)
missing_docs = st.slider("Missing or unclear documents", 0, 5, 2)
relevant_history = st.slider("Relevant history score", 0, 10, 5)
sensitive_context = st.checkbox("Sensitive context may require human review", value=True)

score, recommendation, tone, uncertainty, factors, triggers = compute_decision(
    capacity, burden_ratio, stable_years, missing_docs, relevant_history, sensitive_context
)
workflow = safer_workflow(recommendation, missing_docs, uncertainty, triggers)
risk = risk_level(uncertainty, triggers)
country_text = COUNTRY_COPY[country]

case = {
    "case_id": "CASE-DEMO-001",
    "country_template": country,
    "scenario": scenario,
    "automated_recommendation": recommendation,
    "score": round(score, 1),
    "uncertainty": round(uncertainty, 1),
    "risk_level": risk,
    "human_review_triggers": triggers,
    "recommended_workflow": workflow,
    "factors": {k: round(v, 2) for k, v in factors.items()},
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

view = st.radio(
    "Choose view",
    [
        "Affected-person notice",
        "Challenge and evidence",
        "Company review dashboard",
        "SaaS business layer",
        "Audit and exports",
    ],
    index=0,
    horizontal=False,
)


# ============================================================
# View 1: Affected-person notice
# ============================================================
if view == "Affected-person notice":
    html('<div class="eyebrow">Case summary</div>')

    render_card(
        title=recommendation,
        body="This is an automated recommendation only. It is not a final human decision.",
        kicker="Recommendation",
        accent=tone,
        badges=[scenario, country],
    )

    render_metric_grid(
        [
            ("Score", f"{score:.0f}/100", "Shown for transparency, not as a final decision."),
            ("Uncertainty", f"{uncertainty:.0f}%", "Used to decide whether human review is needed."),
            ("Review risk", risk, "Based on uncertainty, missing data, and sensitivity."),
            ("Review target", country_text["timeline"], "Configurable per country and company policy."),
        ]
    )

    render_bar("Recommendation score", score, "blue")
    render_bar("Uncertainty level", uncertainty, "purple")

    render_card(
        title="What this means",
        body=country_text["notice"],
        kicker="Plain-language notice",
        accent="blue",
    )

    render_card(
        title="Recommended safer workflow",
        body=workflow,
        kicker="Next safest step",
        accent="purple",
    )

    st.subheader("Why human review may be needed")
    if triggers:
        for trig in triggers:
            render_card("Review trigger", trig, accent="amber")
    else:
        render_card(
            "No automatic trigger detected",
            "The affected person can still request explanation or review if they believe the data is incorrect.",
            accent="green",
        )

    st.subheader("Human-readable explanation")
    sorted_factors = sorted(factors.items(), key=lambda item: item[1])
    for name, value in sorted_factors:
        accent = "red" if value < -10 else "green" if value > 10 else "slate"
        render_card(
            title=name,
            body=f"Influence: {value:.1f}. {factor_text(name, value)}",
            kicker="Factor explanation",
            accent=accent,
        )

    render_card(
        title="Evidence that may help",
        body=(
            f"For this {scenario.lower()} case, useful evidence may include: "
            f"{SCENARIO_EVIDENCE[scenario]}. The affected person should not upload unrelated private information."
        ),
        kicker="Data minimization",
        accent="slate",
    )


# ============================================================
# View 2: Challenge and evidence
# ============================================================
elif view == "Challenge and evidence":
    html('<div class="eyebrow">Affected-person action</div>')
    st.subheader("Challenge the recommendation")

    render_card(
        title="Before uploading evidence",
        body="Share only information that is necessary for this specific review. Do not upload unrelated personal documents.",
        kicker="Purpose-limited consent",
        accent="blue",
    )

    st.write("Select the reasons for the challenge:")
    reason_options = [
        "Incorrect data was used",
        "Important document is missing",
        "The model misunderstood my context",
        "The recommendation may be unfair or biased",
        "The uncertainty is too high for automatic processing",
        "I want human review",
    ]
    selected_reasons: List[str] = []
    for option in reason_options:
        if st.checkbox(option, key=f"reason_{option}"):
            selected_reasons.append(option)

    explanation = st.text_area(
        "Explain your challenge",
        placeholder="Example: My current income is higher than shown, and one employment document was missing.",
        height=150,
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
    uploaded_file = st.file_uploader(
        "Upload optional evidence",
        type=["pdf", "png", "jpg", "jpeg", "docx"],
    )
    consent = st.checkbox(
        "I consent to share only the selected information for this specific review purpose."
    )

    if st.button("Submit challenge request"):
        if not selected_reasons:
            st.error("Please select at least one challenge reason.")
        elif not consent:
            st.error("Please confirm purpose-limited consent before submitting.")
        else:
            st.session_state.submission = {
                "reasons": selected_reasons,
                "explanation": explanation,
                "review_path": review_path,
                "uploaded_file": uploaded_file.name if uploaded_file else "No file uploaded",
                "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.session_state.review_status = "Submitted"
            add_audit_event("Affected person submitted challenge request")
            st.success("Challenge request submitted successfully.")

    if st.session_state.submission:
        sub = st.session_state.submission
        render_card(
            title="Challenge receipt",
            body=f"Review path: {sub['review_path']}. Uploaded evidence: {sub['uploaded_file']}. Submitted at: {sub['submitted_at']}.",
            kicker="Receipt",
            accent="green",
        )
        render_list_card("Selected challenge reasons", sub["reasons"], accent="slate")
        if sub["explanation"]:
            render_card("Affected-person explanation", sub["explanation"], accent="blue")


# ============================================================
# View 3: Company dashboard
# ============================================================
elif view == "Company review dashboard":
    html('<div class="eyebrow">Company side</div>')
    st.subheader("Reviewer dashboard")

    render_metric_grid(
        [
            ("Case ID", case["case_id"], "Internal reference for the company."),
            ("Status", st.session_state.review_status, "Updated by the reviewer."),
            ("Risk", risk, "Used for routing and SLA priority."),
            ("Submitted evidence", "Yes" if st.session_state.submission else "No", "Affected-person evidence status."),
        ]
    )

    render_card(
        title="Reviewer priority",
        body=workflow,
        kicker="Recommended action",
        accent="purple",
    )

    if st.session_state.submission:
        sub = st.session_state.submission
        render_card(
            title="Affected-person submission",
            body=f"Reasons: {', '.join(sub['reasons'])}. Review path: {sub['review_path']}. Evidence: {sub['uploaded_file']}.",
            kicker="Submission summary",
            accent="blue",
        )
    else:
        render_card(
            title="No challenge submitted yet",
            body="The reviewer can still inspect the automated recommendation and decide whether proactive human review is needed.",
            accent="slate",
        )

    current_status_index = REVIEW_STATUSES.index(st.session_state.review_status) if st.session_state.review_status in REVIEW_STATUSES else 0
    new_status = st.radio("Update review status", REVIEW_STATUSES, index=current_status_index, horizontal=False)
    reviewer_note = st.text_area(
        "Reviewer note",
        value=st.session_state.reviewer_note,
        placeholder="Example: Request updated income document and rerun recommendation before final decision.",
        height=140,
    )

    if st.button("Save reviewer update"):
        st.session_state.review_status = new_status
        st.session_state.reviewer_note = reviewer_note
        add_audit_event(f"Reviewer updated status to: {new_status}")
        st.success("Reviewer update saved.")

    render_card(
        title="Compliance value for company",
        body="This dashboard reduces support chaos by turning AI complaints into structured cases with evidence, reviewer ownership, status tracking, and exportable audit records.",
        kicker="Why a company pays",
        accent="green",
    )


# ============================================================
# View 4: SaaS business layer
# ============================================================
elif view == "SaaS business layer":
    html('<div class="eyebrow">SaaS profitability layer</div>')
    st.subheader("How this becomes a paid product")

    render_card(
        title="Core paid promise",
        body="Companies pay for a contestability and human-review layer around automated decisions. Affected people use the portal for free.",
        kicker="Business model",
        accent="green",
    )

    render_card(
        title="Starter: $49 to $99/month",
        body="Hosted review portal, manual case creation, 2 reviewers, basic audit export, and company branding.",
        kicker="Pricing tier",
        accent="slate",
    )
    render_card(
        title="Growth: $199 to $499/month",
        body="API case creation, evidence uploads, reviewer queue, analytics, country templates, and domain templates for fintech, HR, insurance, education, platforms, and NGOs.",
        kicker="Pricing tier",
        accent="blue",
    )
    render_card(
        title="Enterprise: custom pricing",
        body="SSO, data residency, custom legal templates, SLA, advanced audit exports, legal review workflow, and integrations with CRM, HR, lending, or claim systems.",
        kicker="Pricing tier",
        accent="purple",
    )

    st.subheader("Simple ROI calculator")
    monthly_cases = st.number_input("Monthly automated decision disputes or review cases", min_value=0, value=300, step=25)
    support_minutes_saved = st.number_input("Estimated support minutes saved per case", min_value=0, value=12, step=1)
    reviewer_hourly_cost = st.number_input("Estimated support/reviewer cost per hour in USD", min_value=0.0, value=8.0, step=1.0)
    monthly_savings = monthly_cases * (support_minutes_saved / 60) * reviewer_hourly_cost
    render_metric_grid(
        [
            ("Estimated monthly savings", f"${monthly_savings:,.0f}", "From reduced support/review handling time."),
            ("Suggested price", "$199-$499/mo", "Works if ROI is clearly above subscription cost."),
        ]
    )

    render_list_card(
        "SaaS features to build next",
        [
            "Multi-company workspaces",
            "Reviewer seats and role permissions",
            "Case creation API and webhook notifications",
            "Country and domain templates",
            "Evidence storage with retention rules",
            "Audit PDF and CSV exports",
            "Email/SMS status notifications",
            "Company branding and custom decision notices",
            "Analytics: dispute rate, reversal rate, time to review",
            "Billing by reviewer seats and monthly case volume",
        ],
        accent="green",
    )

    st.subheader("API fields companies would send")
    api_rows = pd.DataFrame(
        [
            ["company_id", "Company workspace identifier"],
            ["case_type", scenario],
            ["country_template", country],
            ["recommendation", recommendation],
            ["score", round(score, 1)],
            ["uncertainty", round(uncertainty, 1)],
            ["reason_factors", "List of factor names and influence values"],
            ["review_triggers", "List of human-review triggers"],
            ["portal_language", "English/Bangla/etc."],
        ],
        columns=["Field", "Example / meaning"],
    )
    st.dataframe(api_rows, hide_index=True, use_container_width=True)


# ============================================================
# View 5: Audit and exports
# ============================================================
elif view == "Audit and exports":
    html('<div class="eyebrow">Audit and exports</div>')
    st.subheader("Audit trail")

    audit_df = pd.DataFrame(st.session_state.audit_log)
    if audit_df.empty:
        st.info("No audit events yet.")
    else:
        st.dataframe(audit_df, hide_index=True, use_container_width=True)

    export_case = dict(case)
    export_case["affected_person_submission"] = st.session_state.submission
    export_case["review_status"] = st.session_state.review_status
    export_case["reviewer_note"] = st.session_state.reviewer_note

    st.download_button(
        "Download case report JSON",
        data=case_report(export_case),
        file_name="contestable_ai_case_report.json",
        mime="application/json",
    )

    st.download_button(
        "Download audit log CSV",
        data=audit_df.to_csv(index=False).encode("utf-8") if not audit_df.empty else "time,event\n".encode("utf-8"),
        file_name="contestable_ai_audit_log.csv",
        mime="text/csv",
    )

    st.subheader("Research framing")
    render_card(
        title="Research contribution",
        body="The interface shifts from transparency alone to procedural empowerment. The affected person receives explanation, uncertainty, review triggers, evidence guidance, purpose-limited consent, and a structured way to challenge the recommendation.",
        accent="blue",
    )
    render_card(
        title="Suggested user study",
        body="Compare this interface against a standard automated rejection notice. Measure decision comprehension, error identification, review-path selection, data-minimization behavior, perceived fairness, trust calibration, and appeal quality.",
        accent="purple",
    )

    if st.button("Reset demo state"):
        st.session_state.audit_log = []
        st.session_state.submission = None
        st.session_state.review_status = "Not started"
        st.session_state.reviewer_note = ""
        st.session_state.audit_started = False
        st.rerun()
