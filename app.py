import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .metric-card {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
        }
        .main {
            padding: 20px;
        }
        h1, h2, h3 {
            color: #667eea;
        }
        .stMetric {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
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

# Header
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; border-radius: 10px; margin-bottom: 30px;'>
        <h1>📊 Sales Intelligence Dashboard</h1>
        <p><strong>InfoEdge - Naukri | IIMJobs | Hirist</strong></p>
    </div>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select View",
    ["Dashboard", "Top Accounts", "Churn Risk", "Account Details"],
    index=0
)

# Dashboard Summary Metrics
summary_data = {
    "totalAccounts": 100,
    "totalRevenue": 15750000,
    "avgRevenuePerAccount": 157500,
    "highValueAccounts": 10,
    "growingAccounts": 45,
    "flatAccounts": 30,
    "decliningAccounts": 25
}

# PAGE 1: DASHBOARD
if page == "Dashboard":
    st.title("📊 Executive Summary")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Accounts",
            value="100"
        )
    
    with col2:
        st.metric(
            label="Total Revenue",
            value="₹1.57Cr"
        )
    
    with col3:
        st.metric(
            label="Avg Revenue/Account",
            value="₹1.57L"
        )
    
    with col4:
        st.metric(
            label="High Value Accounts",
            value="10"
        )
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Account Health Distribution")
        health_data = {
            "Status": ["Growing", "Flat", "Declining"],
            "Count": [45, 30, 25],
            "Color": ["#00b386", "#ffc107", "#ff6b6b"]
        }
        fig = px.pie(
            health_data,
            values="Count",
            names="Status",
            color="Status",
            color_discrete_map={"Growing": "#00b386", "Flat": "#ffc107", "Declining": "#ff6b6b"},
            hole=0.3
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Sector Distribution")
        sector_data = {
            "Sector": ["IT Services", "Startup", "BFSI", "Product", "Other"],
            "Count": [30, 25, 20, 15, 10]
        }
        df_sector = pd.DataFrame(sector_data)
        fig = px.bar(df_sector, x="Count", y="Sector", orientation="h", color="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Key Insights
    st.subheader("🔍 Key Insights")
    insights = [
        "✅ **45% accounts are growing** - Strong market momentum but 25% at risk of declining",
        "💰 **₹1.57 Cr total revenue** - Average ₹1.57L/account shows large base of SME accounts",
        "🎯 **High-value accounts concentrated** - Top 10 accounts drive 40%+ of revenue",
        "⚠️ **Churn risk in declining segment** - 10 accounts in critical renewal stage"
    ]
    
    for insight in insights:
        st.info(insight)

# PAGE 2: TOP ACCOUNTS
elif page == "Top Accounts":
    st.title("🏆 Top 10 High-Value Accounts")
    
    for i, account in enumerate(top_accounts, 1):
        with st.expander(f"**{i}. {account['companyName']}** - {account['customerId']}", expanded=False):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Sector", account['sector'])
                st.metric("ACM", account['acmName'])
            
            with col2:
                st.metric("Branch", account['branch'])
                st.metric("Employee Size", account['employeeSize'])
            
            with col3:
                st.metric("Renewal Quarter", account['renewalQuarter'])
                st.metric("Days to Renewal", account['daysToRenewal'])
            
            st.divider()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Last FY Revenue", f"₹{account['lastFyRevenue']/100000:.2f}L")
                st.metric("Current FY Revenue", f"₹{account['currentFyRevenue']/100000:.2f}L")
            
            with col2:
                growth_color = "green" if account['growthPercentage'] >= 0 else "red"
                st.metric("Growth %", f"{account['growthPercentage']}%")
                st.metric("Status", account['status'])
            
            st.divider()
            
            st.markdown("**🔴 Pain Points:**")
            for pain_point in account['painPoints']:
                st.write(f"• {pain_point}")
            
            st.divider()
            
            st.markdown("**💡 Sales Pitch:**")
            st.info(account['salesPitch'])
            
            st.divider()
            
            st.markdown("**📦 Product Health:**")
            product_df = pd.DataFrame(account['productHealth'])
            st.dataframe(product_df, use_container_width=True)
            
            st.markdown("**🎯 Top Jobs:**")
            jobs_df = pd.DataFrame(account['topJobs'])
            st.dataframe(jobs_df, use_container_width=True)

# PAGE 3: CHURN RISK
elif page == "Churn Risk":
    st.title("⚠️ Churn Risk Accounts (Urgent Renewal)")
    
    for account in churn_risk:
        with st.expander(f"**{account['companyName']}** - {account['customerId']} - CRITICAL", expanded=True):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Days to Renewal", account['daysToRenewal'], delta="URGENT")
                st.metric("Growth %", f"{account['growthPercentage']}%")
            
            with col2:
                st.metric("Renewal Quarter", account['renewalQuarter'])
                st.metric("Status", account['status'])
            
            st.divider()
            
            st.markdown("**🔴 Critical Issues:**")
            for pain_point in account['painPoints']:
                st.write(f"⚠️ {pain_point}")
            
            st.divider()
            
            st.markdown("**💡 Urgent Action Required:**")
            st.error(account['salesPitch'])
            
            st.divider()
            
            st.markdown("**📦 Product Health:**")
            product_df = pd.DataFrame(account['productHealth'])
            st.dataframe(product_df, use_container_width=True)

# PAGE 4: ACCOUNT DETAILS
elif page == "Account Details":
    st.title("🔎 Account Detail Search")
    
    all_accounts = top_accounts + churn_risk
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_company = st.selectbox(
            "Select Account",
            options=[acc['companyName'] for acc in all_accounts],
            index=0
        )
    
    # Find selected account
    selected_account = next(acc for acc in all_accounts if acc['companyName'] == selected_company)
    
    # Display detailed view
    st.markdown(f"### {selected_account['companyName']}")
    st.markdown(f"**Customer ID:** {selected_account['customerId']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sector", selected_account['sector'])
    with col2:
        st.metric("ACM Name", selected_account['acmName'])
    with col3:
        st.metric("Branch", selected_account['branch'])
    with col4:
        st.metric("Days to Renewal", selected_account['daysToRenewal'])
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Last FY Revenue", f"₹{selected_account['lastFyRevenue']/100000:.2f}L")
    with col2:
        st.metric("Current FY Revenue", f"₹{selected_account['currentFyRevenue']/100000:.2f}L")
    with col3:
        st.metric("Growth %", f"{selected_account['growthPercentage']}%")
    with col4:
        st.metric("Employee Size", selected_account['employeeSize'])
    
    st.divider()
    
    st.subheading("🔴 Pain Points & Issues")
    for point in selected_account['painPoints']:
        st.write(f"• {point}")
    
    st.divider()
    
    st.subheading("💡 Sales Pitch")
    st.info(selected_account['salesPitch'])
    
    st.divider()
    
    st.subheading("📦 Product Health & Utilization")
    product_df = pd.DataFrame(selected_account['productHealth'])
    st.dataframe(product_df, use_container_width=True)
    
    st.divider()
    
    st.subheading("🎯 Top Premium Jobs (Last 6 Months)")
    jobs_df = pd.DataFrame(selected_account['topJobs'])
    st.dataframe(jobs_df, use_container_width=True)
    
    st.divider()
    
    st.subheading("🚀 Recommended Actions")
    actions = [
        "✓ Schedule renewal discussion 30 days before renewal date",
        "✓ Present upsell opportunities for underutilized products",
        "✓ Benchmark their metrics against sector peers",
        "✓ Propose product optimization strategy"
    ]
    for action in actions:
        st.write(action)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px; padding: 20px;'>
        <p>Sales Intelligence Engine | Powered by Streamlit | Last Updated: March 2026</p>
        <p>InfoEdge (India) Ltd. - Naukri | IIMJobs | Hirist</p>
    </div>
""", unsafe_allow_html=True)
