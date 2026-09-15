import streamlit as st
import nflreadpy as nfl
import pandas as pd
import numpy as np

st.set_page_config(page_title="The Pick Don Clone", layout="wide")
st.title("🎯 Betting Analysis Engine")

@st.cache_data(ttl=86400)
def load_data():
    df = nfl.load_pbp(seasons=[2025])
    if not isinstance(df, pd.DataFrame):
        df = df.to_pandas()
    scrimmage = df[df['play_type'].isin(['pass', 'run']) & df['epa'].notna()].copy()
    
    avg_plays = 5.8
    off_epa = scrimmage.groupby('posteam')['epa'].mean()
    def_epa = scrimmage.groupby('defteam')['epa'].mean()
    
    # Estimate yards per play metrics
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

try:
    epa_df = load_data()
    teams = sorted(list(epa_df.index))

    col1, col2 = st.columns(2)
    with col1:
        away_team = st.selectbox("Away Team", teams, index=teams.index("WAS") if "WAS" in teams else 0)
    with col2:
        home_team = st.selectbox("Home Team", teams, index=teams.index("DAL") if "DAL" in teams else 1)

    if st.button("Run Betting & Stat Analysis"):
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
        
        # Fair Lines Calculations
        fair_spread = -np.mean(margins)
        fair_total = np.mean(totals)
        
        spread_ci = (np.percentile(-margins, 2.5), np.percentile(-margins, 97.5))
        total_ci = (np.percentile(totals, 2.5), np.percentile(totals, 97.5))
        
        st.markdown("---")
        st.header("🎯 BETTING ANALYSIS")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Win Probability")
            st.write(f"**{home_team}:** {h_win_prob*100:.1f}% | **{away_team}:** {a_win_prob*100:.1f}%")
            
            st.subheader("Fair Moneyline Odds")
            st.write(f"**{home_team}:** {prob_to_american(h_win_prob)} | **{away_team}:** {prob_to_american(a_win_prob)}")
            
        with c2:
            st.metric("Fair Total (Over/Under)", f"{fair_total:.1f}", f"CI: {total_ci[0]:.1f} to {total_ci[1]:.1f}")
            st.metric("Fair Spread", f"{home_team} {fair_spread:+.2f}", f"CI: {spread_ci[0]:.1f} to {spread_ci[1]:.1f}")

        st.markdown("---")
        st.header("📊 SIMULATED TEAM STATS")
        
        h_pass = max(100.0, epa_df.loc[home_team, 'pass_yds'] + np.random.normal(0, 10))
        a_pass = max(100.0, epa_df.loc[away_team, 'pass_yds'] + np.random.normal(0, 10))
        h_rush = max(50.0, epa_df.loc[home_team, 'rush_yds'] + np.random.normal(0, 8))
        a_rush = max(50.0, epa_df.loc[away_team, 'rush_yds'] + np.random.normal(0, 8))
        
        st.write(f"**Passing Yards:** {home_team} `{h_pass:.1f} yds` vs {away_team} `{a_pass:.1f} yds`")
        st.progress(float(h_pass / (h_pass + a_pass)))
        
        st.write(f"**Rushing Yards:** {home_team} `{h_rush:.1f} yds` vs {away_team} `{a_rush:.1f} yds`")
        st.progress(float(h_rush / (h_rush + a_rush)))
        
        st.write(f"**EPA/Play:** {home_team} `{epa_df.loc[home_team, 'off_epa_play']:.3f}` vs {away_team} `{epa_df.loc[away_team, 'off_epa_play']:.3f}`")

except Exception as e:
    st.error(f"Loading engine data... ({e})")
