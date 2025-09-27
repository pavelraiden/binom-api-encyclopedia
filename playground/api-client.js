
// Advanced API Client for Binom API Playground
class BinomAPIClient {
    constructor(apiKey, baseUrl = 'https://pierdun.com/public/api/v1') {
        this.apiKey = apiKey;
        this.baseUrl = baseUrl;
        this.requestHistory = [];
    }
    
    async makeRequest(method, endpoint, data = null) {
        const url = `${this.baseUrl}${endpoint}`;
        const startTime = Date.now();
        
        const options = {
            method: method,
            headers: {
                'api-key': this.apiKey,
                'Content-Type': 'application/json'
            }
        };
        
        if (data && method !== 'GET') {
            options.body = JSON.stringify(data);
        } else if (data && method === 'GET') {
            const params = new URLSearchParams(data);
            url += `?${params}`;
        }
        
        try {
            const response = await fetch(url, options);
            const responseTime = Date.now() - startTime;
            const responseData = await response.json();
            
            const requestRecord = {
                timestamp: new Date().toISOString(),
                method,
                endpoint,
                status: response.status,
                responseTime,
                success: response.ok,
                data: responseData
            };
            
            this.requestHistory.push(requestRecord);
            return requestRecord;
            
        } catch (error) {
            const requestRecord = {
                timestamp: new Date().toISOString(),
                method,
                endpoint,
                status: 0,
                responseTime: Date.now() - startTime,
                success: false,
                error: error.message
            };
            
            this.requestHistory.push(requestRecord);
            return requestRecord;
        }
    }
    
    getRequestHistory() {
        return this.requestHistory;
    }
    
    getEndpointStats(endpoint) {
        const endpointRequests = this.requestHistory.filter(r => r.endpoint === endpoint);
        if (endpointRequests.length === 0) return null;
        
        const successCount = endpointRequests.filter(r => r.success).length;
        const avgResponseTime = endpointRequests.reduce((sum, r) => sum + r.responseTime, 0) / endpointRequests.length;
        
        return {
            totalRequests: endpointRequests.length,
            successRate: (successCount / endpointRequests.length) * 100,
            avgResponseTime: Math.round(avgResponseTime),
            lastRequest: endpointRequests[endpointRequests.length - 1]
        };
    }
}

// Enhanced Playground UI
class PlaygroundUI {
    constructor() {
        this.apiClient = null;
        this.currentEndpoint = null;
    }
    
    init() {
        this.setupEventListeners();
        this.loadEndpointExamples();
    }
    
    setupEventListeners() {
        document.getElementById('api-key').addEventListener('input', (e) => {
            if (e.target.value) {
                this.apiClient = new BinomAPIClient(e.target.value);
            }
        });
        
        document.getElementById('endpoint').addEventListener('change', (e) => {
            this.currentEndpoint = e.target.value;
            this.updateEndpointInfo();
            this.loadExampleForEndpoint();
        });
        
        document.getElementById('send-request').addEventListener('click', () => {
            this.sendRequest();
        });
    }
    
    async sendRequest() {
        if (!this.apiClient || !this.currentEndpoint) {
            this.showError('Please select an endpoint and enter API key');
            return;
        }
        
        const [method, path] = this.currentEndpoint.split(' ');
        const requestBody = document.getElementById('request-body').value;
        
        let data = null;
        if (requestBody.trim()) {
            try {
                data = JSON.parse(requestBody);
            } catch (e) {
                this.showError('Invalid JSON in request body');
                return;
            }
        }
        
        this.showLoading(true);
        const result = await this.apiClient.makeRequest(method, path, data);
        this.showLoading(false);
        
        this.displayResult(result);
        this.updateEndpointStats();
    }
    
    displayResult(result) {
        const statusElement = document.getElementById('response-status');
        const bodyElement = document.getElementById('response-body');
        
        const statusClass = result.success ? 'status-success' : 'status-error';
        const statusText = result.success ? `✅ ${result.status} OK` : `❌ ${result.status} Error`;
        
        statusElement.innerHTML = `<span class="status-indicator ${statusClass}">${statusText}</span>`;
        statusElement.innerHTML += `<span class="response-time">${result.responseTime}ms</span>`;
        
        const responseContent = result.success ? 
            JSON.stringify(result.data, null, 2) : 
            JSON.stringify({error: result.error || 'Request failed'}, null, 2);
            
        bodyElement.innerHTML = `<pre>${responseContent}</pre>`;
    }
    
    updateEndpointStats() {
        if (!this.apiClient || !this.currentEndpoint) return;
        
        const [method, path] = this.currentEndpoint.split(' ');
        const stats = this.apiClient.getEndpointStats(path);
        
        if (stats) {
            const statsHtml = `
                <div class="endpoint-stats">
                    <h4>Endpoint Statistics</h4>
                    <p>Total Requests: ${stats.totalRequests}</p>
                    <p>Success Rate: ${stats.successRate.toFixed(1)}%</p>
                    <p>Avg Response Time: ${stats.avgResponseTime}ms</p>
                </div>
            `;
            
            document.getElementById('endpoint-info').innerHTML += statsHtml;
        }
    }
    
    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'block' : 'none';
    }
    
    showError(message) {
        const statusElement = document.getElementById('response-status');
        statusElement.innerHTML = `<span class="status-indicator status-error">❌ ${message}</span>`;
    }
}

// Initialize playground when page loads
document.addEventListener('DOMContentLoaded', () => {
    const playground = new PlaygroundUI();
    playground.init();
});
