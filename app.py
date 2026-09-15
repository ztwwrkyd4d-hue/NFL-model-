import streamlit as st
import nflreadpy as nfl
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(page_title="The Pick Don Clone", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to force mobile-friendly flexbox layouts and custom card theme
st.markdown("""
<style>
    .stApp {
        background-color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    .brand-header {
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #0f172a;
        text-transform: uppercase;
        text-align: center;
        margin-bottom: 16px;
    }
    .unlimited-banner {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 20px;
        text-align: center;
    }
    .banner-title {
        font-weight: 800;
        color: #166534;
        font-size: 15px;
    }
    .banner-sub {
        color: #15803d;
        font-size: 12px;
    }
    /* Mobile-safe side-by-side flexbox header */
    .matchup-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        background-color: #ffffff;
        padding: 16px 10px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .team-box {
        text-align: center;
        width: 40%;
    }
    .team-logo {
        width: 65px;
        height: 65px;
        object-fit: contain;
    }
    .team-title {
        font-weight: 800;
        font-size: 13px;
        color: #0f172a;
        margin-top: 6px;
        line-height: 1.2;
    }
    .team-abbr {
        font-size: 11px;
        color: #64748b;
        font-weight: 600;
    }
    .vs-box {
        text-align: center;
        width: 20%;
    }
    .vs-text {
        font-weight: 900;
        font-size: 18px;
        color: #94a3b8;
    }
    .stat-label {
        font-weight: 700;
        color: #334155;
        font-size: 13px;
        margin-top: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Team Name & ESPN Logo Mapping
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

def prob_to_american(p):
    if p >= 0.5:
        return f"-{int(round((p / (1.0 - p)) * 100))}"
    else:
        return f"+{int(round(((1.0 - p) / p) * 100))}"

# App Header
st.markdown('<div class="brand-header">⚡ THE PICK DON ENGINE</div>', unsafe_allow_html=True)

# Unlimited Banner Card
st.markdown("""
<div class="unlimited-banner">
    <div class="banner-title">🟢 UNLIMITED SIMULATIONS ACTIVE</div>
    <div class="banner-sub">Monte Carlo 50,000 Iteration Engine</div>
</div>
""", unsafe_allow_html=True)

try:
    epa_df = load_data()
    teams = sorted(list(epa_df.index))

    col1, col2 = st.columns(2)
    with col1:
        away_team = st.selectbox("Away Team", teams, index=teams.index("WAS") if "WAS" in teams else 0)
    with col2:
        home_team = st.selectbox("Home Team", teams, index=teams.index("PHI") if "PHI" in teams else 1)

    # Pure HTML Flexbox header guarantees horizontal layout on mobile
    st.markdown(f"""
    <div class="matchup-container">
        <div class="team-box">
            <img src="{get_logo(away_team)}" class="team-logo"/>
            <div class="team-title">{get_full_name(away_team)}</div>
            <div class="team-abbr">{away_team}</div>
        </div>
        <div class="vs-box">
            <div class="vs-text">VS</div>
        </div>
        <div class="team-box">
            <img src="{get_logo(home_team)}" class="team-logo"/>
            <div class="team-title">{get_full_name(home_team)}</div>
            <div class="team-abbr">{home_team}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Run Algorithm Simulation", use_container_width=True):
        num_sims = 50000
        num_drives = 11
        
        h_off = epa_df.loc[home_team, 'off_epa_drive']
        h_def = epa_df.loc[home_team, 'def_epa_drive']
        a_off = epa_df.loc[away_team, 'off_epa_drive']
        a_def = epa_df.loc[away_team, 'def_epa_drive']
        
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
        
        spread_ci = (np.percentile(-margins, 2.5), np.percentile(-margins, 97.5))
        total_ci = (np.percentile(totals, 2.5), np.percentile(totals, 97.5))
        
        st.markdown("### 🎯 SIMULATION PROJECTIONS")
        
        b1, b2, b3 = st.columns(3)
        with b1:
            st.metric("Win Probability", f"{home_team} {h_win_prob*100:.1f}%", f"{away_team} {a_win_prob*100:.1f}%")
        with b2:
            st.metric("Fair Spread", f"{home_team} {fair_spread:+.1f}", f"95% CI: [{spread_ci[0]:.1f}, {spread_ci[1]:.1f}]")
        with b3:
            st.metric("Fair Total (O/U)", f"{fair_total:.1f} pts", f"95% CI: [{total_ci[0]:.1f}, {total_ci[1]:.1f}]")

        st.markdown("### 💰 FAIR MONEYLINE ODDS")
        m1, m2 = st.columns(2)
        with m1:
            st.metric(f"{away_team} Fair ML", prob_to_american(a_win_prob))
        with m2:
            st.metric(f"{home_team} Fair ML", prob_to_american(h_win_prob))

        st.markdown("### 📊 SIMULATED GAME METRICS")
        
        h_pass = max(120.0, epa_df.loc[home_team, 'pass_yds'] + np.random.normal(0, 12))
        a_pass = max(120.0, epa_df.loc[away_team, 'pass_yds'] + np.random.normal(0, 12))
        h_rush = max(60.0, epa_df.loc[home_team, 'rush_yds'] + np.random.normal(0, 8))
        a_rush = max(60.0, epa_df.loc[away_team, 'rush_yds'] + np.random.normal(0, 8))
        
        st.markdown(f'<div class="stat-label">Passing Yards: {away_team} ({a_pass:.0f} yds) vs {home_team} ({h_pass:.0f} yds)</div>', unsafe_allow_html=True)
        st.progress(float(h_pass / (h_pass + a_pass)))
        
        st.markdown(f'<div class="stat-label">Rushing Yards: {away_team} ({a_rush:.0f} yds) vs {home_team} ({h_rush:.0f} yds)</div>', unsafe_allow_html=True)
        st.progress(float(h_rush / (h_rush + a_rush)))
        
        st.markdown(f'<div class="stat-label">Offensive EPA/Play: {away_team} ({epa_df.loc[away_team, "off_epa_play"]:.3f}) vs {home_team} ({epa_df.loc[home_team, "off_epa_play"]:.3f})</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Loading engine data... ({e})")
