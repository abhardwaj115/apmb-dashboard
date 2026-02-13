# 🚢 APMB Investor Tracking Dashboard v2.0

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](YOUR_STREAMLIT_URL_HERE)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![License](https://img.shields.io/badge/License-Gov%20AP-green)

**A production-ready, cloud-deployed interactive dashboard for tracking domestic and international investors in the Andhra Pradesh maritime sector.**

> 🚀 **[View Live Dashboard](YOUR_STREAMLIT_URL_HERE)** ← Add your URL after deployment

---

## 🎯 Quick Start

### For Users (No Installation)
Simply visit the live dashboard URL above and start exploring!

### For Developers (Local Development)
```bash
git clone https://github.com/YOUR_USERNAME/apmb-dashboard.git
cd apmb-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## ✨ Features

### 🎨 **Visual Excellence**
- **Animated KPI Counters** - Smooth count-up effects with pulse animations
- **Risk-Based Color System** - Intuitive Green/Amber/Red/Gray status indicators
- **Professional Gradients** - Government-grade color schemes
- **Hover Effects** - Interactive card animations
- **Responsive Design** - Works on desktop, tablet, and mobile

### 📊 **5 Interactive Analysis Tabs**

#### 1️⃣ Executive Summary
- 8 animated KPI cards
- Investment distribution by location
- Investor type breakdown
- Pipeline funnel visualization

#### 2️⃣ Land & Infrastructure
- Total land demand: 5,900+ acres
- Waterfront requirements analysis
- Draft depth comparisons
- Interactive scatter plots

#### 3️⃣ Employment Impact
- Direct jobs: 1,800
- Indirect jobs: 6,500
- Firm-wise breakdown
- Location distribution

#### 4️⃣ Risk Monitor
- Color-coded status tracking
- Immediate attention alerts (>60 days)
- Complete investor status table
- Risk distribution charts

#### 5️⃣ International Investors
- 3 countries represented
- Country-wise analysis
- Infrastructure requirements
- Global shipyard tracking

### 🔧 **Advanced Capabilities**
- **Dynamic Filtering** - Location, Type, Stage, Risk Status
- **PDF Export** - Executive summary with one-click download
- **CSV Export** - Full data export with timestamps
- **Optional Password Protection** - Secure access via secrets
- **Real-time Updates** - Auto-refresh on data changes

---

---

## 🚀 Deploy to Streamlit Cloud (Get Your Live URL)

### Prerequisites
- GitHub account (free)
- 10 minutes of your time
- No credit card required

### Deployment Steps

#### **Step 1: Create GitHub Repository**
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `apmb-dashboard`
3. Make it **Public**
4. Click "Create repository"

#### **Step 2: Upload Files**
1. Click "uploading an existing file"
2. Upload these files:
   - `app.py`
   - `requirements.txt`
   - `.gitignore`
3. Commit changes

#### **Step 3: Deploy to Streamlit**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Main file: `app.py`
6. Click "Deploy!"

#### **Step 4: Get Your URL**
After 2-3 minutes, your dashboard will be live at:
```
https://YOUR-USERNAME-apmb-dashboard-app-xxxxx.streamlit.app
```

### 🔐 Optional: Password Protection

To add password protection:

1. In Streamlit Cloud → Settings → Secrets
2. Add:
```toml
APP_PASSWORD = "your_secure_password"
```
3. Save and restart

**To disable:** Remove the secret or leave blank.

---

## 📊 Dashboard Data

### Current Portfolio
- **Total Investors:** 20 (17 Domestic + 3 International)
- **Total Investment:** ₹4,500 Crores
- **Employment Impact:** 8,300 jobs
- **Land Requirements:** 5,900+ acres
- **MoUs Signed:** 2 (HSL, GSL)

### Data Coverage
- Hindustan Shipyard Limited - ₹3,000 Cr, MoU Signed
- Goa Shipyard Limited - ₹1,500 Cr, MoU Signed
- Mazagaon Dock Limited - Site visit complete
- International: Hyundai KSOE, Hanwha Ocean, Damen

### Update Frequency
Data reflects investor tracking through November 2025.

---

## 🎨 Design System

### Color Palette
```css
Active Status:   #10b981 → #059669 (Green)
Delayed Status:  #f59e0b → #d97706 (Amber)
Stalled Status:  #ef4444 → #dc2626 (Red)
Closed Status:   #6b7280 → #4b5563 (Gray)
Primary Brand:   #1e3a8a → #3b82f6 (Blue)
Purple Accent:   #667eea → #764ba2
```

### Typography
- **Headers:** 3rem, weight 800
- **Subheaders:** 1.3rem, weight 500
- **Body:** Segoe UI font family
- **KPI Values:** 2.8rem, weight 800

### Animations
- Count-up: 1.5s ease-out
- Pulse: 3s infinite
- Hover: 0.3s ease

---

## 📁 Repository Structure

```
apmb-dashboard/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── DEPLOYMENT_GUIDE.md      # Detailed deployment instructions
├── CHANGELOG.md             # Version history
└── VISUAL_SHOWCASE.txt      # Feature showcase
```

---

## 🛠️ Technical Stack

### Frontend
- **Streamlit** 1.29.0 - Web framework
- **Plotly** 5.18.0 - Interactive charts
- **Custom CSS** - Animations & styling

### Backend
- **Python** 3.8+
- **Pandas** 2.1.4 - Data manipulation
- **NumPy** 1.26.2 - Numerical operations

### Deployment
- **Platform:** Streamlit Community Cloud
- **Cost:** FREE (unlimited)
- **Uptime:** 24/7
- **SSL:** Automatic HTTPS

---

## 🔧 Configuration

### Password Protection (Optional)

Create `.streamlit/secrets.toml`:
```toml
APP_PASSWORD = "your_password_here"
```

### Custom Styling

Modify CSS in `app.py` starting at line 70:
```python
st.markdown("""
<style>
    /* Your custom styles here */
</style>
""", unsafe_allow_html=True)
```

---

## 📈 Usage Examples

### For Executives
1. **Dashboard Access** → View live KPIs
2. **Filter by Location** → Focus on specific ports
3. **Export PDF** → Download executive summary
4. **Share URL** → Send to stakeholders

### For Analysts
1. **Risk Monitor** → Identify attention-needed investors
2. **Export CSV** → Further analysis in Excel
3. **Filter by Stage** → Pipeline health check
4. **Employment Tab** → Economic impact assessment

### For Administrators
1. **Update Data** → Edit `load_data()` function
2. **Push to GitHub** → Automatic deployment
3. **Monitor Access** → Streamlit Cloud analytics
4. **Manage Secrets** → Password updates

---

## 🐛 Troubleshooting

### Common Issues

**App won't start**
- Check `requirements.txt` is present
- Verify Python version compatibility
- Review Streamlit Cloud logs

**Data not displaying**
- Check filter settings (may be too restrictive)
- Verify data in `load_data()` function
- Clear browser cache

**Charts not rendering**
- Ensure Plotly is installed
- Check browser JavaScript is enabled
- Try different browser

**Password not working**
- Verify `APP_PASSWORD` in secrets
- Check for typos
- Restart app after secret changes

### Getting Help
- [Streamlit Forum](https://discuss.streamlit.io)
- [Streamlit Docs](https://docs.streamlit.io)
- [GitHub Issues](YOUR_REPO_URL/issues)

---

## 📝 License

**Internal Use - Government of Andhra Pradesh**

This dashboard is developed for the Andhra Pradesh Maritime Board and is intended for official government use only. Unauthorized distribution or commercial use is prohibited.

---

## 👥 Credits

**Developed by:** APMB Data Analytics Team  
**Organization:** Andhra Pradesh Maritime Board  
**Government:** Government of Andhra Pradesh  
**Version:** 2.0 Cloud Edition  
**Last Updated:** December 2025

---

## 🎉 What's Next?

After deploying your dashboard:

1. ✅ **Test All Features** - Navigate through all 5 tabs
2. ✅ **Share URL** - Send to team members
3. ✅ **Export PDFs** - Download executive summaries
4. ✅ **Monitor Usage** - Check Streamlit Cloud analytics
5. ✅ **Collect Feedback** - Gather user insights
6. ✅ **Plan Updates** - Schedule data refreshes

---

## 🔗 Quick Links

- 🚀 [Deploy Now](https://share.streamlit.io)
- 📚 [Streamlit Docs](https://docs.streamlit.io)
- 💬 [Community Forum](https://discuss.streamlit.io)
- 📊 [Plotly Gallery](https://plotly.com/python/)
- 🐙 [GitHub Guides](https://guides.github.com)

---

**Made with ❤️ for Andhra Pradesh Maritime Board**

*Transforming maritime investment data into actionable intelligence*
- **8 Key Performance Indicators (KPIs)**
  - Total Investment (₹ Crores)
  - Direct & Indirect Employment
  - Active Investors
  - MoUs Signed
  - Land & Waterfront Requirements
  - Delayed/Stalled Projects
  
- **Visualizations**
  - Investment by Location (Bar Chart)
  - Investor Type Distribution (Pie Chart)
  - Investment Pipeline Funnel

### **Land & Infrastructure Tab**
- Total land demand analysis
- Waterfront requirements mapping
- Draft requirement comparisons
- Interactive scatter plot (Waterfront vs Draft)
- Color-coded heatmap table

### **Employment Impact Tab**
- Direct vs Indirect employment breakdown
- Firm-wise employment charts
- Location-wise job distribution
- Total employment metrics

### **Risk Monitor Tab**
- Real-time status tracking (Active/Delayed/Stalled/Closed)
- Color-coded risk indicators
  - 🟢 Green: Active & Progressing
  - 🟡 Amber: Delayed/DPR Pending
  - 🔴 Red: Stalled/No Update >60 days
- Immediate attention alerts
- Days since last activity tracking

### **International Investors Tab**
- Country-wise breakdown
- Separate infrastructure analysis
- Status monitoring
- Comparative metrics

---

## 🎯 KPI Logic & Calculations

### 1. **Total Potential Investment (₹ Cr)**
```python
Sum of all confirmed investment amounts from MoU proposals
Excludes: Investors without specified amounts
```

### 2. **Total Direct Employment**
```python
Sum of direct jobs from investors with confirmed employment data
HSL: 300, GSL: 1,500
```

### 3. **Total Indirect Employment**
```python
Sum of indirect jobs through supply chain and ecosystem
HSL: 1,500, GSL: 5,000
```

### 4. **Total Land Requested (Acres)**
```python
Sum of land requirements from all active proposals
Includes ranges calculated as midpoint (e.g., 200-250 → 225)
```

### 5. **Total Waterfront Requested (Meters)**
```python
Sum of waterfront access requirements
Critical for shipyard operations
```

### 6. **Number of MoUs Signed**
```python
Count of investors in "MoU Signed" stage
Current: HSL, GSL
```

### 7. **Number of Active Investors**
```python
Count of investors with Risk_Status = "Active"
Regular engagement, progressing discussions
```

### 8. **Number of Delayed/Stalled Investors**
```python
Count of investors with Risk_Status in ["Delayed", "Stalled"]
Require immediate follow-up action
```

### 9. **Domestic vs International Count**
```python
Investor_Type == "Domestic" → Indian companies
Investor_Type == "International" → Foreign shipyards
```

### 10. **Location-wise Investment Exposure**
```python
Group investments by Location_Interest
Key locations: Machilipatnam, Mulapeta, Kakinada, Dugarajapatnam
```

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Step 1: Clone/Download Files**
Ensure you have these files:
```
project-folder/
├── app.py
├── requirements.txt
└── README.md
```

### **Step 2: Create Virtual Environment (Recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Run the Dashboard**
```bash
streamlit run app.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

---

## 📁 Data Structure

### **Embedded Dataset Columns**

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `Firm_Name` | String | Company/Shipyard name | "Hindustan Shipyard Limited" |
| `Investor_Type` | Categorical | Domestic/International | "Domestic" |
| `Sector` | Categorical | Business sector | "Shipbuilding" |
| `Location_Interest` | String | Preferred locations | "Mulapeta/Kakinada" |
| `Current_Stage` | Categorical | Pipeline stage | "MoU Signed" |
| `Investment_INR_Cr` | Float | Investment amount | 3000.0 |
| `Land_Requirement_Acres` | Float | Land needed | 225.0 |
| `Waterfront_Requirement_Meters` | Float | Waterfront access | 800.0 |
| `Draft_Requirement_Meters` | Float | Port draft depth | 16.5 |
| `Direct_Employment` | Float | Direct jobs | 300 |
| `Indirect_Employment` | Float | Indirect jobs | 1500 |
| `Support_Requested` | String | Required support | "Land, Infra, Clearances" |
| `Risk_Status` | Categorical | Engagement risk | "Active" |
| `Next_Action` | String | Follow-up action | "RFP Participation" |
| `Last_Activity_Month` | String | Last contact | "November 2025" |
| `Country` | String | Origin country | "India" |

---

## 🎨 Key Features

### **Interactive Filters**
- **Location**: Filter by port/location
- **Investor Type**: Domestic vs International
- **Current Stage**: Pipeline stage
- **Risk Status**: Active/Delayed/Stalled/Closed

### **Export Capabilities**
- Download filtered data as CSV
- Export summary reports
- Timestamp-based file naming

### **Real-time Calculations**
- Dynamic KPI updates based on filters
- Automatic days-since-activity tracking
- Risk status color coding

### **Professional UI**
- Wide layout optimized for presentations
- Custom color palette (government-friendly)
- Gradient KPI cards
- Responsive design
- Clean typography

---

## 📊 Sample Investors Included

### **Domestic (17 firms)**
- Hindustan Shipyard Limited (HSL) - **MoU Signed**
- Mazagaon Dock Limited (MDL)
- Goa Shipyard Limited (GSL) - **MoU Signed**
- Garden Reach Shipbuilders (GRSE)
- Cochin Shipyard Limited (CSL)
- Reliance Infrastructure
- Adani Ports & SEZ
- L&T
- And 9 more...

### **International (3 firms)**
- Hyundai HD KSOE (South Korea)
- Hanwha Ocean (South Korea)
- Damen Shipyard Groups (Netherlands)

---

## 🔧 Customization

### **Adding New Data**
Modify the `load_data()` function in `app.py`:
```python
def load_data():
    data = {
        'Firm_Name': [...],
        'Investor_Type': [...],
        # Add your data here
    }
    return pd.DataFrame(data)
```

### **Uploading Excel/CSV**
Replace embedded data with file upload:
```python
uploaded_file = st.file_uploader("Upload Investor Data")
if uploaded_file:
    df = pd.read_excel(uploaded_file)  # or pd.read_csv()
```

### **Changing Color Scheme**
Modify CSS in `app.py`:
```python
st.markdown("""
<style>
    .kpi-card {
        background: linear-gradient(135deg, #YOUR_COLOR1, #YOUR_COLOR2);
    }
</style>
""")
```

---

## 🎯 Usage Scenarios

1. **CEO Briefings**: Tab 1 - Executive Summary with all KPIs
2. **Land Allocation Planning**: Tab 2 - Infrastructure requirements
3. **Economic Impact Assessment**: Tab 3 - Employment generation
4. **Follow-up Meetings**: Tab 4 - Risk monitoring with action items
5. **International Relations**: Tab 5 - Global investor tracking

---

## 📈 Data Insights

### **Key Findings from Current Data**
- **Total Investment Potential**: ₹4,500 Crores (confirmed MoUs)
- **Employment Generation**: 1,800 direct + 6,500 indirect = 8,300 jobs
- **Land Requirement**: 5,900+ acres across all locations
- **Top Location**: Machilipatnam (multiple investors interested)
- **International Interest**: 3 global shipyards in discussions

---

## 🐛 Troubleshooting

### **Port Already in Use**
```bash
streamlit run app.py --server.port 8502
```

### **Module Not Found Error**
```bash
pip install --upgrade -r requirements.txt
```

### **Browser Doesn't Open**
Manually navigate to: `http://localhost:8501`

### **Data Not Displaying**
- Check that all columns exist in DataFrame
- Verify no missing critical fields
- Review browser console for errors

---

## 📝 Notes

- **Data Date**: Based on November 2025 tracking document
- **Update Frequency**: Manual updates to embedded data
- **Performance**: Optimized for 50-100 investor records
- **Browser Support**: Chrome, Firefox, Safari, Edge

---

## 🤝 Support

For questions or issues:
1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure Python version 3.8+
4. Review filter settings if data appears missing

---

## 📜 License

Internal use - Andhra Pradesh Maritime Board

---

## 🎉 Quick Start Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run dashboard
streamlit run app.py

# 3. Open browser
# http://localhost:8501

# 4. Start exploring!
```

---

**Dashboard Version**: 2.0 Enhanced Edition  
**Last Updated**: December 2025  
**What's New**: Animated KPIs • Risk Colors • PDF Export • Enhanced Design  
**Developer**: APMB Data Analytics Team
