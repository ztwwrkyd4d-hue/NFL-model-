import streamlit as st
import nflreadpy as nfl
import pandas as pd
import numpy as np

st.set_page_config(page_title="NFL Simulation Model", layout="wide")
st.title("🏈 NFL Matchup Simulation Engine")

@st.cache_data(ttl=86400)
def load_data():
    df = nfl.load_pbp(seasons=[2025])
    if not isinstance(df, pd.DataFrame):
        df = df.to_pandas()
    scrimmage = df[df['play_type'].isin(['pass', 'run']) & df['epa'].notna()].copy()
    
    avg_plays = 5.8
    off_epa = scrimmage.groupby('posteam')['epa'].mean() * avg_plays
    def_epa = scrimmage.groupby('defteam')['epa'].mean() * avg_plays
    
    return pd.DataFrame({
        'off_epa_drive': off_epa - off_epa.mean(),
        'def_epa_drive': def_epa - def_epa.mean()
    })

try:
    epa_df = load_data()
    teams = sorted(list(epa_df.index))

    col1, col2 = st.columns(2)
    with col1:
        away_team = st.selectbox("Away Team", teams, index=teams.index("WAS") if "WAS" in teams else 0)
    with col2:
        home_team = st.selectbox("Home Team", teams, index=teams.index("DAL") if "DAL" in teams else 1)

    spread_input = st.number_input("Market Spread (Home Team)", value=-3.5, step=0.5)

    if st.button("Run Simulation"):
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
        margin = h_scores - a_scores
        
        h_win_prob = np.mean(margin > 0)
        cover_prob = np.mean(margin > -spread_input)
        
        st.subheader("Simulation Analysis")
        st.metric("Predicted Score", f"{away_team} {np.mean(a_scores):.1f} - {np.mean(h_scores):.1f} {home_team}")
        st.write(f"**{home_team} Win Probability:** {h_win_prob * 100:.1f}%")
        st.write(f"**{home_team} Cover Spread ({spread_input}):** {cover_prob * 100:.1f}%")

except Exception as e:
    st.error(f"Loading data... ({e})")
