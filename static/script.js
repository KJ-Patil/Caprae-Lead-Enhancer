/**
 * Caprae Lead Enhancer - Frontend JavaScript
 * Handles user interactions, API calls, and dynamic content updates
 */

// Global variables
let leads = [];
let processedLeads = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Set up form submission
    document.getElementById('leadForm').addEventListener('submit', handleFormSubmit);
    
    // Set up button event handlers
    setupButtonHandlers();
    
    // Initialize empty state
    updateLeadCount();
}

function setupButtonHandlers() {
    // Sample data button
    const sampleDataBtn = document.getElementById('sampleDataBtn');
    if (sampleDataBtn) {
        sampleDataBtn.addEventListener('click', loadSampleData);
    }
    
    // Upload leads button
    const uploadBtn = document.getElementById('uploadLeadsBtn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', handleCsvUpload);
    }
    
    // Add file input for CSV upload
    addCsvUploadInput();
}

// Handle form submission
function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const lead = {
        company_name: document.getElementById('companyName').value.trim(),
        contact_name: document.getElementById('contactName').value.trim(),
        email: document.getElementById('email').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        industry: document.getElementById('industry').value,
        company_size: document.getElementById('companySize').value,
        revenue: document.getElementById('revenue').value,
        website: document.getElementById('website').value.trim(),
        linkedin: document.getElementById('linkedin').value.trim()
    };
    
    // Validate required fields
    if (!lead.company_name || !lead.contact_name || !lead.email || !lead.phone || !lead.industry) {
        showAlert('Please fill in all required fields', 'warning');
        return;
    }
    
    // Add lead to list
    addLeadToList(lead);
    
    // Clear form
    clearForm();
    
    showAlert('Lead added successfully!', 'success');
}

// Add lead to the leads list
function addLeadToList(lead) {
    const leadId = Date.now() + Math.random();
    lead.id = leadId;
    leads.push(lead);
    
    updateLeadCount();
    renderLeadsList();
    updateProcessButton();
}

// Render the leads list
function renderLeadsList() {
    const leadsList = document.getElementById('leadsList');
    
    if (leads.length === 0) {
        leadsList.innerHTML = `
            <div class="list-group-item text-center text-muted py-4">
                <i class="fas fa-inbox fa-3x mb-3"></i>
                <p class="mb-0">No leads added yet. Add your first lead above!</p>
            </div>
        `;
        return;
    }
    
    leadsList.innerHTML = leads.map(lead => `
        <div class="list-group-item d-flex justify-content-between align-items-center">
            <div>
                <h6 class="mb-1">${lead.company_name}</h6>
                <small class="text-muted">${lead.contact_name} • ${lead.email} • ${lead.industry}</small>
            </div>
            <button class="btn btn-sm btn-outline-danger" onclick="removeLead(${lead.id})">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
}

// Remove lead from list
function removeLead(leadId) {
    leads = leads.filter(lead => lead.id !== leadId);
    updateLeadCount();
    renderLeadsList();
    updateProcessButton();
}

// Update lead count
function updateLeadCount() {
    document.getElementById('leadCount').textContent = leads.length;
}

// Update process button state
function updateProcessButton() {
    const processBtn = document.getElementById('processBtn');
    processBtn.disabled = leads.length === 0;
}

// Clear form
function clearForm() {
    document.getElementById('leadForm').reset();
}

// Clear all leads
function clearLeads() {
    if (leads.length === 0) return;
    
    if (confirm('Are you sure you want to clear all leads?')) {
        leads = [];
        updateLeadCount();
        renderLeadsList();
        updateProcessButton();
        hideResults();
    }
}

// Load sample data
function loadSampleData() {
    fetch('/api/sample-data')
        .then(response => response.json())
        .then(data => {
            leads = data.leads.map((lead, index) => ({
                ...lead,
                id: Date.now() + index
            }));
            updateLeadCount();
            renderLeadsList();
            updateProcessButton();
            showAlert('Sample data loaded successfully!', 'success');
        })
        .catch(error => {
            console.error('Error loading sample data:', error);
            showAlert('Error loading sample data', 'danger');
        });
}

// Process leads
function processLeads() {
    if (leads.length === 0) {
        showAlert('No leads to process', 'warning');
        return;
    }
    
    // Show loading state
    showLoading();
    
    // Prepare data for API
    const leadsData = leads.map(lead => {
        const { id, ...leadData } = lead;
        return leadData;
    });
    
    // Call scoring API
    fetch('/api/score-leads', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ leads: leadsData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            processedLeads = data.leads;
            showResults(data);
        } else {
            throw new Error(data.error || 'Failed to process leads');
        }
    })
    .catch(error => {
        console.error('Error processing leads:', error);
        showAlert('Error processing leads: ' + error.message, 'danger');
        hideLoading();
    });
}

// Show loading state
function showLoading() {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('loadingSection').classList.remove('loading');
    document.getElementById('resultsSection').classList.add('results-section');
}

// Hide loading state
function hideLoading() {
    document.getElementById('loadingSection').classList.add('loading');
}

// Show results
function showResults(data) {
    hideLoading();
    document.getElementById('resultsSection').classList.remove('results-section');
    
    // Update summary metrics
    updateSummaryMetrics(data.summary);
    
    // Update results table
    updateResultsTable(data.leads);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

// Update summary metrics
function updateSummaryMetrics(summary) {
    const metricsContainer = document.getElementById('summaryMetrics');
    
    metricsContainer.innerHTML = `
        <div class="col-md-3">
            <div class="metric-card">
                <h3 class="text-primary">${summary.total_leads}</h3>
                <p class="mb-0">Total Leads</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <h3 class="text-success">${summary.high_priority}</h3>
                <p class="mb-0">High Priority</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <h3 class="text-warning">${summary.medium_priority}</h3>
                <p class="mb-0">Medium Priority</p>
            </div>
        </div>
        <div class="col-md-3">
            <div class="metric-card">
                <h3 class="text-danger">${summary.low_priority}</h3>
                <p class="mb-0">Low Priority</p>
            </div>
        </div>
    `;
}

// Update results table
function updateResultsTable(leads) {
    const tableBody = document.getElementById('resultsTable');
    
    tableBody.innerHTML = leads.map(lead => {
        const priorityClass = `priority-${lead.priority_level.toLowerCase()}`;
        const priorityBadge = getPriorityBadge(lead.priority_level);
        const scoreColor = getScoreColor(lead.lead_score);
        const dataQuality = lead.data_quality_score || 'N/A';
        
        return `
            <tr>
                <td><span class="badge ${priorityBadge}">${lead.priority_level}</span></td>
                <td>
                    <strong>${lead.company_name}</strong>
                    ${lead.website ? `<br><small class="text-muted">${lead.website}</small>` : ''}
                </td>
                <td>
                    ${lead.contact_name}<br>
                    <small class="text-muted">${lead.email}</small>
                </td>
                <td>${lead.industry}</td>
                <td>
                    <span class="badge ${scoreColor}">${lead.lead_score}/100</span>
                </td>
                <td>
                    <div class="progress" style="height: 20px;">
                        <div class="progress-bar" role="progressbar" style="width: ${dataQuality}%">
                            ${dataQuality}%
                        </div>
                    </div>
                </td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="showLeadDetails('${lead.company_name}')">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Get priority badge class
function getPriorityBadge(priority) {
    switch(priority) {
        case 'High': return 'bg-success';
        case 'Medium': return 'bg-warning';
        case 'Low': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

// Get score color class
function getScoreColor(score) {
    if (score >= 80) return 'bg-success';
    if (score >= 60) return 'bg-warning';
    return 'bg-danger';
}

// Show lead details modal
function showLeadDetails(companyName) {
    const lead = processedLeads.find(l => l.company_name === companyName);
    if (!lead) return;
    
    // Create modal content
    const modalContent = `
        <div class="modal fade" id="leadDetailsModal" tabindex="-1">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Lead Details - ${lead.company_name}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Company Information</h6>
                                <p><strong>Name:</strong> ${lead.company_name}</p>
                                <p><strong>Industry:</strong> ${lead.industry}</p>
                                <p><strong>Size:</strong> ${lead.company_size || 'Not specified'}</p>
                                <p><strong>Revenue:</strong> ${lead.revenue || 'Not specified'}</p>
                                ${lead.website ? `<p><strong>Website:</strong> <a href="${lead.website}" target="_blank">${lead.website}</a></p>` : ''}
                            </div>
                            <div class="col-md-6">
                                <h6>Contact Information</h6>
                                <p><strong>Name:</strong> ${lead.contact_name}</p>
                                <p><strong>Email:</strong> ${lead.email}</p>
                                <p><strong>Phone:</strong> ${lead.phone}</p>
                                ${lead.linkedin ? `<p><strong>LinkedIn:</strong> <a href="${lead.linkedin}" target="_blank">View Profile</a></p>` : ''}
                            </div>
                        </div>
                        <hr>
                        <div class="row">
                            <div class="col-md-6">
                                <h6>Scoring Breakdown</h6>
                                <p><strong>Total Score:</strong> ${lead.lead_score}/100</p>
                                <p><strong>Company Score:</strong> ${lead.score_breakdown.company}/100</p>
                                <p><strong>Contact Score:</strong> ${lead.score_breakdown.contact}/100</p>
                                <p><strong>Completeness:</strong> ${lead.score_breakdown.completeness}/100</p>
                                <p><strong>Engagement:</strong> ${lead.score_breakdown.engagement}/100</p>
                            </div>
                            <div class="col-md-6">
                                <h6>Recommendations</h6>
                                <ul class="list-unstyled">
                                    ${lead.recommendations.map(rec => `<li><i class="fas fa-lightbulb text-warning me-2"></i>${rec}</li>`).join('')}
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Remove existing modal if any
    const existingModal = document.getElementById('leadDetailsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Add modal to page
    document.body.insertAdjacentHTML('beforeend', modalContent);
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('leadDetailsModal'));
    modal.show();
}

// Export results to CSV
function exportResults() {
    if (processedLeads.length === 0) {
        showAlert('No results to export', 'warning');
        return;
    }
    
    // Prepare data for export
    const exportData = processedLeads.map(lead => ({
        'Company Name': lead.company_name,
        'Contact Name': lead.contact_name,
        'Email': lead.email,
        'Phone': lead.phone,
        'Industry': lead.industry,
        'Company Size': lead.company_size || '',
        'Revenue': lead.revenue || '',
        'Website': lead.website || '',
        'LinkedIn': lead.linkedin || '',
        'Lead Score': lead.lead_score,
        'Priority Level': lead.priority_level,
        'Data Quality Score': lead.data_quality_score || ''
    }));
    
    // Call export API
    fetch('/api/export', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ leads: exportData })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Export failed');
    })
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `enhanced_leads_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showAlert('Results exported successfully!', 'success');
    })
    .catch(error => {
        console.error('Export error:', error);
        showAlert('Error exporting results', 'danger');
    });
}

// Hide results section
function hideResults() {
    document.getElementById('resultsSection').classList.add('results-section');
    processedLeads = [];
}

// Scroll to upload section
function scrollToUpload() {
    document.getElementById('uploadSection').scrollIntoView({ behavior: 'smooth' });
}

// Add CSV upload input
function addCsvUploadInput() {
    // Create hidden file input
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '.csv';
    fileInput.style.display = 'none';
    fileInput.id = 'csvFileInput';
    fileInput.addEventListener('change', handleCsvFileSelect);
    
    document.body.appendChild(fileInput);
}

// Handle CSV upload button click
function handleCsvUpload() {
    const fileInput = document.getElementById('csvFileInput');
    if (fileInput) {
        fileInput.click();
    }
}

// Handle CSV file selection
function handleCsvFileSelect(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.toLowerCase().endsWith('.csv')) {
        showAlert('Please select a CSV file', 'warning');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const csvData = e.target.result;
            const csvLeads = parseCsvData(csvData);
            
            if (csvLeads.length === 0) {
                showAlert('No valid leads found in CSV file', 'warning');
                return;
            }
            
            // Add leads to the list
            csvLeads.forEach((lead, index) => {
                lead.id = Date.now() + index;
                leads.push(lead);
            });
            
            updateLeadCount();
            renderLeadsList();
            updateProcessButton();
            showAlert(`Successfully loaded ${csvLeads.length} leads from CSV`, 'success');
            
            // Scroll to upload section
            scrollToUpload();
            
        } catch (error) {
            console.error('Error parsing CSV:', error);
            showAlert('Error parsing CSV file. Please check the format.', 'danger');
        }
    };
    
    reader.readAsText(file);
}

// Parse CSV data
function parseCsvData(csvText) {
    const lines = csvText.split('\n').filter(line => line.trim());
    if (lines.length < 2) return [];
    
    // Get headers
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    
    // Map common column names
    const columnMap = {
        'company_name': ['company_name', 'company', 'company name', 'business name'],
        'contact_name': ['contact_name', 'contact name', 'name', 'contact', 'full name'],
        'email': ['email', 'email address', 'e-mail'],
        'phone': ['phone', 'phone number', 'telephone', 'mobile'],
        'industry': ['industry', 'sector', 'business type'],
        'company_size': ['company_size', 'company size', 'size', 'employees'],
        'revenue': ['revenue', 'annual revenue', 'revenue range'],
        'website': ['website', 'web', 'url', 'company website'],
        'linkedin': ['linkedin', 'linkedin profile', 'linkedin url']
    };
    
    // Find column indices
    const columnIndices = {};
    Object.keys(columnMap).forEach(key => {
        const possibleNames = columnMap[key];
        for (let i = 0; i < headers.length; i++) {
            if (possibleNames.some(name => headers[i].toLowerCase().includes(name.toLowerCase()))) {
                columnIndices[key] = i;
                break;
            }
        }
    });
    
    // Parse data rows
    const leads = [];
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',').map(v => v.trim().replace(/"/g, ''));
        
        const lead = {};
        Object.keys(columnIndices).forEach(key => {
            const index = columnIndices[key];
            if (index !== undefined && values[index]) {
                lead[key] = values[index];
            }
        });
        
        // Only add if we have minimum required fields
        if (lead.company_name && lead.contact_name && lead.email) {
            leads.push(lead);
        }
    }
    
    return leads;
}

// Show alert message
function showAlert(message, type) {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertContainer);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}
