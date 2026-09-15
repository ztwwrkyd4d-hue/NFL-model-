import streamlit as st
import nflreadpy as nfl
import pandas as pd
import numpy as np

# Page setup
st.set_page_config(page_title="APEX SPORTS HUB", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS for crisp light-mode visibility
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
        font-size: 11px;
        text-align: center;
        color: #64748b;
        margin-bottom: 16px;
        font-weight: 600;
    }
    .unlimited-banner {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 16px;
        text-align: center;
    }
    .banner-title {
        font-weight: 800;
        color: #166534;
        font-size: 14px;
    }
    .banner-sub-text {
        color: #15803d;
        font-size: 11px;
    }
    .game-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .game-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .game-team {
        font-weight: 700;
        font-size: 13px;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .game-logo {
        width: 26px;
        height: 26px;
        object-fit: contain;
    }
    .game-meta {
        font-size: 11px;
        color: #64748b;
        margin-top: 6px;
    }
    .matchup-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #ffffff;
        padding: 14px 10px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 16px;
    }
    .team-box { text-align: center; width: 40%; }
    .team-logo-lg { width: 60px; height: 60px; object-fit: contain; }
    .team-title { font-weight: 800; font-size: 12px; color: #0f172a; margin-top: 4px; }
    .vs-box { text-align: center; width: 20%; font-weight: 900; font-size: 16px; color: #94a3b8; }
    
    /* Custom light-mode safe data boxes to prevent invisible text */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-title { font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; }
    .metric-value { font-size: 18px; font-weight: 900; color: #0f172a; margin-top: 4px; }
    .metric-sub { font-size: 11px; color: #059669; font-weight: 600; margin-top: 2px; }

    .stat-label { font-weight: 700; color: #334155; font-size: 12px; margin-top: 10px; }
    .footer-text { text-align: center; font-size: 10px; color: #94a3b8; margin-top: 30px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Team Map & Logos
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
    if p >= 0.5:
        return f"-{int(round((p / (1.0 - p)) * 100))}"
    else:
        return f"+{int(round(((1.0 - p) / p) * 100))}"

@st.cache_data(ttl=86400)
def load_data():
    df = nfl.load_pbp(seasons=[2025])
    if not isinstance(df, pd.DataFrame):
        df = df.to_pandas()
    scrimmage = df[df['play_type'].isin(['pass', 'run']) & df['epa'].notna()].copy()
    
    avg_plays = 5.8
    off_epa = scrimmage.groupby('posteam')['epa'].mean()
    def_epa = scrimmage.groupby('defteam')['epa'].mean()
    
    pass_plays = scrimmage[scrimmage['play_type'] == 'pass']
    run_plays = scrimmage[scrimmage['play_type'] == 'run']
    
    off_pass_yds = pass_plays.groupby('posteam')['yards_gained'].mean() * 32.0
    off_rush_yds = run_plays.groupby('posteam')['yards_gained'].mean() * 26.0
    
    return pd.DataFrame({
        'off_epa_drive': off_epa * avg_plays - (off_epa * avg_plays).mean(),
        'def_epa_drive': def_epa * avg_plays - (def_epa * avg_plays).mean(),
        'off_epa_play': off_epa,
        'pass_yds': off_pass_yds,
        'rush_yds': off_rush_yds
    }).fillna(0)

# Branding Header
st.markdown('<div class="brand-title">⚡ APEX ALGO HUB</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-sub">POWERED BY APEX ANALYTICS ENGINE</div>', unsafe_allow_html=True)

# League Selector
sport = st.selectbox("Select League", ["🏈 NFL", "🏈 NCAAF", "⚾ MLB", "🏀 NBA"], index=0)

# Banner
st.markdown("""
<div class="unlimited-banner">
    <div class="banner-title">🟢 UNLIMITED SIMULATIONS ACTIVE</div>
    <div class="banner-sub-text">50,000 Monte Carlo Iterations Enabled</div>
</div>
""", unsafe_allow_html=True)

UPCOMING_GAMES = [
    {"away": "WAS", "home": "PHI", "date": "Sep 13th", "time": "1:00 PM EST", "venue": "Lincoln Financial Field"},
    {"away": "BAL", "home": "IND", "date": "Sep 13th", "time": "1:00 PM EST", "venue": "Lucas Oil Stadium"},
    {"away": "BUF", "home": "HOU", "date": "Sep 13th", "time": "1:00 PM EST", "venue": "NRG Stadium"},
    {"away": "NO",  "home": "DET", "date": "Sep 13th", "time": "1:00 PM EST", "venue": "Ford Field"},
    {"away": "TB",  "home": "CIN", "date": "Sep 13th", "time": "4:25 PM EST", "venue": "Paycor Stadium"},
]

try:
    epa_df = load_data()

    st.markdown("### 🏈 NFL Upcoming Games")
    
    selected_game_idx = st.selectbox(
        "Choose a matchup:",
        range(len(UPCOMING_GAMES)),
        format_func=lambda i: f"{UPCOMING_GAMES[i]['away']} @ {UPCOMING_GAMES[i]['home']} — {UPCOMING_GAMES[i]['date']}"
    )

    game = UPCOMING_GAMES[selected_game_idx]
    away_team, home_team = game["away"], game["home"]

    # Matchup Display Header
    st.markdown(f"""
    <div class="matchup-container">
        <div class="team-box">
            <img src="{get_logo(away_team)}" class="team-logo-lg"/>
            <div class="team-title">{get_full_name(away_team)}</div>
            <div style="font-size:10px; color:#64748b;">{away_team}</div>
        </div>
        <div class="vs-box">VS</div>
        <div class="team-box">
            <img src="{get_logo(home_team)}" class="team-logo-lg"/>
            <div class="team-title">{get_full_name(home_team)}</div>
            <div style="font-size:10px; color:#64748b;">{home_team}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Run Algorithm Simulation", use_container_width=True):
        num_sims = 50000
        num_drives = 11
        
        h_off = epa_df.loc[home_team, 'off_epa_drive'] if home_team in epa_df.index else 0
        h_def = epa_df.loc[home_team, 'def_epa_drive'] if home_team in epa_df.index else 0
        a_off = epa_df.loc[away_team, 'off_epa_drive'] if away_team in epa_df.index else 0
        a_def = epa_df.loc[away_team, 'def_epa_drive'] if away_team in epa_df.index else 0
        
        exp_h = 2.0 + (h_off - a_def) + (1.8 / num_drives)
        exp_a = 2.0 + (a_off - h_def)
        
        outcomes = [0, 3, 6, 7, 8]
        def get_probs(exp_ppd):
            p_td = max(0.10, min(0.40, exp_ppd * 0.11))
            p_fg = max(0.08, min(0.30, exp_ppd * 0.07))
            p_zero = max(0.30, 1.0 - (p_td + p_fg))
            p = np.array([p_zero, p_fg, 0.01, p_td, 0.01])
            return p / p.sum()

        h_drives = np.random.choice(outcomes, size=(num_sims, num_drives), p=get_probs(exp_h))
        a_drives = np.random.choice(outcomes, size=(num_sims, num_drives), p=get_probs(exp_a))
        
        h_scores = np.sum(h_drives, axis=1)
        a_scores = np.sum(a_drives, axis=1)
        
        margins = h_scores - a_scores
        totals = h_scores + a_scores
        
        h_win_prob = np.mean(margins > 0)
        a_win_prob = 1.0 - h_win_prob
        
        fair_spread = -np.mean(margins)
        fair_total = np.mean(totals)
        
        st.markdown("### 🎯 SIMULATION PROJECTIONS")
        
        # Custom mobile-safe HTML cards for projections
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Win Probability</div>
                <div class="metric-value">{home_team} {h_win_prob*100:.1f}%</div>
                <div class="metric-sub">{away_team} {a_win_prob*100:.1f}%</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fair Spread</div>
                <div class="metric-value">{home_team} {fair_spread:+.1f}</div>
                <div class="metric-sub">Model Line</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Fair Total</div>
                <div class="metric-value">{fair_total:.1f} pts</div>
                <div class="metric-sub">O/U Line</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("### 💰 FAIR MONEYLINE ODDS")
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{away_team} Fair ML</div>
                <div class="metric-value">{prob_to_american(a_win_prob)}</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{home_team} Fair ML</div>
                <div class="metric-value">{prob_to_american(h_win_prob)}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("### 📊 SIMULATED GAME METRICS")
        h_pass = max(120.0, epa_df.loc[home_team, 'pass_yds'] + np.random.normal(0, 12)) if home_team in epa_df.index else 220
        a_pass = max(120.0, epa_df.loc[away_team, 'pass_yds'] + np.random.normal(0, 12)) if away_team in epa_df.index else 220
        
        st.markdown(f'<div class="stat-label">Passing Yards: {away_team} ({a_pass:.0f} yds) vs {home_team} ({h_pass:.0f} yds)</div>', unsafe_allow_html=True)
        st.progress(float(h_pass / (h_pass + a_pass)))

    st.markdown('<div class="footer-text">© 2026 APEX ANALYTICS. ALL RIGHTS RESERVED.<br>Powered by Apex Simulation Engine</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Engine loading... ({e})")
