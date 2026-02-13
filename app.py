"""
APMB Investor Tracking Dashboard v2.0
Andhra Pradesh Maritime Board - Strategic Investment Intelligence Platform

Author: APMB Data Analytics Team
License: Government of Andhra Pradesh - Internal Use
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import io
import hashlib

# Page Configuration
st.set_page_config(
    page_title="APMB Investor Dashboard",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Password Protection (Optional)
def check_password():
    """Returns `True` if user has entered correct password."""
    
    # Check if password protection is enabled
    try:
        required_password = st.secrets.get("APP_PASSWORD", None)
    except:
        # Secrets file doesn't exist or APP_PASSWORD not set - no protection needed
        return True
    
    if required_password is None or required_password == "":
        # No password configured - app is public
        return True
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == hashlib.sha256(required_password.encode()).hexdigest():
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <h1>🚢 APMB Investor Dashboard</h1>
            <p style='color: #64748b; font-size: 1.2rem;'>Secure Access Required</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Enter Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Password"
            )
            st.caption("Contact APMB administrator for access credentials.")
        return False
    
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <h1>🚢 APMB Investor Dashboard</h1>
            <p style='color: #64748b; font-size: 1.2rem;'>Secure Access Required</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Enter Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Password"
            )
            st.error("😕 Password incorrect. Please try again.")
            st.caption("Contact APMB administrator for access credentials.")
        return False
    
    else:
        # Password correct
        return True

# Check password before showing app
if not check_password():
    st.stop()

# Custom CSS with animations and improved design
st.markdown("""
<style>
    /* Main container spacing */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    /* Headers */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .sub-header {
        font-size: 1.3rem;
        color: #64748b;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Animated KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 1.5rem;
        border-radius: 16px;
        color: white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 3s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
    }
    
    .kpi-value {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0.8rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: countUp 1.5s ease-out;
    }
    
    @keyframes countUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .kpi-label {
        font-size: 0.95rem;
        opacity: 0.95;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .kpi-icon {
        font-size: 1.5rem;
    }
    
    /* Risk status colors */
    .risk-active {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    }
    
    .risk-delayed {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    }
    
    .risk-stalled {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
    }
    
    .risk-closed {
        background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
    }
    
    /* Metric containers */
    .metric-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    
    .metric-container:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2.5rem;
        background: linear-gradient(to right, #f8fafc 0%, #f1f5f9 100%);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 1.15rem;
        font-weight: 600;
        color: #64748b;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        color: #3b82f6;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Data tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Section spacing */
    .section-gap {
        margin: 3rem 0;
    }
    
    /* Footer */
    .dashboard-footer {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-top: 4rem;
        text-align: center;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.1);
    }
    
    .footer-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        margin-bottom: 1rem;
    }
    
    .footer-meta {
        font-size: 0.9rem;
        opacity: 0.6;
        margin-top: 1rem;
    }
    
    /* Button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Spacing utilities */
    div[data-testid="stHorizontalBlock"] {
        gap: 1.5rem;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 1.5rem;
    }
    
    /* Alert boxes */
    .alert-box {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        font-weight: 500;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        color: #92400e;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        color: #065f46;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        color: #991b1b;
    }
</style>
""", unsafe_allow_html=True)

# Data Definition with caching
@st.cache_data
def load_data():
    """Load and return the cleaned investor dataset"""
    
    data = {
        'Firm_Name': [
            'Hindustan Shipyard Limited (HSL)',
            'Mazagaon Dock Limited (MDL)',
            'Goa Shipyard Limited (GSL)',
            'Garden Reach Shipbuilders & Engineers (GRSE)',
            'Cochin Shipyard Limited (CSL)',
            'Reliance Infrastructure',
            'Adani Ports & SEZ',
            'Larsen & Toubro (L&T)',
            'Shapoorji Pallonji',
            'ABG Shipyard',
            'Essar Group',
            'Goodluck Maritime',
            'Chowgule Group',
            'Navyuga Constructions',
            'P&P Marine',
            'Mahathi Infra Services',
            'San Marine',
            'Hyundai HD KSOE',
            'Hanwha Ocean',
            'Damen Shipyard Groups'
        ],
        'Investor_Type': [
            'Domestic', 'Domestic', 'Domestic', 'Domestic', 'Domestic',
            'Domestic', 'Domestic', 'Domestic', 'Domestic', 'Domestic',
            'Domestic', 'Domestic', 'Domestic', 'Domestic', 'Domestic',
            'Domestic', 'Domestic',
            'International', 'International', 'International'
        ],
        'Sector': [
            'Shipbuilding', 'Shipbuilding', 'Shipbuilding', 'Shipbuilding', 'Shipbuilding',
            'Marine Infra', 'Marine Infra', 'Shipbuilding', 'Marine Infra', 'Ship Repair',
            'Shipbuilding', 'Shipbuilding', 'Ship Repair', 'Shipbuilding/Marine Infra',
            'Shipbuilding', 'Shipbuilding', 'Shipbuilding',
            'Shipbuilding', 'Shipbuilding', 'Shipbuilding'
        ],
        'Location_Interest': [
            'Dugarajapatnam/Mulapeta/Kakinada',
            'Machilipatnam/Mulapeta',
            'Machilipatnam',
            'Machilipatnam/Mulapeta/Kakinada',
            'Kakinada/Machilipatnam',
            'Visakhapatnam',
            'Multiple Locations',
            'Mulapeta/Kakinada',
            'Machilipatnam',
            'Visakhapatnam',
            'Kakinada',
            'Bhavanapadu',
            'Visakhapatnam',
            'Multiple Locations',
            'TBD',
            'TBD',
            'Kakinada',
            'Machilipatnam/Dugarajapatnam',
            'TBD',
            'TBD'
        ],
        'Current_Stage': [
            'MoU Signed',
            'Site Visit Complete',
            'MoU Signed',
            'DPR Pending',
            'EOI Submitted',
            'Inactive',
            'Early Discussion',
            'EOI Submitted',
            'Inactive',
            'Inactive',
            'Inactive',
            'EOI Submitted',
            'EOI Submitted',
            'DPR Pending',
            'Early Discussion',
            'DPR Pending',
            'Land Allotted',
            'High-Level Meeting',
            'Early Discussion',
            'Declined'
        ],
        'Investment_INR_Cr': [
            3000.0, np.nan, 1500.0, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan
        ],
        'Land_Requirement_Acres': [
            225.0, 1100.0, 200.0, 300.0, 150.0,
            np.nan, np.nan, 200.0, np.nan, np.nan,
            np.nan, 1200.0, 1200.0, 1200.0, np.nan,
            100.0, 19.0, 500.0, np.nan, np.nan
        ],
        'Waterfront_Requirement_Meters': [
            800.0, 1250.0, 300.0, 600.0, 400.0,
            np.nan, np.nan, 500.0, np.nan, np.nan,
            np.nan, 1000.0, 1000.0, 1000.0, np.nan,
            800.0, 175.0, 3000.0, np.nan, np.nan
        ],
        'Draft_Requirement_Meters': [
            16.5, 17.0, 12.5, 12.0, 10.0,
            np.nan, np.nan, 14.0, np.nan, np.nan,
            np.nan, 8.0, 8.0, 8.0, np.nan,
            4.5, 7.0, 15.0, np.nan, np.nan
        ],
        'Direct_Employment': [
            300.0, np.nan, 1500.0, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan
        ],
        'Indirect_Employment': [
            1500.0, np.nan, 5000.0, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan,
            np.nan, np.nan, np.nan, np.nan, np.nan
        ],
        'Support_Requested': [
            'Land, Infra, Clearances',
            'Land, Waterfront',
            'Land, Infra, Housing',
            'Land, Infra, Data',
            'Land, Clearances',
            'Fiscal Incentives',
            'Land, Exclusivity',
            'Land, Infra',
            'Fiscal Incentives',
            'Restructuring',
            'Land',
            'Land, Fiscal, Exclusivity',
            'Land, Fiscal, Exclusivity',
            'Land, Fiscal, Exclusivity',
            'Consultation',
            'Land, Jetty, Infra',
            'Land, Infra',
            'Land, Waterfront, Long Lease',
            'TBD',
            'Brownfield Only'
        ],
        'Risk_Status': [
            'Active',
            'Active',
            'Active',
            'Delayed',
            'Delayed',
            'Stalled',
            'Active',
            'Delayed',
            'Stalled',
            'Closed',
            'Stalled',
            'Delayed',
            'Delayed',
            'Delayed',
            'Active',
            'Delayed',
            'Active',
            'Active',
            'Delayed',
            'Closed'
        ],
        'Next_Action': [
            'RFP Participation (Dec 2025)',
            'RFP Invitation (Dec 2025)',
            'RFP Participation (Dec 2025)',
            'Follow-up on DPR',
            'DPR Submission Required',
            'Re-engagement',
            'Detailed Proposal',
            'Site Finalization',
            'Re-engagement',
            'Archive',
            'Re-engagement',
            'DPR Submission',
            'DPR Submission',
            'DPR Submission',
            'Schedule Meeting',
            'DPR Submission',
            'Implementation Support',
            'Follow-up Post Meeting',
            'Awaiting Response',
            'Archive'
        ],
        'Last_Activity_Month': [
            'November 2025',
            'October 2025',
            'November 2025',
            'October 2025',
            'October 2025',
            'March 2025',
            'August 2025',
            'October 2025',
            'April 2025',
            'January 2025',
            'May 2025',
            'October 2025',
            'October 2025',
            'October 2025',
            'October 2025',
            'October 2025',
            'October 2025',
            'October 2025',
            'August 2025',
            'July 2025'
        ],
        'Country': [
            'India', 'India', 'India', 'India', 'India',
            'India', 'India', 'India', 'India', 'India',
            'India', 'India', 'India', 'India', 'UAE',
            'India', 'India',
            'South Korea', 'South Korea', 'Netherlands'
        ]
    }
    
    df = pd.DataFrame(data)
    
    # Calculate days since last activity
    df['Last_Activity_Date'] = pd.to_datetime(df['Last_Activity_Month'], format='%B %Y')
    current_date = pd.Timestamp('2025-12-01')
    df['Days_Since_Activity'] = (current_date - df['Last_Activity_Date']).dt.days
    
    return df

# KPI Calculation Functions
@st.cache_data
def calculate_kpis(df):
    """Calculate executive KPIs"""
    kpis = {
        'Total_Investment': df['Investment_INR_Cr'].sum(),
        'Total_Direct_Employment': df['Direct_Employment'].sum(),
        'Total_Indirect_Employment': df['Indirect_Employment'].sum(),
        'Total_Land_Requested': df['Land_Requirement_Acres'].sum(),
        'Total_Waterfront': df['Waterfront_Requirement_Meters'].sum(),
        'MoUs_Signed': len(df[df['Current_Stage'] == 'MoU Signed']),
        'Active_Investors': len(df[df['Risk_Status'] == 'Active']),
        'Delayed_Stalled': len(df[df['Risk_Status'].isin(['Delayed', 'Stalled'])]),
        'Domestic_Count': len(df[df['Investor_Type'] == 'Domestic']),
        'International_Count': len(df[df['Investor_Type'] == 'International'])
    }
    return kpis

# Visualization Functions
def create_kpi_card(title, value, icon="📊", risk_level=None):
    """Create an enhanced animated KPI card with risk-based colors"""
    
    # Determine card class based on risk level
    card_class = "kpi-card"
    if risk_level == "active":
        card_class += " risk-active"
    elif risk_level == "delayed":
        card_class += " risk-delayed"
    elif risk_level == "stalled":
        card_class += " risk-stalled"
    elif risk_level == "closed":
        card_class += " risk-closed"
    
    if isinstance(value, float):
        if value >= 1000:
            display_value = f"₹{value:,.0f} Cr"
        elif value > 0:
            display_value = f"{value:,.0f}"
        else:
            display_value = "N/A"
    else:
        display_value = str(value)
    
    return f"""
    <div class="{card_class}">
        <div class="kpi-label">
            <span class="kpi-icon">{icon}</span>
            <span>{title}</span>
        </div>
        <div class="kpi-value">{display_value}</div>
    </div>
    """

def generate_executive_summary_html(df, kpis):
    """Generate HTML for Executive Summary PDF"""
    
    current_date = datetime.now().strftime('%B %d, %Y')
    
    # Top investors by investment
    top_investors = df[df['Investment_INR_Cr'].notna()].nlargest(5, 'Investment_INR_Cr')[['Firm_Name', 'Investment_INR_Cr', 'Current_Stage']]
    
    # Risk breakdown
    risk_breakdown = df['Risk_Status'].value_counts().to_dict()
    
    # Location breakdown
    location_inv = df.groupby('Location_Interest')['Investment_INR_Cr'].sum().sort_values(ascending=False).head(5)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 2cm;
            }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #1e293b;
                max-width: 210mm;
                margin: 0 auto;
                background: white;
            }}
            .header {{
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                color: white;
                padding: 2rem;
                text-align: center;
                border-radius: 8px;
                margin-bottom: 2rem;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
            }}
            .header p {{
                margin: 0.5rem 0 0 0;
                opacity: 0.9;
                font-size: 1rem;
            }}
            .kpi-grid {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 1rem;
                margin: 2rem 0;
            }}
            .kpi-box {{
                background: #f8fafc;
                border-left: 4px solid #667eea;
                padding: 1.5rem;
                border-radius: 8px;
            }}
            .kpi-box h3 {{
                margin: 0;
                font-size: 2rem;
                color: #667eea;
                font-weight: 700;
            }}
            .kpi-box p {{
                margin: 0.5rem 0 0 0;
                color: #64748b;
                font-size: 0.9rem;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .section {{
                margin: 2rem 0;
                page-break-inside: avoid;
            }}
            .section h2 {{
                color: #1e3a8a;
                border-bottom: 3px solid #667eea;
                padding-bottom: 0.5rem;
                margin-bottom: 1rem;
                font-size: 1.5rem;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 1rem 0;
                background: white;
            }}
            th {{
                background: #667eea;
                color: white;
                padding: 0.75rem;
                text-align: left;
                font-weight: 600;
            }}
            td {{
                padding: 0.75rem;
                border-bottom: 1px solid #e2e8f0;
            }}
            tr:hover {{
                background: #f8fafc;
            }}
            .status-active {{ color: #10b981; font-weight: 600; }}
            .status-delayed {{ color: #f59e0b; font-weight: 600; }}
            .status-stalled {{ color: #ef4444; font-weight: 600; }}
            .status-closed {{ color: #6b7280; font-weight: 600; }}
            .footer {{
                margin-top: 3rem;
                padding-top: 2rem;
                border-top: 2px solid #e2e8f0;
                text-align: center;
                color: #64748b;
                font-size: 0.9rem;
            }}
            .footer-brand {{
                font-size: 1.2rem;
                font-weight: 700;
                color: #1e3a8a;
                margin-bottom: 0.5rem;
            }}
            .highlight-box {{
                background: #fef3c7;
                border-left: 4px solid #f59e0b;
                padding: 1rem;
                margin: 1rem 0;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🚢 APMB Investor Dashboard</h1>
            <p>Executive Summary Report | {current_date}</p>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-box">
                <h3>₹{kpis['Total_Investment']:,.0f} Cr</h3>
                <p>Total Investment</p>
            </div>
            <div class="kpi-box">
                <h3>{kpis['Total_Direct_Employment']:,.0f}</h3>
                <p>Direct Jobs</p>
            </div>
            <div class="kpi-box">
                <h3>{kpis['Total_Indirect_Employment']:,.0f}</h3>
                <p>Indirect Jobs</p>
            </div>
            <div class="kpi-box">
                <h3>{kpis['Active_Investors']}</h3>
                <p>Active Investors</p>
            </div>
            <div class="kpi-box">
                <h3>{kpis['MoUs_Signed']}</h3>
                <p>MoUs Signed</p>
            </div>
            <div class="kpi-box">
                <h3>{kpis['Total_Land_Requested']:,.0f}</h3>
                <p>Acres Required</p>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Key Investor Highlights</h2>
            <div class="highlight-box">
                <strong>Portfolio Overview:</strong> Tracking {len(df)} investors across 
                {df['Location_Interest'].nunique()} locations in Andhra Pradesh maritime sector.
            </div>
        </div>
        
        <div class="section">
            <h2>💰 Top 5 Investors by Investment</h2>
            <table>
                <tr>
                    <th>Firm Name</th>
                    <th>Investment (₹ Cr)</th>
                    <th>Current Stage</th>
                </tr>
    """
    
    for _, row in top_investors.iterrows():
        html += f"""
                <tr>
                    <td>{row['Firm_Name']}</td>
                    <td>₹{row['Investment_INR_Cr']:,.0f} Cr</td>
                    <td>{row['Current_Stage']}</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>⚠️ Risk Status Breakdown</h2>
            <table>
                <tr>
                    <th>Status</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
    """
    
    total_count = len(df)
    for status, count in risk_breakdown.items():
        percentage = (count / total_count * 100)
        status_class = f"status-{status.lower()}"
        html += f"""
                <tr>
                    <td class="{status_class}">{status}</td>
                    <td>{count}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
        """
    
    html += """
            </table>
        </div>
        
        <div class="section">
            <h2>📍 Top 5 Locations by Investment</h2>
            <table>
                <tr>
                    <th>Location</th>
                    <th>Investment (₹ Cr)</th>
                </tr>
    """
    
    for location, inv in location_inv.items():
        if pd.notna(inv) and inv > 0:
            html += f"""
                <tr>
                    <td>{location}</td>
                    <td>₹{inv:,.0f} Cr</td>
                </tr>
            """
    
    html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>🌍 Investor Type Distribution</h2>
            <table>
                <tr>
                    <th>Type</th>
                    <th>Count</th>
                    <th>Percentage</th>
                </tr>
                <tr>
                    <td>Domestic</td>
                    <td>{kpis['Domestic_Count']}</td>
                    <td>{(kpis['Domestic_Count'] / (kpis['Domestic_Count'] + kpis['International_Count']) * 100):.1f}%</td>
                </tr>
                <tr>
                    <td>International</td>
                    <td>{kpis['International_Count']}</td>
                    <td>{(kpis['International_Count'] / (kpis['Domestic_Count'] + kpis['International_Count']) * 100):.1f}%</td>
                </tr>
            </table>
        </div>
        
        <div class="footer">
            <div class="footer-brand">AP Maritime Strategic Dashboard</div>
            <p>Andhra Pradesh Maritime Board | Government of Andhra Pradesh</p>
            <p style="font-size: 0.8rem; margin-top: 1rem;">
                Generated on {current_date} | Confidential - For Internal Use Only
            </p>
        </div>
    </body>
    </html>
    """
    
    return html

def plot_investment_by_location(df):
    """Bar chart of investment by location"""
    location_inv = df.groupby('Location_Interest')['Investment_INR_Cr'].sum().sort_values(ascending=True)
    location_inv = location_inv[location_inv > 0]
    
    fig = go.Figure(go.Bar(
        x=location_inv.values,
        y=location_inv.index,
        orientation='h',
        marker=dict(
            color=location_inv.values,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="₹ Cr")
        ),
        text=[f"₹{v:,.0f} Cr" for v in location_inv.values],
        textposition='auto',
    ))
    
    fig.update_layout(
        title="Investment Distribution by Location",
        xaxis_title="Investment (₹ Crores)",
        yaxis_title="Location",
        height=400,
        template="plotly_white",
        showlegend=False
    )
    
    return fig

def plot_investor_type_pie(df):
    """Pie chart of investor types"""
    type_counts = df['Investor_Type'].value_counts()
    
    fig = go.Figure(go.Pie(
        labels=type_counts.index,
        values=type_counts.values,
        hole=0.4,
        marker=dict(colors=['#667eea', '#764ba2']),
        textinfo='label+percent+value',
        textfont_size=14
    ))
    
    fig.update_layout(
        title="Investor Type Distribution",
        height=400,
        template="plotly_white"
    )
    
    return fig

def plot_stage_funnel(df):
    """Funnel chart showing stage progression"""
    stage_order = ['Early Discussion', 'EOI Submitted', 'Site Visit Complete', 
                   'DPR Pending', 'MoU Signed', 'Land Allotted', 'High-Level Meeting']
    
    stage_counts = df['Current_Stage'].value_counts()
    
    # Filter to stages present in data
    stages_present = [s for s in stage_order if s in stage_counts.index]
    values = [stage_counts[s] for s in stages_present]
    
    fig = go.Figure(go.Funnel(
        y=stages_present,
        x=values,
        textinfo="value+percent initial",
        marker=dict(color=['#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#06b6d4', '#14b8a6', '#f43f5e']),
        connector=dict(line=dict(color="#64748b", width=2))
    ))
    
    fig.update_layout(
        title="Investment Pipeline Funnel",
        height=500,
        template="plotly_white"
    )
    
    return fig

def plot_land_demand_by_location(df):
    """Bar chart of land demand by location"""
    land_data = df.groupby('Location_Interest')['Land_Requirement_Acres'].sum().sort_values(ascending=False)
    land_data = land_data[land_data > 0].head(10)
    
    fig = go.Figure(go.Bar(
        x=land_data.index,
        y=land_data.values,
        marker=dict(color='#10b981'),
        text=[f"{v:,.0f}" for v in land_data.values],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Land Demand by Location (Top 10)",
        xaxis_title="Location",
        yaxis_title="Land Required (Acres)",
        height=450,
        template="plotly_white",
        xaxis_tickangle=-45
    )
    
    return fig

def plot_waterfront_draft_scatter(df):
    """Scatter plot of waterfront vs draft requirements"""
    df_clean = df.dropna(subset=['Waterfront_Requirement_Meters', 'Draft_Requirement_Meters'])
    
    fig = go.Figure(go.Scatter(
        x=df_clean['Waterfront_Requirement_Meters'],
        y=df_clean['Draft_Requirement_Meters'],
        mode='markers+text',
        marker=dict(
            size=df_clean['Land_Requirement_Acres'] / 10,
            color=df_clean['Investment_INR_Cr'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title="Investment<br>₹ Cr"),
            line=dict(width=1, color='white')
        ),
        text=df_clean['Firm_Name'].str.split().str[0],
        textposition='top center',
        textfont=dict(size=9),
        hovertemplate='<b>%{text}</b><br>Waterfront: %{x}m<br>Draft: %{y}m<extra></extra>'
    ))
    
    fig.update_layout(
        title="Waterfront vs Draft Requirements (Bubble size = Land needed)",
        xaxis_title="Waterfront Required (Meters)",
        yaxis_title="Draft Requirement (Meters)",
        height=500,
        template="plotly_white"
    )
    
    return fig

def plot_employment_impact(df):
    """Stacked bar chart of employment impact"""
    df_emp = df[df['Direct_Employment'].notna()].copy()
    df_emp = df_emp.sort_values('Direct_Employment', ascending=False)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Direct Employment',
        x=df_emp['Firm_Name'],
        y=df_emp['Direct_Employment'],
        marker_color='#3b82f6'
    ))
    
    fig.add_trace(go.Bar(
        name='Indirect Employment',
        x=df_emp['Firm_Name'],
        y=df_emp['Indirect_Employment'],
        marker_color='#8b5cf6'
    ))
    
    fig.update_layout(
        title="Employment Impact by Firm",
        xaxis_title="Firm",
        yaxis_title="Number of Jobs",
        barmode='stack',
        height=450,
        template="plotly_white",
        xaxis_tickangle=-45,
        showlegend=True,
        legend=dict(x=0.8, y=1)
    )
    
    return fig

def create_risk_monitor_table(df):
    """Create color-coded risk monitoring table"""
    df_display = df[['Firm_Name', 'Current_Stage', 'Risk_Status', 'Days_Since_Activity', 
                     'Next_Action', 'Last_Activity_Month']].copy()
    
    # Color mapping
    def color_risk(val):
        if val == 'Active':
            return 'background-color: #d1fae5; color: #065f46'
        elif val == 'Delayed':
            return 'background-color: #fef3c7; color: #92400e'
        elif val in ['Stalled', 'Closed']:
            return 'background-color: #fee2e2; color: #991b1b'
        return ''
    
    styled_df = df_display.style.applymap(color_risk, subset=['Risk_Status'])
    
    return styled_df

# Main Application
def main():
    # Enhanced Header with better spacing
    st.markdown('<div class="main-header">🚢 APMB Investor Tracking Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Andhra Pradesh Maritime Board - Strategic Investment Intelligence Platform</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Location filter
    locations = ['All'] + sorted(df['Location_Interest'].unique().tolist())
    selected_location = st.sidebar.selectbox("Location", locations)
    
    # Investor Type filter
    investor_types = ['All'] + sorted(df['Investor_Type'].unique().tolist())
    selected_investor = st.sidebar.selectbox("Investor Type", investor_types)
    
    # Stage filter
    stages = ['All'] + sorted(df['Current_Stage'].unique().tolist())
    selected_stage = st.sidebar.selectbox("Current Stage", stages)
    
    # Risk Status filter
    risk_statuses = ['All'] + sorted(df['Risk_Status'].unique().tolist())
    selected_risk = st.sidebar.selectbox("Risk Status", risk_statuses)
    
    # Apply filters
    df_filtered = df.copy()
    if selected_location != 'All':
        df_filtered = df_filtered[df_filtered['Location_Interest'].str.contains(selected_location, case=False, na=False)]
    if selected_investor != 'All':
        df_filtered = df_filtered[df_filtered['Investor_Type'] == selected_investor]
    if selected_stage != 'All':
        df_filtered = df_filtered[df_filtered['Current_Stage'] == selected_stage]
    if selected_risk != 'All':
        df_filtered = df_filtered[df_filtered['Risk_Status'] == selected_risk]
    
    # Calculate KPIs
    kpis = calculate_kpis(df_filtered)
    
    # Download buttons in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Options")
    
    # Export filtered data as CSV
    csv_buffer = io.StringIO()
    df_filtered.to_csv(csv_buffer, index=False)
    st.sidebar.download_button(
        label="📊 Download Data (CSV)",
        data=csv_buffer.getvalue(),
        file_name=f"apmb_investors_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Generate and export Executive Summary PDF
    st.sidebar.markdown("")
    executive_html = generate_executive_summary_html(df_filtered, kpis)
    st.sidebar.download_button(
        label="📄 Executive Summary (HTML)",
        data=executive_html,
        file_name=f"apmb_executive_summary_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html",
        use_container_width=True,
        help="Download executive summary - Open in browser and print to PDF"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Executive Summary",
        "🏗️ Land & Infrastructure",
        "👥 Employment Impact",
        "⚠️ Risk Monitor",
        "🌍 International Investors"
    ])
    
    # TAB 1: Executive Summary
    with tab1:
        st.markdown("### 🎯 Key Performance Indicators")
        st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # KPI Cards Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(create_kpi_card("Total Investment", kpis['Total_Investment'], "💰"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_kpi_card("Direct Jobs", kpis['Total_Direct_Employment'], "👔"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_kpi_card("Active Investors", kpis['Active_Investors'], "✅", "active"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_kpi_card("MoUs Signed", kpis['MoUs_Signed'], "📝"), unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # KPI Cards Row 2
        col5, col6, col7, col8 = st.columns(4)
        
        with col5:
            st.markdown(create_kpi_card("Land Required (Acres)", kpis['Total_Land_Requested'], "🏞️"), unsafe_allow_html=True)
        
        with col6:
            st.markdown(create_kpi_card("Indirect Jobs", kpis['Total_Indirect_Employment'], "👥"), unsafe_allow_html=True)
        
        with col7:
            st.markdown(create_kpi_card("Delayed/Stalled", kpis['Delayed_Stalled'], "⚠️", "delayed"), unsafe_allow_html=True)
        
        with col8:
            total_investors = kpis['Domestic_Count'] + kpis['International_Count']
            st.markdown(create_kpi_card("Total Investors", total_investors, "🏢"), unsafe_allow_html=True)
        
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        
        # Charts
        st.markdown("### 📈 Investment Analytics")
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.plotly_chart(plot_investment_by_location(df_filtered), use_container_width=True)
        
        with col_right:
            st.plotly_chart(plot_investor_type_pie(df_filtered), use_container_width=True)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        st.plotly_chart(plot_stage_funnel(df_filtered), use_container_width=True)
        
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        
        # Summary statistics
        st.markdown("### 💼 Investment Summary by Type")
        col_stats1, col_stats2 = st.columns(2)
        
        with col_stats1:
            domestic_inv = df_filtered[df_filtered['Investor_Type'] == 'Domestic']['Investment_INR_Cr'].sum()
            st.metric("Domestic Investment", f"₹{domestic_inv:,.0f} Cr" if not np.isnan(domestic_inv) else "N/A")
        
        with col_stats2:
            intl_inv = df_filtered[df_filtered['Investor_Type'] == 'International']['Investment_INR_Cr'].sum()
            st.metric("International Investment", f"₹{intl_inv:,.0f} Cr" if not np.isnan(intl_inv) else "N/A")
    
    # TAB 2: Land & Infrastructure
    with tab2:
        st.markdown("### 🏗️ Land & Infrastructure Requirements")
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_land = df_filtered['Land_Requirement_Acres'].sum()
            st.metric("Total Land Demand", f"{total_land:,.0f} Acres" if not np.isnan(total_land) else "N/A")
        
        with col2:
            total_waterfront = df_filtered['Waterfront_Requirement_Meters'].sum()
            st.metric("Total Waterfront", f"{total_waterfront:,.0f} m" if not np.isnan(total_waterfront) else "N/A")
        
        with col3:
            avg_draft = df_filtered['Draft_Requirement_Meters'].mean()
            st.metric("Average Draft Required", f"{avg_draft:.1f} m" if not np.isnan(avg_draft) else "N/A")
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        st.plotly_chart(plot_land_demand_by_location(df_filtered), use_container_width=True)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        st.plotly_chart(plot_waterfront_draft_scatter(df_filtered), use_container_width=True)
        
        # Detailed table
        st.markdown("### Infrastructure Requirements Heatmap")
        infra_df = df_filtered[['Firm_Name', 'Location_Interest', 'Land_Requirement_Acres', 
                                 'Waterfront_Requirement_Meters', 'Draft_Requirement_Meters']].copy()
        infra_df = infra_df.dropna(subset=['Land_Requirement_Acres'])
        
        st.dataframe(
            infra_df.style.background_gradient(cmap='YlOrRd', subset=['Land_Requirement_Acres', 'Waterfront_Requirement_Meters']),
            use_container_width=True,
            height=400
        )
    
    # TAB 3: Employment Impact
    with tab3:
        st.markdown("### 👥 Employment Generation Potential")
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_direct = df_filtered['Direct_Employment'].sum()
            st.metric("Total Direct Jobs", f"{total_direct:,.0f}" if not np.isnan(total_direct) else "N/A")
        
        with col2:
            total_indirect = df_filtered['Indirect_Employment'].sum()
            st.metric("Total Indirect Jobs", f"{total_indirect:,.0f}" if not np.isnan(total_indirect) else "N/A")
        
        with col3:
            total_jobs = total_direct + total_indirect
            st.metric("Total Employment", f"{total_jobs:,.0f}" if not np.isnan(total_jobs) else "N/A")
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        st.plotly_chart(plot_employment_impact(df_filtered), use_container_width=True)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # Location-wise employment
        st.markdown("### 📍 Employment Distribution by Location")
        emp_location = df_filtered.groupby('Location_Interest')[['Direct_Employment', 'Indirect_Employment']].sum()
        emp_location = emp_location[emp_location['Direct_Employment'] > 0]
        
        fig_emp_loc = go.Figure()
        fig_emp_loc.add_trace(go.Bar(
            name='Direct',
            x=emp_location.index,
            y=emp_location['Direct_Employment'],
            marker_color='#3b82f6'
        ))
        fig_emp_loc.add_trace(go.Bar(
            name='Indirect',
            x=emp_location.index,
            y=emp_location['Indirect_Employment'],
            marker_color='#8b5cf6'
        ))
        
        fig_emp_loc.update_layout(
            barmode='group',
            height=400,
            template="plotly_white",
            xaxis_tickangle=-45,
            xaxis_title="Location",
            yaxis_title="Jobs",
            showlegend=True
        )
        
        st.plotly_chart(fig_emp_loc, use_container_width=True)
    
    # TAB 4: Risk Monitor
    with tab4:
        st.markdown("### ⚠️ Risk & Follow-up Monitoring")
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        # Enhanced status overview with color-coded cards
        col1, col2, col3, col4 = st.columns(4)
        
        active_count = len(df_filtered[df_filtered['Risk_Status'] == 'Active'])
        delayed_count = len(df_filtered[df_filtered['Risk_Status'] == 'Delayed'])
        stalled_count = len(df_filtered[df_filtered['Risk_Status'] == 'Stalled'])
        closed_count = len(df_filtered[df_filtered['Risk_Status'] == 'Closed'])
        
        with col1:
            st.markdown(create_kpi_card("Active", active_count, "✅", "active"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_kpi_card("Delayed", delayed_count, "⏱️", "delayed"), unsafe_allow_html=True)
        
        with col3:
            st.markdown(create_kpi_card("Stalled", stalled_count, "⛔", "stalled"), unsafe_allow_html=True)
        
        with col4:
            st.markdown(create_kpi_card("Closed", closed_count, "⚫", "closed"), unsafe_allow_html=True)
        
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        
        # Immediate attention list with enhanced alert box
        st.markdown("### 🚨 Immediate Attention Required")
        attention_df = df_filtered[df_filtered['Days_Since_Activity'] > 60].copy()
        attention_df = attention_df.sort_values('Days_Since_Activity', ascending=False)
        
        if len(attention_df) > 0:
            st.markdown(f"""
            <div class="alert-box alert-danger">
                <strong>⚠️ Alert:</strong> {len(attention_df)} investors have not been contacted in over 60 days. 
                Immediate follow-up action required to prevent further deterioration.
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(
                attention_df[['Firm_Name', 'Current_Stage', 'Days_Since_Activity', 'Next_Action', 'Risk_Status']],
                use_container_width=True,
                height=300
            )
        else:
            st.markdown("""
            <div class="alert-box alert-success">
                <strong>✅ Excellent:</strong> All investors have been contacted within the last 60 days! 
                Proactive engagement is maintaining strong pipeline health.
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="section-gap"></div>', unsafe_allow_html=True)
        
        # Full risk monitor table
        st.markdown("### Complete Investor Status Monitor")
        
        def color_code_row(row):
            if row['Risk_Status'] == 'Active':
                return ['background-color: #d1fae5'] * len(row)
            elif row['Risk_Status'] == 'Delayed':
                return ['background-color: #fef3c7'] * len(row)
            elif row['Risk_Status'] in ['Stalled', 'Closed']:
                return ['background-color: #fee2e2'] * len(row)
            return [''] * len(row)
        
        display_cols = ['Firm_Name', 'Investor_Type', 'Current_Stage', 'Risk_Status', 
                        'Days_Since_Activity', 'Next_Action', 'Last_Activity_Month']
        
        styled_table = df_filtered[display_cols].style.apply(color_code_row, axis=1)
        
        st.dataframe(styled_table, use_container_width=True, height=500)
        
        # Risk distribution chart
        st.markdown("### Risk Status Distribution")
        risk_counts = df_filtered['Risk_Status'].value_counts()
        
        fig_risk = go.Figure(go.Bar(
            x=risk_counts.index,
            y=risk_counts.values,
            marker=dict(color=['#10b981', '#f59e0b', '#ef4444', '#6b7280']),
            text=risk_counts.values,
            textposition='auto'
        ))
        
        fig_risk.update_layout(
            title="Investor Count by Risk Status",
            xaxis_title="Risk Status",
            yaxis_title="Count",
            height=350,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # TAB 5: International Investors
    with tab5:
        st.markdown("### 🌍 International Investor Analysis")
        st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
        
        df_intl = df_filtered[df_filtered['Investor_Type'] == 'International'].copy()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("International Investors", len(df_intl))
        
        with col2:
            active_intl = len(df_intl[df_intl['Risk_Status'] == 'Active'])
            st.metric("Active International", active_intl)
        
        with col3:
            countries = df_intl['Country'].nunique()
            st.metric("Countries Represented", countries)
        
        st.markdown('<div style="margin: 2rem 0;"></div>', unsafe_allow_html=True)
        
        # Country-wise breakdown
        st.markdown("### 🗺️ Country-wise Distribution")
        country_counts = df_intl['Country'].value_counts()
        
        fig_country = go.Figure(go.Bar(
            x=country_counts.index,
            y=country_counts.values,
            marker_color='#764ba2',
            text=country_counts.values,
            textposition='auto'
        ))
        
        fig_country.update_layout(
            title="International Investors by Country",
            xaxis_title="Country",
            yaxis_title="Number of Investors",
            height=350,
            template="plotly_white"
        )
        
        st.plotly_chart(fig_country, use_container_width=True)
        
        # International investor details
        st.markdown("### International Investor Details")
        intl_display = df_intl[['Firm_Name', 'Country', 'Sector', 'Location_Interest', 
                                 'Current_Stage', 'Land_Requirement_Acres', 
                                 'Waterfront_Requirement_Meters', 'Risk_Status']].copy()
        
        st.dataframe(intl_display, use_container_width=True, height=400)
        
        # Land and waterfront demand visualization
        if len(df_intl[df_intl['Land_Requirement_Acres'].notna()]) > 0:
            st.markdown("### Infrastructure Requirements - International Investors")
            
            fig_intl_infra = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Land Requirement", "Waterfront Requirement")
            )
            
            intl_land = df_intl[df_intl['Land_Requirement_Acres'].notna()]
            
            fig_intl_infra.add_trace(
                go.Bar(x=intl_land['Firm_Name'], y=intl_land['Land_Requirement_Acres'], 
                       name='Land (Acres)', marker_color='#10b981'),
                row=1, col=1
            )
            
            intl_water = df_intl[df_intl['Waterfront_Requirement_Meters'].notna()]
            
            fig_intl_infra.add_trace(
                go.Bar(x=intl_water['Firm_Name'], y=intl_water['Waterfront_Requirement_Meters'],
                       name='Waterfront (m)', marker_color='#3b82f6'),
                row=1, col=2
            )
            
            fig_intl_infra.update_layout(
                height=400,
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig_intl_infra, use_container_width=True)
    
    # Enhanced Professional Footer
    st.markdown('<div style="margin-top: 4rem;"></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="dashboard-footer">
        <div class="footer-title">🚢 AP Maritime Strategic Dashboard</div>
        <div class="footer-subtitle">
            Andhra Pradesh Maritime Board • Government of Andhra Pradesh<br>
            Strategic Investment Intelligence & Portfolio Management System
        </div>
        <div style="margin: 1.5rem 0; padding: 1rem 0; border-top: 1px solid rgba(255,255,255,0.1); border-bottom: 1px solid rgba(255,255,255,0.1);">
            <strong>Dashboard Snapshot:</strong> Tracking {len(df_filtered)} Investors • 
            ₹{kpis['Total_Investment']:,.0f} Cr Potential Investment • 
            {kpis['Total_Direct_Employment'] + kpis['Total_Indirect_Employment']:,.0f} Jobs Impact
        </div>
        <div class="footer-meta">
            Version 2.0 • Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')} • 
            Powered by Advanced Analytics<br>
            <span style="font-size: 0.8rem; opacity: 0.5;">
                For official use only • Confidential investment data
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
