# app.py
# Contestable AI Decision Interface
# Mobile-corrected Streamlit MVP for AI contestability / usable security research
# Run locally with: streamlit run app.py

from __future__ import annotations

from datetime import datetime
from io import StringIO

import pandas as pd
import streamlit as st


# ==========================================================
# Page setup
# ==========================================================
st.set_page_config(
    page_title="Contestable AI Decision Interface",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)


# ==========================================================
# CSS: mobile-first, high contrast, no Streamlit tabs
# ==========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #f6f8fc;
        --panel: #ffffff;
        --panel-soft: #f8fafc;
        --text: #0f172a;
        --muted: #475569;
        --subtle: #64748b;
        --border: #d9e2ef;
        --border-strong: #b8c7dc;
        --blue: #2563eb;
        --blue-soft: #eff6ff;
        --green: #16a34a;
        --green-soft: #ecfdf5;
        --amber: #d97706;
        --amber-soft: #fffbeb;
        --red: #dc2626;
        --red-soft: #fef2f2;
        --violet: #7c3aed;
        --violet-soft: #f5f3ff;
        --shadow: 0 10px 24px rgba(15, 23, 42, 0.08);
        --radius: 20px;
    }

    /* Force light readable app even when browser/Streamlit is in dark mode */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    .block-container {
        max-width: 980px !important;
        padding-top: 1.25rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        padding-bottom: 6.5rem !important;
    }

    /* Hide Streamlit chrome as much as Streamlit allows. Streamlit Cloud's top bar may still remain. */
    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], [data-testid="stDeployButton"] {
        display: none !important;
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0rem !important;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, span, label,
    .stMarkdown, .stText, .stCaption,
    div[data-testid="stMarkdownContainer"] {
        color: var(--text) !important;
    }

    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {
        font-size: 1.02rem;
        line-height: 1.72;
    }

    h1 {
        letter-spacing: -0.045em !important;
        line-height: 1.05 !important;
    }

    h2, h3 {
        letter-spacing: -0.035em !important;
        line-height: 1.15 !important;
        margin-top: 1.15rem !important;
    }

    hr {
        border-color: var(--border) !important;
    }

    /* Native widget readability */
    input, textarea,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] input {
        background: #ffffff !important;
        color: var(--text) !important;
        border-color: var(--border-strong) !important;
        border-radius: 14px !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    /* Buttons */
    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        border-radius: 14px !important;
        border: 1px solid #1d4ed8 !important;
        background: #2563eb !important;
        color: #ffffff !important;
        font-weight: 750 !important;
        min-height: 44px !important;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.18) !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #1d4ed8 !important;
        color: #ffffff !important;
    }

    /* Dataframe wrapper: prevent tiny dark tables on mobile */
    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        overflow: hidden !important;
    }

    /* Core layout components */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 58%, #2563eb 100%);
        color: #ffffff !important;
        border-radius: 26px;
        padding: 1.45rem;
        box-shadow: var(--shadow);
        margin-bottom: 1.1rem;
    }

    .hero h1, .hero p, .hero span, .hero b {
        color: #ffffff !important;
    }

    .hero-title {
        font-size: 2.25rem;
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.055em;
        margin: 0 0 0.65rem 0;
    }

    .hero-subtitle {
        color: #dbeafe !important;
        font-size: 1.03rem;
        line-height: 1.65;
        max-width: 760px;
        margin: 0;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1rem;
    }

    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        padding: 0.42rem 0.7rem;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.24);
        font-weight: 750;
        font-size: 0.82rem;
    }

    .section-kicker {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.76rem;
        color: var(--blue) !important;
        font-weight: 900;
        margin-bottom: 0.35rem;
    }

    .section-title {
        font-size: 1.55rem;
        font-weight: 900;
        letter-spacing: -0.045em;
        color: var(--text) !important;
        margin: 1rem 0 0.75rem 0;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.85rem 0 1.1rem 0;
    }

    .grid-2 {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.85rem 0 1.1rem 0;
    }

    .card {
        background: var(--panel);
        color: var(--text) !important;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1rem;
        box-shadow: var(--shadow);
        margin-bottom: 0.85rem;
        overflow-wrap: anywhere;
    }

    .card * {
        color: inherit !important;
    }

    .metric-card {
        min-height: 128px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .metric-label {
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        font-size: 0.78rem;
        font-weight: 900;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        color: var(--text) !important;
        font-size: 1.75rem;
        font-weight: 950;
        letter-spacing: -0.045em;
        line-height: 1.05;
    }

    .metric-help {
        color: var(--muted) !important;
        font-size: 0.94rem;
        line-height: 1.45;
        margin-top: 0.65rem;
    }

    .soft-blue { background: var(--blue-soft); border-color: #bfdbfe; }
    .soft-green { background: var(--green-soft); border-color: #bbf7d0; }
    .soft-amber { background: var(--amber-soft); border-color: #fed7aa; }
    .soft-red { background: var(--red-soft); border-color: #fecaca; }
    .soft-violet { background: var(--violet-soft); border-color: #ddd6fe; }

    .left-blue { border-left: 7px solid var(--blue); }
    .left-green { border-left: 7px solid var(--green); }
    .left-amber { border-left: 7px solid var(--amber); }
    .left-red { border-left: 7px solid var(--red); }
    .left-violet { border-left: 7px solid var(--violet); }

    .pill {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 0.32rem 0.62rem;
        font-size: 0.78rem;
        font-weight: 850;
        border: 1px solid var(--border);
        background: #ffffff;
        color: var(--text) !important;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
    }

    .pill-red { background: var(--red-soft); border-color: #fecaca; color: #991b1b !important; }
    .pill-amber { background: var(--amber-soft); border-color: #fed7aa; color: #92400e !important; }
    .pill-green { background: var(--green-soft); border-color: #bbf7d0; color: #166534 !important; }
    .pill-blue { background: var(--blue-soft); border-color: #bfdbfe; color: #1e40af !important; }
    .pill-violet { background: var(--violet-soft); border-color: #ddd6fe; color: #5b21b6 !important; }

    .progress-shell {
        width: 100%;
        height: 12px;
        background: #e2e8f0;
        border-radius: 999px;
        overflow: hidden;
        margin-top: 0.8rem;
    }

    .progress-bar {
        height: 100%;
        border-radius: 999px;
    }

    .bar-blue { background: linear-gradient(90deg, #60a5fa, #2563eb); }
    .bar-green { background: linear-gradient(90deg, #86efac, #16a34a); }
    .bar-amber { background: linear-gradient(90deg, #fcd34d, #d97706); }
    .bar-red { background: linear-gradient(90deg, #fca5a5, #dc2626); }

    .mini-list {
        margin: 0.25rem 0 0 0;
        padding-left: 1.1rem;
    }

    .mini-list li {
        margin-bottom: 0.35rem;
        line-height: 1.55;
        color: var(--text) !important;
    }

    .timeline-item {
        border-left: 4px solid #bfdbfe;
        padding: 0.15rem 0 0.7rem 0.8rem;
        margin-left: 0.35rem;
    }

    .timeline-time {
        color: var(--subtle) !important;
        font-size: 0.85rem;
        font-weight: 800;
    }

    .timeline-event {
        color: var(--text) !important;
        font-weight: 750;
        margin-top: 0.1rem;
    }

    .notice {
        font-size: 0.95rem;
        line-height: 1.65;
        color: var(--muted) !important;
    }

    .big-readable {
        font-size: 1.08rem;
        line-height: 1.82;
        color: var(--text) !important;
    }

    @media (max-width: 760px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 0.85rem !important;
        }
        .hero {
            padding: 1rem;
            border-radius: 22px;
        }
        .hero-title {
            font-size: 1.72rem;
        }
        .hero-subtitle {
            font-size: 0.96rem;
            line-height: 1.55;
        }
        .grid-3, .grid-2 {
            grid-template-columns: 1fr !important;
            gap: 0.55rem;
        }
        .card {
            padding: 0.9rem;
            border-radius: 18px;
            margin-bottom: 0.7rem;
            box-shadow: 0 7px 18px rgba(15, 23, 42, 0.07);
        }
        .metric-card {
            min-height: auto;
        }
        .metric-value {
            font-size: 1.45rem;
        }
        .section-title {
            font-size: 1.32rem;
            margin-top: 0.95rem;
        }
        div[data-testid="stMarkdownContainer"] p,
        div[data-testid="stMarkdownContainer"] li {
            font-size: 0.98rem;
            line-height: 1.65;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Session state
# ==========================================================
def init_state() -> None:
    defaults = {
        "audit_log": [],
        "contestation_submitted": False,
        "review_status": "Not started",
        "review_outcome": "Pending",
        "reviewer_notes": "",
        "decision_logged": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def add_audit_event(event: str) -> None:
    st.session_state.audit_log.append(
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Event": event}
    )


# ==========================================================
# Decision model and wording helpers
# ==========================================================
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
    """
    score = 50
    score += min(income / 2000, 20)
    score -= debt_ratio * 35
    score += min(employment_years * 3, 15)
    score += credit_history * 1.5
    score -= missing_docs * 8
    score = max(0, min(100, score))

    if score >= 70:
        recommendation = "Proceed"
        tone = "green"
        public_wording = "The automated system suggests the case may proceed."
    elif score >= 55:
        recommendation = "Conditional human review"
        tone = "amber"
        public_wording = "The automated system suggests conditional review before any final outcome."
    else:
        recommendation = "Do not approve automatically"
        tone = "red"
        public_wording = "The automated system does not recommend automatic approval. This is not a final human decision."

    uncertainty = max(15, min(85, 100 - abs(score - 55) * 1.5))

    factors = {
        "Income / capacity indicator": min(income / 2000, 20),
        "Debt or burden ratio": -debt_ratio * 35,
        "Stable work/activity history": min(employment_years * 3, 15),
        "Relevant previous history": credit_history * 1.5,
        "Missing or unclear documents": -missing_docs * 8,
    }

    review_triggers: list[str] = []
    if uncertainty >= 60:
        review_triggers.append(
            "The uncertainty is high enough that automatic processing may be unsafe."
        )
    if missing_docs >= 2:
        review_triggers.append(
            "Important documents may be missing or unclear, so the case may be incomplete."
        )
    if sensitive_context:
        review_triggers.append(
            "The case includes sensitive context and should be checked by a human reviewer."
        )
    if recommendation == "Do not approve automatically" and score >= 45:
        review_triggers.append(
            "The case is close enough to the review boundary that corrected information could matter."
        )

    return score, recommendation, tone, public_wording, uncertainty, factors, review_triggers


def uncertainty_label(uncertainty: float) -> tuple[str, str]:
    if uncertainty >= 65:
        return "High uncertainty", "red"
    if uncertainty >= 45:
        return "Moderate uncertainty", "amber"
    return "Low uncertainty", "blue"


def risk_label(tone: str, review_triggers: list[str]) -> tuple[str, str]:
    if tone == "red" or len(review_triggers) >= 3:
        return "High", "red"
    if tone == "amber" or review_triggers:
        return "Elevated", "amber"
    return "Routine", "green"


def factor_explanation(factor: str, value: float) -> str:
    if factor == "Income / capacity indicator":
        if value >= 15:
            return "This factor strongly supports the case."
        if value >= 8:
            return "This factor moderately supports the case."
        return "This factor provides limited support."

    if factor == "Debt or burden ratio":
        if value <= -25:
            return "This factor strongly reduced the score."
        if value <= -10:
            return "This factor moderately reduced the score."
        return "This factor had only a limited negative effect."

    if factor == "Stable work/activity history":
        if value >= 12:
            return "A stable history increased confidence."
        if value >= 6:
            return "This gave moderate support."
        return "This gave limited support."

    if factor == "Relevant previous history":
        if value >= 12:
            return "Relevant history strongly supported the case."
        if value >= 6:
            return "Relevant history moderately supported the case."
        return "Relevant history gave limited support."

    if factor == "Missing or unclear documents":
        if value <= -24:
            return "Missing documents strongly reduced confidence."
        if value < 0:
            return "Missing documents reduced confidence."
        return "No missing documents reduced the score."

    return "This factor influenced the recommendation."


def safer_workflow_recommendation(
    recommendation: str,
    missing_docs: int,
    uncertainty: float,
    review_triggers: list[str],
) -> str:
    if missing_docs >= 2:
        return "Request missing or clearer documents before any final decision."
    if uncertainty >= 60:
        return "Send the case to fast human review instead of relying only on automation."
    if recommendation == "Do not approve automatically" and review_triggers:
        return "Allow structured appeal and data correction before final rejection."
    if recommendation == "Conditional human review":
        return "Use conditional review with limited additional evidence."
    if recommendation == "Proceed":
        return "Proceed, while preserving the audit trail and purpose limitation."
    return "Offer explanation and a clear human-review path."


def country_notice(country: str) -> str:
    notices = {
        "Bangladesh": "This notice uses plain-language review wording suitable for a Bangladesh pilot. The user may request human review, correct data, and submit relevant evidence for this case only.",
        "EU / UK": "This notice emphasizes meaningful human review, contestability, explanation, and purpose-limited data sharing for an automated-decision context.",
        "United States": "This notice uses a practical adverse-action-style structure: reason, correction route, evidence submission, and reviewer accountability.",
        "India": "This notice emphasizes user clarification, data correction, grievance-style review, and limited-purpose evidence sharing.",
        "Generic global": "This notice provides a country-neutral contestability workflow: explanation, uncertainty, challenge reason, human review, and audit trail.",
    }
    return notices[country]


def tone_classes(tone: str) -> tuple[str, str, str]:
    if tone == "green":
        return "soft-green left-green", "pill-green", "bar-green"
    if tone == "amber":
        return "soft-amber left-amber", "pill-amber", "bar-amber"
    if tone == "red":
        return "soft-red left-red", "pill-red", "bar-red"
    if tone == "violet":
        return "soft-violet left-violet", "pill-violet", "bar-blue"
    return "soft-blue left-blue", "pill-blue", "bar-blue"


def progress_html(value: float, tone: str) -> str:
    _, _, bar_class = tone_classes(tone)
    value = max(0, min(100, int(round(value))))
    return f"""
    <div class="progress-shell" aria-label="Progress value {value} percent">
        <div class="progress-bar {bar_class}" style="width:{value}%;"></div>
    </div>
    """


def metric_card(label: str, value: str, help_text: str, tone: str = "blue") -> str:
    card_class, _, _ = tone_classes(tone)
    return f"""
    <div class="card metric-card {card_class}">
        <div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        <div class="metric-help">{help_text}</div>
    </div>
    """


def section(title: str, kicker: str | None = None) -> None:
    if kicker:
        st.markdown(f'<div class="section-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def download_text_report(
    case_id: str,
    country: str,
    scenario: str,
    recommendation: str,
    score: float,
    uncertainty: float,
    review_triggers: list[str],
    recommended_workflow: str,
    factors: dict[str, float],
) -> str:
    buffer = StringIO()
    buffer.write("Contestable AI Decision Interface — Case Report\n")
    buffer.write("================================================\n\n")
    buffer.write(f"Case ID: {case_id}\n")
    buffer.write(f"Country template: {country}\n")
    buffer.write(f"Scenario: {scenario}\n")
    buffer.write(f"Automated recommendation: {recommendation}\n")
    buffer.write(f"Score: {score:.1f}/100\n")
    buffer.write(f"Estimated uncertainty: {uncertainty:.1f}%\n")
    buffer.write(f"Recommended safer workflow: {recommended_workflow}\n\n")
    buffer.write("Review triggers:\n")
    if review_triggers:
        for item in review_triggers:
            buffer.write(f"- {item}\n")
    else:
        buffer.write("- No automatic human-review trigger detected.\n")
    buffer.write("\nFactor explanations:\n")
    for factor, value in factors.items():
        buffer.write(f"- {factor}: {value:.1f} — {factor_explanation(factor, value)}\n")
    buffer.write("\nAudit trail:\n")
    for row in st.session_state.audit_log:
        buffer.write(f"- {row['Time']}: {row['Event']}\n")
    return buffer.getvalue()


# ==========================================================
# Header
# ==========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🛡️ Contestable AI Decision Interface</div>
        <p class="hero-subtitle">
            A mobile-readable prototype showing how automated recommendations can become explainable,
            contestable, reviewable, and safer for affected people.
        </p>
        <div class="badge-row">
            <span class="badge">Affected-person portal</span>
            <span class="badge">Human review</span>
            <span class="badge">Evidence upload</span>
            <span class="badge">Audit trail</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Input area: not hidden in sidebar, mobile friendly
# ==========================================================
with st.expander("Configure demo case", expanded=True):
    input_col1, input_col2 = st.columns(2)

    with input_col1:
        country = st.selectbox(
            "Country / legal template",
            ["Bangladesh", "EU / UK", "United States", "India", "Generic global"],
        )
        scenario = st.selectbox(
            "Decision scenario",
            [
                "Loan application",
                "Hiring shortlist",
                "Insurance claim",
                "University admission",
                "Platform account restriction",
                "NGO beneficiary selection",
            ],
        )
        case_id = st.text_input("Case ID", value="CASE-2026-0001")

    with input_col2:
        income = st.slider("Income / capacity indicator", 500, 10000, 2600, step=100)
        debt_ratio = st.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
        employment_years = st.slider("Years of stable work/activity", 0, 15, 2)
        missing_docs = st.slider("Missing or unclear documents", 0, 5, 2)
        credit_history = st.slider("Relevant history score", 0, 10, 5)
        sensitive_context = st.checkbox(
            "Sensitive context may require human review", value=True
        )


(
    score,
    recommendation,
    rec_tone,
    public_wording,
    uncertainty,
    factors,
    review_triggers,
) = compute_decision(
    income,
    debt_ratio,
    employment_years,
    missing_docs,
    credit_history,
    sensitive_context,
)

uncertainty_text, uncertainty_tone = uncertainty_label(uncertainty)
risk_text, risk_tone = risk_label(rec_tone, review_triggers)
recommended_workflow = safer_workflow_recommendation(
    recommendation, missing_docs, uncertainty, review_triggers
)

if not st.session_state.decision_logged:
    add_audit_event("Decision page viewed")
    st.session_state.decision_logged = True


# ==========================================================
# Summary cards
# ==========================================================
st.markdown(
    f"""
    <div class="grid-3">
        {metric_card("Automated recommendation", recommendation, "Not a final human decision", rec_tone)}
        {metric_card("Uncertainty", f"{uncertainty:.0f}%", uncertainty_text, uncertainty_tone)}
        {metric_card("Review risk", risk_text, "Based on triggers and uncertainty", risk_tone)}
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# Navigation: Streamlit tabs removed because they render badly on mobile
# ==========================================================
view = st.selectbox(
    "Choose view",
    [
        "Affected-person portal",
        "Explanation",
        "Contest / appeal",
        "Company review dashboard",
        "Audit and exports",
        "Research and SaaS framing",
    ],
)


# ==========================================================
# View 1: Affected-person portal
# ==========================================================
if view == "Affected-person portal":
    section("Your decision notice", "Affected-person view")

    card_class, pill_class, _ = tone_classes(rec_tone)
    st.markdown(
        f"""
        <div class="card {card_class}">
            <span class="pill {pill_class}">{scenario}</span>
            <span class="pill pill-blue">{country}</span>
            <h3 style="margin:0.7rem 0 0.45rem 0;">{recommendation}</h3>
            <p class="big-readable">{public_wording}</p>
            {progress_html(score, rec_tone)}
            <p class="notice"><b>Score shown for transparency:</b> {score:.1f}/100. This score is part of a simulated demonstration, not a real institutional score.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card soft-blue left-blue">
            <h3 style="margin-top:0;">What this means</h3>
            <p class="big-readable">{country_notice(country)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Why human review may be needed")
    if review_triggers:
        trigger_html = "".join(f"<li>{t}</li>" for t in review_triggers)
        st.markdown(
            f"""
            <div class="card soft-amber left-amber">
                <ul class="mini-list">{trigger_html}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="card soft-green left-green">
                No automatic human-review trigger was detected, but the affected person can still request an explanation or review.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="card soft-violet left-violet">
            <h3 style="margin-top:0;">Recommended safer workflow</h3>
            <p class="big-readable">{recommended_workflow}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==========================================================
# View 2: Explanation
# ==========================================================
elif view == "Explanation":
    section("Plain-language explanation", "Affected-person view")

    factor_df = pd.DataFrame(
        {
            "Factor": list(factors.keys()),
            "Influence": list(factors.values()),
            "Plain-language meaning": [
                factor_explanation(k, v) for k, v in factors.items()
            ],
        }
    ).sort_values("Influence")

    st.markdown(
        """
        <div class="card soft-blue left-blue">
            <p class="big-readable">
            This section avoids a complex model chart. It tells the affected person which factors helped,
            which factors hurt, and what can be corrected or clarified.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Mobile-friendly cards first
    for _, row in factor_df.iterrows():
        value = float(row["Influence"])
        if value <= -10:
            tone = "red"
            label = "Reduced score"
        elif value >= 10:
            tone = "green"
            label = "Supported case"
        else:
            tone = "blue"
            label = "Limited influence"
        card_class, pill_class, _ = tone_classes(tone)
        st.markdown(
            f"""
            <div class="card {card_class}">
                <span class="pill {pill_class}">{label}</span>
                <h3 style="margin:0.65rem 0 0.25rem 0;">{row['Factor']}</h3>
                <p class="notice"><b>Influence:</b> {value:.1f}</p>
                <p class="big-readable">{row['Plain-language meaning']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("Show table version"):
        st.dataframe(factor_df, use_container_width=True, hide_index=True)


# ==========================================================
# View 3: Contest / appeal
# ==========================================================
elif view == "Contest / appeal":
    section("Contest the recommendation", "Affected-person view")

    st.markdown(
        """
        <div class="card soft-blue left-blue">
            <p class="big-readable">
            Use this form only for information relevant to this specific review. Do not upload unrelated private documents.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    suggested_reasons = [
        "Incorrect data was used",
        "Important document is missing",
        "The model misunderstood my context",
        "The decision may be unfair or biased",
        "The uncertainty is too high for automatic processing",
        "I want human review",
    ]
    if missing_docs >= 2:
        suggested_default = ["Important document is missing", "I want human review"]
    elif uncertainty >= 60:
        suggested_default = ["The uncertainty is too high for automatic processing", "I want human review"]
    else:
        suggested_default = ["I want human review"]

    with st.form("contest_form"):
        reasons = st.multiselect(
            "What do you want to challenge?",
            suggested_reasons,
            default=suggested_default,
        )

        explanation = st.text_area(
            "Explain your challenge",
            height=140,
            placeholder="Example: My current information is incomplete. One required document was missing, and I want a human reviewer to consider the updated evidence.",
        )

        uploaded_file = st.file_uploader(
            "Upload optional evidence",
            type=["pdf", "png", "jpg", "jpeg", "docx"],
            help="Upload only evidence needed for this review purpose.",
        )

        review_path = st.radio(
            "Choose review path",
            [
                "Fast human review",
                "Correct data and rerun recommendation",
                "Full appeal review",
                "Request explanation only",
            ],
        )

        consent = st.checkbox(
            "I consent to share only the selected information for this specific review purpose."
        )

        submitted = st.form_submit_button("Submit contestation request")

    if submitted:
        if not reasons:
            st.error("Please select at least one reason for contesting the recommendation.")
        elif not consent:
            st.error("Please give purpose-limited consent before submitting.")
        else:
            st.session_state.contestation_submitted = True
            st.session_state.review_status = "Submitted"
            add_audit_event("Contestation request submitted")
            st.success("Contestation request submitted successfully.")
            st.markdown(
                f"""
                <div class="card soft-green left-green">
                    <h3 style="margin-top:0;">Contestation receipt</h3>
                    <p><b>Original automated recommendation:</b> {recommendation}</p>
                    <p><b>Review path:</b> {review_path}</p>
                    <p><b>Purpose limitation:</b> Submitted information may be used only to evaluate this contestation request.</p>
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


# ==========================================================
# View 4: Company review dashboard
# ==========================================================
elif view == "Company review dashboard":
    section("Reviewer workspace", "Company side")

    st.markdown(
        f"""
        <div class="grid-2">
            {metric_card("Case", case_id, scenario, "blue")}
            {metric_card("Current review status", st.session_state.review_status, "Company-side workflow state", "violet")}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="card soft-amber left-amber">
            <h3 style="margin-top:0;">Reviewer checklist</h3>
            <ul class="mini-list">
                <li>Check whether missing documents caused the recommendation.</li>
                <li>Check whether uncertainty is too high for automatic processing.</li>
                <li>Check whether sensitive context requires human judgment.</li>
                <li>Record the reviewer’s reasoning, not only the final outcome.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("reviewer_form"):
        new_status = st.selectbox(
            "Review status",
            ["Not started", "Submitted", "In review", "Need more evidence", "Resolved"],
            index=["Not started", "Submitted", "In review", "Need more evidence", "Resolved"].index(
                st.session_state.review_status
            ),
        )
        outcome = st.selectbox(
            "Reviewer outcome",
            [
                "Pending",
                "Original recommendation upheld",
                "Data corrected and recommendation rerun",
                "Changed after human review",
                "More evidence requested",
            ],
        )
        reviewer_notes = st.text_area(
            "Reviewer notes",
            height=150,
            value=st.session_state.reviewer_notes,
            placeholder="Explain what was checked, what evidence was considered, and why the outcome is fair or needs correction.",
        )
        saved = st.form_submit_button("Save reviewer update")

    if saved:
        st.session_state.review_status = new_status
        st.session_state.review_outcome = outcome
        st.session_state.reviewer_notes = reviewer_notes
        add_audit_event(f"Reviewer update saved: {new_status} / {outcome}")
        st.success("Reviewer update saved.")


# ==========================================================
# View 5: Audit and exports
# ==========================================================
elif view == "Audit and exports":
    section("Audit trail", "Accountability")

    if st.session_state.audit_log:
        for item in st.session_state.audit_log:
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">{item['Time']}</div>
                    <div class="timeline-event">{item['Event']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No audit events recorded yet.")

    audit_df = pd.DataFrame(st.session_state.audit_log)
    audit_csv = audit_df.to_csv(index=False).encode("utf-8")
    report_text = download_text_report(
        case_id,
        country,
        scenario,
        recommendation,
        score,
        uncertainty,
        review_triggers,
        recommended_workflow,
        factors,
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.download_button(
            "Download audit CSV",
            audit_csv,
            file_name=f"{case_id}_audit_log.csv",
            mime="text/csv",
        )
    with col_b:
        st.download_button(
            "Download case report",
            report_text,
            file_name=f"{case_id}_case_report.txt",
            mime="text/plain",
        )

    if st.button("Reset demo case"):
        st.session_state.audit_log = []
        st.session_state.contestation_submitted = False
        st.session_state.review_status = "Not started"
        st.session_state.review_outcome = "Pending"
        st.session_state.reviewer_notes = ""
        st.session_state.decision_logged = False
        st.rerun()


# ==========================================================
# View 6: Research and SaaS framing
# ==========================================================
elif view == "Research and SaaS framing":
    section("Research contribution")
    st.markdown(
        """
        <div class="card soft-blue left-blue">
            <p class="big-readable">
            This MVP demonstrates <b>actionable contestability</b>. The affected person does not only receive an automated recommendation.
            They receive a plain-language explanation, uncertainty information, review triggers, a safer workflow recommendation,
            and a structured way to challenge the decision.
            </p>
            <p class="big-readable">
            The central design shift is from transparency alone to procedural empowerment: the interface makes the safe and fair path
            easier than a vague appeal process.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("Suggested user study")
    st.markdown(
        """
        <div class="card">
            <p class="big-readable"><b>Study design:</b> Compare this interface against a standard automated rejection notice.</p>
            <p class="big-readable">Measure whether users can understand the decision, identify possible errors, choose an appropriate review path, avoid unnecessary data sharing, and feel that the process is fair.</p>
            <hr>
            <p><b>Possible outcome measures</b></p>
            <ul class="mini-list">
                <li>Decision comprehension</li>
                <li>Error identification accuracy</li>
                <li>Correct review-path selection</li>
                <li>Data minimization behavior</li>
                <li>Perceived procedural fairness</li>
                <li>Trust calibration</li>
                <li>Appeal quality</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("How this becomes a real SaaS")
    st.markdown(
        """
        <div class="card soft-violet left-violet">
            <p class="big-readable"><b>Next.js frontend</b> for the public portal and company dashboard.</p>
            <p class="big-readable"><b>FastAPI or Django backend</b> for case creation, review workflow, and API integrations.</p>
            <p class="big-readable"><b>PostgreSQL</b> for companies, users, decision cases, appeals, audit logs, templates, and subscriptions.</p>
            <p class="big-readable"><b>S3/Supabase Storage</b> for encrypted evidence files.</p>
            <p class="big-readable"><b>Auth0/Clerk/Supabase Auth</b> for company login, reviewer roles, and secure access.</p>
            <p class="big-readable"><b>Stripe</b> for company subscriptions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    section("UI/UX corrections made in this version")
    st.markdown(
        """
        <div class="card soft-green left-green">
            <ul class="mini-list">
                <li>Removed Streamlit tabs because they break visually on mobile.</li>
                <li>Added a clear mobile-friendly <b>Choose view</b> selector.</li>
                <li>Forced light, high-contrast colors even when Streamlit opens in dark mode.</li>
                <li>Made all headings, paragraphs, cards, inputs, and buttons readable.</li>
                <li>Converted tables into stacked explanation cards for phone screens.</li>
                <li>Kept advanced tables only inside an optional expander.</li>
                <li>Moved configuration into the main page so mobile users do not depend on the hidden sidebar.</li>
                <li>Used single-column layout on narrow screens.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
