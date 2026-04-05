// Pentesting Intelligence Platform - Client Logic
class IntelligencePlatform {
    constructor() {
        this.apiBase = 'http://localhost:8000';
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkServerStatus();
        setInterval(() => this.checkServerStatus(), 30000); // Check every 30 seconds
    }

    bindEvents() {
        const searchBtn = document.getElementById('searchBtn');
        const analyzeBtn = document.getElementById('analyzeBtn');
        const queryInput = document.getElementById('queryInput');
        const topKSelect = document.getElementById('topKSelect');

        searchBtn.addEventListener('click', () => this.performSearch());
        analyzeBtn.addEventListener('click', () => this.performAnalysis());
        queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch();
            }
        });

        topKSelect.addEventListener('change', () => {
            if (this.lastQuery) {
                this.performSearch(this.lastQuery);
            }
        });
    }

    async checkServerStatus() {
        const statusIndicator = document.getElementById('statusIndicator');
        const statusIcon = statusIndicator.querySelector('i');
        const statusText = statusIndicator.querySelector('span');

        try {
            const response = await fetch(`${this.apiBase}/health`);
            if (response.ok) {
                statusIndicator.classList.remove('error');
                statusIndicator.classList.add('connected');
                statusText.textContent = 'System Online';
                statusIcon.style.color = 'var(--primary-blue)';
            } else {
                throw new Error('Server responded with error');
            }
        } catch (error) {
            statusIndicator.classList.remove('connected');
            statusIndicator.classList.add('error');
            statusText.textContent = 'Connection Failed';
            statusIcon.style.color = 'var(--accent-magenta)';
            console.error('Server status check failed:', error);
        }
    }

    async performSearch(query = null) {
        const queryInput = document.getElementById('queryInput');
        const searchQuery = query || queryInput.value.trim();

        if (!searchQuery) {
            this.showError('Please enter a search query');
            return;
        }

        this.lastQuery = searchQuery;
        this.showLoading('searchBtn', true);
        this.clearError();

        try {
            const topK = document.getElementById('topKSelect').value;
            const response = await fetch(`${this.apiBase}/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: searchQuery,
                    top_k: parseInt(topK)
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            this.displaySearchResults(data.results, searchQuery);
            this.showResultsSection();

        } catch (error) {
            console.error('Search failed:', error);
            this.showError(`Search failed: ${error.message}`);
        } finally {
            this.showLoading('searchBtn', false);
        }
    }

    async performAnalysis() {
        const queryInput = document.getElementById('queryInput');
        const query = queryInput.value.trim();

        if (!query) {
            this.showError('Please enter a query for analysis');
            return;
        }

        this.showLoading('analyzeBtn', true);
        this.clearError();

        const analysisStatus = document.getElementById('analysisStatus');
        const analysisResult = document.getElementById('analysisResult');

        analysisStatus.textContent = 'Processing analysis...';
        analysisResult.textContent = '';
        this.showAnalysisSection();

        try {
            const response = await fetch(`${this.apiBase}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query
                })
            });

            if (!response.ok) {
                if (response.status === 503) {
                    throw new Error('Ollama service is not available. Please ensure Ollama is running.');
                }
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            analysisStatus.textContent = 'Analysis complete';
            analysisResult.textContent = data.analysis || 'No analysis data received';

        } catch (error) {
            console.error('Analysis failed:', error);
            analysisStatus.textContent = 'Analysis failed';
            analysisResult.textContent = `Error: ${error.message}`;
            this.showError(`Analysis failed: ${error.message}`);
        } finally {
            this.showLoading('analyzeBtn', false);
        }
    }

    displaySearchResults(results, query) {
        const resultsContainer = document.getElementById('searchResults');

        if (!results || results.length === 0) {
            resultsContainer.innerHTML = `
                <div class="result-item">
                    <div class="result-title">No Results Found</div>
                    <div class="result-content">
                        No documents matched the query: "${query}"
                    </div>
                </div>
            `;
            return;
        }

        const resultsHtml = results.map(result => {
            const score = result.score ? (result.score * 100).toFixed(1) : 'N/A';
            const source = result.metadata?.source || 'Unknown';
            const content = this.truncateText(result.content || result.page_content || '', 300);

            return `
                <div class="result-item">
                    <div class="result-title">${this.escapeHtml(result.title || 'Untitled')}</div>
                    <div class="result-source">
                        <i class="fas fa-file-alt"></i> ${this.escapeHtml(source)}
                        <span class="result-score">Relevance: ${score}%</span>
                    </div>
                    <div class="result-content">${this.escapeHtml(content)}</div>
                </div>
            `;
        }).join('');

        resultsContainer.innerHTML = resultsHtml;
    }

    showResultsSection() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    showAnalysisSection() {
        const analysisSection = document.getElementById('analysisSection');
        analysisSection.style.display = 'block';
        analysisSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    showLoading(buttonId, show) {
        const button = document.getElementById(buttonId);
        const icon = button.querySelector('i');
        const text = button.querySelector('span');

        if (show) {
            button.disabled = true;
            icon.className = 'fas fa-spinner loading';
            if (text) text.textContent = buttonId === 'searchBtn' ? 'Searching...' : 'Analyzing...';
        } else {
            button.disabled = false;
            icon.className = buttonId === 'searchBtn' ? 'fas fa-search' : 'fas fa-brain';
            if (text) text.textContent = buttonId === 'searchBtn' ? '' : 'Analyze';
        }
    }

    showError(message) {
        const queryInput = document.getElementById('queryInput');
        queryInput.classList.add('error');

        let errorDiv = document.querySelector('.error-message');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'error-message';
            queryInput.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }

    clearError() {
        const queryInput = document.getElementById('queryInput');
        queryInput.classList.remove('error');

        const errorDiv = document.querySelector('.error-message');
        if (errorDiv) {
            errorDiv.remove();
        }
    }

    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Global functions for HTML onclick handlers
function setQuery(query) {
    document.getElementById('queryInput').value = query;
}

// Initialize the interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.platform = new IntelligencePlatform();
});