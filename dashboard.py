import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sports Facility Planner (India)", layout="wide")

st.title("🇮🇳 Indian Sports Facility Planner & Competitor Analysis")
st.markdown("### Interactive Strategic Dashboard for New Operators")

# --- SIDEBAR: FACILITY PARAMETERS ---
st.sidebar.header("1. Define Your Facility Concept")

location_tier = st.sidebar.selectbox("City Tier", ["Tier 1 (Mumbai/Delhi/Blr)", "Tier 2 (Pune/Ahd/Hyd)", "Tier 3"])
market_position = st.sidebar.select_slider("Market Positioning", options=["Budget (YMCA style)", "Mid-Market (Gold's style)", "Premium (David Lloyd style)"])
size_sqft = st.sidebar.number_input("Facility Size (sq ft)", value=5000, step=500)

st.sidebar.subheader("Amenities")
has_pool = st.sidebar.checkbox("Swimming Pool", value=True)
has_gym = st.sidebar.checkbox("Gym Floor", value=True)
has_squash = st.sidebar.checkbox("Squash/Badminton", value=False)
has_studio = st.sidebar.checkbox("Group Class Studio", value=False)

# --- BACKEND LOGIC FOR ESTIMATES (India Market Benchmarks) ---
def get_pricing_estimate(tier, position):
    # Base monthly fees in INR based on market data
    base = 0
    if tier == "Tier 1 (Mumbai/Delhi/Blr)":
        if position == "Budget (YMCA style)": base = 1500
        elif position == "Mid-Market (Gold's style)": base = 3500
        else: base = 8000
    elif tier == "Tier 2 (Pune/Ahd/Hyd)":
        if position == "Budget (YMCA style)": base = 1000
        elif position == "Mid-Market (Gold's style)": base = 2500
        else: base = 5500
    else: # Tier 3
        if position == "Budget (YMCA style)": base = 800
        elif position == "Mid-Market (Gold's style)": base = 1800
        else: base = 3500
    return base

avg_fee = get_pricing_estimate(location_tier, market_position)
cap_per_sqft = 0.8 # Members per sqft capacity (industry rule of thumb)
max_members = int(size_sqft * 0.15) # Rough active member capacity

# --- TAB 1: COMPETITOR MATRIX ---
tab1, tab2, tab3 = st.tabs(["Competitor Benchmark", "Revenue Simulator", "Schedule Optimizer"])

with tab1:
    st.header("Who are you competing against?")
    
    # Data from research
    competitor_data = pd.DataFrame({
        'Brand': ['David Lloyd (Pune)', 'YMCA (Mumbai)', 'Cult.fit (Fitso)', 'The Club (Mumbai)', 'Your Concept'],
        'Position': ['Premium Family', 'Budget Community', 'Tech/Flexi', 'Luxury Private', market_position],
        'Monthly_Fee_INR': [7000, 1500, 2500, 12000, avg_fee],
        'Pool': ['Yes (Heated)', 'Yes (Basic)', 'Yes (Partner)', 'Yes (Resort)', 'Yes' if has_pool else 'No'],
        'Women_Only_Hrs': ['No', 'Yes', 'No', 'No', 'TBD'],
        'Primary_Focus': ['Family/Kids', 'Community/Sports', 'Young Pros', 'Elite Networking', 'Start-up']
    })

    # Scatter Plot
    fig = px.scatter(competitor_data, x="Monthly_Fee_INR", y="Position", 
                     color="Brand", size=[40, 40, 40, 40, 60],
                     title="Market Positioning Matrix (Price vs Segment)",
                     hover_data=["Pool", "Women_Only_Hrs"])
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(competitor_data)
    st.info("💡 **Insight:** Notice the gap in the 'Mid-Market' with Pools. Most pools are either Luxury (David Lloyd) or Budget (YMCA). A clean, mid-range pool facility (₹3000-4000/mo) is a high-potential niche in India.")

# --- TAB 2: REVENUE SIMULATOR ---
with tab2:
    st.header("Financial Feasibility (Monthly)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        member_count = st.slider("Target Member Count", min_value=100, max_value=max_members*2, value=int(max_members*0.8))
    
    with col2:
        monthly_fee = st.number_input("Membership Fee (INR)", value=avg_fee)
    
    with col3:
        add_on_rev = st.number_input("Avg. Add-on Spend (Coaching/F&B)", value=500 if market_position == "Premium" else 100)

    # Calculations
    membership_revenue = member_count * monthly_fee
    ancillary_revenue = member_count * add_on_rev
    total_revenue = membership_revenue + ancillary_revenue
    
    # Rent Estimate (Rough India Commercial RE averages)
    rent_per_sqft = 150 if location_tier == "Tier 1 (Mumbai/Delhi/Blr)" else 80
    rent_cost = size_sqft * rent_per_sqft
    
    st.markdown("---")
    r_col1, r_col2, r_col3 = st.columns(3)
    r_col1.metric("Est. Monthly Revenue", f"₹ {total_revenue:,.0f}")
    r_col2.metric("Est. Rent Cost", f"₹ {rent_cost:,.0f}", delta_color="inverse")
    r_col3.metric("Gross Margin (Pre-Staff/Ops)", f"₹ {total_revenue - rent_cost:,.0f}")
    
    if (total_revenue - rent_cost) < 0:
        st.error("⚠️ Warning: Your estimated rent exceeds revenue. You need more density or higher prices.")
    else:
        st.success("✅ Positive Gross Margin. Ensure staff/electricity costs are under 50% of the remaining margin.")

# --- TAB 3: SCHEDULE OPTIMIZER ---
with tab3:
    st.header("Smart Scheduling: Maximizing Yield")
    st.write("Based on Indian cultural patterns (School runs, Office hours).")
    
    schedule_data = [
        dict(Task="Early Birds (Serious Swimmers/Gym)", Start='06:00', Finish='09:00', Resource='Mixed'),
        dict(Task="Ladies Only / Seniors (Privacy Focus)", Start='10:30', Finish='12:30', Resource='Women/Seniors'),
        dict(Task="Dead Zone (Discounts/Maintenance)", Start='13:00', Finish='15:30', Resource='Empty'),
        dict(Task="Junior Coaching Academy (High Revenue)", Start='16:00', Finish='18:30', Resource='Kids'),
        dict(Task="Peak Post-Work Rush", Start='18:30', Finish='21:00', Resource='Mixed'),
    ]
    
    df_sched = pd.DataFrame(schedule_data)
    
    # Simple Visual Timeline
    st.table(df_sched)
    
    st.markdown("""
    ### 🧠 Operator Intelligence for Schedule:
    1.  **16:00 - 18:30 is Gold:** If you have a pool/court, *do not* give this to adult members for free. Run paid kids coaching batches (like David Lloyd). This pays the rent.
    2.  **10:30 - 12:30 is Inclusion:** In India, this is the prime time for homemakers. If you offer a "Women Only" swim/gym slot here, you capture a demographic that competitors ignore.
    3.  **App Booking:** Use a slot-booking system (like Cult) for the 18:30 peak hour to prevent overcrowding and arguments.
    """)

# --- EXPORT ---
st.sidebar.markdown("---")
st.sidebar.info("This tool simulates basic economics. Real estate costs vary wildly by micro-market.")