let currentData = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

// Fetch data from the server
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        currentData = await response.json();
        populateTopAccounts();
        populateChurnRisk();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Show specific section
function showSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
    });

    // Remove active from all nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected section
    document.getElementById(sectionId).classList.add('active');

    // Add active to clicked button
    event.target.classList.add('active');
}

// Populate top accounts
function populateTopAccounts() {
    if (!currentData) return;

    const container = document.getElementById('topAccountsList');
    container.innerHTML = currentData.topAccounts.map(account => `
        <div class="account-card" onclick="showAccountDetail(${account.id})">
            <div class="account-header">
                <div>
                    <div class="account-title">${account.companyName}</div>
                    <div class="account-customer-id">${account.customerId}</div>
                </div>
                <span class="status-badge status-${account.status.toLowerCase()}">${account.status}</span>
            </div>

            <div class="account-grid">
                <div class="account-info">
                    <div class="info-label">Sector</div>
                    <div class="info-value">${account.sector}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">ACM</div>
                    <div class="info-value">${account.acmName}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Branch</div>
                    <div class="info-value">${account.branch}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Renewal</div>
                    <div class="info-value">${account.renewalQuarter}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Days to Renewal</div>
                    <div class="info-value">${account.daysToRenewal} days</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Current FY Revenue</div>
                    <div class="info-value">₹${(account.currentFyRevenue / 100000).toFixed(2)}L</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Growth %</div>
                    <div class="info-value" style="color: ${account.growthPercentage >= 0 ? '#00b386' : '#ff6b6b'}">
                        ${account.growthPercentage > 0 ? '+' : ''}${account.growthPercentage}%
                    </div>
                </div>
            </div>

            <div class="pain-points">
                <div class="pain-points-title">🔴 Pain Points</div>
                <ul class="pain-points-list">
                    ${account.painPoints.map(point => `<li>${point}</li>`).join('')}
                </ul>
            </div>

            <div class="sales-pitch">
                <strong>💡 Sales Pitch:</strong> ${account.salesPitch}
            </div>
        </div>
    `).join('');
}

// Populate churn risk
function populateChurnRisk() {
    if (!currentData) return;

    const container = document.getElementById('churnRiskList');
    container.innerHTML = currentData.churnRiskAccounts.map(account => `
        <div class="account-card" style="border-left: 4px solid #ff6b6b;" onclick="showAccountDetail(${account.id})">
            <div class="account-header">
                <div>
                    <div class="account-title">${account.companyName}</div>
                    <div class="account-customer-id">${account.customerId}</div>
                </div>
                <span class="status-badge" style="background: #f8d7da; color: #721c24;">⚠️ CRITICAL</span>
            </div>

            <div class="account-grid">
                <div class="account-info">
                    <div class="info-label">Sector</div>
                    <div class="info-value">${account.sector}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">ACM</div>
                    <div class="info-value">${account.acmName}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Branch</div>
                    <div class="info-value">${account.branch}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Renewal</div>
                    <div class="info-value">${account.renewalQuarter}</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Days to Renewal</div>
                    <div class="info-value" style="color: #ff6b6b; font-weight: bold;">${account.daysToRenewal} days ⏰</div>
                </div>
                <div class="account-info">
                    <div class="info-label">Growth %</div>
                    <div class="info-value" style="color: #ff6b6b;">
                        ${account.growthPercentage}%
                    </div>
                </div>
            </div>

            <div class="pain-points">
                <div class="pain-points-title">🔴 Critical Issues</div>
                <ul class="pain-points-list">
                    ${account.painPoints.map(point => `<li>${point}</li>`).join('')}
                </ul>
            </div>

            <div class="sales-pitch" style="background: #ffe7e7; border-left-color: #ff6b6b;">
                <strong>⚠️ Urgent Action:</strong> ${account.salesPitch}
            </div>
        </div>
    `).join('');
}

// Show account detail
function showAccountDetail(accountId) {
    document.getElementById('accountIdInput').value = accountId;
    loadAccountDetail();
}

// Load account detail
async function loadAccountDetail() {
    const accountId = document.getElementById('accountIdInput').value;
    
    if (!accountId) {
        alert('Please enter an Account ID');
        return;
    }

    try {
        const response = await fetch(`/api/account/${accountId}`);
        if (!response.ok) throw new Error('Account not found');
        
        const account = await response.json();
        displayAccountDetail(account);

        // Switch to detail section
        showSection('accountDetail');
        document.querySelector('[onclick="showSection(\'accountDetail\')"]').click();
    } catch (error) {
        document.getElementById('accountDetailContent').innerHTML = `
            <div style="background: #f8d7da; padding: 20px; border-radius: 6px; color: #721c24;">
                ❌ ${error.message}
            </div>
        `;
    }
}

// Display account detail
function displayAccountDetail(account) {
    const container = document.getElementById('accountDetailContent');

    const productHealthHTML = account.productHealth.map(product => {
        const statusClass = product.status.includes('Critical') ? 'health-critical' : 
                          product.status.includes('Poor') ? 'health-warning' : 'health-healthy';
        return `
            <tr>
                <td><strong>${product.product}</strong></td>
                <td><span class="health-status ${statusClass}">${product.status}</span></td>
                <td><strong>${product.utilization}%</strong></td>
            </tr>
        `;
    }).join('');

    const topJobsHTML = account.topJobs.map(job => `
        <tr>
            <td><strong>${job.title}</strong></td>
            <td>${job.ctc}</td>
            <td>${job.experience}</td>
            <td>${job.applies}</td>
        </tr>
    `).join('');

    container.innerHTML = `
        <div class="account-detail show">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h2 style="color: white; border: none; margin: 0; padding: 0; margin-bottom: 10px;">${account.companyName}</h2>
                        <div style="font-size: 14px; opacity: 0.9;">Customer ID: ${account.customerId}</div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 24px; font-weight: bold; margin-bottom: 5px;">${account.status}</div>
                        <div style="font-size: 13px; opacity: 0.9;">${account.renewalQuarter}</div>
                    </div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;">
                <div style="background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <div style="color: #999; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">Sector</div>
                    <div style="font-size: 16px; font-weight: bold; color: #333;">${account.sector}</div>
                </div>
                <div style="background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <div style="color: #999; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">Employee Size</div>
                    <div style="font-size: 16px; font-weight: bold; color: #333;">${account.employeeSize}</div>
                </div>
                <div style="background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <div style="color: #999; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">Days to Renewal</div>
                    <div style="font-size: 16px; font-weight: bold; color: #333;">${account.daysToRenewal} days</div>
                </div>
                <div style="background: #f8f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <div style="color: #999; font-size: 12px; text-transform: uppercase; margin-bottom: 8px;">Current FY Revenue</div>
                    <div style="font-size: 16px; font-weight: bold; color: #333;">₹${(account.currentFyRevenue / 100000).toFixed(2)}L</div>
                </div>
            </div>

            <div style="background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; margin-bottom: 30px;">
                <h3 style="color: #856404; margin-bottom: 15px;">🔴 Pain Points & Issues</h3>
                <ul style="list-style: none; color: #666; font-size: 14px; line-height: 1.8;">
                    ${account.painPoints.map(point => `<li style="margin-bottom: 8px;">→ ${point}</li>`).join('')}
                </ul>
            </div>

            <div style="background: #e7f3ff; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 30px;">
                <h3 style="color: #004085; margin-bottom: 10px;">💡 Sales Pitch</h3>
                <p style="color: #004085; font-size: 14px; line-height: 1.6;">${account.salesPitch}</p>
            </div>

            <div style="background: white; border: 1px solid #eee; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h3 style="margin-bottom: 15px;">📦 Product Health & Utilization</h3>
                <table class="products-table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Status</th>
                            <th>Utilization %</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${productHealthHTML}
                    </tbody>
                </table>
            </div>

            <div style="background: white; border: 1px solid #eee; padding: 20px; border-radius: 8px; margin-bottom: 30px;">
                <h3 style="margin-bottom: 15px;">🎯 Top Premium Jobs in Last 6 Months</h3>
                <table class="products-table">
                    <thead>
                        <tr>
                            <th>Job Title</th>
                            <th>CTC</th>
                            <th>Experience</th>
                            <th>Applications</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${topJobsHTML}
                    </tbody>
                </table>
            </div>

            <div style="background: #e7f3ff; padding: 20px; border-radius: 8px;">
                <h3 style="color: #004085; margin-bottom: 15px;">🚀 Recommended Actions</h3>
                <ul style="list-style: none; color: #004085; font-size: 14px; line-height: 1.8;">
                    <li style="margin-bottom: 10px;">✓ Schedule renewal discussion 30 days before renewal date</li>
                    <li style="margin-bottom: 10px;">✓ Present upsell opportunities for underutilized products</li>
                    <li style="margin-bottom: 10px;">✓ Benchmark their metrics against sector peers</li>
                    <li style="margin-bottom: 10px;">✓ Propose product optimization strategy</li>
                </ul>
            </div>
        </div>
    `;
}

// Allow Enter key to load account
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('accountIdInput')?.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') loadAccountDetail();
    });
});
