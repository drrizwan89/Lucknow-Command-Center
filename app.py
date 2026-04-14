import streamlit as st
import pandas as pd
import json
import plotly.express as px
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Mumbai NE War Room", layout="wide", initial_sidebar_state="collapsed")

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
    .role-banner {
        background: linear-gradient(90deg, #ef4444 0%, #b91c1c 100%);
        color: white; padding: 15px; border-radius: 12px; text-align: center;
        font-weight: 800; font-size: 20px; margin-bottom: 20px; text-transform: uppercase;
    }
    .strategy-box {
        background: rgba(30, 41, 59, 0.7); border-left: 5px solid #ef4444; 
        padding: 20px; border-radius: 12px; color: #e2e8f0; margin-bottom: 15px;
    }
    .booth-a { border-left: 5px solid #22c55e; background: rgba(34, 197, 94, 0.1); padding: 10px; border-radius: 6px; margin-bottom: 5px; }
    .booth-b { border-left: 5px solid #eab308; background: rgba(234, 179, 8, 0.1); padding: 10px; border-radius: 6px; margin-bottom: 5px; }
    .booth-c { border-left: 5px solid #f97316; background: rgba(249, 115, 22, 0.1); padding: 10px; border-radius: 6px; margin-bottom: 5px; }
    .booth-d { border-left: 5px solid #ef4444; background: rgba(239, 68, 68, 0.1); padding: 10px; border-radius: 6px; margin-bottom: 5px; }
    .prio-high { border-left: 5px solid #ef4444; background: rgba(239, 68, 68, 0.1); padding: 10px; margin-bottom: 8px; border-radius: 6px; color: #fca5a5; font-size: 13px; }
    .prio-med { border-left: 5px solid #f59e0b; background: rgba(245, 158, 11, 0.1); padding: 10px; margin-bottom: 8px; border-radius: 6px; color: #fde047; font-size: 13px; }
    </style>
    """, unsafe_allow_html=True)

# --- RESEARCH DATABASE ---
research_csv = """Assembly,Category,Title,Severity,Detail,Tactical_Angle
Mulund,Infrastructure,Parking Crisis,High,Severe shortage in core markets,Target RWAs with smart parking plan
Mulund,Civic,Property Tax,Medium,Middle-class discontent on rates,Promise tax review audit
Vikhroli,Identity,Marathi Connect,Very High,Strong emotional hold of SS(UBT),Deploy local Marathi faces
Vikhroli,Housing,SRA Delays,Very High,Huge anger over stalled redevelopment,Attack opponent on 'Broken Home' promises
Bhandup,Utility,Water Timing,Very High,Only 1-3 hrs supply in slums,Direct 'Paani' delivery narrative
Bhandup,Utility,Drainage Overflow,High,Chronic flooding in Sonapur,Focus on 'Gutter-Free' Bhandup
Ghatkopar W,Infrastructure,LBS Road Choke,Very High,Extreme traffic congestion,Promise integrated traffic management
Ghatkopar W,Civic,Parking Shortage,High,Residential parking conflicts,Focus on society-level solutions
Ghatkopar E,Infrastructure,Garodia Nagar Traffic,Very High,Congestion near education hub,Target high-income professional voters
Ghatkopar E,Civic,Footpath Encroachment,Medium,Street vendor chaos,Promote 'Smart City' cleanliness
Mankhurd,Health,Life Expectancy,Very High,Lowest in Mumbai ~39Y,Sledgehammer attack on civic neglect
Mankhurd,Water,Tainted Supply,Very High,Black/Yellow water in slums,Commit to 100-day clean water fix
Mankhurd,Women,Toilet Safety,Very High,85% feel unsafe at night,Direct attack on women's dignity failure
"""
master_df = pd.read_csv(io.StringIO(research_csv))

def load_structural_data():
    try:
        with open('data.json', 'r') as f: return json.load(f)
    except: return {}

struct_data = load_structural_data()

# --- UI ---
st.markdown("<h1 class='main-header'>Mumbai North East War Room</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#94a3b8; margin-bottom:30px;'>Sovereign Intelligence Command | Booth-Level Execution Suite</p>", unsafe_allow_html=True)

if not struct_data:
    st.error("data.json not found.")
    st.stop()

# --- FILTERS ---
with st.container():
    f1, f2, f3 = st.columns(3)
    with f1: sel_const = st.selectbox("🏛️ Region", list(struct_data.keys()))
    
    if sel_const:
        # ADDED: Constituency Overview option
        assemblies = ["CONSTITUENCY OVERVIEW"] + list(struct_data[sel_const].keys())
        with f2: sel_ass = st.selectbox("🚩 Assembly", assemblies)
        
        if sel_ass != "CONSTITUENCY OVERVIEW":
            wards_dict = struct_data[sel_const][sel_ass].get('wards', {})
            # CHANGED: Overall Assembly View -> Ward Overview
            wards_list = ["WARD OVERVIEW"] + list(wards_dict.keys())
            with f3: sel_ward = st.selectbox("📍 Target Ward", wards_list)
        else:
            # If Constituency Overview is selected, we disable/set ward to Overview
            with f3: sel_ward = st.selectbox("📍 Target Ward", ["CONSTITUENCY VIEW"], index=0)
    else: st.stop()

# --- DATA RESOLUTION LOGIC ---
if sel_ass == "CONSTITUENCY OVERVIEW":
    # Aggregate data from all assemblies
    all_ass = struct_data[sel_const]
    total_voters = sum([a.get('demographics', {}).get('total_voters', 0) for a in all_ass.values()])
    avg_prob = sum([a.get('demographics', {}).get('win_probability', 0) for a in all_ass.values()]) / len(all_ass)
    avg_margin = sum([a.get('demographics', {}).get('margin', 0) for a in all_ass.values()]) / len(all_ass)
    avg_turnout = sum([a.get('demographics', {}).get('turnout', 0) for a in all_ass.values()]) / len(all_ass)
    
    role = "Full Constituency"
    model = "Mixed Hybrid"
    demog = {"total_voters": total_voters, "win_probability": avg_prob, "margin": avg_margin}
    current_ward_meta = {"demographics": demog, "severity": "MIXED"}
    ass_demog = {"turnout": avg_turnout}

else:
    ass_data = struct_data[sel_const][sel_ass]
    ass_demog = ass_data.get('demographics', {})
    role = ass_data.get('role', 'Unknown')
    model = ass_data.get('model', 'Unknown')

    if sel_ward == "WARD OVERVIEW":
        wards_dict = ass_data.get('wards', {})
        total_voters = ass_demog.get("total_voters", 0)
        avg_prob = sum([w.get('demographics', {}).get('win_probability', 0) for w in wards_dict.values()]) / (len(wards_dict) if wards_dict else 1)
        avg_margin = sum([w.get('demographics', {}).get('margin', 0) for w in wards_dict.values()]) / (len(wards_dict) if wards_dict else 1)
        demog = {"total_voters": total_voters, "win_probability": avg_prob, "margin": avg_margin}
        current_ward_meta = {"demographics": demog, "severity": "MIXED"}
    else:
        current_ward_meta = ass_data.get('wards', {}).get(sel_ward, {})
        demog = current_ward_meta.get('demographics', {})

# --- STRATEGIC BANNER ---
st.markdown(f"<div class='role-banner'>STRATEGIC ROLE: {role} | VOTING MODEL: {model}</div>", unsafe_allow_html=True)

# --- TABS ---
t1, t2, t3, t4, t5 = st.tabs(["📈 EXEC SUMMARY", "⚔️ BOOTH STRATEGY", "🚨 VULNERABILITY", "🗺️ RISK MAP", "📑 DOSSIER"])

with t1:
    k1, k2, k3, k4 = st.columns(4)
    with k1: st.markdown(f'<div class="metric-card"><div class="kpi-label">Win Prob</div><div class="kpi-value">{demog.get("win_probability", 0):.1f}%</div></div>', unsafe_allow_html=True)
    with k2: 
        st.markdown(f'<div class="metric-card"><div class="kpi-label">Margin / Sway</div><div class="kpi-value" style="color:#f87171;">{demog.get("margin", 0):,.0f}</div></div>', unsafe_allow_html=True)
    with k3: 
        st.markdown(f'<div class="metric-card"><div class="kpi-label">Total Voters</div><div class="kpi-value">{demog.get("total_voters", 0):,}</div></div>', unsafe_allow_html=True)
    with k4: 
        st.markdown(f'<div class="metric-card"><div class="kpi-label">Turnout Est</div><div class="kpi-value">{ass_demog.get("turnout", 0)}%</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Handle header for priority matrix
    matrix_title = "Constituency" if sel_ass == "CONSTITUENCY OVERVIEW" else sel_ass
    st.markdown(f"### 🎯 {matrix_title} Priority Matrix")
    
    if sel_ass == "CONSTITUENCY OVERVIEW":
        filtered_issues = master_df
    else:
        filtered_issues = master_df[master_df['Assembly'] == sel_ass]

    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("**🔴 CRITICAL ATTACK POINTS**")
        for _, row in filtered_issues[filtered_issues['Severity'] == "Very High"].iterrows(): 
            st.markdown(f'<div class="prio-high"><b>{row["Title"]}</b><br>{row["Tactical_Angle"]}</div>', unsafe_allow_html=True)
    with p_col2:
        st.markdown("**🟡 SECONDARY LEVERS**")
        for _, row in filtered_issues[filtered_issues['Severity'] == "High"].iterrows(): 
            st.markdown(f'<div class="prio-med"><b>{row["Title"]}</b><br>{row["Tactical_Angle"]}</div>', unsafe_allow_html=True)

with t2:
    st.markdown("### ⚔️ Booth Segmentation Framework")
    st.markdown('<div class="strategy-box"><b>Winning Formula:</b> Retain 95% of A booths + Convert 30% of C booths + Drive 5% Turnout increase in B booths.</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="booth-a"><b>🟢 TYPE A: Strong BJP</b><br>Goal: Maximize Turnout. Strategy: RWA mobilization & Society WhatsApp.</div>', unsafe_allow_html=True)
        st.markdown('<div class="booth-b"><b>🟡 TYPE B: Lean BJP</b><br>Goal: Consolidation. Strategy: Door-to-door focus on local issues.</div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="booth-c"><b>🟠 TYPE C: Swing</b><br>Goal: Conversion. Strategy: Hyper-local utility promises.</div>', unsafe_allow_html=True)
        st.markdown('<div class="booth-d"><b>🔴 TYPE D: Opposition</b><br>Goal: Damage Control. Strategy: Target silent voters only.</div>', unsafe_allow_html=True)

with t3:
    st.markdown("### 🚨 Opponent Vulnerability Audit")
    # Logic for Vulnerability
    if sel_ass != "CONSTITUENCY OVERVIEW" and sel_ward != "WARD OVERVIEW":
        # We are looking at a specific ward
        ward_issues = master_df[master_df['Assembly'] == sel_ass]
        if not ward_issues.empty:
            primary = ward_issues.iloc[0]
            st.markdown(f'<div class="strategy-box"><b>TACTICAL HIT: {sel_ward}</b><br>Focus on {primary["Title"]} to disrupt opponent base. Narrative: "{primary["Detail"]} is a failure of current leadership."</div>', unsafe_allow_html=True)
        else: st.info("No specific failure data for this ward.")
    elif sel_ass != "CONSTITUENCY OVERVIEW":
        # We are looking at a Ward Overview (Assembly level)
        ward_issues = master_df[master_df['Assembly'] == sel_ass]
        if not ward_issues.empty:
            primary = ward_issues.iloc[0]
            st.markdown(f'<div class="strategy-box"><b>ASSEMBLY-WIDE HIT: {sel_ass}</b><br>Focus on {primary["Title"]} to disrupt opponent base. Narrative: "{primary["Detail"]} is a failure of current leadership."</div>', unsafe_allow_html=True)
    else:
        st.info("Select a specific assembly or ward to generate a localized failure audit.")

with t4:
    st.markdown("### 🗺️ Risk-Based Battlefield Map")
    # Mapping logic for constituency vs assembly
    if sel_ass == "CONSTITUENCY OVERVIEW":
        all_assemblies = struct_data[sel_const]
        map_list = []
        for ass_name, ass_data in all_assemblies.items():
            wards = ass_data.get('wards', {})
            for w_name, w_data in wards.items():
                sev = w_data.get("severity", "Low")
                color = "Red" if sev == "Very High" else "Orange" if sev == "High" else "Yellow"
                map_list.append({"lat": w_data['coords'][0], "lon": w_data['coords'][1], "Ward": w_name, "Size": 5, "Severity": color})
    else:
        all_wards = struct_data[sel_const][sel_ass].get('wards', {})
        map_list = []
        for w_name, w_data in all_wards.items():
            sev = w_data.get("severity", "Low")
            color = "Red" if sev == "Very High" else "Orange" if sev == "High" else "Yellow"
            size = 15 if (sel_ward != "WARD OVERVIEW" and w_name == sel_ward) else 5
            map_list.append({"lat": w_data['coords'][0], "lon": w_data['coords'][1], "Ward": w_name, "Size": size, "Severity": color})
    
    map_df = pd.DataFrame(map_list)
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="Size", color="Severity",
                                color_discrete_map={"Red": "#ef4444", "Orange": "#f97316", "Yellow": "#facc15"},
                                zoom=11, height=600, template="plotly_dark")
    fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_map, use_container_width=True)

with t5:
    st.markdown("### 📑 Intelligence Master Dossier")
    search_query = st.text_input("🔍 Search the Dossier (e.g., 'SRA', 'Water', 'Marathi')")
    if search_query:
        filtered_df = master_df[master_df['Title'].str.contains(search_query, case=False) | 
                                master_df['Detail'].str.contains(search_query, case=False)]
    else:
        filtered_df = master_df
    st.dataframe(filtered_df, use_container_width=True)
