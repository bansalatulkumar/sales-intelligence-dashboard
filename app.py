import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0f1419;
            color: #fff;
        }
        
        .main {
            padding: 0;
            background-color: #0f1419;
        }
        
        .stApp {
            background-color: #0f1419;
        }
        
        .header-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 30px;
            margin: -20px -20px 40px -20px;
            border-radius: 0;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        
        .header-title {
            font-size: 3em;
            font-weight: 800;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }
        
        .header-subtitle {
            font-size: 1.2em;
            opacity: 0.95;
            font-weight: 300;
        }
        
        .metric-card {
            background: #1a1f2e;
            padding: 20px;
            border-radius: 12px;
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            margin-bottom: 15px;
            color: #fff;
        }
        
        .stMetric {
            background-color: #1a1f2e !important;
            padding: 15px !important;
            border-radius: 10px !important;
            border-left: 4px solid #667eea;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        }
        
        .stMetric label {
            color: #a0aec0 !important;
            font-size: 0.85em !important;
        }
        
        .stMetric [data-testid="metricDeltaContainer"] {
            color: #667eea !important;
        }
        
        .filter-section {
            background: #1a1f2e;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            margin-bottom: 30px;
            border-top: 3px solid #667eea;
        }
        
        .account-card {
            background: #1a1f2e;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.4);
            border-left: 4px solid #667eea;
            transition: all 0.3s ease;
        }
        
        .account-card:hover {
            box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
            transform: translateY(-2px);
            background: #232a3a;
        }
        
        .account-card.churn {
            border-left: 4px solid #ff9800;
        }
        
        .account-header {
            font-size: 1.4em;
            font-weight: 700;
            color: #fff;
            margin-bottom: 15px;
        }
        
        .status-badge {
            display: inline-block;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 700;
            margin-right: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .status-growing {
            background: rgba(76, 175, 80, 0.2);
            color: #4caf50;
            border: 1px solid rgba(76, 175, 80, 0.4);
        }
        
        .status-flat {
            background: rgba(255, 193, 7, 0.2);
            color: #ffc107;
            border: 1px solid rgba(255, 193, 7, 0.4);
        }
        
        .status-declining {
            background: rgba(255, 152, 0, 0.2);
            color: #ff9800;
            border: 1px solid rgba(255, 152, 0, 0.4);
        }
        
        .pain-points-box {
            background: rgba(255, 193, 7, 0.1);
            padding: 18px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #ffc107;
            color: #fff;
        }
        
        .sales-pitch-box {
            background: rgba(102, 126, 234, 0.1);
            padding: 18px;
            border-radius: 10px;
            margin: 15px 0;
            border-left: 4px solid #667eea;
            font-size: 0.95em;
            line-height: 1.7;
            color: #fff;
        }
        
        .mini-metric {
            background: #232a3a;
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #2d3546;
            color: #fff;
            transition: all 0.2s ease;
        }
        
        .mini-metric:hover {
            background: #2d3546;
            border-color: #667eea;
        }
        
        .mini-metric-label {
            font-size: 0.75em;
            color: #8892b0;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
            font-weight: 600;
        }
        
        .mini-metric-value {
            font-size: 1.3em;
            font-weight: 700;
            color: #fff;
        }
        
        h2 {
            color: #fff;
            margin: 40px 0 25px 0;
            padding-bottom: 12px;
            border-bottom: 2px solid #667eea;
            font-size: 1.9em;
            font-weight: 700;
        }
        
        h3 {
            color: #667eea;
            margin: 20px 0 15px 0;
            font-size: 1.2em;
            font-weight: 600;
        }
        
        .stMultiSelect, .stSelectbox, .stTextInput, .stSlider {
            color: #fff !important;
        }
        
        .stMultiSelect label, .stSelectbox label, .stTextInput label, .stSlider label {
            color: #a0aec0 !important;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# Sample Data - Sales Intelligence
@st.cache_data
def load_data():
    top_accounts = [
        {
            "id": 1,
            "companyName": "TCS Limited",
            "customerId": "CUST/00001",
            "sector": "IT Services",
            "acmName": "Rajesh Kumar",
            "branch": "Bangalore",
            "renewalQuarter": "FY2026-Q2",
            "daysToRenewal": 45,
            "lastFyRevenue": 850000,
            "currentFyRevenue": 1020000,
            "growthPercentage": 20,
            "status": "Growing",
            "category": "Key",
            "employeeSize": "10K+",
            "painPoints": ["Low applies on premium roles", "Under-utilization of Hirist platform", "Over-dependence on Naukri"],
            "productHealth": [
                {"product": "Naukri Job Postings", "status": "Healthy", "utilization": 85},
                {"product": "Hirist Premium Jobs", "status": "Upsell Opportunity", "utilization": 45},
                {"product": "IIMJobs Premium", "status": "Not Activated", "utilization": 0}
            ],
            "topJobs": [
                {"title": "Senior Software Engineer", "ctc": "45 LPA", "experience": "5-8 yrs", "applies": 87},
                {"title": "Data Scientist", "ctc": "52 LPA", "experience": "3-7 yrs", "applies": 62}
            ],
            "salesPitch": "TCS is getting strong volume on Naukri but missing high-value tech talent via Hirist. We can increase premium role fills by 40% by activating Hirist for senior positions."
        },
        {
            "id": 2,
            "companyName": "Infosys Limited",
            "customerId": "CUST/00002",
            "sector": "IT Services",
            "acmName": "Priya Sharma",
            "branch": "Bangalore",
            "renewalQuarter": "FY2026-Q3",
            "daysToRenewal": 98,
            "lastFyRevenue": 720000,
            "currentFyRevenue": 720000,
            "growthPercentage": 0,
            "status": "Flat",
            "category": "Key",
            "employeeSize": "10K+",
            "painPoints": ["Flat revenue despite increased hiring", "Paying for unused Zwayam license", "Low employer branding investment"],
            "productHealth": [
                {"product": "Naukri Job Postings", "status": "Healthy", "utilization": 75},
                {"product": "Zwayam", "status": "Poor Utilization", "utilization": 20}
            ],
            "topJobs": [
                {"title": "Project Manager", "ctc": "32 LPA", "experience": "8-12 yrs", "applies": 43}
            ],
            "salesPitch": "Infosys can drive 30% revenue growth by leveraging Employer Branding + Zwayam optimization for high-volume hiring."
        },
        {
            "id": 3,
            "companyName": "Goldman Sachs India",
            "customerId": "CUST/00003",
            "sector": "BFSI",
            "acmName": "Amit Patel",
            "branch": "Mumbai",
            "renewalQuarter": "FY2026-Q2",
            "daysToRenewal": 52,
            "lastFyRevenue": 580000,
            "currentFyRevenue": 696000,
            "growthPercentage": 20,
            "status": "Growing",
            "category": "Key",
            "employeeSize": "1K–10K",
            "painPoints": ["Premium roles underperforming on Naukri", "Not using IIMJobs for leadership hiring"],
            "productHealth": [
                {"product": "Naukri Job Postings", "status": "Healthy", "utilization": 80},
                {"product": "IIMJobs Premium Jobs", "status": "Upsell Opportunity", "utilization": 30}
            ],
            "topJobs": [
                {"title": "Analyst", "ctc": "48 LPA", "experience": "4-6 yrs", "applies": 156},
                {"title": "Vice President", "ctc": "80 LPA", "experience": "15+ yrs", "applies": 18}
            ],
            "salesPitch": "Goldman Sachs can fill leadership roles 3x faster using IIMJobs Premium. Peers in BFSI are getting 10x better response rates."
        }
    ]
    
    churn_risk = [
        {
            "id": 4,
            "companyName": "ABC Consulting",
            "customerId": "CUST/00004",
            "sector": "Consulting",
            "acmName": "Vivek Singh",
            "branch": "Delhi NCR",
            "renewalQuarter": "FY2026-Q1",
            "daysToRenewal": 15,
            "lastFyRevenue": 125000,
            "currentFyRevenue": 95000,
            "growthPercentage": -24,
            "status": "Declining",
            "category": "Retail",
            "employeeSize": "50–200",
            "painPoints": ["Severe decline in hiring demand", "Low applies across all channels", "Products completely underutilized"],
            "productHealth": [
                {"product": "Naukri Job Postings", "status": "Critical - Churn Risk", "utilization": 10}
            ],
            "topJobs": [
                {"title": "Management Consultant", "ctc": "28 LPA", "experience": "3-5 yrs", "applies": 5}
            ],
            "salesPitch": "Urgent renewal required. ABC Consulting shows severe underutilization. Need immediate intervention with product optimization or risk losing account."
        }
    ]
    
    return top_accounts, churn_risk

top_accounts, churn_risk = load_data()
all_accounts = top_accounts + churn_risk

# === HEADER ===
st.markdown("""
    <div class='header-section'>
        <div class='header-title'>📊 Sales Intelligence Dashboard</div>
        <div class='header-subtitle'>InfoEdge - Naukri | IIMJobs | Hirist | Live Account Analytics</div>
    </div>
""", unsafe_allow_html=True)

# === SUMMARY METRICS ===
summary_data = {
    "totalAccounts": 100,
    "totalRevenue": 15750000,
    "avgRevenuePerAccount": 157500,
    "highValueAccounts": len(top_accounts),
    "growingAccounts": 45,
    "flatAccounts": 30,
    "decliningAccounts": 25,
    "churnRiskAccounts": len(churn_risk)
}

st.markdown("<h2>📈 Executive Summary</h2>", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("Total Accounts", "100", "+15")
with col2:
    st.metric("Total Revenue", "₹1.57Cr", "+20%")
with col3:
    st.metric("Avg Revenue/Account", "₹1.57L", "")
with col4:
    st.metric("High Value", "10", "📈")
with col5:
    st.metric("Growing", "45%", "+5%")
with col6:
    st.metric("Churn Risk", f"{summary_data['churnRiskAccounts']}", "⚠️")

# === CHARTS ===
col1, col2 = st.columns(2)

with col1:
    st.subheader("Account Health Distribution")
    health_data = {
        "Status": ["Growing", "Flat", "Declining"],
        "Count": [45, 30, 25]
    }
    fig = px.pie(
        health_data,
        values="Count",
        names="Status",
        color="Status",
        color_discrete_map={"Growing": "#4caf50", "Flat": "#ffc107", "Declining": "#ff9800"},
        hole=0.35
    )
    fig.update_traces(textposition='inside', textinfo='label+percent')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Status")
    revenue_data = {
        "Status": ["Growing", "Flat", "Declining"],
        "Revenue": [6300000, 4800000, 3150000]
    }
    df_revenue = pd.DataFrame(revenue_data)
    fig = px.bar(
        df_revenue,
        x="Status",
        y="Revenue",
        color="Status",
        color_discrete_map={"Growing": "#4caf50", "Flat": "#ffc107", "Declining": "#ff9800"},
        text="Revenue"
    )
    fig.update_traces(texttemplate='₹%{y/1000000:.1f}Cr', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# === HELPER FUNCTION (Define before using) ===
def display_account_card(account, is_churn=False):
    card_class = "account-card churn" if is_churn else "account-card"
    
    st.markdown(f"""
        <div class='{card_class}'>
            <div class='account-header'>
                {account['companyName']} ({account['customerId']})
                <span class='status-badge status-{account['status'].lower()}'>{account['status']}</span>
            </div>
    """, unsafe_allow_html=True)
    
    # Key metrics in grid
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    
    with metric_col1:
        st.markdown(f"""
            <div class='mini-metric'>
                <div class='mini-metric-label'>Sector</div>
                <div class='mini-metric-value'>{account['sector']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown(f"""
            <div class='mini-metric'>
                <div class='mini-metric-label'>ACM</div>
                <div class='mini-metric-value' style='font-size: 0.9em;'>{account['acmName']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown(f"""
            <div class='mini-metric'>
                <div class='mini-metric-label'>Days to Renewal</div>
                <div class='mini-metric-value'>{account['daysToRenewal']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        growth_color = "green" if account['growthPercentage'] >= 0 else "red"
        st.markdown(f"""
            <div class='mini-metric'>
                <div class='mini-metric-label'>Growth %</div>
                <div class='mini-metric-value' style='color: {growth_color};'>{account['growthPercentage']}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with metric_col5:
        st.markdown(f"""
            <div class='mini-metric'>
                <div class='mini-metric-label'>Current Revenue</div>
                <div class='mini-metric-value' style='font-size: 0.95em;'>₹{account['currentFyRevenue']/100000:.1f}L</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Pain points
    st.markdown(f"""
        <div class='pain-points-box'>
            <strong>🔴 Pain Points:</strong><br>
            {'<br>'.join([f'• {p}' for p in account['painPoints']])}
        </div>
    """, unsafe_allow_html=True)
    
    # Sales pitch
    st.markdown(f"""
        <div class='sales-pitch-box'>
            <strong>💡 Sales Pitch:</strong><br>
            {account['salesPitch']}
        </div>
    """, unsafe_allow_html=True)
    
    # Product health data table
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<strong>📦 Product Health & Utilization</strong>")
        product_df = pd.DataFrame(account['productHealth'])
        st.dataframe(product_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.markdown("<strong>🎯 Top Premium Jobs</strong>")
        jobs_df = pd.DataFrame(account['topJobs'])
        st.dataframe(jobs_df, use_container_width=True, hide_index=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("")

# === FILTERS ===
st.markdown("<h2>🔍 Smart Filters & Search</h2>", unsafe_allow_html=True)

filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

with filter_col1:
    selected_sector = st.multiselect(
        "Sector",
        options=list(set([acc['sector'] for acc in all_accounts])),
        default=list(set([acc['sector'] for acc in all_accounts]))
    )

with filter_col2:
    selected_status = st.multiselect(
        "Account Status",
        options=["Growing", "Flat", "Declining"],
        default=["Growing", "Flat", "Declining"]
    )

with filter_col3:
    renewal_days = st.slider(
        "Days to Renewal",
        min_value=0,
        max_value=180,
        value=(0, 180),
        step=10
    )

with filter_col4:
    revenue_range = st.slider(
        "Revenue Range (₹L)",
        min_value=0,
        max_value=100,
        value=(0, 100),
        step=5
    )

with filter_col5:
    search_text = st.text_input("🔎 Search Company Name", "")

st.divider()

# === APPLY FILTERS ===
filtered_accounts = []

for account in all_accounts:
    # Filter by sector
    if account['sector'] not in selected_sector:
        continue
    
    # Filter by status
    if account['status'] not in selected_status:
        continue
    
    # Filter by days to renewal
    if not (renewal_days[0] <= account['daysToRenewal'] <= renewal_days[1]):
        continue
    
    # Filter by revenue (in ₹L)
    revenue_in_L = account['currentFyRevenue'] / 100000
    if not (revenue_range[0] <= revenue_in_L <= revenue_range[1]):
        continue
    
    # Filter by search text
    if search_text and search_text.lower() not in account['companyName'].lower():
        continue
    
    filtered_accounts.append(account)

# === DISPLAY FILTERED RESULTS ===
st.markdown(f"<h2>📋 Showing {len(filtered_accounts)} Accounts</h2>", unsafe_allow_html=True)

if len(filtered_accounts) == 0:
    st.warning("No accounts match your filters. Try adjusting the filter criteria.")
else:
    # Separate accounts by status
    churn_accounts = [acc for acc in filtered_accounts if acc['status'] == 'Declining' and acc['daysToRenewal'] < 90]
    growing_accounts = [acc for acc in filtered_accounts if acc['status'] == 'Growing']
    other_accounts = [acc for acc in filtered_accounts if acc not in churn_accounts and acc not in growing_accounts]
    
    # Display churn risk first
    if churn_accounts:
        st.markdown("<h3>⚠️ URGENT: Critical Renewal (Churn Risk)</h3>", unsafe_allow_html=True)
        for account in churn_accounts:
            display_account_card(account, is_churn=True)
    
    # Display growing accounts
    if growing_accounts:
        st.markdown("<h3>🎉 Growing Accounts (Upsell Opportunity)</h3>", unsafe_allow_html=True)
        for account in growing_accounts:
            display_account_card(account, is_churn=False)
    
    # Display other accounts
    if other_accounts:
        st.markdown("<h3>📊 Other Accounts</h3>", unsafe_allow_html=True)
        for account in other_accounts:
            display_account_card(account, is_churn=False)

st.divider()

# === KEY INSIGHTS ===
st.markdown("<h2>💡 Key Insights & Recommendations</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3>📈 Growth Opportunities</h3>", unsafe_allow_html=True)
    st.markdown("""
    - **45% of accounts showing strong growth** → Focus on upselling additional products
    - **High-value accounts in growing sector** → Bundle offers for expanded platforms
    - **Underutilized premium products** → Launch product education campaigns
    """)

with col2:
    st.markdown("<h3>⚠️ Risk & Churn Prevention</h3>", unsafe_allow_html=True)
    st.markdown("""
    - **1 account in critical renewal** → Immediate ACM intervention required
    - **Flat revenue accounts** → Need product optimization discussions
    - **Poor utilization patterns** → Trigger health check reviews
    """)

st.divider()

# === FOOTER ===
st.markdown("""
    <div style='text-align: center; color: #5a6f7d; font-size: 11px; padding: 30px 20px;'>
        <p style='margin-bottom: 8px;'>Sales Intelligence Engine | Powered by Streamlit | Last Updated: March 2026</p>
        <p>InfoEdge (India) Ltd. - Naukri | IIMJobs | Hirist</p>
    </div>
""", unsafe_allow_html=True)
