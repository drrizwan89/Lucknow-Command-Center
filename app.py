import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob

# --- PAGE CONFIG ---
st.set_page_config(page_title="LKO Executive Command", layout="wide", initial_sidebar_state="collapsed")

# --- EXECUTIVE PROFESSIONAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=Roboto+Mono:wght@400;700&display=swap');

    .stApp { background-color: #0f172a; color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Professional Glass Cards */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px; padding: 20px; text-align: center;
        backdrop-filter: blur(8px); transition: all 0.2s ease;
    }
    .metric-card:hover { border: 1px solid #38bdf8; background: rgba(51, 65, 85, 0.9); }
    
    .kpi-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }
    .kpi-value { color: #f8fafc; font-size: 32px; font-weight: 800; font-family: 'Inter', sans-serif; }

    .main-header {
        text-align: center; color: #f8fafc;
        font-size: 2.5rem; font-weight: 800; font-family: 'Inter', sans-serif;
        letter-spacing: -1px; margin-bottom: 0;
    }
    
    .strategy-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #38bdf8;
        padding: 20px; border-radius: 8px; color: #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC ---
def analyze_sentiment_ai(text):
    if not text or pd.isna(text): return "Neutral"
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0.1: return "Positive"
    elif analysis.sentiment.polarity < -0.1: return "Negative"
    else: return "Neutral"

def load_live_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/1PYL525ka_4pZ8clrEmpQYUoPMNMGiscnkxy90FGs94I/export?format=csv"
    try:
        df = pd.read_csv(sheet_url)
        df['Ward_Clean'] = df['Ward'].astype(str).str.strip().str.lower()
        return df
    except: return pd.DataFrame()

def load_structural_data():
    with open('data.json', 'r') as f: return json.load(f)

struct_data = load_structural_data()
live_df = load_live_data()

# --- UI ---
st.markdown("<h1 class='main-header'>LUCKNOW EXECUTIVE COMMAND</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:30px;'>Voter Intelligence & Strategic Action Engine</p>", unsafe_allow_html=True)

with st.container():
    f1, f2, f3 = st.columns(3)
    with f1: sel_const = st.selectbox("Constituency", list(struct_data.keys()))
    with f2: sel_ass = st.selectbox("Assembly Segment", list(struct_data[sel_const].keys()))
    with f3: sel_ward = st.selectbox("Target Ward", list(struct_data[sel_const][sel_ass].keys()))

ward_meta = struct_data[sel_const][sel_ass][sel_ward]
demog = ward_meta['demographics']
ward_clean_name = sel_ward.strip().lower()
ward_live_data = live_df[live_df['Ward_Clean'] == ward_clean_name] if not live_df.empty else pd.DataFrame()

# --- TABS ---
t1, t2, t3, t4 = st.tabs(["📈 STRATEGIC ANALYSIS", "🤖 AI INSIGHTS", "🗺️ BATTLE MAP", "📑 MASTER FEED"])

with t1:
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="metric-card"><div class="kpi-label">Win Prob</div><div class="kpi-value">{demog["win_probability"]}%</div></div>', unsafe_allow_html=True)
    with k2: st.markdown(f'<div class="metric-card"><div class="kpi-label">Swing Voters</div><div class="kpi-value" style="color:#f87171;">{demog["swing_voters"]:,}</div></div>', unsafe_allow_html=True)
    with k3: st.markdown(f'<div class="metric-card"><div class="kpi-label">Youth Segment</div><div class="kpi-value">{demog["youth_18_25"]:,}</div></div>', unsafe_allow_html=True)
    with k4: 
        st.markdown(f'<div class="metric-card"><div class="kpi-label">Live Reports</div><div class="kpi-value">{len(ward_live_data)}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- STRATEGY ENGINE ---
    st.markdown("### 🎯 Tactical Strategy Recommendation")
    if not ward_live_data.empty:
        neg_count = len(ward_live_data[ward_live_data['Complaint'].apply(analyze_sentiment_ai) == 'Negative'])
        pos_count = len(ward_live_data[ward_live_data['Complaint'].apply(analyze_sentiment_ai) == 'Positive'])
        
        if neg_count > pos_count:
            rec = "🔴 **HIGH FRICTION:** Negative sentiment outweighs positive. **Strategy:** Immediate 'Ground-Connect' visit. Address the top 3 complaints publicly via social media to neutralize anger."
        elif pos_count > neg_count:
            rec = "🟢 **STRONGHOLD:** Positive momentum detected. **Strategy:** Mobilization phase. Convert 'Positive' voters into 'Campaign Volunteers' for door-to-door outreach."
        else:
            rec = "🟡 **SWAY OPPORTUNITY:** Neutral sentiment dominates. **Strategy:** Targeted micro-campaigns focusing on youth and swing voters. Focus on 'New Development' promises."
        
        st.markdown(f'<div class="strategy-box">{rec}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="strategy-box">🟡 **BASELINE:** No live reports. Strategy: Standard outreach and routine booth monitoring.</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📈 Sentiment Distribution")
        if not ward_live_data.empty:
            processed = ward_live_data.copy()
            processed['AI_Mood'] = processed['Complaint'].apply(analyze_sentiment_ai)
            mood_counts = processed['AI_Mood'].value_counts().reset_index()
            mood_counts.columns = ['Mood', 'Count']
            fig_mood = px.pie(mood_counts, names='Mood', values='Count', 
                              color='Mood', color_discrete_map={'Positive':'#22c55e', 'Neutral':'#94a3b8', 'Negative':'#ef4444'},
                              template="plotly_dark", hole=0.7)
            st.plotly_chart(fig_mood, use_container_width=True)
        else:
            st.info("Awaiting live data stream...")

    with c2:
        st.markdown("#### 🔮 Adjusted Win Probability")
        if not ward_live_data.empty:
            neg_ratio = len(ward_live_data[ward_live_data['Complaint'].apply(analyze_sentiment_ai) == 'Negative']) / len(ward_live_data)
            sim_prob = demog['win_probability'] - (neg_ratio * 12)
            st.markdown(f"AI Analysis: Sentiment friction is adjusting probability to **{sim_prob:.1f}%**")
            st.progress(sim_prob/100)
        else:
            st.success(f"Baseline Probability: {demog['win_probability']}%")

with t2:
    st.markdown("### 🤖 AI Insight Feed")
    if not ward_live_data.empty:
        processed = ward_live_data.copy()
        processed['AI_Analysis'] = processed['Complaint'].apply(analyze_sentiment_ai)
        st.dataframe(processed[['Complaint', 'AI_Analysis', 'Priority', 'Status']], use_container_width=True)
    else:
        st.warning("No active intelligence feed for this ward.")

with t3:
    st.markdown("### 🗺️ Tactical Battlefield Map")
    all_wards = struct_data[sel_const][sel_ass]
    map_list = []
    for w_name, w_data in all_wards.items():
        size = 15 if w_name == sel_ward else 5
        map_list.append({"lat": w_data['coords'][0], "lon": w_data['coords'][1], "Ward": w_name, "Size": size})
    
    map_df = pd.DataFrame(map_list)
    fig_map = px.scatter_mapbox(
        map_df, lat="lat", lon="lon", size="Size", color="Ward",
        zoom=12, height=600, template="plotly_dark"
    )
    fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with t4:
    st.markdown("### 📋 Intelligence Master Feed")
    if not live_df.empty:
        st.dataframe(live_df, use_container_width=True)
    else:
        st.write("No data found.")
