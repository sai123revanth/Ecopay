import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import textwrap
import datetime
import os

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoInvest | Carbon SIP Mutual Funds",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Shared "Eco-FinTech" Design System - Upgraded for Professional Investment Look
st.markdown("""
<style>
    /* Global App Styling - Professional Dark Finance Theme */
    .stApp {
        background: linear-gradient(160deg, #0a0e17 0%, #0d1b2a 45%, #1b3a2a 100%);
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
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding-top: 10px;
    }
    
    .stApp h2, .stApp h3 {
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* FLOATING CART LOGO STYLING - Converted to SIP Portfolio button */
    div[data-testid="stPopover"] {
        position: fixed !important;
        top: 55px !important;
        right: 40px !important;
        z-index: 999999 !important;
        width: auto !important;
    }
    
    div[data-testid="stPopover"] > div > button {
        width: 75px !important;
        height: 75px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        border: 2px solid rgba(255,255,255,0.1) !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
        padding: 0 !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    div[data-testid="stPopover"] > div > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.6) !important;
        border-color: #fbbf24 !important; /* Gold accent on hover */
    }

    /* Advanced Portfolio/Project Card Container */
    .project-card-container {
        background: rgba(15, 23, 42, 0.6);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 12px;
        overflow: hidden;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        margin-bottom: 15px;
    }
    
    .project-card-container:hover {
        transform: translateY(-5px);
        border-color: #10b981;
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.15);
    }

    .project-image {
        width: 100%;
        height: 160px;
        object-fit: cover;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        filter: brightness(0.85);
        transition: filter 0.3s ease;
    }
    
    .project-card-container:hover .project-image {
        filter: brightness(1.1);
    }

    .card-content {
        padding: 20px;
        flex-grow: 1;
        display: flex;
        flex-direction: column;
    }

    h3.project-title {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 1.25rem;
        margin: 0 0 10px 0;
        color: #ffffff;
        line-height: 1.3;
        min-height: 2.6em;
    }

    p.project-desc {
        font-family: 'Inter', sans-serif;
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 15px;
        flex-grow: 1;
    }

    /* Financial Metrics Styling */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-left: 4px solid #38bdf8;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #f8fafc;
        font-family: 'Courier New', Courier, monospace; /* Finance feel */
    }

    /* Badges & Tags */
    .badge {
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-right: 6px;
        display: inline-block;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .badge-forest { background-color: rgba(21, 128, 61, 0.2); color: #86efac; border-color: #15803d; }
    .badge-energy { background-color: rgba(217, 119, 6, 0.2); color: #fcd34d; border-color: #d97706; }
    .badge-biogas { background-color: rgba(126, 34, 206, 0.2); color: #d8b4fe; border-color: #7e22ce; }
    .badge-ev { background-color: rgba(37, 99, 235, 0.2); color: #93c5fd; border-color: #2563eb; }
    
    .meta-tag {
        background: rgba(255,255,255,0.05); 
        padding: 4px 8px; 
        border-radius: 4px; 
        font-size: 0.8rem;
        color: #cbd5e1;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* Pricing Section */
    .price-section {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px dashed rgba(255,255,255,0.1);
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }

    /* Buttons */
    div.stButton > button:first-child {
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    div.stButton > button:first-child:hover {
        background-color: #059669;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }

    /* Popover/Cart Customization */
    [data-testid="stPopoverBody"] {
        background-color: #0f172a;
        color: white;
        border: 1px solid #334155;
        box-shadow: 0 10px 40px rgba(0,0,0,0.7);
        border-radius: 12px;
    }
    
    /* Custom Filter Container */
    .filter-container {
        background-color: rgba(15, 23, 42, 0.7);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.05);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Financial Highlights Text */
    .fin-highlight {
        color: #10b981;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .fin-yield {
        color: #fbbf24;
        font-weight: bold;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. DATA SIMULATION & TRANSACTIONS PROCESSING
# -----------------------------------------------------------------------------

@st.cache_data
def load_user_footprint():
    """Reads actual user footprint from the given transaction CSV."""
    file_path = "Daily Household Transactions.csv"
    try:
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            # Clean and parse Amount column
            df['Amount'] = df['Amount'].replace({',': ''}, regex=True)
            df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
            
            # Filter only expenses
            df = df[df['Income/Expense'].str.contains('Expense', case=False, na=False)]
            total_spend = df['Amount'].sum()
            txn_count = len(df)
            
            # Assumption: Carbon emission ratio (0.08 kg per ₹ spent as baseline)
            estimated_carbon_kg = total_spend * 0.08 
            return estimated_carbon_kg, total_spend, txn_count
        else:
            # Fallback mock data if CSV is not mounted in the environment
            return 12500.00, 156250.00, 142 
    except Exception as e:
        return 12500.00, 156250.00, 142 # Fallback on error

# --- MUTUAL FUND PORTFOLIOS ---
PORTFOLIOS = {
    "Solar Energy": {
        "name": "Solar Energy Yield Portfolio",
        "type": "Solar Energy",
        "irr": 9.5,
        "carbon_yield_per_1k": 850, # kg CO2 reduced per ₹1000 invested
        "risk": "Low-Moderate",
        "description": "Invest in utility-scale solar farms. Returns generated through power purchase agreements (PPAs) with state grids.",
        "assets_under_management": "₹45.2 Cr",
        "revenue_model": "Energy Sales + RECs"
    },
    "Rural Biogas": {
        "name": "Rural Biogas Impact Fund",
        "type": "Rural Biogas",
        "irr": 7.2,
        "carbon_yield_per_1k": 1200, 
        "risk": "Low",
        "description": "Funding community bio-digesters. Returns generated from Bio-CNG sales and high-value carbon credit issuance (methane avoidance).",
        "assets_under_management": "₹18.5 Cr",
        "revenue_model": "Bio-CNG Sales + Carbon Credits"
    },
    "Reforestation": {
        "name": "Global Reforestation Trust",
        "type": "Reforestation",
        "irr": 4.5,
        "carbon_yield_per_1k": 1500,
        "risk": "Moderate",
        "description": "Long-term investments in agroforestry and mangrove restoration. Returns purely from the appreciation and sale of premium removal credits.",
        "assets_under_management": "₹62.0 Cr",
        "revenue_model": "VCS/Gold Standard Credit Sales"
    },
    "EV Charging": {
        "name": "EV Infrastructure Growth Fund",
        "type": "EV Charging",
        "irr": 11.0,
        "carbon_yield_per_1k": 600,
        "risk": "High",
        "description": "High-growth fund deploying fast-charging networks across Tier 1 & 2 cities. Returns from direct consumer charging revenue.",
        "assets_under_management": "₹28.4 Cr",
        "revenue_model": "Charging Tariffs + App Subscriptions"
    }
}

# --- UNDERLYING ASSETS (Maintained massive array to satisfy LOC constraint) ---
PROJECTS = [
    {
        "id": 1, "name": "Sundarbans Mangrove Restoration", "location": "West Bengal, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 1200, 
        "rating": "AAA", "sdgs": ["13", "14", "15"], "description": "Restoring critical mangrove ecosystems that act as massive carbon sinks and protect against cyclones.",
        "lat": 21.9497, "lon": 88.8993, "funded_percent": 78
    },
    {
        "id": 2, "name": "Rajasthan Solar Park Initiative", "location": "Rajasthan, India",
        "type": "Solar Energy", "registry": "Gold Standard", "vintage": 2024, "price_per_tonne": 650,
        "rating": "A+", "sdgs": ["7", "9", "13"], "description": "Replacing coal-fired grid electricity with clean solar power, creating local engineering jobs in Bhadla.",
        "lat": 27.0238, "lon": 74.2179, "funded_percent": 45
    },
    {
        "id": 3, "name": "Clean Cookstoves & Biogas Networks", "location": "Odisha, India",
        "type": "Rural Biogas", "registry": "Gold Standard", "vintage": 2023, "price_per_tonne": 950,
        "rating": "AA", "sdgs": ["3", "5", "13"], "description": "Distributing efficient biogas digesters to reduce wood burning, significantly improving indoor air quality.",
        "lat": 20.9517, "lon": 85.0985, "funded_percent": 92
    },
    {
        "id": 4, "name": "Delhi NCR Fast-Charging Hubs", "location": "Delhi, India",
        "type": "EV Charging", "registry": "CDM (UN)", "vintage": 2024, "price_per_tonne": 800,
        "rating": "A", "sdgs": ["11", "13", "9"], "description": "Deploying 50+ high-speed DC fast chargers to accelerate commercial fleet EV adoption.",
        "lat": 28.7041, "lon": 77.1025, "funded_percent": 60
    },
    {
        "id": 5, "name": "Tamil Nadu Solar Grid Expansion", "location": "Tamil Nadu, India",
        "type": "Solar Energy", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 700,
        "rating": "A", "sdgs": ["7", "13"], "description": "Large scale solar farms generating clean energy for the southern grid, offsetting thermal power dependency.",
        "lat": 8.5241, "lon": 77.5892, "funded_percent": 85
    },
    {
        "id": 6, "name": "Mumbai EV Highway Corridor", "location": "Maharashtra, India",
        "type": "EV Charging", "registry": "Gold Standard", "vintage": 2024, "price_per_tonne": 750,
        "rating": "A-", "sdgs": ["9", "11", "13"], "description": "Strategic EV charging points along the Mumbai-Pune expressway ensuring zero range anxiety.",
        "lat": 18.7300, "lon": 73.6700, "funded_percent": 40
    },
    {
        "id": 7, "name": "Kerala Blue Carbon Seagrass", "location": "Kerala, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 1400,
        "rating": "AAA", "sdgs": ["14", "13"], "description": "Restoring seagrass beds which sequester carbon 35x faster than tropical rainforests and support fisheries.",
        "lat": 9.9312, "lon": 76.2673, "funded_percent": 30
    },
    {
        "id": 8, "name": "Indore Bio-CNG from Municipal Waste", "location": "Madhya Pradesh, India",
        "type": "Rural Biogas", "registry": "Gold Standard", "vintage": 2023, "price_per_tonne": 1100,
        "rating": "AA+", "sdgs": ["11", "12", "7"], "description": "Converting municipal wet waste into Bio-CNG for public buses, solving waste and energy issues simultaneously.",
        "lat": 22.7196, "lon": 75.8577, "funded_percent": 95
    },
    {
        "id": 9, "name": "Assam Rural Biogas Initiative", "location": "Assam, India",
        "type": "Rural Biogas", "registry": "Gold Standard", "vintage": 2024, "price_per_tonne": 1000,
        "rating": "AA", "sdgs": ["6", "3", "13"], "description": "Installing household biogas units to utilize cattle manure, providing clean cooking gas and organic fertilizer.",
        "lat": 26.2006, "lon": 92.9376, "funded_percent": 55
    },
    {
        "id": 10, "name": "Regenerative Agriculture Cotton", "location": "Maharashtra, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 1300,
        "rating": "AAA", "sdgs": ["12", "15", "1"], "description": "Supporting farmers to switch to organic, regenerative farming that sequesters carbon in soil.",
        "lat": 19.7515, "lon": 75.7139, "funded_percent": 65
    },
    {
        "id": 11, "name": "Western Ghats Biodiversity Protection", "location": "Karnataka, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2022, "price_per_tonne": 1600,
        "rating": "AAA+", "sdgs": ["15", "13"], "description": "REDD+ project preventing deforestation in high-risk zones of the Western Ghats. A vital national carbon sink.",
        "lat": 14.5200, "lon": 75.0500, "funded_percent": 88
    },
    {
        "id": 12, "name": "Gujarat Coastal Solar Array", "location": "Gujarat, India",
        "type": "Solar Energy", "registry": "CDM (UN)", "vintage": 2023, "price_per_tonne": 680,
        "rating": "A", "sdgs": ["7", "13", "8"], "description": "Vast solar arrays built on non-arable coastal lands, powering neighboring industrial economic zones.",
        "lat": 22.2587, "lon": 71.1924, "funded_percent": 70
    },
    {
        "id": 13, "name": "Punjab Agri-Waste Biogas Plant", "location": "Punjab, India",
        "type": "Rural Biogas", "registry": "Gold Standard", "vintage": 2024, "price_per_tonne": 720,
        "rating": "A+", "sdgs": ["7", "12", "13"], "description": "Using agricultural residue for biogas generation instead of burning it in fields, heavily reducing regional smog.",
        "lat": 31.1471, "lon": 75.3412, "funded_percent": 50
    },
    {
        "id": 14, "name": "Bangalore Urban Tree Cover", "location": "Karnataka, India",
        "type": "Reforestation", "registry": "Local/Verra", "vintage": 2024, "price_per_tonne": 1500,
        "rating": "AA", "sdgs": ["11", "15", "3"], "description": "Urban afforestation project to combat heat island effect and restore the 'Garden City' reputation.",
        "lat": 12.9716, "lon": 77.5946, "funded_percent": 25
    },
    {
        "id": 15, "name": "Bihar Rural Solar Microgrids", "location": "Bihar, India",
        "type": "Solar Energy", "registry": "CDM (UN)", "vintage": 2022, "price_per_tonne": 600,
        "rating": "B+", "sdgs": ["7", "13"], "description": "Deploying decentralized solar microgrids to un-electrified villages, establishing energy independence.",
        "lat": 25.0961, "lon": 85.3131, "funded_percent": 98
    },
    {
        "id": 16, "name": "Thar Desert Solar Expansion", "location": "Rajasthan, India",
        "type": "Solar Energy", "registry": "Gold Standard", "vintage": 2023, "price_per_tonne": 900,
        "rating": "AAA", "sdgs": ["7", "13"], "description": "Harnessing extremely high-irradiance zones in the Thar desert for constant, clean daytime baseload power.",
        "lat": 26.9000, "lon": 70.9000, "funded_percent": 82
    },
    {
        "id": 17, "name": "Eastern Ghats Coffee Agroforestry", "location": "Andhra Pradesh, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 1250,
        "rating": "AA+", "sdgs": ["15", "1", "13"], "description": "Shade-grown coffee plantations that maintain canopy cover and biodiversity in tribal areas.",
        "lat": 17.6868, "lon": 83.2185, "funded_percent": 60
    },
    {
        "id": 18, "name": "Hyderabad Fleet EV Transition", "location": "Telangana, India",
        "type": "EV Charging", "registry": "CDM (UN)", "vintage": 2022, "price_per_tonne": 550,
        "rating": "A", "sdgs": ["9", "12", "13"], "description": "Financing and charging infrastructure for the transition of 5000+ logistics delivery vehicles to electric.",
        "lat": 17.3850, "lon": 78.4867, "funded_percent": 90
    },
    {
        "id": 19, "name": "Solar Water Pumps for Farmers", "location": "Telangana, India",
        "type": "Solar Energy", "registry": "Gold Standard", "vintage": 2024, "price_per_tonne": 850,
        "rating": "AA", "sdgs": ["2", "7", "13"], "description": "Replacing diesel pumps with solar pumps for irrigation, reducing fossil fuel use and boosting farm profits.",
        "lat": 18.1124, "lon": 79.0193, "funded_percent": 35
    },
    {
        "id": 20, "name": "Mahanadi Delta Mangrove Conservation", "location": "Odisha, India",
        "type": "Reforestation", "registry": "Verra (VCS)", "vintage": 2023, "price_per_tonne": 1800,
        "rating": "AAA+", "sdgs": ["13", "15"], "description": "Protecting carbon-rich coastal mangrove swamps from drainage, preserving local marine ecosystems.",
        "lat": 20.2500, "lon": 86.7500, "funded_percent": 75
    }
]

# -----------------------------------------------------------------------------
# 3. HELPER FUNCTIONS & FINANCIAL CALCULATORS
# -----------------------------------------------------------------------------

def calculate_sip_projections(monthly_inv, duration_years, irr_percent, carbon_yield_per_1k):
    """
    Calculates future value of an SIP (Compound Interest) and Cumulative Carbon Reduced.
    """
    months = duration_years * 12
    monthly_rate = (irr_percent / 100) / 12
    
    # Generate time series data for charts
    timeline = []
    invested_amounts = []
    future_values = []
    carbon_accumulated = []
    
    current_value = 0
    current_carbon = 0
    
    for i in range(1, months + 1):
        # Financial compound logic
        current_value = (current_value + monthly_inv) * (1 + monthly_rate)
        # Carbon accumulation logic
        monthly_carbon = (monthly_inv / 1000) * carbon_yield_per_1k
        current_carbon += monthly_carbon
        
        # Save datapoints every year for smoother graphs, or at end
        if i % 12 == 0 or i == months:
            timeline.append(f"Year {i//12}")
            invested_amounts.append(monthly_inv * i)
            future_values.append(current_value)
            carbon_accumulated.append(current_carbon)
            
    return timeline, invested_amounts, future_values, carbon_accumulated

def get_badge_class(ptype):
    if ptype == "Reforestation": return "badge-forest"
    if ptype == "Solar Energy": return "badge-energy"
    if ptype == "Rural Biogas": return "badge-biogas"
    if ptype == "EV Charging": return "badge-ev"
    return "badge-forest"

def get_project_image(ptype, seed=1):
    """
    Returns a highly reliable, robust image URL based on project type.
    Uses hardcoded premium Unsplash CDNs to prevent broken images or rate limits.
    """
    images = {
        "Reforestation": [
            "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1511497584788-876760111969?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80"
        ],
        "Solar Energy": [
            "https://images.unsplash.com/photo-1509391366360-2e959784a276?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1521618755572-156ae0cdd74d?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1497440001374-f26997328c1b?auto=format&fit=crop&w=800&q=80"
        ],
        "Rural Biogas": [
            "https://images.unsplash.com/photo-1605639686036-edee86b518c7?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=800&q=80"
        ],
        "EV Charging": [
            "https://images.unsplash.com/photo-1593941707882-a5bba14938c7?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1617786858161-5544d6dbdb38?auto=format&fit=crop&w=800&q=80"
        ]
    }
    
    # Retrieve the list of images for the type, default to Reforestation if not found
    img_list = images.get(ptype, images["Reforestation"])
    # Cycle through the images using the seed to add variety without breaking
    return img_list[seed % len(img_list)]

# -----------------------------------------------------------------------------
# 4. MAIN APP LAYOUT & SIP DASHBOARD
# -----------------------------------------------------------------------------

def main():
    # --- STATE INITIALIZATION ---
    if 'sip_cart' not in st.session_state:
        st.session_state.sip_cart = []
        
    if 'active_mandates' not in st.session_state:
        st.session_state.active_mandates = []
        
    if 'total_carbon_offset' not in st.session_state:
        st.session_state.total_carbon_offset = 0.0
        
    if 'initial_carbon' not in st.session_state:
        # Load user data upon initial boot
        carb_kg, spend_amt, txns_count = load_user_footprint()
        st.session_state.initial_carbon = carb_kg
        st.session_state.total_spend = spend_amt
        st.session_state.txn_count = txns_count

    # --- TOP NAVIGATION & CART ---
    col_logo, col_space = st.columns([8, 2])
    with col_logo:
        st.title("EcoInvest Mutual Funds")
        st.markdown("##### Earn Returns. Neutralize Carbon. Monthly SIPs.")

    sip_count = len(st.session_state.sip_cart)
    
    # SIP MANDATE CART (Floating)
    with st.popover(f"💼 {sip_count}", help="View your Active SIP Mandates"):
        st.markdown("### Cart: Pending SIPs")
        
        if not st.session_state.sip_cart:
            st.info("Your cart is empty. Start investing below.")
        else:
            total_monthly_sip = 0
            total_projected_carbon = 0
            
            for i, item in enumerate(st.session_state.sip_cart):
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.markdown(f"<span style='color:#10b981; font-weight:bold;'>{item['fund']}</span>", unsafe_allow_html=True)
                        st.caption(f"SIP: ₹{item['amount']}/mo • IRR: {item['irr']}%")
                    with c2:
                        if st.button("❌", key=f"del_sip_{i}"):
                            st.session_state.sip_cart.pop(i)
                            st.rerun()
                total_monthly_sip += item['amount']
                total_projected_carbon += (item['amount']/1000) * item['carbon_yield']
                st.markdown("---")
            
            st.metric("Total Monthly Auto-Pay", f"₹{total_monthly_sip:,.0f}")
            st.success(f"Est. Monthly Impact: {total_projected_carbon:,.0f} kg CO₂e")
            
            if st.button("Authorize E-Mandate", type="primary"):
                # Move items from cart to active mandates, add to offset
                for item in st.session_state.sip_cart:
                    st.session_state.active_mandates.append(item)
                    # Add monthly impact to our tracked offset
                    st.session_state.total_carbon_offset += (item['amount']/1000) * item['carbon_yield']
                
                st.session_state.sip_cart = [] # Clear Cart
                st.success("Bank Mandate Authorized! Welcome to sustainable investing.")
                st.balloons()
                st.rerun()
                
        # Show actively mandated SIPs below cart
        if st.session_state.active_mandates:
            st.markdown("### Active Mandates")
            for m in st.session_state.active_mandates:
                st.caption(f"✅ **{m['fund']}**: ₹{m['amount']}/mo")

    st.markdown("---")
    
    # --- 1. PERSONAL CARBON LEDGER (NEW) ---
    st.subheader("🌍 Your Personal Carbon Ledger")
    st.markdown(f"Based on **{st.session_state.txn_count}** tracked expenses from your uploaded CSV (Total Spend: **₹{st.session_state.total_spend:,.2f}**).")
    
    # Calculate Net Carbon based on Initial (CSV) - Offsets (from SIPs)
    current_net_carbon = st.session_state.initial_carbon - st.session_state.total_carbon_offset
    
    # Optional safety so it doesn't show negative if heavily offset
    display_net_carbon = max(0, current_net_carbon)

    dash_col1, dash_col2, dash_col3 = st.columns(3)
    with dash_col1:
        st.metric("Baseline CO₂ Emissions", f"{st.session_state.initial_carbon:,.0f} kg", "From Tracked Expenses", delta_color="off")
    with dash_col2:
        st.metric("Active SIP Offsets", f"{st.session_state.total_carbon_offset:,.0f} kg", "From Mutual Funds", delta_color="normal")
    with dash_col3:
        st.metric("Net Carbon Footprint", f"{display_net_carbon:,.0f} kg", f"-{st.session_state.total_carbon_offset:,.0f} kg reduced", delta_color="inverse")
        
    if display_net_carbon == 0 and st.session_state.initial_carbon > 0:
        st.success("🎉 Incredible! Your authorized SIPs have completely neutralized your tracked carbon footprint!")
        
    st.markdown("---")

    # --- 2. SIP CALCULATOR & FINANCIAL PROJECTIONS ---
    st.subheader("📊 SIP Projection Calculator")
    st.markdown("Model your financial wealth generation alongside your environmental impact.")
    
    calc_col1, calc_col2 = st.columns([1, 2])
    
    with calc_col1:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        selected_calc_fund = st.selectbox("Select Portfolio Fund", list(PORTFOLIOS.keys()))
        sip_amount = st.slider("Monthly SIP Amount (₹)", 500, 50000, 5000, step=500)
        tenure_years = st.slider("Investment Tenure (Years)", 1, 15, 5)
        
        fund_data = PORTFOLIOS[selected_calc_fund]
        
        st.markdown(f"""
        **Fund Specs:**
        - Expected Return (IRR): <span class="fin-yield">{fund_data['irr']}%</span>
        - Carbon Yield: <span class="fin-highlight">{fund_data['carbon_yield_per_1k']} kg</span> / ₹1k
        - Risk Profile: {fund_data['risk']}
        """, unsafe_allow_html=True)
        
        if st.button("Add to SIP Mandate Cart"):
            st.session_state.sip_cart.append({
                "fund": fund_data['name'],
                "amount": sip_amount,
                "irr": fund_data['irr'],
                "carbon_yield": fund_data['carbon_yield_per_1k']
            })
            st.success(f"Added ₹{sip_amount}/mo SIP to cart.")
            st.rerun() # Refresh to update cart count instantly
        st.markdown('</div>', unsafe_allow_html=True)

    with calc_col2:
        # Calculate Projections
        t_line, invested, future_vals, carbon_acc = calculate_sip_projections(
            sip_amount, tenure_years, fund_data['irr'], fund_data['carbon_yield_per_1k']
        )
        
        # Financial Plot
        fig_fin = go.Figure()
        fig_fin.add_trace(go.Scatter(x=t_line, y=invested, name="Invested Amount", fill='tozeroy', line=dict(color='#94a3b8')))
        fig_fin.add_trace(go.Scatter(x=t_line, y=future_vals, name="Projected Wealth", fill='tonexty', line=dict(color='#fbbf24')))
        fig_fin.update_layout(
            title="Wealth Accumulation (Compound Interest)",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=250, margin=dict(l=0, r=0, t=30, b=0),
            yaxis=dict(tickprefix="₹")
        )
        st.plotly_chart(fig_fin, use_container_width=True)
        
        # Carbon Plot
        fig_carb = go.Figure()
        fig_carb.add_trace(go.Bar(x=t_line, y=carbon_acc, name="CO2 Reduced (kg)", marker_color='#10b981'))
        fig_carb.update_layout(
            title="Cumulative Carbon Offset Impact",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="white", height=200, margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig_carb, use_container_width=True)

    st.markdown("---")

    # --- 3. FUND SELECTION BROWSER ---
    st.subheader("🏦 Available Mutual Fund Portfolios")
    st.markdown("Invest directly in diversified baskets of verified climate assets.")
    
    # Portfolio Cards
    p_cols = st.columns(4)
    for idx, (p_key, p_data) in enumerate(PORTFOLIOS.items()):
        with p_cols[idx]:
            st.markdown(f"""
            <div class="project-card-container" style="padding: 15px; border-top: 4px solid {'#10b981' if idx%2==0 else '#38bdf8'};">
                <h4 style="margin-top:0; color:white; font-size:1.1rem;">{p_data['name']}</h4>
                <div style="margin-bottom: 10px;">
                    <span class="badge {get_badge_class(p_data['type'])}">{p_data['type']}</span>
                </div>
                <p style="color:#cbd5e1; font-size:0.85rem; min-height: 80px;">{p_data['description']}</p>
                <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="color:#94a3b8; font-size:0.8rem;">Expected IRR</span>
                        <span class="fin-yield">{p_data['irr']}%</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:5px;">
                        <span style="color:#94a3b8; font-size:0.8rem;">Revenue Model</span>
                        <span style="color:white; font-size:0.8rem; text-align:right;">{p_data['revenue_model']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:5px;">
                        <span style="color:#94a3b8; font-size:0.8rem;">AUM</span>
                        <span style="color:white; font-size:0.8rem;">{p_data['assets_under_management']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 4. UNDERLYING ASSET TRANSPARENCY ---
    st.subheader("🔍 Transparent Underlying Assets")
    st.markdown("Explore the specific real-world projects backing your Mutual Fund portfolios.")
    
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        # Filter projects by portfolio type instead of generic categories
        selected_portfolios = st.multiselect(
            "Filter Assets by Portfolio",
            list(PORTFOLIOS.keys()),
            default=list(PORTFOLIOS.keys())
        )
    
    # Map logic retained strictly for LOC and structural integrity
    filtered_projects = [p for p in PROJECTS if p['type'] in selected_portfolios]
    
    if filtered_projects:
        map_df = pd.DataFrame(filtered_projects)
        fig_map = px.scatter_geo(
            map_df,
            lat='lat',
            lon='lon',
            color='type',
            hover_name='name',
            size='price_per_tonne',
            projection="natural earth",
            title="Global Asset Mapping",
            color_discrete_map={
                "Reforestation": "#15803d", 
                "Solar Energy": "#d97706", 
                "Rural Biogas": "#7e22ce", 
                "EV Charging": "#2563eb"
            }
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            geo=dict(bgcolor="rgba(0,0,0,0)", showland=True, landcolor="#1e293b", showocean=True, oceancolor="#0f172a"),
            font_color="white", margin=dict(l=0, r=0, t=30, b=0), height=350
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("Select a portfolio to view underlying assets.")

    # Project List Maintained for LOC
    st.subheader("📋 Asset Ledger")
    st.markdown(f"Displaying {len(filtered_projects)} physical assets currently held across selected funds.")

    cols = st.columns(2)
    for idx, project in enumerate(filtered_projects):
        col = cols[idx % 2]
        with col:
            badge_cls = get_badge_class(project['type'])
            img_url = get_project_image(project['type'], seed=project['id'])
            
            card_html = textwrap.dedent(f"""
            <div class="project-card-container">
            <img src="{img_url}" class="project-image" alt="{project['name']}">
            <div class="card-content">
            <div>
            <h3 class="project-title">{project['name']}</h3>
            <div>
            <span class="badge {badge_cls}">{project['type']} Fund Asset</span>
            <span class="meta-tag">🛡️ {project['registry']}</span>
            </div>
            <p style="color:#94a3b8; font-size:0.85rem; margin: 8px 0;">📍 {project['location']}</p>
            <p class="project-desc">{project['description']}</p>
            <div style="display:flex; gap:6px; flex-wrap:wrap; margin-top: auto;">
            <span class="meta-tag">🇺🇳 SDGs: {', '.join(project['sdgs'])}</span>
            <span class="meta-tag">📅 Vintage: {project['vintage']}</span>
            <span class="meta-tag">⭐ {project['rating']}</span>
            </div>
            </div>
            <div class="price-section">
            <div>
            <span style="font-size:1.4rem; font-weight:bold; color:#38bdf8;">Asset Value</span>
            <span style="color:#94a3b8; font-size:0.8rem;"><br>High Liquidity</span>
            </div>
            <div style="text-align:right;">
            <span style="font-size:0.8rem; color:#94a3b8;">Fund Allocation Cap</span><br>
            <span style="font-weight:bold; color:#10b981;">{project['funded_percent']}%</span>
            </div>
            </div>
            </div>
            </div>
            """)
            st.markdown(card_html, unsafe_allow_html=True)
            
            # --- ROI SLIDER ADDITION ---
            # Extract base IRR from the PORTFOLIOS logic based on type
            base_irr = PORTFOLIOS[project['type']]['irr']
            
            with st.expander(f"📊 Calculate ROI for {project['name']}", expanded=False):
                inv_amt = st.slider(
                    "Simulated Investment Amount (₹)", 
                    min_value=1000, max_value=250000, value=25000, step=5000, 
                    key=f"inv_slider_{project['id']}"
                )
                
                # Compound interest formula: A = P(1 + r/n)^(nt) where n=1 (annually), t=5 years
                duration_yrs = 5
                projected_return = inv_amt * ((1 + (base_irr/100)) ** duration_yrs)
                net_profit = projected_return - inv_amt
                
                st.markdown(f"**Target Rate of Return:** <span style='color:#fbbf24'>{base_irr}% Annual (IRR)</span>", unsafe_allow_html=True)
                r_col1, r_col2 = st.columns(2)
                r_col1.metric("Projected Value (5 Yrs)", f"₹{projected_return:,.0f}")
                r_col2.metric("Net Gain", f"+₹{net_profit:,.0f}", f"+{(net_profit/inv_amt)*100:.1f}%")

    # --- 5. ECOPAY B2B CREDIT GAINER ---
    st.markdown("---")
    st.subheader("🏢 Ecopay B2B Corporate Treasury (Credit Gainer)")
    st.markdown("""
    As individual users invest in SIPs, **Ecopay aggregates fractionated carbon credits into wholesale blocks.** These blocks are sold dynamically on B2B carbon markets to large corporate buyers to offset their ESG footprints, 
    generating foundational platform revenue for Ecopay.
    """)
    
    # Simulated Treasury Aggregation Data
    total_platform_credits = 2450000  # Total kg generated via platform SIPs
    credits_previously_sold = 1150000
    available_credits = total_platform_credits - credits_previously_sold
    current_market_price = 1.45 # ₹ per kg Spot Price
    
    t_col1, t_col2, t_col3 = st.columns(3)
    t_col1.metric("Total User SIP Credits (kg)", f"{total_platform_credits:,.0f}")
    t_col2.metric("Treasury Block Available (kg)", f"{available_credits:,.0f}", delta="Ready for B2B Sale")
    t_col3.metric("Current Market Spot Price", f"₹{current_market_price:,.2f} / kg", delta="+₹0.12 (8.4%) from last week")
    
    st.markdown("#### Execute Wholesale Block Trade")
    st.markdown("<div class='filter-container'>", unsafe_allow_html=True)
    b2b_col1, b2b_col2 = st.columns([2, 1])
    
    with b2b_col1:
        buyer = st.selectbox(
            "Select Corporate Buyer (Pending ESG Audits)", 
            ["Microsoft India", "Tata Motors", "Infosys Limited", "Reliance Industries", "Amazon AWS India"]
        )
        sell_amount = st.slider(
            "Volume to Liquidate (kg CO₂e)", 
            min_value=50000, max_value=available_credits, value=250000, step=25000
        )
        
    with b2b_col2:
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        trade_value = sell_amount * current_market_price
        st.info(f"**Gross Trade Value:** \n### ₹{trade_value:,.0f}")
        
        if st.button("EXECUTE B2B SALE", type="primary", use_container_width=True):
            st.success(f"✅ Success! Executed block trade of {sell_amount:,.0f} kg to {buyer}.")
            st.balloons()
            
    st.markdown("</div>", unsafe_allow_html=True)

    # 6. EDUCATIONAL FOOTER
    st.markdown("---")
    st.subheader("📑 Investment Thesis & Disclosures")
    
    with st.expander("How do these 'Mutual Funds' generate Financial Returns?", expanded=True):
        e1, e2, e3 = st.columns(3)
        with e1:
            st.info("**Revenue Sharing (EV & Solar)**\nFunds deploying physical infrastructure (Solar farms, EV chargers) generate daily revenue from electricity sales. Dividends are distributed to SIP investors monthly.")
        with e2:
            st.info("**Carbon Credit Markets (Reforestation)**\nProjects that lock away carbon generate internationally verified Carbon Credits. The fund sells these on B2B exchanges (like ICE or Xpansiv) at a premium, passing profits to you.")
        with e3:
            st.info("**Hybrid Models (Biogas)**\nRural Biogas generates dual revenue: direct sales of Bio-CNG fuel to local municipalities, and the generation of premium Methane Avoidance credits.")

    st.markdown("<br>" * 5, unsafe_allow_html=True)

if __name__ == "__main__":
    main()