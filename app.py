import streamlit as st
import base64
from dashboard import show_dashboard

st.set_page_config(
    page_title="Fake News Detection — ML Comparative Study",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Encode background image ──────────────────────────────────────────────────
def get_base64_bg(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

bg_data = get_base64_bg("assets/bkg.jpg")
bg_css = ""
if bg_data:
    bg_css = f"""
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bg_data}");
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    .main {{
        background: transparent !important;
    }}
    [data-testid="stAppViewContainer"] {{
        background: rgba(0,0,0,0.15) !important;
    }}
    [data-testid="stAppViewContainer"] > section:first-child {{
        background: transparent !important;
    }}
    """

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

/* Reset & base */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
}}

.main .block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}

/* Background image */
{bg_css}

/* Full page overlay for readability */
[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(160deg,
        rgba(5, 4, 20, 0.82) 0%,
        rgba(20, 5, 40, 0.78) 40%,
        rgba(10, 3, 30, 0.80) 100%
    );
    pointer-events: none;
    z-index: 0;
}}

[data-testid="stAppViewContainer"] > * {{
    position: relative;
    z-index: 1;
}}

/* ── LANDING PAGE ── */

.hero-wrapper {{
    background: transparent;
    min-height: auto;
    padding: 0;
    position: relative;
    overflow: hidden;
}}

.hero-wrapper::before {{
    content: '';
    position: absolute;
    top: -40%;
    right: -20%;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(168,85,247,0.14) 0%, transparent 70%);
    pointer-events: none;
}}

.hero-wrapper::after {{
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(236,72,153,0.10) 0%, transparent 70%);
    pointer-events: none;
}}

.hero-inner {{
    max-width: 900px;
    margin: 0 auto;
    padding: 40px 40px 40px;
    position: relative;
    z-index: 1;
}}

.eyebrow {{
    display: inline-block;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #d8b4fe;
    background: rgba(168,85,247,0.12);
    border: 1px solid rgba(168,85,247,0.30);
    padding: 6px 14px;
    border-radius: 4px;
    margin-bottom: 28px;
}}

.hero-title {{
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 700;
    line-height: 1.12;
    color: #f5f0ff;
    letter-spacing: -0.02em;
    margin-bottom: 12px;
}}

.hero-title span {{
    background: linear-gradient(135deg, #c084fc 0%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.hero-subtitle {{
    font-size: 15px;
    font-weight: 400;
    color: #c4b5d8;
    letter-spacing: 0.01em;
    margin-bottom: 40px;
    line-height: 1.6;
}}

.divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(192,132,252,0.30), transparent);
    margin: 40px 0;
}}

.overview-text {{
    font-size: 15px;
    color: #b8a8d0;
    line-height: 1.8;
    max-width: 720px;
}}

.stats-row {{
    display: flex;
    gap: 20px;
    margin: 48px 0;
    flex-wrap: wrap;
}}

.stat-card {{
    flex: 1;
    min-width: 160px;
    background: rgba(168,85,247,0.07);
    border: 1px solid rgba(168,85,247,0.20);
    border-radius: 10px;
    padding: 24px 28px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: border-color 0.2s, background 0.2s;
}}

.stat-card:hover {{
    border-color: rgba(244,114,182,0.40);
    background: rgba(244,114,182,0.08);
}}

.stat-value {{
    font-size: 36px;
    font-weight: 700;
    color: #f5f0ff;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 6px;
}}

.stat-label {{
    font-size: 12px;
    font-weight: 500;
    color: #9d8cb8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

.tech-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 32px;
}}

.tech-badge {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    font-weight: 500;
    color: #d8b4fe;
    background: rgba(168,85,247,0.08);
    border: 1px solid rgba(168,85,247,0.22);
    padding: 5px 12px;
    border-radius: 4px;
    letter-spacing: 0.04em;
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}}

/* ── CTA button (Streamlit button override) ── */
.stButton > button {{
    background: linear-gradient(135deg, #7c3aed 0%, #be185d 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    padding: 14px 36px !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 28px rgba(168,85,247,0.40) !important;
}}

.stButton > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 36px rgba(244,114,182,0.45) !important;
}}

/* ── DASHBOARD GLOBAL (used by dashboard.py) ── */

.db-wrapper {{
    background: transparent;
    min-height: auto;
    padding: 0;
}}

.db-topbar {{
    background: rgba(10,5,25,0.70);
    border-bottom: 1px solid rgba(168,85,247,0.18);
    padding: 18px 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}}

.db-logo {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    font-weight: 500;
    color: #c084fc;
    letter-spacing: 0.06em;
}}

.db-title {{
    font-size: 18px;
    font-weight: 600;
    color: #f5f0ff;
    letter-spacing: -0.01em;
}}

.db-content {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 40px 40px 80px;
}}

.section-eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c084fc;
    margin-bottom: 8px;
}}

.section-title {{
    font-size: 26px;
    font-weight: 700;
    color: #f5f0ff;
    letter-spacing: -0.02em;
    margin-bottom: 4px;
}}

.section-desc {{
    font-size: 14px;
    color: #8b7aa8;
    margin-bottom: 32px;
    line-height: 1.6;
}}

/* Metric cards */
.metric-grid {{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 32px;
}}

.metric-card {{
    flex: 1;
    min-width: 140px;
    background: rgba(168,85,247,0.07);
    border: 1px solid rgba(168,85,247,0.18);
    border-radius: 10px;
    padding: 20px 22px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: border-color 0.2s;
}}

.metric-card:hover {{
    border-color: rgba(244,114,182,0.35);
}}

.metric-card-value {{
    font-size: 28px;
    font-weight: 700;
    color: #f5f0ff;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 6px;
}}

.metric-card-label {{
    font-size: 11px;
    font-weight: 500;
    color: #7c6d98;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}}

.metric-card-accent  {{ border-top: 2px solid #9333ea; }}
.metric-card-accent2 {{ border-top: 2px solid #ec4899; }}
.metric-card-accent3 {{ border-top: 2px solid #a855f7; }}
.metric-card-accent4 {{ border-top: 2px solid #f472b6; }}

/* Best model banner */
.best-banner {{
    background: linear-gradient(135deg, rgba(168,85,247,0.10) 0%, rgba(236,72,153,0.10) 100%);
    border: 1px solid rgba(168,85,247,0.30);
    border-radius: 10px;
    padding: 18px 24px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 12px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}}

.best-banner-icon {{ font-size: 20px; }}
.best-banner-text {{ font-size: 15px; font-weight: 600; color: #f3e8ff; }}
.best-banner-sub  {{ font-size: 13px; color: #d8b4fe; margin-top: 2px; }}

/* Nav tabs */
.nav-strip {{
    display: flex;
    gap: 4px;
    background: rgba(168,85,247,0.06);
    border: 1px solid rgba(168,85,247,0.14);
    border-radius: 10px;
    padding: 5px;
    margin-bottom: 36px;
}}

/* Methodology pipeline */
.pipeline-step {{
    display: flex;
    align-items: flex-start;
    gap: 20px;
    margin-bottom: 8px;
    position: relative;
}}

.pipeline-num {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #c084fc;
    background: rgba(168,85,247,0.10);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 4px;
    padding: 3px 8px;
    white-space: nowrap;
    margin-top: 14px;
}}

.pipeline-card {{
    flex: 1;
    background: rgba(30,10,60,0.55);
    border: 1px solid rgba(168,85,247,0.16);
    border-radius: 10px;
    padding: 18px 22px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: border-color 0.2s;
}}

.pipeline-card:hover {{ border-color: rgba(244,114,182,0.30); }}

.pipeline-card-title {{
    font-size: 14px;
    font-weight: 600;
    color: #ede9fe;
    margin-bottom: 6px;
}}

.pipeline-card-desc {{
    font-size: 13px;
    color: #8b7aa8;
    line-height: 1.6;
}}

.pipeline-arrow {{
    text-align: center;
    color: #6b5a88;
    font-size: 16px;
    margin: 4px 0 4px 76px;
}}

/* Conclusion */
.conclusion-card {{
    background: linear-gradient(135deg, rgba(124,58,237,0.08) 0%, rgba(190,24,93,0.08) 100%);
    border: 1px solid rgba(168,85,247,0.25);
    border-radius: 12px;
    padding: 32px 36px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}}

.conclusion-card-title {{
    font-size: 13px;
    font-weight: 600;
    color: #c084fc;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 20px;
}}

.conclusion-row {{
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid rgba(168,85,247,0.10);
    align-items: center;
}}

.conclusion-row:last-child {{ border-bottom: none; }}
.conclusion-key {{ font-size: 13px; color: #8b7aa8; font-weight: 500; }}
.conclusion-val {{ font-size: 14px; color: #ede9fe; font-weight: 600; font-family: 'IBM Plex Mono', monospace; }}

.finding-card {{
    background: rgba(30,10,60,0.50);
    border: 1px solid rgba(168,85,247,0.15);
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 12px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}}

.finding-card-label {{
    font-size: 11px;
    font-weight: 600;
    color: #c084fc;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 8px;
}}

.finding-card-text {{
    font-size: 14px;
    color: #b8a8d0;
    line-height: 1.7;
}}

/* Plotly chart container */
.chart-shell {{
    background: rgba(20,8,45,0.55);
    border: 1px solid rgba(168,85,247,0.14);
    border-radius: 12px;
    padding: 8px;
    margin-bottom: 24px;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}}

/* Streamlit dataframe theming */
.stDataFrame {{
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid rgba(168,85,247,0.15) !important;
}}

/* Streamlit native metric widget */
[data-testid="stMetric"] {{
    background: rgba(168,85,247,0.07) !important;
    border: 1px solid rgba(168,85,247,0.18) !important;
    border-radius: 10px !important;
    padding: 16px 18px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
}}

[data-testid="stMetricLabel"] {{
    color: #8b7aa8 !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}

[data-testid="stMetricValue"] {{
    color: #f5f0ff !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}}

/* Select box */
.stSelectbox label {{
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #8b7aa8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}}

[data-testid="stSelectbox"] > div > div {{
    background: rgba(30,10,60,0.60) !important;
    border: 1px solid rgba(168,85,247,0.22) !important;
    border-radius: 8px !important;
    color: #ede9fe !important;
    backdrop-filter: blur(8px) !important;
    -webkit-backdrop-filter: blur(8px) !important;
}}

/* Download button */
.stDownloadButton > button {{
    background: rgba(168,85,247,0.10) !important;
    border: 1px solid rgba(168,85,247,0.25) !important;
    color: #d8b4fe !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}}

.stDownloadButton > button:hover {{
    background: rgba(168,85,247,0.18) !important;
    border-color: rgba(244,114,182,0.40) !important;
}}

/* HR dividers */
hr {{
    border-color: rgba(168,85,247,0.15) !important;
}}
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── HOME PAGE ────────────────────────────────────────────────────────────────
if st.session_state.page == "home":

    st.markdown('<div class="hero-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="hero-inner">', unsafe_allow_html=True)

    st.markdown('<div class="eyebrow">Final Year Project · Machine Learning</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-title">
        Machine Learning based Comparative study of <br>
        <span>Fake News Detection</span>
    </div>
    <div class="hero-subtitle">
        A Comparative Study of Machine Learning Models — evaluating feature extraction,<br>
        dimensionality reduction, and classification performance.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="overview-text">
        The rapid spread of misinformation through digital platforms has made fake news detection
        a critical research problem. This project presents a systematic comparison of seven
        machine learning classifiers across multiple feature engineering pipelines — measuring
        each combination against five standard evaluation metrics to identify the most effective
        approach for automated fake news identification.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">7</div>
            <div class="stat-label">ML Models</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">6</div>
            <div class="stat-label">Feature Techniques</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">5</div>
            <div class="stat-label">Evaluation Metrics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="tech-grid">
        <span class="tech-badge">TF-IDF</span>
        <span class="tech-badge">Entropy Feature Selection</span>
        <span class="tech-badge">PCA</span>
        <span class="tech-badge">SVD</span>
        <span class="tech-badge">Logistic Regression</span>
        <span class="tech-badge">SVM</span>
        <span class="tech-badge">Random Forest</span>
        <span class="tech-badge">MLP</span>
        <span class="tech-badge">KNN</span>
        <span class="tech-badge">J48</span>
        <span class="tech-badge">PART</span>
    </div>
    """, unsafe_allow_html=True)


    st.markdown("<br><br>", unsafe_allow_html=True)

    col_l, col_btn, col_r = st.columns([1.5, 1, 1.5])
    with col_btn:
        if st.button("View Dashboard →", width="stretch"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# ── DASHBOARD PAGE ───────────────────────────────────────────────────────────
elif st.session_state.page == "dashboard":
    show_dashboard()