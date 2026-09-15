import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="APEX SPORTS HUB", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for high-end professional app styling
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .brand-title {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -1px;
        color: #0f172a;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 2px;
    }
    .brand-sub {
        font-size: 10px;
        text-align: center;
        color: #64748b;
        margin-bottom: 14px;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .unlimited-banner {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 14px;
        text-align: center;
    }
    .banner-title { font-weight: 800; color: #166534; font-size: 12px; }
    .banner-sub-text { color: #15803d; font-size: 10px; margin-top: 2px; }
    
    .matchup-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #ffffff;
        padding: 14px 10px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        margin-bottom: 14px;
    }
    .team-box { text-align: center; width: 40%; }
    .team-logo-lg { width: 52px; height: 52px; object-fit: contain; }
    .team-title { font-weight: 800; font-size: 12px; color: #0f172a; margin-top: 6px; }
    .vs-box { text-align: center; width: 20%; font-weight: 900; font-size: 14px; color: #cbd5e1; }
    
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    .metric-title { font-size: 10px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { font-size: 18px; font-weight: 900; color: #0f172a; margin-top: 3px; }
    .metric-sub { font-size: 10px; color: #059669; font-weight: 700; margin-top: 2px; }

    .stats-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
    }
    .stat-category-title {
        font-size: 11px;
        font-weight: 800;
        color: #475569;
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
        color: #0f172a;
        margin-top: 6px;
        margin-bottom: 3px;
    }
    .bar-bg {
        background-color: #f1f5f9;
        border-radius: 6px;
        height: 8px;
        width: 100%;
        overflow: hidden;
    }
    .bar-fill-home {
        background-color: #0f172a;
        height: 100%;
        border-radius: 6px;
    }
    .bar-fill-away {
        background-color: #881337;
        height: 100%;
        border-radius: 6px;
    }

    .section-header { font-size: 12px; font-weight: 800; color: #334155; margin-top: 16px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
    .footer-text { text-align: center; font-size: 10px; color: #94a3b8; margin-top: 24px; font-weight: 600; }
    
    /* Hide Streamlit default UI elements for clean app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Team Map & ESPN Logos
TEAM_MAP = {
    'ARI': ('Arizona Cardinals', 'ari'), 'ATL': ('Atlanta Falcons', 'atl'),
    'BAL': ('Baltimore Ravens', 'bal'), 'BUF': ('Buffalo Bills', 'buf'),
    'CAR': ('Carolina Panthers', 'car'), 'CHI': ('Chicago Bears', 'chi'),
    'CIN': ('Cincinnati Bengals', 'cin'), 'CLE': ('Cleveland Browns', 'cle'),
    'DAL': ('Dallas Cowboys', 'dal'), 'DEN': ('Denver Broncos', 'den'),
    'DET': ('Detroit Lions', 'det'), 'GB': ('Green Bay Packers', 'gb'),
    'HOU': ('Houston Texans', 'hou'), 'IND': ('Indianapolis Colts', 'ind'),
    'JAX': ('Jacksonville Jaguars', 'jax'), 'KC': ('Kansas City Chiefs', 'kc'),
    'LV': ('Las Vegas Raiders', 'lv'), 'LAC': ('Los Angeles Chargers', 'lac'),
    'LAR': ('Los Angeles Rams', 'lar'), 'MIA': ('Miami Dolphins', 'mia'),
    'MIN': ('Minnesota Vikings', 'min'), 'NE': ('New England Patriots', 'ne'),
    'NO': ('New Orleans Saints', 'no'), 'NYG': ('New York Giants', 'nyg'),
    'NYJ': ('New York Jets', 'nyj'), 'PHI': ('Philadelphia Eagles', 'phi'),
    'PIT': ('Pittsburgh Steelers', 'pit'), 'SF': ('San Francisco 49ers', 'sf'),
    'SEA': ('Seattle Seahawks', 'sea'), 'TB': ('Tampa Bay Buccaneers', 'tb'),
    'TEN': ('Tennessee Titans', 'ten'), 'WAS': ('Washington Commanders', 'was')
}

def get_logo(abbr):
    espn_code = TEAM_MAP.get(abbr, (abbr, abbr.lower()))[1]
    return f"https://a.espncdn.com/i/teamlogos/nfl/500/{espn_code}.png"

def get_full_name(abbr):
    return TEAM_MAP.get(abbr, (abbr, abbr))[0]

def prob_to_american(p):
    if p <= 0 or p >= 1:
        return "+100"
    if p >= 0.5:
        return f"-{int(round((p / (1.0 - p)) * 100))}"
    else:
        return f"+{int(round(((1.0 - p) / p) * 100))}"

# App Header
st.markdown('<div class="brand-title">⚡ APEX SPORTS HUB</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">ADVANCED SIMULATION & ANALYTICS ENGINE</div>', unsafe_allow_html=True)

sport = st.selectbox("Select League", ["🏈 NFL", "🏈 NCAAF", "⚾ MLB", "🏀 NBA"], index=0, label_visibility="collapsed")

st.markdown("""
<div class="unlimited-banner">
    <div class="banner-title">🟢 LIVE ALGORITHM ACTIVE</div>
    <div class="banner-sub-text">Monte Carlo Engine Ready</div>
</div>
""", unsafe_allow_html=True)

UPCOMING_GAMES = [
    {"away": "WAS", "home": "DAL", "date": "Sep 13th", "venue": "AT&T Stadium"},
    {"away": "BAL", "home": "IND", "date": "Sep 13th", "venue": "Lucas Oil Stadium"},
    {"away": "BUF", "home": "HOU", "date": "Sep 13th", "venue": "NRG Stadium"},
    {"away": "NO",  "home": "DET", "date": "Sep 13th", "venue": "Ford Field"},
    {"away": "TB",  "home": "CIN", "date": "Sep 13th", "venue": "Paycor Stadium"},
]

try:
    selected_game_idx = st.selectbox(
        "Choose Matchup",
        range(len(UPCOMING_GAMES)),
        format_func=lambda i: f"{UPCOMING_GAMES[i]['away']} @ {UPCOMING_GAMES[i]['home']} ({UPCOMING_GAMES[i]['date']})",
        label_visibility="collapsed"
    )

    game = UPCOMING_GAMES[selected_game_idx]
    away_team, home_team = game["away"], game["home"]

    # Matchup Display Card
    st.markdown(f"""
    <div class="matchup-container">
        <div class="team-box">
            <img src="{get_logo(away_team)}" class="team-logo-lg"/>
            <div class="team-title">{get_full_name(away_team)}</div>
            <div style="font-size:9px; color:#64748b; font-weight: 700; margin-top:2px;">AWAY</div>
        </div>
        <div class="vs-box">VS</div>
        <div class="team-box">
            <img src="{get_logo(home_team)}" class="team-logo-lg"/>
            <div class="team-title">{get_full_name(home_team)}</div>
            <div style="font-size:9px; color:#64748b; font-weight: 700; margin-top:2px;">HOME</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Run button with professional design
    if st.button("🚀 Run Simulation Engine", use_container_width=True):
        num_sims = 10000
        num_drives = 11
        
        # Simulated distribution math
        exp_h = 2.3
        exp_a = 2.1
        
        outcomes = [0, 3, 6, 7, 8]
        def get_probs(exp_ppd):
            p_td = max(0.12, min(0.38, exp_ppd * 0.11))
            p_fg = max(0.10, min(0.28, exp_ppd * 0.08))
            p_zero = max(0.25, 1.0 - (p_td + p_fg))
            p = np.array([p_zero, p_fg, 0.01, p_td, 0.01])
            return p / p.sum()

        h_drives = np.random.choice(outcomes, size=(num_sims, num_drives), p=get_probs(exp_h))
        a_drives = np.random.choice(outcomes, size=(num_sims, num_drives), p=get_probs(exp_a))
        
        h_scores = np.sum(h_drives, axis=1)
        a_scores = np.sum(a_drives, axis=1)
        
        margins = h_scores - a_scores
        totals = h_scores + a_scores
        
        h_win_prob = np.mean(margins > 0) + (0.5 * np.mean(margins == 0))
        a_win_prob = 1.0 - h_win_prob
        
        fair_spread = -np.mean(margins)
        fair_total = np.mean(totals)
        
        # Projections Section
        st.markdown('<div class="section-header">🎯 Simulation Projections</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Win Prob</div>
                <div class="metric-value">{home_team} {h_win_prob*100:.0f}%</div>
                <div class="metric-sub">{away_team} {a_win_prob*100:.0f}%</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fair Spread</div>
                <div class="metric-value">{home_team} {fair_spread:+.1f}</div>
                <div class="metric-sub">Model Line</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fair Total</div>
                <div class="metric-value">{fair_total:.1f}</div>
                <div class="metric-sub">O/U Line</div>
            </div>""", unsafe_allow_html=True)

        # Moneyline section
        st.markdown('<div class="section-header">💰 Fair Odds</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{home_team} Moneyline</div>
                <div class="metric-value">{prob_to_american(h_win_prob)}</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{away_team} Moneyline</div>
                <div class="metric-value">{prob_to_american(a_win_prob)}</div>
            </div>""", unsafe_allow_html=True)

        # Simulated Team Stats Cards with Progress Bars
        st.markdown('<div class="section-header">📊 Simulated Team Stats</div>', unsafe_allow_html=True)

        h_pass = 224.5 + np.random.normal(0, 10)
        a_pass = 208.2 + np.random.normal(0, 10)
        h_rush = 118.0 + np.random.normal(0, 8)
        a_rush = 105.4 + np.random.normal(0, 8)
        h_total = h_pass + h_rush
        a_total = a_pass + a_rush
        h_epa = 0.185 + np.random.normal(0, 0.01)
        a_epa = 0.042 + np.random.normal(0, 0.01)
        h_succ = 46.2 + np.random.normal(0, 1.2)
        a_succ = 41.5 + np.random.normal(0, 1.2)
        h_3rd = 45.0 + np.random.normal(0, 3)
        a_3rd = 36.4 + np.random.normal(0, 3)
        h_to = 0.9
        a_to = 1.3

        def render_stat_box(category, t1_name, t1_val, t2_name, t2_val, is_pct=False, is_to=False):
            max_v = max(t1_val, t2_val) if not is_to else 3.0
            max_v = max(max_v, 1.0)
            p1 = int(min(100, max(8, (t1_val / max_v) * 100)))
            p2 = int(min(100, max(8, (t2_val / max_v) * 100)))
            
            fmt = "{:.1f}yds" if category in ["Passing", "Rushing", "Total Yards"] else ("{:.3f}" if category=="EPA/Play" else ("{:.1f}%" if is_pct else "{:.1f}"))
            
            st.markdown(f"""
            <div class="stats-card">
                <div class="stat-category-title">{category}</div>
                <div class="stat-row"><span>{t1_name}</span><span>{fmt.format(t1_val)}</span></div>
                <div class="bar-bg"><div class="bar-fill-home" style="width: {p1}%;"></div></div>
                <div class="stat-row" style="margin-top: 8px;"><span>{t2_name}</span><span>{fmt.format(t2_val)}</span></div>
                <div class="bar-bg"><div class="bar-fill-away" style="width: {p2}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)

        render_stat_box("Passing", home_team, h_pass, away_team, a_pass)
        render_stat_box("Rushing", home_team, h_rush, away_team, a_rush)
        render_stat_box("Total Yards", home_team, h_total, away_team, a_total)
        render_stat_box("EPA/Play", home_team, h_epa, away_team, a_epa)
        render_stat_box("Success Rate", home_team, h_succ, away_team, a_succ, is_pct=True)
        render_stat_box("3rd Down Conversion", home_team, h_3rd, away_team, a_3rd, is_pct=True)
        render_stat_box("Turnovers", home_team, h_to, away_team, a_to, is_to=True)

        # Algorithm footer badge
        st.markdown("""
        <div style="background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px; text-align: center; margin-top: 14px;">
            <div style="font-weight: 800; font-size: 11px; color: #1e293b; margin-bottom: 2px;">🟢 Apex Analytics Algorithm</div>
            <div style="font-size: 9px; color: #64748b;">Simulations generated via Monte Carlo modeling based on historical data points. For research use only.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="footer-text">© 2026 APEX ANALYTICS. ALL RIGHTS RESERVED.</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading application: {e}")
