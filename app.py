# app.py
# Contestable AI Decision Interface
# Clean mobile-first Streamlit MVP
# Run with: streamlit run app.py

from __future__ import annotations

from datetime import datetime
from html import escape
from io import StringIO

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
# CSS
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #f6f8fc;
        --panel: #ffffff;
        --text: #111827;
        --muted: #4b5563;
        --border: #d6dde8;
        --blue: #2563eb;
        --blue-bg: #eff6ff;
        --green: #16a34a;
        --green-bg: #ecfdf5;
        --amber: #d97706;
        --amber-bg: #fffbeb;
        --red: #dc2626;
        --red-bg: #fef2f2;
        --violet: #7c3aed;
        --violet-bg: #f5f3ff;
        --shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
    }

    /* Force readable light interface even when Streamlit/browser dark mode is active */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"],
    section.main {
        background: var(--bg) !important;
        color: var(--text) !important;
    }

    .block-container {
        max-width: 920px !important;
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-bottom: 6rem !important;
    }

    /* Hide Streamlit chrome where possible. The Cloud/Fork bar may still appear. */
    #MainMenu, footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stDeployButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }

    h1, h2, h3, h4, h5, h6,
    p, li, span, label,
    .stMarkdown, .stText,
    div[data-testid="stMarkdownContainer"] {
        color: var(--text) !important;
    }

    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li {
        font-size: 1rem;
        line-height: 1.65;
    }

    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 62%, #2563eb 100%);
        border-radius: 24px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow);
    }

    .hero, .hero * {
        color: #ffffff !important;
    }

    .hero-title {
        font-size: 2.05rem;
        line-height: 1.08;
        letter-spacing: -0.05em;
        font-weight: 950;
        margin-bottom: 0.65rem;
    }

    .hero-subtitle {
        font-size: 1.02rem;
        line-height: 1.55;
        color: #dbeafe !important;
        margin: 0;
    }

    .badge-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.45rem;
        margin-top: 0.9rem;
    }

    .badge {
        display: inline-flex;
        border-radius: 999px;
        padding: 0.36rem 0.62rem;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.25);
        font-size: 0.8rem;
        font-weight: 800;
    }

    .section-kicker {
        color: var(--blue) !important;
        font-weight: 950;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-size: 0.76rem;
        margin-top: 0.85rem;
        margin-bottom: 0.2rem;
    }

    .section-title {
        font-size: 1.55rem;
        line-height: 1.15;
        letter-spacing: -0.04em;
        font-weight: 950;
        margin-bottom: 0.75rem;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 0.8rem 0 1rem 0;
    }

    .grid-2 {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.75rem;
        margin: 0.8rem 0 1rem 0;
    }

    .app-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 22px;
        padding: 1.05rem;
        margin-bottom: 0.8rem;
        box-shadow: var(--shadow);
        overflow-wrap: anywhere;
    }

    .app-card * {
        color: var(--text) !important;
    }

    .soft-blue { background: var(--blue-bg); border-color: #bfdbfe; border-left: 7px solid var(--blue); }
    .soft-green { background: var(--green-bg); border-color: #bbf7d0; border-left: 7px solid var(--green); }
    .soft-amber { background: var(--amber-bg); border-color: #fed7aa; border-left: 7px solid var(--amber); }
    .soft-red { background: var(--red-bg); border-color: #fecaca; border-left: 7px solid var(--red); }
    .soft-violet { background: var(--violet-bg); border-color: #ddd6fe; border-left: 7px solid var(--violet); }

    .metric-label {
        color: var(--muted) !important;
        font-size: 0.76rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 950;
        margin-bottom: 0.4rem;
    }

    .metric-value {
        font-size: 1.55rem;
        line-height: 1.1;
        letter-spacing: -0.04em;
        font-weight: 950;
        margin-bottom: 0.6rem;
    }

    .metric-help,
    .notice {
        color: var(--muted) !important;
        font-size: 0.95rem;
        line-height: 1.55;
    }

    .big-readable {
        font-size: 1.05rem;
        line-height: 1.75;
    }

    .pill {
        display: inline-flex;
        border-radius: 999px;
        padding: 0.32rem 0.62rem;
        margin-right: 0.35rem;
        margin-bottom: 0.35rem;
        background: #ffffff;
        border: 1px solid var(--border);
        font-size: 0.78rem;
        font-weight: 850;
    }

    .pill-red { background: var(--red-bg); border-color: #fecaca; color: #991b1b !important; }
    .pill-amber { background: var(--amber-bg); border-color: #fed7aa; color: #92400e !important; }
    .pill-green { background: var(--green-bg); border-color: #bbf7d0; color: #166534 !important; }
    .pill-blue { background: var(--blue-bg); border-color: #bfdbfe; color: #1e40af !important; }
    .pill-violet { background: var(--violet-bg); border-color: #ddd6fe; color: #5b21b6 !important; }

    .progress-shell {
        width: 100%;
        height: 12px;
        background: #e5e7eb;
        border-radius: 999px;
        overflow: hidden;
        margin: 0.9rem 0 0.75rem 0;
    }

    .progress-bar {
        height: 100%;
        border-radius: 999px;
    }

    .bar-red { background: linear-gradient(90deg, #fca5a5, #dc2626); }
    .bar-amber { background: linear-gradient(90deg, #fcd34d, #d97706); }
    .bar-green { background: linear-gradient(90deg, #86efac, #16a34a); }
    .bar-blue { background: linear-gradient(90deg, #93c5fd, #2563eb); }
    .bar-violet { background: linear-gradient(90deg, #c4b5fd, #7c3aed); }

    .clean-list {
        margin: 0.2rem 0 0 1.1rem;
        padding: 0;
    }

    .clean-list li {
        margin-bottom: 0.35rem;
        line-height: 1.55;
    }

    .timeline-item {
        border-left: 4px solid #bfdbfe;
        padding: 0.15rem 0 0.7rem 0.8rem;
        margin-left: 0.35rem;
    }

    .timeline-time {
        color: var(--muted) !important;
        font-size: 0.86rem;
        font-weight: 800;
    }

    .timeline-event {
        font-weight: 800;
        margin-top: 0.12rem;
    }

    input, textarea,
    div[data-baseweb="select"] > div,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="input"] input {
        background: #ffffff !important;
        color: var(--text) !important;
        border-color: #cbd5e1 !important;
        border-radius: 14px !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #94a3b8 !important;
        opacity: 1 !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    .stFormSubmitButton > button {
        border-radius: 14px !important;
        min-height: 44px !important;
        background: #2563eb !important;
        color: #ffffff !important;
        border: 1px solid #1d4ed8 !important;
        font-weight: 850 !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: #1d4ed8 !important;
        color: #ffffff !important;
    }

    div[data-testid="stDataFrame"] {
        background: #ffffff !important;
        border-radius: 16px !important;
        border: 1px solid var(--border) !important;
        overflow: hidden !important;
    }

    @media (max-width: 760px) {
        .block-container {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 0.75rem !important;
        }

        .hero {
            padding: 1rem;
            border-radius: 20px;
        }

        .hero-title {
            font-size: 1.55rem;
        }

        .hero-subtitle {
            font-size: 0.95rem;
        }

        .grid-3,
        .grid-2 {
            grid-template-columns: 1fr !important;
            gap: 0.55rem;
        }

        .app-card {
            padding: 0.9rem;
            border-radius: 18px;
        }

        .section-title {
            font-size: 1.35rem;
        }

        .metric-value {
            font-size: 1.35rem;
        }

        .big-readable {
            font-size: 0.98rem;
            line-height: 1.65;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# State
# =========================================================
def init_state() -> None:
    defaults = {
        "audit_log": [],
        "decision_logged": False,
        "contestation_submitted": False,
        "review_status": "Not started",
        "review_outcome": "Pending",
        "reviewer_notes": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def add_audit_event(event: str) -> None:
    st.session_state.audit_log.append(
        {"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Event": event}
    )


# =========================================================
# Helpers
# =========================================================
def compute_decision(
    income: int,
    debt_ratio: float,
    employment_years: int,
    missing_docs: int,
    credit_history: int,
    sensitive_context: bool,
):
    """Transparent simulated model for demo purposes only."""
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
        public_wording = "The automated system suggests the case may proceed. This should still be recorded with an audit trail."
    elif score >= 55:
        recommendation = "Conditional human review"
        tone = "amber"
        public_wording = "The automated system suggests conditional review before any final outcome. A person should check the case."
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
        review_triggers.append("The uncertainty is high enough that automatic processing may be unsafe.")
    if missing_docs >= 2:
        review_triggers.append("Important documents may be missing or unclear, so the case may be incomplete.")
    if sensitive_context:
        review_triggers.append("The case includes sensitive context and should be checked by a human reviewer.")
    if recommendation == "Do not approve automatically" and score >= 45:
        review_triggers.append("The case is close enough to the review boundary that corrected information could matter.")

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


def tone_class(tone: str) -> str:
    return {
        "green": "soft-green",
        "amber": "soft-amber",
        "red": "soft-red",
        "blue": "soft-blue",
        "violet": "soft-violet",
    }.get(tone, "soft-blue")


def pill_class(tone: str) -> str:
    return {
        "green": "pill-green",
        "amber": "pill-amber",
        "red": "pill-red",
        "blue": "pill-blue",
        "violet": "pill-violet",
    }.get(tone, "pill-blue")


def bar_class(tone: str) -> str:
    return {
        "green": "bar-green",
        "amber": "bar-amber",
        "red": "bar-red",
        "blue": "bar-blue",
        "violet": "bar-violet",
    }.get(tone, "bar-blue")


def progress_html(value: float, tone: str) -> str:
    safe_value = max(0, min(100, int(round(value))))
    return (
        f'<div class="progress-shell" aria-label="{safe_value} percent">'
        f'<div class="progress-bar {bar_class(tone)}" style="width:{safe_value}%;"></div>'
        f'</div>'
    )


def metric_card(label: str, value: str, help_text: str, tone: str) -> str:
    return f"""
    <div class="app-card {tone_class(tone)}">
        <div class="metric-label">{escape(label)}</div>
        <div class="metric-value">{escape(value)}</div>
        <div class="metric-help">{escape(help_text)}</div>
    </div>
    """


def section(title: str, kicker: str | None = None) -> None:
    if kicker:
        st.markdown(f'<div class="section-kicker">{escape(kicker)}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{escape(title)}</div>', unsafe_allow_html=True)


def render_notice_card(
    recommendation: str,
    scenario: str,
    country: str,
    wording: str,
    score: float,
    tone: str,
) -> None:
    html = f"""
    <div class="app-card {tone_class(tone)}">
        <span class="pill {pill_class(tone)}">{escape(scenario)}</span>
        <span class="pill pill-blue">{escape(country)}</span>
        <h3 style="margin:0.65rem 0 0.35rem 0; font-size:1.55rem; line-height:1.15;">{escape(recommendation)}</h3>
        <p class="big-readable">{escape(wording)}</p>
        {progress_html(score, tone)}
        <p class="notice"><b>Score shown for transparency:</b> {score:.1f}/100. This is a simulated demonstration score, not a real institutional score.</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_simple_card(title: str, body: str, tone: str = "blue") -> None:
    html = f"""
    <div class="app-card {tone_class(tone)}">
        <h3 style="margin-top:0;">{escape(title)}</h3>
        <p class="big-readable">{escape(body)}</p>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_list_card(items: list[str], tone: str = "amber", title: str | None = None) -> None:
    title_html = f'<h3 style="margin-top:0;">{escape(title)}</h3>' if title else ""
    list_html = "".join(f"<li>{escape(item)}</li>" for item in items)
    html = f"""
    <div class="app-card {tone_class(tone)}">
        {title_html}
        <ul class="clean-list">{list_html}</ul>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def make_report(
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


# =========================================================
# Header
# =========================================================
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


# =========================================================
# Configuration
# =========================================================
with st.expander("Configure demo case", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
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
    with col2:
        income = st.slider("Income / capacity indicator", 500, 10000, 2600, step=100)
        debt_ratio = st.slider("Debt or burden ratio", 0.0, 1.0, 0.42, step=0.01)
        employment_years = st.slider("Years of stable work/activity", 0, 15, 2)
        missing_docs = st.slider("Missing or unclear documents", 0, 5, 2)
        credit_history = st.slider("Relevant history score", 0, 10, 5)
        sensitive_context = st.checkbox("Sensitive context may require human review", value=True)


(
    score,
    recommendation,
    rec_tone,
    public_wording,
    uncertainty,
    factors,
    review_triggers,
) = compute_decision(income, debt_ratio, employment_years, missing_docs, credit_history, sensitive_context)

uncertainty_text, uncertainty_tone = uncertainty_label(uncertainty)
risk_text, risk_tone = risk_label(rec_tone, review_triggers)
recommended_workflow = safer_workflow_recommendation(recommendation, missing_docs, uncertainty, review_triggers)

if not st.session_state.decision_logged:
    add_audit_event("Decision page viewed")
    st.session_state.decision_logged = True


# =========================================================
# Top summary
# =========================================================
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


# =========================================================
# View selector
# =========================================================
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


# =========================================================
# View: affected person
# =========================================================
if view == "Affected-person portal":
    section("Your decision notice", "Affected-person view")
    render_notice_card(recommendation, scenario, country, public_wording, score, rec_tone)
    render_simple_card("What this means", country_notice(country), "blue")

    section("Why human review may be needed")
    if review_triggers:
        render_list_card(review_triggers, "amber")
    else:
        render_simple_card(
            "No automatic trigger detected",
            "No automatic human-review trigger was detected, but the affected person can still request an explanation or review.",
            "green",
        )

    render_simple_card("Recommended safer workflow", recommended_workflow, "violet")


# =========================================================
# View: explanation
# =========================================================
elif view == "Explanation":
    section("Plain-language explanation", "Affected-person view")
    render_simple_card(
        "Simple explanation first",
        "This section avoids a complex model chart. It tells the affected person which factors helped, which factors hurt, and what can be corrected or clarified.",
        "blue",
    )

    factor_df = pd.DataFrame(
        {
            "Factor": list(factors.keys()),
            "Influence": list(factors.values()),
            "Plain-language meaning": [factor_explanation(k, v) for k, v in factors.items()],
        }
    ).sort_values("Influence")

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

        html = f"""
        <div class="app-card {tone_class(tone)}">
            <span class="pill {pill_class(tone)}">{escape(label)}</span>
            <h3 style="margin:0.65rem 0 0.25rem 0;">{escape(str(row['Factor']))}</h3>
            <p class="notice"><b>Influence:</b> {value:.1f}</p>
            <p class="big-readable">{escape(str(row['Plain-language meaning']))}</p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    with st.expander("Show compact table"):
        st.dataframe(factor_df, use_container_width=True, hide_index=True)


# =========================================================
# View: contest / appeal
# =========================================================
elif view == "Contest / appeal":
    section("Contest the recommendation", "Affected-person view")
    render_simple_card(
        "Purpose-limited evidence",
        "Use this form only for information relevant to this specific review. Do not upload unrelated private documents.",
        "blue",
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
        reasons = st.multiselect("What do you want to challenge?", suggested_reasons, default=suggested_default)
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
        consent = st.checkbox("I consent to share only the selected information for this specific review purpose.")
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
            render_simple_card(
                "Contestation receipt",
                f"Original automated recommendation: {recommendation}. Review path: {review_path}. Submitted information may be used only to evaluate this contestation request.",
                "green",
            )
            st.write("**Selected challenge reasons:**")
            for reason in reasons:
                st.write(f"- {reason}")
            if explanation:
                st.write("**User explanation:**")
                st.write(explanation)
            if uploaded_file is not None:
                st.write(f"**Uploaded evidence:** {uploaded_file.name}")


# =========================================================
# View: company review dashboard
# =========================================================
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
    render_list_card(
        [
            "Check whether missing documents caused the recommendation.",
            "Check whether uncertainty is too high for automatic processing.",
            "Check whether sensitive context requires human judgment.",
            "Record the reviewer’s reasoning, not only the final outcome.",
        ],
        "amber",
        "Reviewer checklist",
    )

    statuses = ["Not started", "Submitted", "In review", "Need more evidence", "Resolved"]
    with st.form("reviewer_form"):
        new_status = st.selectbox(
            "Review status",
            statuses,
            index=statuses.index(st.session_state.review_status) if st.session_state.review_status in statuses else 0,
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


# =========================================================
# View: audit and exports
# =========================================================
elif view == "Audit and exports":
    section("Audit trail", "Accountability")

    if st.session_state.audit_log:
        for item in st.session_state.audit_log:
            st.markdown(
                f"""
                <div class="timeline-item">
                    <div class="timeline-time">{escape(item['Time'])}</div>
                    <div class="timeline-event">{escape(item['Event'])}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No audit events recorded yet.")

    audit_df = pd.DataFrame(st.session_state.audit_log)
    audit_csv = audit_df.to_csv(index=False).encode("utf-8")
    report_text = make_report(
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
        st.download_button("Download audit CSV", audit_csv, file_name=f"{case_id}_audit_log.csv", mime="text/csv")
    with col_b:
        st.download_button("Download case report", report_text, file_name=f"{case_id}_case_report.txt", mime="text/plain")

    if st.button("Reset demo case"):
        st.session_state.audit_log = []
        st.session_state.contestation_submitted = False
        st.session_state.review_status = "Not started"
        st.session_state.review_outcome = "Pending"
        st.session_state.reviewer_notes = ""
        st.session_state.decision_logged = False
        st.rerun()


# =========================================================
# View: research and SaaS framing
# =========================================================
elif view == "Research and SaaS framing":
    section("Research contribution")
    render_simple_card(
        "Actionable contestability",
        "This MVP demonstrates actionable contestability. The affected person does not only receive an automated recommendation. They receive a plain-language explanation, uncertainty information, review triggers, a safer workflow recommendation, and a structured way to challenge the decision.",
        "blue",
    )
    render_simple_card(
        "Design shift",
        "The central design shift is from transparency alone to procedural empowerment. The interface makes the safe and fair path easier than a vague appeal process.",
        "violet",
    )

    section("Suggested user study")
    render_simple_card(
        "Study design",
        "Compare this interface against a standard automated rejection notice. Measure whether users can understand the decision, identify possible errors, choose an appropriate review path, avoid unnecessary data sharing, and feel that the process is fair.",
        "green",
    )
    render_list_card(
        [
            "Decision comprehension",
            "Error identification accuracy",
            "Correct review-path selection",
            "Data minimization behavior",
            "Perceived procedural fairness",
            "Trust calibration",
            "Appeal quality",
        ],
        "blue",
        "Possible outcome measures",
    )

    section("How this becomes a real SaaS")
    render_list_card(
        [
            "Next.js frontend for the public portal and company dashboard.",
            "FastAPI or Django backend for case creation, review workflow, and API integrations.",
            "PostgreSQL for companies, users, decision cases, appeals, audit logs, templates, and subscriptions.",
            "S3 or Supabase Storage for encrypted evidence files.",
            "Auth0, Clerk, or Supabase Auth for company login, reviewer roles, and secure access.",
            "Stripe for company subscriptions.",
        ],
        "violet",
    )

    section("Important UI fix in this version")
    render_list_card(
        [
            "Removed the malformed progress-card HTML that created the black rectangle on mobile.",
            "Reduced nested HTML so Streamlit dark mode cannot convert card text into a dark code-like block.",
            "Kept progress bars inside well-formed card markup.",
            "Escaped dynamic text before inserting it into HTML cards.",
            "Kept mobile-first single-column behavior.",
        ],
        "green",
    )
