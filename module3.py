import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & PREMIUM STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoInvest | Corporate Emissions Liability",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Shared "Eco-FinTech" Design System - Adapted for Corporate Risk Warning
st.markdown("""
<style>
    /* Global App Styling - Professional Dark Finance Theme */
    .stApp {
        background: linear-gradient(160deg, #0a0e17 0%, #1a0f14 45%, #2a0808 100%);
        background-attachment: fixed;
        color: #e2e8f0;
    }
    
    /* Heading Adjustments */
    .stApp h1 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #ffffff;
        font-size: 2.4rem !important;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    
    .stApp h2, .stApp h3, .stApp h4 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #f8fafc;
        font-weight: 600;
    }

    /* Advanced KPI Card Container */
    .kpi-card {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(239, 68, 68, 0.2); /* Red warning border */
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        margin-bottom: 15px;
        border-left: 4px solid #ef4444;
    }
    
    .kpi-title {
        color: #94a3b8;
        font-size: 0.95rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace;
    }
    
    .kpi-sub {
        color: #ef4444;
        font-size: 0.85rem;
        font-weight: bold;
        margin-top: 5px;
    }

    /* Risk Profile Container */
    .risk-container {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 12px;
        padding: 25px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-top: 20px;
    }

    .risk-badge {
        background-color: rgba(239, 68, 68, 0.2); 
        color: #fca5a5; 
        border: 1px solid #ef4444;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 8px;
        display: inline-block;
        margin-bottom: 10px;
    }

    .info-badge {
        background-color: rgba(56, 189, 248, 0.1); 
        color: #7dd3fc; 
        border: 1px solid #38bdf8;
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        margin-right: 8px;
    }

    /* Custom Table Styling */
    .dataframe {
        width: 100%;
        color: white;
    }
    
    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA GENERATION (Top 20 Indian Corporate Polluters)
# -----------------------------------------------------------------------------

@st.cache_data
def load_corporate_data():
    """
    Simulates the emissions database for the Top 20 largest Indian corporate polluters.
    Numbers are scaled to believable absolute values (Millions/Billions of kg) to match the SIP scale.
    """
    data = [
        {"Rank": 1, "Company": "NTPC Limited", "Sector": "Power Generation", "Annual_Emissions_kg": 850000000, "Country": "India"},
        {"Rank": 2, "Company": "Reliance Industries", "Sector": "Petrochemicals", "Annual_Emissions_kg": 720000000, "Country": "India"},
        {"Rank": 3, "Company": "Tata Steel", "Sector": "Manufacturing", "Annual_Emissions_kg": 680000000, "Country": "India"},
        {"Rank": 4, "Company": "Coal India Ltd", "Sector": "Mining", "Annual_Emissions_kg": 610000000, "Country": "India"},
        {"Rank": 5, "Company": "Adani Power", "Sector": "Power Generation", "Annual_Emissions_kg": 590000000, "Country": "India"},
        {"Rank": 6, "Company": "Indian Oil Corp (IOCL)", "Sector": "Oil & Gas", "Annual_Emissions_kg": 540000000, "Country": "India"},
        {"Rank": 7, "Company": "JSW Steel", "Sector": "Manufacturing", "Annual_Emissions_kg": 490000000, "Country": "India"},
        {"Rank": 8, "Company": "UltraTech Cement", "Sector": "Construction Materials", "Annual_Emissions_kg": 460000000, "Country": "India"},
        {"Rank": 9, "Company": "ONGC", "Sector": "Oil & Gas", "Annual_Emissions_kg": 420000000, "Country": "India"},
        {"Rank": 10, "Company": "Vedanta Limited", "Sector": "Mining & Metals", "Annual_Emissions_kg": 390000000, "Country": "India"},
        {"Rank": 11, "Company": "Hindalco Industries", "Sector": "Metals", "Annual_Emissions_kg": 350000000, "Country": "India"},
        {"Rank": 12, "Company": "Bharat Petroleum (BPCL)", "Sector": "Oil & Gas", "Annual_Emissions_kg": 310000000, "Country": "India"},
        {"Rank": 13, "Company": "Hindustan Petroleum (HPCL)", "Sector": "Oil & Gas", "Annual_Emissions_kg": 280000000, "Country": "India"},
        {"Rank": 14, "Company": "Ambuja Cements", "Sector": "Construction Materials", "Annual_Emissions_kg": 250000000, "Country": "India"},
        {"Rank": 15, "Company": "Larsen & Toubro (L&T)", "Sector": "Construction & Engg", "Annual_Emissions_kg": 210000000, "Country": "India"},
        {"Rank": 16, "Company": "Grasim Industries", "Sector": "Textiles & Chemicals", "Annual_Emissions_kg": 180000000, "Country": "India"},
        {"Rank": 17, "Company": "Tata Motors", "Sector": "Automotive", "Annual_Emissions_kg": 150000000, "Country": "India"},
        {"Rank": 18, "Company": "Mahindra & Mahindra", "Sector": "Automotive", "Annual_Emissions_kg": 120000000, "Country": "India"},
        {"Rank": 19, "Company": "Shree Cement", "Sector": "Construction Materials", "Annual_Emissions_kg": 95000000, "Country": "India"},
        {"Rank": 20, "Company": "Maruti Suzuki", "Sector": "Automotive", "Annual_Emissions_kg": 75000000, "Country": "India"}
    ]
    
    df = pd.DataFrame(data)
    
    # CALCULATIONS
    # Safe Target: Corporate compliance requires a 45% reduction from baseline
    df['Safe_Target_kg'] = df['Annual_Emissions_kg'] * 0.55
    
    # Credits Needed: The deficit they must purchase to avoid fines
    df['Credits_Needed_kg'] = df['Annual_Emissions_kg'] - df['Safe_Target_kg']
    
    # Financial Liability: Assume a domestic carbon tax / credit market price of ₹1.5 per kg
    market_price_per_kg = 1.50
    df['Financial_Liability_INR'] = df['Credits_Needed_kg'] * market_price_per_kg
    
    return df

df_corps = load_corporate_data()

# -----------------------------------------------------------------------------
# 3. HELPER TEXTS & RISK PROFILES
# -----------------------------------------------------------------------------

def get_risk_profile(company_name, sector):
    """Generates a professional problem statement contextualized for the Indian market."""
    
    base_problems = f"""
    **{company_name}** is currently operating vastly outside the parameters of India's Net Zero 2070 commitments. As a heavy emitter in the {sector} sector, their excessive carbon footprint exposes them to severe local and global risks:
    
    **1. SEBI BRSR & Regulatory Fines:**
    With the mandate of SEBI's Business Responsibility and Sustainability Reporting (BRSR), exact emissions are now public. Future implementation of the Indian Carbon Market (ICM) will levy direct financial penalties for every kilogram of CO₂ emitted above their allowance.
    
    **2. Stranded Assets & Export Tariffs:**
    As the European Union strictly enforces the Carbon Border Adjustment Mechanism (CBAM), {company_name}'s exports will face massive "carbon taxes" at international borders, rendering their products uncompetitive globally.
    
    **3. ESG Capital Divestment:**
    Domestic mutual funds and international Foreign Institutional Investors (FIIs) are heavily screening for ESG compliance. Failure to offset this deficit drastically increases their cost of borrowing and limits capital expansion.
    
    **4. Ecopay B2B Solution:**
    To avoid these billions in liabilities, {company_name} must immediately purchase aggregated carbon credits from retail platforms like **Ecopay**, effectively transferring wealth from polluting corporates to green retail investors.
    """
    return base_problems

def format_large_number(num):
    """Formats large numbers into readable Billions/Millions."""
    if num >= 1e9:
        return f"{num / 1e9:.2f} Billion"
    elif num >= 1e6:
        return f"{num / 1e6:.2f} Million"
    else:
        return f"{num:,.0f}"

# -----------------------------------------------------------------------------
# 4. MAIN DASHBOARD LAYOUT
# -----------------------------------------------------------------------------

def main():
    # --- HEADER ---
    col1, col2 = st.columns([7, 3])
    with col1:
        st.title("Indian Corporate Liability Radar")
        st.markdown("##### Tracking the Top 20 Indian Polluters & Their Carbon Credit Deficits")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌐 Route to Retail SIP Portal"):
            st.toast("Navigating to Retail Investment Portal...")

    st.markdown("---")

    # --- KPI ROW ---
    total_emissions = df_corps['Annual_Emissions_kg'].sum()
    total_deficit = df_corps['Credits_Needed_kg'].sum()
    total_liability = df_corps['Financial_Liability_INR'].sum()

    k1, k2, k3 = st.columns(3)
    
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Top 20 Total Emissions</div>
            <div class="kpi-value">{format_large_number(total_emissions)} <span style="font-size:1rem; color:#94a3b8;">kg CO₂e</span></div>
            <div class="kpi-sub">Critical BRSR threshold exceeded</div>
        </div>
        """, unsafe_allow_html=True)
        
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Domestic Credit Deficit</div>
            <div class="kpi-value">{format_large_number(total_deficit)} <span style="font-size:1rem; color:#94a3b8;">kg</span></div>
            <div class="kpi-sub">Volume needed to achieve safe limits</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Financial Liability</div>
            <div class="kpi-value">₹ {format_large_number(total_liability)}</div>
            <div class="kpi-sub">Estimated cost to offset at ₹1.5/kg</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRAPHICAL ANALYSIS ---
    st.subheader("📊 Emissions Distribution & Credit Deficit")
    
    g_col1, g_col2 = st.columns([1, 1])
    
    with g_col1:
        # Treemap of Emissions
        fig_tree = px.treemap(
            df_corps, 
            path=['Sector', 'Company'], 
            values='Annual_Emissions_kg',
            color='Annual_Emissions_kg',
            color_continuous_scale='Reds',
            title="Emission Weight by Sector & Company"
        )
        fig_tree.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(t=40, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    with g_col2:
        # Bar chart showing Current vs Target
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_corps['Company'][:10], # Top 10 for clarity
            y=df_corps['Annual_Emissions_kg'][:10],
            name='Current Emissions',
            marker_color='#ef4444'
        ))
        fig_bar.add_trace(go.Bar(
            x=df_corps['Company'][:10],
            y=df_corps['Safe_Target_kg'][:10],
            name='Safe Target Limit',
            marker_color='#10b981'
        ))
        fig_bar.update_layout(
            title="Top 10: Current Emissions vs. Safe Limits (kg)",
            barmode='overlay',
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            margin=dict(t=40, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("---")

    # --- DEEP DIVE & PROBLEM STATEMENT ---
    st.subheader("🏢 Corporate Deep Dive & Risk Analysis")
    st.markdown("Select a specific corporation to view their operational deficit and exact risk profile.")
    
    dd_col1, dd_col2 = st.columns([1, 2])
    
    with dd_col1:
        st.markdown('<div class="risk-container" style="padding:15px;">', unsafe_allow_html=True)
        selected_company = st.selectbox("Select Top 20 Polluter", df_corps['Company'].tolist())
        
        # Get company specific data
        c_data = df_corps[df_corps['Company'] == selected_company].iloc[0]
        
        st.markdown(f"### {c_data['Company']}")
        st.markdown(f"<span class='info-badge'>📍 {c_data['Country']}</span> <span class='info-badge'>🏭 {c_data['Sector']}</span>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown(f"**Gross Emissions:**<br><span style='color:#ef4444; font-size:1.4rem; font-weight:bold;'>{c_data['Annual_Emissions_kg']:,.0f} kg</span>", unsafe_allow_html=True)
        
        st.markdown(f"**Target Safe Limit:**<br><span style='color:#10b981; font-size:1.4rem; font-weight:bold;'>{c_data['Safe_Target_kg']:,.0f} kg</span>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.markdown(f"**Credits Required (Deficit):**<br><span style='color:#fbbf24; font-size:1.6rem; font-weight:bold;'>{c_data['Credits_Needed_kg']:,.0f} kg</span>", unsafe_allow_html=True)
        
        st.markdown(f"**Financial Liability:**<br><span style='color:#f8fafc; font-size:1.4rem; font-weight:bold;'>₹{c_data['Financial_Liability_INR']:,.0f}</span>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(f"Force B2B Credit Purchase"):
            st.success(f"Initiated massive B2B block trade request to Ecopay Treasury to offset {format_large_number(c_data['Credits_Needed_kg'])} kg for {c_data['Company']}.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    with dd_col2:
        st.markdown('<div class="risk-container">', unsafe_allow_html=True)
        st.markdown(f"### Problem Statement & Liability Assessment")
        st.markdown("<span class='risk-badge'>Regulatory High Risk</span> <span class='risk-badge'>CBAM Export Threat</span>", unsafe_allow_html=True)
        
        # Display the custom risk profile text
        st.markdown(get_risk_profile(c_data['Company'], c_data['Sector']))
        
        # Gauge Chart for Risk Meter
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = (c_data['Annual_Emissions_kg'] / total_emissions) * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Share of Top 20 Indian Emissions (%)", 'font': {'color': 'white'}},
            gauge = {
                'axis': {'range': [None, 15], 'tickcolor': "white"},
                'bar': {'color': "#ef4444"},
                'steps': [
                    {'range': [0, 5], 'color': "rgba(16, 185, 129, 0.2)"},
                    {'range': [5, 10], 'color': "rgba(251, 191, 36, 0.2)"},
                    {'range': [10, 15], 'color': "rgba(239, 68, 68, 0.2)"}],
            }
        ))
        fig_gauge.update_layout(height=250, margin=dict(t=40, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)", font_color="white")
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- DATAFRAME EXPANDER ---
    st.markdown("---")
    with st.expander("🗄️ View Complete Corporate Emissions Ledger (Raw Data)", expanded=False):
        # Formatting for display
        df_display = df_corps.copy()
        for col in ['Annual_Emissions_kg', 'Safe_Target_kg', 'Credits_Needed_kg']:
            df_display[col] = df_display[col].apply(lambda x: f"{x:,.0f} kg")
        df_display['Financial_Liability_INR'] = df_display['Financial_Liability_INR'].apply(lambda x: f"₹{x:,.0f}")
        
        # Custom styling for the dataframe
        st.dataframe(
            df_display.set_index('Rank'),
            use_container_width=True,
            height=400
        )

    # --- EXTRA BOTTOM PADDING / SPACING ---
    # Adding generous empty space at the bottom of the page
    # This ensures the dashboard doesn't cut off abruptly
    # and allows users to scroll comfortably past the last element.
    # We use multiple breaks to ensure a clean, floating footer feel.
    st.markdown("<br>" * 5, unsafe_allow_html=True)
    st.markdown("<br>" * 5, unsafe_allow_html=True)
    st.markdown("<br>" * 5, unsafe_allow_html=True)

if __name__ == "__main__":
    main()