# Sales Intelligence Dashboard - Setup Guide

## 📊 Project Overview

This is a Node.js/Express web application that serves a Sales Intelligence Dashboard for InfoEdge (Naukri, IIMJobs, Hirist).

## 📁 Project Structure

```
project/
├── server.js              # Express server (main entry point)
├── package.json          # Node.js dependencies
├── README.md            # This file
└── public/
    ├── index.html       # Main dashboard HTML
    ├── styles.css       # Dashboard styling
    └── script.js        # Frontend interactions
```

## 🚀 Quick Start

### Step 1: Install Dependencies
Open terminal in the `project` folder and run:
```bash
npm install
```

This will install:
- **express** - Web server framework
- **cors** - Cross-Origin Resource Sharing
- **body-parser** - Parse request bodies

### Step 2: Start the Server
```bash
npm start
```

You should see:
```
🎯 Sales Intelligence Dashboard running at http://localhost:8000
Press Ctrl+C to stop the server
```

### Step 3: Open in Browser
Navigate to: **http://localhost:8000**

## 📋 Dashboard Features

### 1. **Dashboard Tab**
- Executive summary with key metrics
- Total accounts: 100
- Total revenue: ₹1.57 Cr
- Account health distribution (Growing/Flat/Declining)
- Sector breakdown
- Key insights

### 2. **Top Accounts Tab**
- View top 10 high-value accounts
- Account details including:
  - Sector, ACM Name, Sales Branch
  - Renewal quarter and days to renewal
  - Revenue and growth %
  - Pain points
  - Sales pitch

### 3. **Churn Risk Tab**
- View top 10 accounts at risk of churn
- Urgent renewal dates (< 90 days)
- Critical utilization issues
- Immediate action items

### 4. **Account Details Tab**
- Search by Account ID (1-100)
- Detailed account analysis
- Product health and utilization %
- Top jobs posted with CTC and applications
- Recommended sales actions

## 🔌 API Endpoints

The server provides the following REST APIs:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serves the main dashboard HTML |
| `/api/data` | GET | Returns all sales intelligence data |
| `/api/accounts` | GET | Returns list of all accounts |
| `/api/account/:id` | GET | Returns specific account details |
| `/api/summary` | GET | Returns executive summary |

### Example: Fetch Account Data
```javascript
fetch('/api/account/1')
  .then(res => res.json())
  .then(data => console.log(data))
```

## 🛠️ Development

### Run with Auto-Reload (Optional)
If you want the server to automatically restart when you modify files:

```bash
npm install -g nodemon
npm run dev
```

Then modify `server.js` or files in `public/` and they'll auto-reload!

## 📊 Data Structure

### Account Object
```json
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
  "painPoints": ["Low applies on premium roles"],
  "productHealth": [
    { "product": "Naukri Job Postings", "status": "Healthy", "utilization": 85 }
  ],
  "topJobs": [
    { "title": "Senior Software Engineer", "ctc": "45 LPA", "experience": "5-8 yrs", "applies": 87 }
  ],
  "salesPitch": "..."
}
```

## 🎨 Customization

### Modify the Dashboard Theme
Edit `public/styles.css` - Change the gradient colors:
```css
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Add More Accounts
Edit `server.js` in the `salesIntelligenceData` object to add more accounts to `topAccounts` and `churnRiskAccounts` arrays.

### Change Port
```bash
PORT=3000 npm start
```
Then visit: http://localhost:3000

## ⚠️ Troubleshooting

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows (find the PID and kill it)
```

### Module Not Found Error
```bash
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors
The server already has CORS enabled. If issues persist, check your browser console for more details.

## 🔗 Integration with Python Script

To integrate the Python sales intelligence generation script:

1. Run the Python script to generate synthetic data:
   ```bash
   python ../generate_sales_intelligence.py
   ```

2. Modify `server.js` to load data from the Python-generated JSON file instead of the hardcoded data.

## 📝 License

Copyright © 2026 InfoEdge (India) Ltd. All rights reserved.

## 📞 Support

For issues or questions, check the browser console (F12) for error messages.

---

**Happy selling! 🚀**
