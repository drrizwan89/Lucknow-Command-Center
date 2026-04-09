import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="LKO-MUM Sovereign Command", layout="wide", initial_sidebar_state="collapsed")

# --- EXECUTIVE CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    .stApp { background-color: #0a0f1d; color: #f8fafc; font-family: 'Inter', sans-serif; }
    .metric-card {
        background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px; padding: 20px; text-align: center; backdrop-filter: blur(8px);
    }
    .kpi-label { color: #94a3b8; font-size: 12px; text-transform: uppercase; font-weight: 600; }
    .kpi-value { color: #f8fafc; font-size: 32px; font-weight: 800; }
    .main-header { text-align: center; color: #f8fafc; font-size: 2.8rem; font-weight: 800; margin-bottom: 0; }
    .strategy-box {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-left: 5px solid #ef4444; padding: 20px; border-radius: 12px; color: #e2e8f0;
    }
    .failure-card {
        background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444;
        padding: 15px; border-radius: 8px; margin-top: 10px; color: #fca5a5;
    }
    .health-card {
        background: rgba(234, 179, 8, 0.1); border: 1px solid #eab308;
        padding: 15px; border-radius: 8px; margin-top: 10px; color: #fde047;
    }
    .gender-card {
        background: rgba(168, 85, 247, 0.1); border: 1px solid #a855f7;
        padding: 15px; border-radius: 8px; margin-top: 10px; color: #d8b4fe;
    }
    .prio-high { border-left: 5px solid #ef4444; background: rgba(239, 68, 68, 0.1); padding: 10px; margin-bottom: 8px; border-radius: 6px; color: #fca5a5; font-size: 13px; }
    .prio-med { border-left: 5px solid #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 10px; margin-bottom: 8px; border-radius: 6px; color: #fde047; font-size: 13px; }
    .prio-low { border-left: 5px solid #3b82f6; background: rgba(59, 130, 246, 0.1); padding: 10px; margin-bottom: 8px; border-radius: 6px; color: #bae6fd; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- RESEARCH DATABASE ---
research_csv = """Ward,Category,Title,Severity,Detail,Health,Failure
Ward 134 (Kamala Nagar),Water,Contaminated Water,High,Residents drink unsafe water for years,Diarrhoea cholera typhoid,Safe pipelines promised 2014 never delivered
Ward 135 (Ramabainagar),Drainage,Nala Choking,High,Nalas never cleaned properly,Malaria dengue,Routine flooding every rainy season
Ward 136 (Shivajinagar Terminus),Pollution,Deonar Dump,High,Constant smoke and stench,Respiratory illness asthma TB,Waste processing plant promised 10 years ago
Ward 137 (Shivajinagar),Housing,Sub-human Conditions,Very High,Inhuman living standards,High infant mortality stunting 47%,SRA project stalled
Ward 143 (Maharashtra Nagar),Water,Extreme Contamination,Very High,Black Yellow water supply,Severe diarrhoea kidney damage,Health outbreaks ignored
Ward 144 (Devnar Village),Pollution,Toxic Fumes,Very High,Constant exposure to poisonous smoke,Life exp ~39y,Closure promised since 2014
Multiple,Women,Unsafe Toilets,Very High,85% women feel unsafe at night,Sexual harassment UTIs,Violation of Swachh Bharat
Multiple,Women,Water Fetching,Very High,Hours spent queuing for water,Back kidney strain child stunting,Irregular supply causing time poverty
Multiple,Infrastructure,Govt Hospitals,High,Overcrowded facilities and missing gas pipelines,Cross-infections,Lack of basic healthcare access
Multiple,Infrastructure,Municipal Schools,High,Crumbling buildings and low quality education,High dropout rates,Failed investment in youth
Multiple,Infrastructure,PWD Neglect,Medium-High,Broken roads and non-functional streetlights,Accident risks,Failed road maintenance
Multiple,Youth,Playground Crisis,High,No proper sporting facilities or open spaces,Child stunting and obesity,Zero investment in youth recreation
Multiple,Health,Life Expectancy,Very High,M-East lowest life exp ~39y,Chronic respiratory disease,Systemic civic neglect
"""
master_df = pd.read_csv(io.StringIO(research_csv))

def load_structural_data():
    try:
        with open('data.json', 'r') as f: return json.load(f)
    except: return {}

struct_data = load_structural_data()

# --- UI ---
st.markdown("<h1 class='main-header'>Sovereign Strategic Command</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:30px;'>High-Density Intelligence Suite | Multi-Regional Command</p>", unsafe_allow_html=True)

if not struct_data:
    st.error("data.json not found. Please check your folder.")
    st.stop()

with st.container():
    f1, f2, f3 = st.columns(3)
    with f1: sel_const = st.selectbox("🏛️ Region", list(struct_data.keys()))
    
    # Logic check for assemblies
    if sel_const:
        assemblies = list(struct_data[sel_const].keys())
        with f2: sel_ass = st.selectbox("🚩 Assembly", assemblies)
        
        if sel_ass:
            wards_dict = struct_data[sel_const][sel_ass].get('wards', {})
            wards_list = ["OVERALL ASSEMBLY VIEW"] + list(wards_dict.keys())
            with f3: sel_ward = st.selectbox("📍 Target Ward", wards_list)
        else: st.stop()
    else: st.stop()

# --- DATA RESOLUTION ---
ass_data = struct_data[sel_const][sel_ass]
ass_demog = ass_data.get('demographics', {})

if sel_ward == "OVERALL ASSEMBLY VIEW":
    wards_dict = ass_data.get('wards', {})
    total_voters = ass_demog.get("total_voters", 0)
    avg_prob = sum([w.get('demographics', {}).get('win_probability', 0) for w in wards_dict.values()]) / (len(wards_dict) if wards_dict else 1)
    avg_margin = sum([w.get('demographics', {}).get('margin', 0) for w in wards_dict.values()]) / (len(wards_dict) if wards_dict else 1)
    current_ward_meta = {"demographics": {"total_voters": total_voters, "win_probability": avg_prob, "margin": avg_margin}, "severity": "MIXED"}
else:
    current_ward_meta = ass_data.get('wards', {}).get(sel_ward, {})

demog = current_ward_meta.get('demographics', {})

# --- TABS ---
t1, t2, t3, t4, t5 = st.tabs(["📈 EXEC SUMMARY", "🚨 VULNERABILITY AUDIT", "👩 SOCIO-CIVIC CRISIS", "🗺️ RISK MAP", "📑 MASTER DOSSIER"])

with t1:
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="metric-card"><div class="kpi-label">Win Prob</div><div class="kpi-value">{demog.get("win_probability", 0):.1f}%</div></div>', unsafe_allow_html=True)
    with k2: 
        label = "Avg Margin" if "Mumbai" in sel_const else "Sway Voters"
        val = demog.get("margin", demog.get("swing_voters", 0))
        st.markdown(f'<div class="metric-card"><div class="kpi-label">{label}</div><div class="kpi-value" style="color:#f87171;">{val:,}</div></div>', unsafe_allow_html=True)
    with k3: 
        if "Mumbai" in sel_const:
            st.markdown(f'<div class="metric-card"><div class="kpi-label">Life Exp (M-East)</div><div class="kpi-value" style="color:#ef4444;">~{ass_demog.get("life_expectancy", "39")}Y</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="metric-card"><div class="kpi-label">Socio-Risk</div><div class="kpi-value" style="color:#fbbf24;">{current_ward_meta.get("severity", "High")}</div></div>', unsafe_allow_html=True)
    with k4: st.markdown(f'<div class="metric-card"><div class="kpi-label">Total Voters</div><div class="kpi-value">{demog.get("total_voters", 0):,}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🎯 Strategic Priority Matrix")
    
    if sel_ward == "OVERALL ASSEMBLY VIEW":
        filtered_issues = master_df
    else:
        filtered_issues = master_df[master_df['Ward'] == sel_ward]

    high_p = filtered_issues[filtered_issues['Severity'] == "Very High"].head(5)
    med_p = filtered_issues[filtered_issues['Severity'] == "High"].head(5)
    low_p = filtered_issues[filtered_issues['Severity'] == "Medium-High"].head(5)

    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown("**🔴 CRITICAL**")
        for _, row in high_p.iterrows(): st.markdown(f'<div class="prio-high"><b>{row["Title"]}</strong><br><small>{row["Category"]}</small></div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown("**🟡 STRATEGIC**")
        for _, row in med_p.iterrows(): st.markdown(f'<div class="prio-med"><b>{row["Title"]}</strong><br><small>{row["Category"]}</small></div>', unsafe_allow_html=True)
    with p_col3:
        st.markdown("**🔵 ROUTINE**")
        for _, row in low_p.iterrows(): st.markdown(f'<div class="prio-low"><b>{row["Title"]}</strong><br><small>{row["Category"]}</small></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 👥 Demographic Power-Grid")
    if sel_ward == "OVERALL ASSEMBLY VIEW":
        m_pct, h_pct, f_val = ass_demog.get("muslim_pct", 0), ass_demog.get("hindu_pct", 0), ass_demog.get("female", 0)
    else:
        m_pct = demog.get("muslim_pct", ass_demog.get("muslim_pct", 0))
        h_pct = demog.get("hindu_pct", ass_demog.get("hindu_pct", 0))
        f_val = demog.get("female", ass_demog.get("female", 0))

    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1: st.markdown(f'<div class="metric-card"><div class="kpi-label">Muslim Influence</div><div class="kpi-value">{m_pct}%</div></div>', unsafe_allow_html=True)
    with d_col2: st.markdown(f'<div class="metric-card"><div class="kpi-label">Hindu Influence</div><div class="kpi-value">{h_pct}%</div></div>', unsafe_allow_html=True)
    with d_col3: st.markdown(f'<div class="metric-card"><div class="kpi-label">Female Voter Base</div><div class="kpi-value">{f_val:,}</div></div>', unsafe_allow_html=True)

with t2:
    st.markdown("### 🚨 Opponent Vulnerability Audit")
    if sel_ward != "OVERALL ASSEMBLY VIEW":
        ward_issues = master_df[master_df['Ward'] == sel_ward]
        if not ward_issues.empty:
            primary = ward_issues.iloc[0]
            margin = demog.get("margin", 0)
            status = "🔴 CRITICAL" if margin < 2000 else "🟡 CONTESTABLE" if margin < 5000 else "🔵 STABLE"
            st.markdown(f'<div class="strategy-box"><b>WARD STATUS: {status}</strong><br>Sledgehammer attack: Focus on {primary["Title"]} to flip the base.</div>', unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f'<div class="failure-card"><b>❌ BROKEN PROMISE: {primary["Title"]}</strong><br>{primary["Failure"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="health-card"><b>⚠️ HEALTH IMPACT: {primary["Health"]}</strong></div>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<div class="angle-box"><b>💡 STRATEGIC ATTACK:</strong><br>Highlight {primary["Detail"]}. Contrast with your commitment to a 100-day fix.</div>', unsafe_allow_html=True)
        else:
            st.info("No specific failure data for this ward.")
    else:
        st.info("Select a specific ward to generate the Failure Audit.")

with t3:
    st.markdown("### 👩 Socio-Civic Crisis Center")
    crisis_df = master_df[master_df['Category'].isin(["Women", "Infrastructure", "Youth", "Health"])]
    st.markdown('<div class="gender-card"><b>DIGNITY CRISIS:</strong><br>85% of women feel unsafe in community toilets. This is the primary emotional lever for Govandi.</div>', unsafe_allow_html=True)
    st.markdown('<div class="health-card"><b>INFRASTRUCTURE GAP:</strong><br>Crumbling municipal schools and overcrowded hospitals are failing the next generation.</div>', unsafe_allow_html=True)
    st.dataframe(crisis_df[['Title', 'Severity', 'Detail', 'Health', 'Failure']], use_container_width=True)

with t4:
    st.markdown("### 🗺️ Risk-Based Battlefield Map")
    all_wards = struct_data[sel_const][sel_ass].get('wards', {})
    map_list = []
    for w_name, w_data in all_wards.items():
        sev = w_data.get("severity", "Low")
        color = "Red" if sev == "Very High" else "Orange" if sev == "High" else "Yellow"
        size = 15 if w_name == sel_ward else 5
        map_list.append({"lat": w_data['coords'][0], "lon": w_data['coords'][1], "Ward": w_name, "Size": size, "Severity": color})
    map_df = pd.DataFrame(map_list)
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="Size", color="Severity",
                                color_discrete_map={"Red": "#ef4444", "Orange": "#f97316", "Yellow": "#facc15"},
                                zoom=12, height=600, template="plotly_dark")
    fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with t5:
    st.markdown("### 📑 Intelligence Master Dossier")
    search_query = st.text_input("🔍 Search the Dossier (e.g., 'SRA', 'Water', 'Health')")
    if search_query:
        filtered_df = master_df[master_df['Title'].str.contains(search_query, case=False) | 
                                master_df['Detail'].str.contains(search_query, case=False)]
    else:
        filtered_df = master_df
    st.dataframe(filtered_df, use_container_width=True)
