// Main JavaScript file for the Traffic Analysis dashboard

document.addEventListener('DOMContentLoaded', function() {
    // Initialize UI components
    initializeUI();
    
    // Initialize chart data if on the dashboard page
    if (document.getElementById('trafficChart')) {
        initializeCharts();
    }
});

function initializeUI() {
    // Add event listeners for accordions
    const accordionButtons = document.querySelectorAll('.accordion-header');
    if (accordionButtons.length > 0) {
        accordionButtons.forEach(button => {
            button.addEventListener('click', function() {
                const content = this.nextElementSibling;
                content.classList.toggle('hidden');
                
                const icon = this.querySelector('svg');
                if (icon) {
                    icon.classList.toggle('transform');
                    icon.classList.toggle('rotate-180');
                }
            });
        });
    }
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

function initializeCharts() {
    // Only initialize charts if Chart.js is available
    if (typeof Chart === 'undefined') {
        console.warn('Chart.js not loaded');
        return;
    }
    
    // Sample chart initialization code for dashboard
    const trafficChartElement = document.getElementById('trafficChart');
    if (trafficChartElement) {
        const ctx = trafficChartElement.getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                datasets: [{
                    label: 'Traffic Volume',
                    data: [65, 59, 80, 81, 56, 55],
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    // Add more chart initializations as needed for other charts
}

// Show message to user
function showMessage(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('main .container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => alertDiv.remove(), 150);
    }, 5000);
}

// Update model report with metrics
function updateModelReport(metrics) {
    const reportContainer = document.getElementById('model-report');
    if (!reportContainer) return;

    // Update traffic model metrics
    if (metrics.traffic_model) {
        updateMetricCard('traffic-accuracy', metrics.traffic_model.accuracy);
        updateMetricCard('traffic-precision', metrics.traffic_model.precision);
        updateMetricCard('traffic-recall', metrics.traffic_model.recall);
        updateMetricCard('traffic-f1', metrics.traffic_model.f1_score);
    }

    // Update node model metrics
    if (metrics.node_model) {
        updateMetricCard('node-accuracy', metrics.node_model.accuracy);
        updateMetricCard('node-precision', metrics.node_model.precision);
        updateMetricCard('node-recall', metrics.node_model.recall);
        updateMetricCard('node-f1', metrics.node_model.f1_score);
    }

    // Update anomaly model metrics
    if (metrics.anomaly_model) {
        updateMetricCard('anomaly-auc', metrics.anomaly_model.auc_roc);
        updateMetricCard('anomaly-precision', metrics.anomaly_model.precision);
        updateMetricCard('anomaly-recall', metrics.anomaly_model.recall);
        updateMetricCard('anomaly-f1', metrics.anomaly_model.f1_score);
    }
}

// Update individual metric card
function updateMetricCard(id, value) {
    const card = document.getElementById(id);
    if (card) {
        const valueElement = card.querySelector('.metric-value');
        if (valueElement) {
            valueElement.textContent = (value * 100).toFixed(1) + '%';
        }
    }
}

// Update Prediction Results
function updatePredictionResults(prediction) {
    const resultsContainer = document.getElementById('predictionResults');
    if (resultsContainer) {
        resultsContainer.innerHTML = `
            <div class="card">
                <div class="card-header">
                    <h5 class="card-title mb-0">Prediction Results</h5>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="metric-card">
                                <h6>Traffic Type</h6>
                                <p>${prediction.traffic_type}</p>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="metric-card">
                                <h6>Anomaly Detection</h6>
                                <p>${prediction.is_anomaly ? 'Anomaly Detected' : 'Normal'}</p>
                            </div>
                        </div>
                        ${prediction.attack_type ? `
                        <div class="col-md-6">
                            <div class="metric-card">
                                <h6>Attack Type</h6>
                                <p>${prediction.attack_type}</p>
                            </div>
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
    }
}

// Update Model Metrics
function updateModelMetrics(metrics) {
    // Update Traffic Classification Metrics
    if (metrics.traffic) {
        document.getElementById('traffic-accuracy').textContent = metrics.traffic.accuracy;
        document.getElementById('traffic-precision').textContent = metrics.traffic.precision;
        document.getElementById('traffic-recall').textContent = metrics.traffic.recall;
        document.getElementById('traffic-f1').textContent = metrics.traffic.f1;
    }
    
    // Update Anomaly Detection Metrics
    if (metrics.anomaly) {
        document.getElementById('anomaly-accuracy').textContent = metrics.anomaly.accuracy;
        document.getElementById('anomaly-precision').textContent = metrics.anomaly.precision;
        document.getElementById('anomaly-recall').textContent = metrics.anomaly.recall;
        document.getElementById('anomaly-f1').textContent = metrics.anomaly.f1;
    }
    
    // Update Attack Classification Metrics
    if (metrics.attack) {
        document.getElementById('attack-accuracy').textContent = metrics.attack.accuracy;
        document.getElementById('attack-precision').textContent = metrics.attack.precision;
        document.getElementById('attack-recall').textContent = metrics.attack.recall;
        document.getElementById('attack-f1').textContent = metrics.attack.f1;
    }
}

// Form Field Validation
function validateFormField(input, validationRules) {
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    if (validationRules.required && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    if (validationRules.min && value < validationRules.min) {
        isValid = false;
        errorMessage = `Value must be at least ${validationRules.min}.`;
    }
    
    if (validationRules.max && value > validationRules.max) {
        isValid = false;
        errorMessage = `Value must be at most ${validationRules.max}.`;
    }
    
    if (validationRules.pattern && !validationRules.pattern.test(value)) {
        isValid = false;
        errorMessage = validationRules.errorMessage || 'Invalid format.';
    }
    
    // Update input state
    input.classList.toggle('is-invalid', !isValid);
    input.classList.toggle('is-valid', isValid);
    
    // Update error message
    let errorDiv = input.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.insertBefore(errorDiv, input.nextSibling);
    }
    errorDiv.textContent = errorMessage;
    
    return isValid;
}

// Initialize Tooltips
document.addEventListener('DOMContentLoaded', function() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Initialize Popovers
document.addEventListener('DOMContentLoaded', function() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const resultDiv = document.getElementById('analysis-result');
    
    try {
        // Show loading state
        resultDiv.innerHTML = '<div class="text-center p-4"><div class="spinner-border text-primary" role="status"></div><div class="mt-2">Analyzing data...</div></div>';
        resultDiv.classList.remove('hidden');
        
        const response = await fetch('/input_data', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Display results based on form type
        let resultHTML = '<div class="bg-white p-6 rounded-lg shadow-sm">';
        resultHTML += '<h3 class="text-xl font-bold mb-4">Analysis Results</h3>';
        
        if (data.traffic_classification) {
            resultHTML += `
                <div class="mb-4">
                    <p class="font-medium">Traffic Classification: <span class="text-blue-600">${data.traffic_classification}</span></p>
                    <p class="font-medium">Risk Level: <span class="text-blue-600">${data.risk_level}</span></p>
                </div>`;
        }
        
        if (data.node_category) {
            resultHTML += `
                <div class="mb-4">
                    <p class="font-medium">Node Category: <span class="text-green-600">${data.node_category}</span></p>
                    <p class="font-medium">Behavior Pattern: <span class="text-green-600">${data.behavior_pattern}</span></p>
                </div>`;
        }
        
        if (data.anomaly_status) {
            resultHTML += `
                <div class="mb-4">
                    <p class="font-medium">Anomaly Status: <span class="text-red-600">${data.anomaly_status}</span></p>
                    <p class="font-medium">Severity Level: <span class="text-red-600">${data.severity_level}</span></p>
                </div>`;
        }
        
        resultHTML += '</div>';
        resultDiv.innerHTML = resultHTML;
        
    } catch (error) {
        resultDiv.innerHTML = `
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
                <p class="font-bold">Error</p>
                <p>Failed to analyze data. Please try again.</p>
            </div>`;
    }
} 