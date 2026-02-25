import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from groq import Groq

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Ecopay | Carbon Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Shared "Eco-FinTech" Design System (Reused & Expanded)
st.markdown("""
<style>
    /* Global App Styling */
    .stApp {
        background: linear-gradient(160deg, #02040a 0%, #062c1b 45%, #0d5c3b 100%);
        background-attachment: fixed;
        color: #fafafa;
    }
    
    /* Headers */
    h1 {
        font-family: 'Inter', sans-serif;
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        background: -webkit-linear-gradient(#fff, #aaa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
    }
    
    h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        color: white;
        font-weight: 700;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(0, 210, 106, 0.5);
        transform: translateY(-2px);
    }

    /* Metric Highlights */
    .metric-value {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00d26a, #96c93d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .metric-label {
        color: #aaa;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Timeline Styling */
    .timeline-item {
        border-left: 3px solid #00d26a;
        padding-left: 20px;
        margin-bottom: 20px;
        position: relative;
    }
    .timeline-item::before {
        content: '';
        position: absolute;
        width: 15px;
        height: 15px;
        background: #02040a;
        border: 3px solid #00d26a;
        border-radius: 50%;
        left: -9px;
        top: 0;
    }

    /* Chat Styling */
    .chat-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #00d26a;
        margin-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 10px;
    }

    /* Button Styling */
    .stButton>button {
        background: linear-gradient(135deg, #00b09b, #96c93d) !important;
        color: #02040a !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        transition: all 0.3s ease !important;
        width: 100%;
        margin-top: 20px;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0, 210, 106, 0.4) !important;
    }

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. GROQ API INTEGRATION
# -----------------------------------------------------------------------------

def get_groq_client():
    """Attempt to initialize the Groq client using 'New_API' key."""
    api_key = None
    if "New_API" in st.secrets:
        api_key = st.secrets["New_API"]
    elif "New_API" in os.environ:
        api_key = os.environ["New_API"]
    
    if api_key:
        return Groq(api_key=api_key)
    return None

def generate_eco_profile(data):
    """Calls Groq API to generate the carbon analysis and action plan."""
    client = get_groq_client()
    
    prompt = f"""
    You are an expert environmental data scientist and sustainability coach. 
    Analyze the following user lifestyle data and provide a highly personalized carbon footprint analysis.
    
    USER DATA:
    - Transport: {data['transport']}
    - Diet: {data['diet']}
    - Energy: {data['energy']}
    - Shopping: {data['shopping']}
    
    Return ONLY a valid JSON object with the exact following structure, no markdown, no extra text:
    {{
        "total_carbon_tons": <float, estimated annual CO2 tons>,
        "comparison_to_average": "<string, e.g., '20% below average'>",
        "breakdown": {{
            "Transport": <int, percentage>,
            "Diet": <int, percentage>,
            "Energy": <int, percentage>,
            "Shopping": <int, percentage>
        }},
        "improvements": [
            {{
                "title": "<string, catchy title>",
                "impact": "<string, estimated CO2 saved>",
                "description": "<string, realistic explanation>"
            }},
            // exactly 3 realistic improvements
        ],
        "action_plan_30_days": [
            {{"week": "Week 1", "focus": "<string>", "action": "<string>"}},
            {{"week": "Week 2", "focus": "<string>", "action": "<string>"}},
            {{"week": "Week 3", "focus": "<string>", "action": "<string>"}},
            {{"week": "Week 4", "focus": "<string>", "action": "<string>"}}
        ]
    }}
    """

    if not client:
        return get_mock_response()

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, 
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        st.error(f"API Error: {str(e)}. Using fallback data.")
        return get_mock_response()

def chat_with_assistant(messages):
    """Handles multilingual chat queries via Groq."""
    client = get_groq_client()
    
    system_prompt = {
        "role": "system",
        "content": "You are a highly professional Eco-FinTech AI assistant. You must converse naturally in ANY Indian language the user prefers (e.g., Hindi, Tamil, Telugu, Bengali, Marathi, etc.) as well as English. Keep answers concise, actionable, and focused on sustainability, carbon footprint reduction, and eco-friendly habits."
    }
    
    full_messages = [system_prompt] + messages
    
    if not client:
        return "मुझे क्षमा करें (I apologize), the AI API key is missing. I am currently running in offline mock mode. कृपया बाद में पुनः प्रयास करें।"
        
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=full_messages,
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"System Offline: Unable to process the request due to {str(e)}."

def get_mock_response():
    """Provides structured realistic data if Groq API fails or key is missing."""
    return {
        "total_carbon_tons": 8.4,
        "comparison_to_average": "15% above global average",
        "breakdown": {
            "Transport": 45,
            "Diet": 25,
            "Energy": 20,
            "Shopping": 10
        },
        "improvements": [
            {
                "title": "Adopt a Hybrid Commute",
                "impact": "Save 1.2 tons/yr",
                "description": "Replacing just two days of driving with public transit or work-from-home reduces your transport footprint significantly."
            },
            {
                "title": "Plant-Based Weekends",
                "impact": "Save 0.6 tons/yr",
                "description": "Cutting out red meat specifically on weekends slashes your diet-related methane footprint without requiring a full lifestyle shift."
            },
            {
                "title": "Vampire Energy Purge",
                "impact": "Save 0.3 tons/yr",
                "description": "Using smart power strips to cut power to dormant electronics (TVs, chargers, consoles) stops passive energy drain."
            }
        ],
        "action_plan_30_days": [
            {"week": "Week 1", "focus": "Audit & Awareness", "action": "Calculate your baseline and unplug all unused electronics. Set up recycling bins clearly."},
            {"week": "Week 2", "focus": "Dietary Shifts", "action": "Meal prep 3 fully vegetarian days. Source groceries from local farmers markets if possible."},
            {"week": "Week 3", "focus": "Mobility Change", "action": "Take public transport, walk, or carpool for at least 50% of your total weekly journeys."},
            {"week": "Week 4", "focus": "Sustainable Consumption", "action": "Cancel unnecessary physical subscriptions. Commit to buying zero new clothing this month."}
        ]
    }

# -----------------------------------------------------------------------------
# 3. UI COMPONENTS
# -----------------------------------------------------------------------------

def plot_footprint_donut(breakdown):
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    colors = ['#00d26a', '#3dd5f3', '#ffc107', '#eb3349']

    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.6,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='outside',
        textfont=dict(color='white')
    )])

    fig.update_layout(
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=0, b=0, l=0, r=0),
        height=300,
        annotations=[dict(text='CO₂e', x=0.5, y=0.5, font_size=24, showarrow=False, font_color='white')]
    )
    return fig

# -----------------------------------------------------------------------------
# 4. MAIN APPLICATION
# -----------------------------------------------------------------------------

def main():
    st.markdown("<h1>Personal Carbon Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#aaa; font-size:1.1rem; margin-bottom:30px;'>Quantify your lifestyle impact, chat with our multilingual AI, and generate a realistic path to Net-Zero.</p>", unsafe_allow_html=True)

    # State management
    if 'report_generated' not in st.session_state:
        st.session_state.report_generated = False
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "नमस्ते! Namaste! Hello! I am your Eco-FinTech Assistant. I can speak any Indian language. How can I help you reduce your carbon footprint today?"}
        ]

    # --- MAIN DASHBOARD LAYOUT (2 COLUMNS) ---
    col_form, col_chat = st.columns([1.6, 1])

    # LEFT COLUMN: THE FLATTENED QUESTIONNAIRE
    with col_form:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📋 Complete Your Comprehensive Eco-Profile")
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 15px 0;'>", unsafe_allow_html=True)
        
        user_data = {}
        
        # 1. Transport Section
        st.markdown("<h4 style='color:#00d26a;'>🚗 Transportation Habits</h4>", unsafe_allow_html=True)
        t_c1, t_c2 = st.columns(2)
        with t_c1:
            commute_type = st.selectbox("Primary Commute Method", ["Gas/Petrol Car", "Diesel Car", "Hybrid Car", "EV", "Motorcycle", "Public Transit", "Bicycle/Walking"])
        with t_c2:
            flights = st.selectbox("Air Travel (Annual)", ["None", "1-2 Short Flights", "3-5 Flights", "Frequent Flyer (6+ flights)", "Long-Haul International"])
        weekly_miles = st.slider("Weekly Commute Distance (Miles/Km equivalent)", 0, 500, 100)
        user_data['transport'] = f"Method: {commute_type}, Distance: {weekly_miles}/wk, Flights: {flights}"
        
        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Diet Section
        st.markdown("<h4 style='color:#00d26a;'>🥗 Diet Patterns</h4>", unsafe_allow_html=True)
        d_c1, d_c2 = st.columns(2)
        with d_c1:
            diet_type = st.selectbox("Primary Diet", ["Heavy Meat Eater (Daily)", "Average (Meat 3-4x/week)", "Pescatarian", "Vegetarian", "Vegan"])
        with d_c2:
            food_source = st.selectbox("Food Sourcing", ["Mostly Supermarket (Imported)", "Mix of Supermarket & Local", "Mostly Local/Farmers Market"])
        user_data['diet'] = f"Type: {diet_type}, Sourcing: {food_source}"
        
        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Energy Section
        st.markdown("<h4 style='color:#00d26a;'>⚡ Energy Consumption</h4>", unsafe_allow_html=True)
        e_c1, e_c2 = st.columns(2)
        with e_c1:
            home_type = st.selectbox("Home Type", ["Apartment (1-2 beds)", "Medium House (3 beds)", "Large House (4+ beds)"])
            hvac = st.checkbox("Heavy Air Conditioning / Heating Usage", value=True)
        with e_c2:
            energy_source = st.selectbox("Energy Grid Setup", ["Standard Grid (Fossil Heavy)", "Mixed Grid", "100% Renewable Tariff / Solar"])
        user_data['energy'] = f"Home: {home_type}, Heavy HVAC: {hvac}, Source: {energy_source}"

        st.markdown("<br>", unsafe_allow_html=True)

        # 4. Shopping Section
        st.markdown("<h4 style='color:#00d26a;'>🛍️ Shopping Behavior</h4>", unsafe_allow_html=True)
        s_c1, s_c2 = st.columns(2)
        with s_c1:
            fashion = st.selectbox("Clothing Purchases", ["Frequent Fast Fashion", "Occasional Mainstream Brands", "Mostly Second-hand/Thrift", "Sustainable Brands Only"])
        with s_c2:
            tech = st.selectbox("Tech Replacement Rate", ["Upgrade yearly", "Upgrade every 2-3 years", "Use until broken"])
        user_data['shopping'] = f"Fashion: {fashion}, Tech: {tech}"

        # Generate Report Button
        if st.button("Generate AI Intelligence Report 🚀"):
            with st.spinner("Initializing Groq AI... Crunching your ecosystem data..."):
                st.session_state.report_data = generate_eco_profile(user_data)
                st.session_state.report_generated = True

        st.markdown("</div>", unsafe_allow_html=True) # End form glass card

    # RIGHT COLUMN: MULTILINGUAL CHATBOT
    with col_chat:
        st.markdown("<div class='glass-card' style='height: 100%; min-height: 850px; display: flex; flex-direction: column;'>", unsafe_allow_html=True)
        st.markdown("<div class='chat-header'>🤖 AI Sustainability Coach</div>", unsafe_allow_html=True)
        
        # Chat container (Scrollable)
        chat_container = st.container(height=650, border=False)
        
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        # Chat Input
        prompt = st.chat_input("Ask me anything in Hindi, Tamil, English...")
        if prompt:
            # 1. Add user message to state and display
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)
            
            # 2. Get AI response
            with chat_container:
                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        # Format message history for Groq
                        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                        response = chat_with_assistant(api_messages)
                        st.markdown(response)
            
            # 3. Add AI response to state
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        st.markdown("</div>", unsafe_allow_html=True) # End chat glass card

    # --- FULL WIDTH RESULTS SECTION ---
    if st.session_state.report_generated and st.session_state.report_data:
        data = st.session_state.report_data
        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 40px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2>📊 Your Environmental Ledger</h2>", unsafe_allow_html=True)
        
        # Top Row: Score & Donut
        col_score, col_chart = st.columns([1, 1.5])
        
        with col_score:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center; padding: 40px 20px;'>
                <div class='metric-label'>Annual Carbon Footprint</div>
                <div class='metric-value'>{data['total_carbon_tons']} <span style='font-size:1.5rem; color:#fff;'>Tons</span></div>
                <div style='color: #ffc107; font-weight: bold; margin-top: 10px;'>{data['comparison_to_average']}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_chart:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align:center; margin-bottom:0;'>Emissions Breakdown</h4>", unsafe_allow_html=True)
            st.plotly_chart(plot_footprint_donut(data['breakdown']), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Middle Row: AI Suggested Improvements
        st.markdown("### 💡 High-Yield Strategic Improvements")
        st.markdown("<p style='color:#aaa;'>Algorithms have identified the lowest-friction, highest-impact changes based on your specific profile.</p>", unsafe_allow_html=True)
        
        imp_cols = st.columns(3)
        for i, imp in enumerate(data['improvements']):
            with imp_cols[i]:
                st.markdown(f"""
                <div class='glass-card' style='height: 100%;'>
                    <h4 style='color: #00d26a; margin-top:0;'>{imp['title']}</h4>
                    <span style='background: rgba(0,210,106,0.2); color: #00d26a; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; font-weight:bold;'>{imp['impact']}</span>
                    <p style='margin-top: 15px; font-size: 0.95rem; color: #ddd;'>{imp['description']}</p>
                </div>
                """, unsafe_allow_html=True)

        # Bottom Row: 30-Day Action Plan
        st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin: 40px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2>🗓️ Your 30-Day Eco-Action Plan</h2>", unsafe_allow_html=True)
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        for week_plan in data['action_plan_30_days']:
            st.markdown(f"""
            <div class='timeline-item'>
                <h4 style='margin: 0; color: white;'>{week_plan['week']}: <span style='color: #00d26a;'>{week_plan['focus']}</span></h4>
                <p style='margin-top: 5px; color: #bbb; font-size: 1.05rem;'>{week_plan['action']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()