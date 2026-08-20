import time
import streamlit as st

from agents import (
    build_reader_agent,
    build_search_agent,
    writer_chain,
    critic_chain,
)


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="InsightForge · AI Research Workspace",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =============================================================================
# CUSTOM CSS
# IMPORTANT: All styling is applied through CSS selectors.
# No HTML containers are opened/closed across separate Streamlit calls.
# =============================================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------------------------
       GLOBAL
    ------------------------------------------------------------------------- */

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse 80% 50% at 15% -10%,
                rgba(76, 145, 255, 0.12) 0%,
                transparent 60%
            ),
            radial-gradient(
                ellipse 60% 40% at 85% 110%,
                rgba(70, 100, 255, 0.07) 0%,
                transparent 55%
            ),
            #090b10;
        color: #e9eef7;
    }

    #MainMenu,
    footer,
    header {
        visibility: hidden;
    }

    .block-container {
        max-width: 1180px;
        padding: 2.5rem 2.5rem 4rem;
    }


    /* -------------------------------------------------------------------------
       HERO
    ------------------------------------------------------------------------- */

    .hero-eyebrow {
        text-align: center;
        font-family: "DM Mono", monospace;
        font-size: 0.68rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: #6fa4ff;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    .hero-title {
        text-align: center;
        font-family: "Syne", sans-serif;
        font-size: clamp(2.7rem, 6vw, 4.8rem);
        line-height: 1;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 0;
        color: #f4f7fb;
    }

    .hero-title-accent {
        color: #6fa4ff;
    }

    .hero-subtitle {
        max-width: 590px;
        margin: 1rem auto 0;
        text-align: center;
        color: #929baa;
        font-size: 0.98rem;
        line-height: 1.65;
        font-weight: 300;
    }

    .hero-divider {
        height: 1px;
        margin: 2.2rem 0 2.5rem;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(111,164,255,0.32),
            transparent
        );
    }


    /* -------------------------------------------------------------------------
       INPUT AREA
    ------------------------------------------------------------------------- */

    .input-label {
        font-family: "DM Mono", monospace;
        font-size: 0.68rem;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        color: #6fa4ff;
        margin-bottom: 0.45rem;
    }

    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.045) !important;
        border: 1px solid rgba(111,164,255,0.22) !important;
        border-radius: 10px !important;
        color: #f0f4fa !important;
        font-family: "DM Sans", sans-serif !important;
        font-size: 0.95rem !important;
        min-height: 44px !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6fa4ff !important;
        box-shadow: 0 0 0 3px rgba(111,164,255,0.10) !important;
    }

    .stTextInput label {
        display: none !important;
    }

    .stButton > button {
        min-height: 44px !important;
        border: none !important;
        border-radius: 10px !important;
        background: linear-gradient(
            135deg,
            #6fa4ff 0%,
            #4778df 100%
        ) !important;
        color: #080b12 !important;
        font-family: "Syne", sans-serif !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.03em !important;
        box-shadow: 0 5px 20px rgba(111,164,255,0.20) !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 8px 25px rgba(111,164,255,0.30) !important;
    }


    /* -------------------------------------------------------------------------
       EXAMPLE TOPICS
    ------------------------------------------------------------------------- */

    .example-title {
        font-family: "DM Mono", monospace;
        font-size: 0.65rem;
        letter-spacing: 0.15em;
        color: #555e6c;
        margin: 1.1rem 0 0.55rem;
    }

    .example-box {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 0.55rem 0.75rem;
        color: #8e98a8;
        font-size: 0.72rem;
        text-align: center;
    }


    /* -------------------------------------------------------------------------
       PIPELINE
    ------------------------------------------------------------------------- */

    .section-title {
        font-family: "Syne", sans-serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #edf2f8;
        margin: 0 0 0.9rem;
    }

    .pipeline-card {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px;
        padding: 0.95rem 1rem;
        margin-bottom: 0.65rem;
    }

    .pipeline-card-active {
        border-color: rgba(111,164,255,0.42);
        background: rgba(111,164,255,0.045);
    }

    .pipeline-card-done {
        border-color: rgba(80,200,120,0.30);
        background: rgba(80,200,120,0.025);
    }

    .pipeline-row {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }

    .pipeline-number {
        font-family: "DM Mono", monospace;
        font-size: 0.62rem;
        color: #6fa4ff;
        min-width: 22px;
    }

    .pipeline-name {
        font-family: "Syne", sans-serif;
        font-size: 0.82rem;
        font-weight: 700;
        color: #e9eef7;
    }

    .pipeline-status {
        margin-left: auto;
        font-family: "DM Mono", monospace;
        font-size: 0.58rem;
        letter-spacing: 0.08em;
    }

    .pipeline-desc {
        color: #687383;
        font-size: 0.67rem;
        margin-top: 0.45rem;
        margin-left: 1.7rem;
    }

    .waiting {
        color: #515a67;
    }

    .running {
        color: #6fa4ff;
    }

    .done {
        color: #50c878;
    }


    /* -------------------------------------------------------------------------
       OUTPUT
    ------------------------------------------------------------------------- */

    .output-divider {
        height: 1px;
        margin: 2.2rem 0;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255,255,255,0.09),
            transparent
        );
    }

    .output-label {
        font-family: "DM Mono", monospace;
        font-size: 0.67rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #6fa4ff;
        margin-bottom: 0.7rem;
    }

    .report-shell {
        background: rgba(255,255,255,0.022);
        border: 1px solid rgba(111,164,255,0.17);
        border-radius: 14px;
        padding: 1.5rem 1.7rem;
        margin-top: 1rem;
    }

    .review-shell {
        background: rgba(255,255,255,0.022);
        border: 1px solid rgba(80,200,120,0.17);
        border-radius: 14px;
        padding: 1.5rem 1.7rem;
        margin-top: 1.2rem;
    }

    .review-label {
        color: #50c878;
    }


    /* -------------------------------------------------------------------------
       EXPANDERS
    ------------------------------------------------------------------------- */

    [data-testid="stExpander"] {
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 10px !important;
        background: rgba(255,255,255,0.018) !important;
    }

    [data-testid="stExpander"] summary {
        font-family: "DM Mono", monospace !important;
        font-size: 0.68rem !important;
        color: #9ba4b2 !important;
    }


    /* -------------------------------------------------------------------------
       DOWNLOAD
    ------------------------------------------------------------------------- */

    .stDownloadButton > button {
        background: rgba(111,164,255,0.08) !important;
        border: 1px solid rgba(111,164,255,0.22) !important;
        color: #9fc0ff !important;
        border-radius: 9px !important;
        font-size: 0.75rem !important;
    }


    /* -------------------------------------------------------------------------
       STATUS / SPINNER
    ------------------------------------------------------------------------- */

    .stSpinner > div {
        color: #6fa4ff !important;
    }


    /* -------------------------------------------------------------------------
       FOOTER
    ------------------------------------------------------------------------- */

    .footer-text {
        text-align: center;
        margin-top: 3rem;
        color: #414956;
        font-family: "DM Mono", monospace;
        font-size: 0.62rem;
        letter-spacing: 0.08em;
    }

    </style>

    <link
        href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500&display=swap"
        rel="stylesheet"
    >
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# HELPERS
# =============================================================================

def text_from_value(value):
    """
    Safely convert LangChain/agent output into displayable text.
    Handles strings, AIMessage-like objects, and simple dict outputs.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if hasattr(value, "content"):
        content = value.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            parts = []

            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        parts.append(str(item["text"]))
                    elif "content" in item:
                        parts.append(str(item["content"]))
                    else:
                        parts.append(str(item))
                else:
                    parts.append(str(item))

            return "\n".join(parts)

        return str(content)

    if isinstance(value, dict):
        if "content" in value:
            return text_from_value(value["content"])

        return str(value)

    return str(value)


def get_agent_message(result):
    """
    Extract the final message from an agent response safely.
    """
    if isinstance(result, dict):
        messages = result.get("messages", [])

        if messages:
            return text_from_value(messages[-1])

    return text_from_value(result)


def pipeline_state(results, running, step):
    """
    Determine the visual state of each pipeline step.
    """
    steps = ["search", "reader", "writer", "critic"]

    if step in results:
        return "done"

    if not running:
        return "waiting"

    for current in steps:
        if current not in results:
            return "running" if current == step else "waiting"

    return "waiting"


def render_pipeline_card(number, title, description, state):
    if state == "done":
        status = "✓ DONE"
        status_class = "done"
        card_class = "pipeline-card-done"

    elif state == "running":
        status = "● RUNNING"
        status_class = "running"
        card_class = "pipeline-card-active"

    else:
        status = "WAITING"
        status_class = "waiting"
        card_class = ""

    st.markdown(
        f"""
        <div class="pipeline-card {card_class}">
            <div class="pipeline-row">
                <span class="pipeline-number">{number}</span>
                <span class="pipeline-name">{title}</span>
                <span class="pipeline-status {status_class}">
                    {status}
                </span>
            </div>
            <div class="pipeline-desc">
                {description}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =============================================================================
# SESSION STATE
# =============================================================================

if "results" not in st.session_state:
    st.session_state.results = {}

if "running" not in st.session_state:
    st.session_state.running = False

if "done" not in st.session_state:
    st.session_state.done = False


# =============================================================================
# HERO
# =============================================================================

st.markdown(
    '<div class="hero-eyebrow">Autonomous Research Workspace</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-title">
        Insight<span class="hero-title-accent">Forge</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-subtitle">
        A multi-agent research workspace that searches, reads, writes,
        and critiques information to produce structured reports.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero-divider"></div>',
    unsafe_allow_html=True,
)


# =============================================================================
# INPUT + PIPELINE
# =============================================================================

col_input, col_gap, col_pipeline = st.columns(
    [5, 0.45, 4],
    vertical_alignment="top",
)


# -----------------------------------------------------------------------------
# LEFT — INPUT
# -----------------------------------------------------------------------------

with col_input:

    st.markdown(
        '<div class="input-label">Research Topic</div>',
        unsafe_allow_html=True,
    )

    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Latest developments in generative AI",
        key="topic_input",
        label_visibility="collapsed",
    )

    run_btn = st.button(
        "⚡  Start Research",
        use_container_width=True,
        type="primary",
    )

    st.markdown(
        '<div class="example-title">TRY →</div>',
        unsafe_allow_html=True,
    )

    example_cols = st.columns(3)

    examples = [
        "LLM agents 2026",
        "AI coding assistants",
        "Fusion energy progress",
    ]

    for column, example in zip(example_cols, examples):
        with column:
            st.markdown(
                f'<div class="example-box">{example}</div>',
                unsafe_allow_html=True,
            )


# -----------------------------------------------------------------------------
# RIGHT — PIPELINE
# -----------------------------------------------------------------------------

with col_pipeline:

    st.markdown(
        '<div class="section-title">Research Pipeline</div>',
        unsafe_allow_html=True,
    )

    results = st.session_state.results
    running = st.session_state.running

    render_pipeline_card(
        "01",
        "Search Agent",
        "Discovers recent web information",
        pipeline_state(results, running, "search"),
    )

    render_pipeline_card(
        "02",
        "Reader Agent",
        "Extracts useful source content",
        pipeline_state(results, running, "reader"),
    )

    render_pipeline_card(
        "03",
        "Writer Chain",
        "Creates the research report",
        pipeline_state(results, running, "writer"),
    )

    render_pipeline_card(
        "04",
        "Critic Chain",
        "Evaluates report quality",
        pipeline_state(results, running, "critic"),
    )


# =============================================================================
# START PIPELINE
# =============================================================================

if run_btn:

    if not topic.strip():
        st.warning("Please enter a research topic first.")

    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


# =============================================================================
# PIPELINE EXECUTION
# =============================================================================

if st.session_state.running and not st.session_state.done:

    results = {}
    topic_val = st.session_state.topic_input.strip()

    # -------------------------------------------------------------------------
    # STEP 1 — SEARCH
    # -------------------------------------------------------------------------

    try:

        with st.status(
            "🔍  Research pipeline running...",
            expanded=True,
        ) as pipeline_status:

            st.write("Searching for recent and reliable information...")

            search_agent = build_search_agent()

            search_response = search_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            (
                                "Find recent, reliable and detailed "
                                f"information about: {topic_val}"
                            ),
                        )
                    ]
                }
            )

            results["search"] = get_agent_message(search_response)

            st.session_state.results = dict(results)

            # -----------------------------------------------------------------
            # STEP 2 — READER
            # -----------------------------------------------------------------

            st.write("📄 Reading the most relevant source...")

            reader_agent = build_reader_agent()

            reader_response = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            (
                                f"Based on the following search results "
                                f"about '{topic_val}', pick the most relevant "
                                "URL and scrape it for deeper content.\n\n"
                                "Search Results:\n"
                                f"{results['search'][:1200]}"
                            ),
                        )
                    ]
                }
            )

            results["reader"] = get_agent_message(reader_response)

            st.session_state.results = dict(results)

            # -----------------------------------------------------------------
            # STEP 3 — WRITER
            # -----------------------------------------------------------------

            st.write("✍️ Writing the research report...")

            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )

            writer_response = writer_chain.invoke(
                {
                    "topic": topic_val,
                    "research": research_combined,
                }
            )

            results["writer"] = text_from_value(writer_response)

            st.session_state.results = dict(results)

            # -----------------------------------------------------------------
            # STEP 4 — CRITIC
            # -----------------------------------------------------------------

            st.write("🧐 Reviewing report quality...")

            critic_response = critic_chain.invoke(
                {
                    "report": results["writer"],
                }
            )

            results["critic"] = text_from_value(critic_response)

            st.session_state.results = dict(results)

            pipeline_status.update(
                label="✓ Research pipeline complete",
                state="complete",
                expanded=False,
            )

    except Exception as exc:

        st.session_state.running = False
        st.session_state.done = False

        st.error(
            "The research pipeline encountered an error."
        )

        with st.expander("Technical error details"):
            st.code(str(exc))

        st.stop()

    st.session_state.results = results
    st.session_state.running = False
    st.session_state.done = True

    st.rerun()


# =============================================================================
# RESULTS
# =============================================================================

results = st.session_state.results

if results:

    st.markdown(
        '<div class="output-divider"></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Research Output</div>',
        unsafe_allow_html=True,
    )

    # -------------------------------------------------------------------------
    # SEARCH RAW OUTPUT
    # -------------------------------------------------------------------------

    if "search" in results:

        with st.expander(
            "🔍  Search Results · Raw Output",
            expanded=False,
        ):
            st.text(results["search"])


    # -------------------------------------------------------------------------
    # READER RAW OUTPUT
    # -------------------------------------------------------------------------

    if "reader" in results:

        with st.expander(
            "📄  Source Analysis · Raw Output",
            expanded=False,
        ):
            st.text(results["reader"])


    # -------------------------------------------------------------------------
    # FINAL REPORT
    # -------------------------------------------------------------------------

    if "writer" in results:

        st.markdown(
            """
            <div class="report-shell">
                <div class="output-label">
                    📝 Generated Research Report
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Render the actual generated Markdown normally.
        st.markdown(results["writer"])

        st.download_button(
            label="⬇  Download Research Report",
            data=results["writer"],
            file_name=(
                f"insightforge_report_{int(time.time())}.md"
            ),
            mime="text/markdown",
            use_container_width=False,
        )


    # -------------------------------------------------------------------------
    # CRITIC REVIEW
    # -------------------------------------------------------------------------

    if "critic" in results:

        st.markdown(
            """
            <div class="review-shell">
                <div class="output-label review-label">
                    🧐 Quality Review
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(results["critic"])


# =============================================================================
# FOOTER
# =============================================================================

st.markdown(
    """
    <div class="footer-text">
        InsightForge · Multi-Agent Research Workspace · LangChain + Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)