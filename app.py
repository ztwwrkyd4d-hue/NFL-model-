st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        overflow-y: auto !important;
    }
    
    .stApp {
        background-color: #0b0f19;
    }

    .brand-container {
        text-align: center;
        padding: 15px 0 5px 0;
        background: linear-gradient(180deg, #111827 0%, #0b0f19 100%);
        border-bottom: 1px solid #1f2937;
        margin-bottom: 15px;
    }
    .brand-title {
        font-size: 28px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #ffffff;
        text-transform: uppercase;
    }
    .brand-title span {
        color: #10b981;
    }
    .brand-sub {
        font-size: 10px;
        color: #9ca3af;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 2px;
    }
    .terminal-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 11px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 14px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .matchup-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #111827;
        padding: 16px 10px;
        border-radius: 14px;
        border: 1px solid #1f2937;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
        margin-bottom: 14px;
    }
    .team-box { text-align: center; width: 40%; }
    .team-logo-lg { width: 56px; height: 56px; object-fit: contain; }
    .team-title { font-weight: 800; font-size: 13px; color: #ffffff; margin-top: 6px; }
    .vs-box { text-align: center; width: 20%; font-weight: 900; font-size: 14px; color: #4b5563; }
    
    .metric-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 14px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title { font-size: 10px; font-weight: 700; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 18px; font-weight: 900; color: #ffffff; margin-top: 4px; }
    .metric-sub { font-size: 10px; color: #34d399; font-weight: 700; margin-top: 2px; }

    .stats-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .stat-category-title {
        font-size: 11px;
        font-weight: 800;
        color: #9ca3af;
        text-align: center;
        text-transform: uppercase;
        margin-bottom: 10px;
        letter-spacing: 0.5px;
    }
    .stat-row {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 6px;
        margin-bottom: 3px;
    }
    .bar-bg {
        background-color: #1f2937;
        border-radius: 6px;
        height: 8px;
        width: 100%;
        overflow: hidden;
    }
    .bar-fill-home {
        background-color: #3b82f6;
        height: 100%;
        border-radius: 6px;
    }
    .bar-fill-away {
        background-color: #ef4444;
        height: 100%;
        border-radius: 6px;
    }

    .sharp-box {
        background: linear-gradient(135deg, #064e3b 0%, #022c22 100%);
        border: 1px solid #059669;
        border-radius: 12px;
        padding: 14px;
        margin-top: 14px;
        margin-bottom: 14px;
    }
    .sharp-title { font-weight: 900; color: #34d399; font-size: 12px; text-transform: uppercase; margin-bottom: 4px; }
    .sharp-text { color: #d1fae5; font-size: 11px; line-height: 1.4; }

    .section-header { font-size: 12px; font-weight: 800; color: #e5e7eb; margin-top: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
    .footer-text { text-align: center; font-size: 10px; color: #6b7280; margin-top: 24px; margin-bottom: 60px; font-weight: 600; }
    
    /* CRITICAL MOBILE DROPDOWN FIXES: Force layer stacking above everything */
    div.stSelectbox > div > div { background-color: #111827; color: white; border: 1px solid #374151; }
    
    div[data-baseweb="popover"] {
        z-index: 999999 !important;
        background-color: #111827 !important;
        border: 1px solid #374151 !important;
        position: absolute !important;
    }
    
    div[data-baseweb="menu"], ul[data-baseweb="menu"] {
        background-color: #111827 !important;
        color: white !important;
        max-height: 250px !important;
        overflow-y: auto !important;
    }
    
    li[data-baseweb="option"] {
        background-color: #111827 !important;
        color: white !important;
    }
    
    li[data-baseweb="option"]:hover {
        background-color: #1f2937 !important;
        color: #34d399 !important;
    }
    
    div.stButton > button { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; font-weight: 900; border: none; border-radius: 10px; padding: 12px; text-transform: uppercase; letter-spacing: 1px; width: 100%; }
    div.stButton > button:hover { background: linear-gradient(135deg, #34d399 0%, #10b981 100%); color: #000; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
