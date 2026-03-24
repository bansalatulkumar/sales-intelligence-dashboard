const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

// Sample sales intelligence data
const salesIntelligenceData = {
  totalAccounts: 100,
  summary: {
    highValueAccounts: 10,
    churnRiskAccounts: 10,
    growth: {
      growing: 45,
      flat: 30,
      declining: 25
    },
    totalRevenue: 15750000,
    avgRevenuePerAccount: 157500
  },
  topAccounts: [
    {
      id: 1,
      companyName: "TCS Limited",
      customerId: "CUST/00001",
      sector: "IT Services",
      acmName: "Rajesh Kumar",
      branch: "Bangalore",
      renewalQuarter: "FY2026-Q2",
      daysToRenewal: 45,
      lastFyRevenue: 850000,
      currentFyRevenue: 1020000,
      growthPercentage: 20,
      status: "Growing",
      category: "Key",
      employeeSize: "10K+",
      painPoints: [
        "Low applies on premium roles",
        "Under-utilization of Hirist platform",
        "Over-dependence on Naukri"
      ],
      productHealth: [
        { product: "Naukri Job Postings", status: "Healthy", utilization: 85 },
        { product: "Hirist Premium Jobs", status: "Upsell Opportunity", utilization: 45 },
        { product: "IIMJobs Premium", status: "Not Activated", utilization: 0 }
      ],
      topJobs: [
        { title: "Senior Software Engineer", ctc: "45 LPA", experience: "5-8 yrs", applies: 87 },
        { title: "Data Scientist", ctc: "52 LPA", experience: "3-7 yrs", applies: 62 }
      ],
      salesPitch: "TCS is getting strong volume on Naukri but missing high-value tech talent via Hirist. We can increase premium role fills by 40% by activating Hirist for senior positions."
    },
    {
      id: 2,
      companyName: "Infosys Limited",
      customerId: "CUST/00002",
      sector: "IT Services",
      acmName: "Priya Sharma",
      branch: "Bangalore",
      renewalQuarter: "FY2026-Q3",
      daysToRenewal: 98,
      lastFyRevenue: 720000,
      currentFyRevenue: 720000,
      growthPercentage: 0,
      status: "Flat",
      category: "Key",
      employeeSize: "10K+",
      painPoints: [
        "Flat revenue despite increased hiring",
        "Paying for unused Zwayam license",
        "Low employer branding investment"
      ],
      productHealth: [
        { product: "Naukri Job Postings", status: "Healthy", utilization: 75 },
        { product: "Zwayam", status: "Poor Utilization", utilization: 20 }
      ],
      topJobs: [
        { title: "Project Manager", ctc: "32 LPA", experience: "8-12 yrs", applies: 43 }
      ],
      salesPitch: "Infosys can drive 30% revenue growth by leveraging Employer Branding + Zwayam optimization for high-volume hiring."
    },
    {
      id: 3,
      companyName: "Goldman Sachs India",
      customerId: "CUST/00003",
      sector: "BFSI",
      acmName: "Amit Patel",
      branch: "Mumbai",
      renewalQuarter: "FY2026-Q2",
      daysToRenewal: 52,
      lastFyRevenue: 580000,
      currentFyRevenue: 696000,
      growthPercentage: 20,
      status: "Growing",
      category: "Key",
      employeeSize: "1K–10K",
      painPoints: [
        "Premium roles underperforming on Naukri",
        "Not using IIMJobs for leadership hiring"
      ],
      productHealth: [
        { product: "Naukri Job Postings", status: "Healthy", utilization: 80 },
        { product: "IIMJobs Premium Jobs", status: "Upsell Opportunity", utilization: 30 }
      ],
      topJobs: [
        { title: "Analyst", ctc: "48 LPA", experience: "4-6 yrs", applies: 156 },
        { title: "Vice President", ctc: "80 LPA", experience: "15+ yrs", applies: 18 }
      ],
      salesPitch: "Goldman Sachs can fill leadership roles 3x faster using IIMJobs Premium. Peers in BFSI are getting 10x better response rates."
    }
  ],
  churnRiskAccounts: [
    {
      id: 4,
      companyName: "ABC Consulting",
      customerId: "CUST/00004",
      sector: "Consulting",
      acmName: "Vivek Singh",
      branch: "Delhi NCR",
      renewalQuarter: "FY2026-Q1",
      daysToRenewal: 15,
      lastFyRevenue: 125000,
      currentFyRevenue: 95000,
      growthPercentage: -24,
      status: "Declining",
      category: "Retail",
      employeeSize: "50–200",
      painPoints: [
        "Severe decline in hiring demand",
        "Low applies across all channels",
        "Products completely underutilized"
      ],
      productHealth: [
        { product: "Naukri Job Postings", status: "Critical - Churn Risk", utilization: 10 }
      ],
      salesPitch: "Urgent renewal required. ABC Consulting shows severe underutilization. Need immediate intervention with product optimization or risk losing account."
    }
  ],
  sectorBenchmarks: {
    "IT Services": {
      avgApplesPerJob: 75,
      premiumHiringPercentage: 45,
      topPlatform: "Hirist"
    },
    "BFSI": {
      avgApplesPerJob: 85,
      premiumHiringPercentage: 60,
      topPlatform: "IIMJobs"
    },
    "Startup": {
      avgApplesPerJob: 42,
      premiumHiringPercentage: 25,
      topPlatform: "Naukri"
    }
  }
};

// Routes
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/data', (req, res) => {
  res.json(salesIntelligenceData);
});

app.get('/api/accounts', (req, res) => {
  res.json({
    totalAccounts: 100,
    topAccounts: salesIntelligenceData.topAccounts,
    churnRiskAccounts: salesIntelligenceData.churnRiskAccounts
  });
});

app.get('/api/account/:id', (req, res) => {
  const accountId = parseInt(req.params.id);
  const allAccounts = [
    ...salesIntelligenceData.topAccounts,
    ...salesIntelligenceData.churnRiskAccounts
  ];
  const account = allAccounts.find(a => a.id === accountId);
  
  if (account) {
    res.json(account);
  } else {
    res.status(404).json({ error: 'Account not found' });
  }
});

app.get('/api/summary', (req, res) => {
  res.json(salesIntelligenceData.summary);
});

// Start server
app.listen(PORT, () => {
  console.log(`🎯 Sales Intelligence Dashboard running at http://localhost:${PORT}`);
  console.log(`Press Ctrl+C to stop the server`);
});
