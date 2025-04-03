from fastapi import APIRouter
from fastapi.responses import HTMLResponse

index_router = APIRouter()


@index_router.get("/", response_class=HTMLResponse)
async def magic():
    return HTMLResponse(
        status_code=200,
        content="""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hosts API Visualizer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            padding: 20px;
        }
        .tabs {
            display: flex;
            border-bottom: 1px solid #ddd;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background-color: #f1f1f1;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 5px 5px 0 0;
            margin-right: 5px;
            transition: all 0.3s;
        }
        .tab:hover {
            background-color: #e1e1e1;
        }
        .tab.active {
            background-color: #3498db;
            color: white;
            border-color: #3498db;
        }
        .tab-content {
            display: none;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
            background-color: white;
        }
        .tab-content.active {
            display: block;
        }
        .endpoint-form {
            margin-bottom: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
            border: 1px solid #eee;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #2980b9;
        }
        button:disabled {
            background-color: #95a5a6;
            cursor: not-allowed;
        }
        .response-container {
            margin-top: 20px;
        }
        .json-viewer {
            font-family: 'Courier New', Courier, monospace;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            max-height: 500px;
            overflow-y: auto;
        }
        .json-key {
            color: #d14;
        }
        .json-string {
            color: #090;
        }
        .json-number {
            color: #905;
        }
        .json-boolean {
            color: #00f;
        }
        .json-null {
            color: #808;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(0,0,0,.3);
            border-radius: 50%;
            border-top-color: #3498db;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .error {
            color: #e74c3c;
            background-color: #fadbd8;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
        }
        .collapsible {
            cursor: pointer;
            position: relative;
            padding-left: 15px;
        }
        .collapsible::before {
            content: '▼';
            position: absolute;
            left: 0;
            font-size: 0.8em;
        }
        .collapsible.collapsed::before {
            content: '▶';
        }
        .hidden {
            display: none;
        }
        .pagination {
            display: flex;
            justify-content: space-between;
            margin-top: 15px;
        }
        .page-info {
            align-self: center;
            font-weight: bold;
        }
        .json-item {
            margin-left: 20px;
        }
        .json-array-length {
            color: #666;
            font-style: italic;
        }
        .json-object-id {
            color: #905;
            font-weight: bold;
        }
        .json-object-header {
            font-weight: bold;
            margin: 5px 0;
        }
        .json-array-item {
            display: flex;
            margin-left: 20px;
        }
        .json-array-index {
            color: #666;
            margin-right: 10px;
        }
        .pre-unfolded {
            display: block !important;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hosts API Visualizer</h1>
        
        <div class="tabs">
            <div class="tab active" data-tab="details">Host Details</div>
            <div class="tab" data-tab="batch">All hosts</div>
            <div class="tab" data-tab="newest">Top verified hosts</div>
            <div class="tab" data-tab="oldest">Latest verified hosts</div>
            <div class="tab" data-tab="vuln-top">Most Vulnerable</div>
            <div class="tab" data-tab="vuln-bottom">Most invulnerable</div>
            <div class="tab" data-tab="vuln-newest">Recently vulnerability scanned</div>
            <div class="tab" data-tab="vuln-oldest">Old vulnerability scan</div>
            <div class="tab" data-tab="agent">By Agent</div>
        </div>
        
        <!-- Host Details Tab -->
        <div class="tab-content active" id="details">
            <div class="endpoint-form">
                <div class="form-group">
                    <label for="hostname">Hostname or External ID:</label>
                    <input type="text" id="hostname" placeholder="Enter hostname or external ID">
                </div>
                <button onclick="fetchHostDetails()">Fetch Host Details</button>
                <div class="response-container">
                    <div id="details-response" class="json-viewer"></div>
                </div>
            </div>
        </div>
        
        <!-- Batch Read Tab -->
        <div class="tab-content" id="batch">
            <div class="endpoint-form">
                <div class="form-group">
                    <label for="agent-name">Agent Name (optional):</label>
                    <input type="text" id="agent-name" placeholder="Filter by agent name">
                </div>
                <button onclick="fetchBatchHosts()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="batch-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="batch-prev" onclick="prevBatchPage()" disabled>Previous</button>
                        <span class="page-info" id="batch-page-info">Page 1</span>
                        <button id="batch-next" onclick="nextBatchPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Newest Audits Tab -->
        <div class="tab-content" id="newest">
            <div class="endpoint-form">
                <button onclick="fetchNewestAudits()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="newest-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="newest-prev" onclick="prevNewestPage()" disabled>Previous</button>
                        <span class="page-info" id="newest-page-info">Page 1</span>
                        <button id="newest-next" onclick="nextNewestPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Oldest Audits Tab -->
        <div class="tab-content" id="oldest">
            <div class="endpoint-form">
                <button onclick="fetchOldestAudits()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="oldest-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="oldest-prev" onclick="prevOldestPage()" disabled>Previous</button>
                        <span class="page-info" id="oldest-page-info">Page 1</span>
                        <button id="oldest-next" onclick="nextOldestPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Most Vulnerable Tab -->
        <div class="tab-content" id="vuln-top">
            <div class="endpoint-form">
                <button onclick="fetchVulnTop()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="vuln-top-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="vuln-top-prev" onclick="prevVulnTopPage()" disabled>Previous</button>
                        <span class="page-info" id="vuln-top-page-info">Page 1</span>
                        <button id="vuln-top-next" onclick="nextVulnTopPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Least Vulnerable Tab -->
        <div class="tab-content" id="vuln-bottom">
            <div class="endpoint-form">
                <button onclick="fetchVulnBottom()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="vuln-bottom-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="vuln-bottom-prev" onclick="prevVulnBottomPage()" disabled>Previous</button>
                        <span class="page-info" id="vuln-bottom-page-info">Page 1</span>
                        <button id="vuln-bottom-next" onclick="nextVulnBottomPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Newest Vuln Scans Tab -->
        <div class="tab-content" id="vuln-newest">
            <div class="endpoint-form">
                <button onclick="fetchVulnNewest()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="vuln-newest-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="vuln-newest-prev" onclick="prevVulnNewestPage()" disabled>Previous</button>
                        <span class="page-info" id="vuln-newest-page-info">Page 1</span>
                        <button id="vuln-newest-next" onclick="nextVulnNewestPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Oldest Vuln Scans Tab -->
        <div class="tab-content" id="vuln-oldest">
            <div class="endpoint-form">
                <button onclick="fetchVulnOldest()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="vuln-oldest-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="vuln-oldest-prev" onclick="prevVulnOldestPage()" disabled>Previous</button>
                        <span class="page-info" id="vuln-oldest-page-info">Page 1</span>
                        <button id="vuln-oldest-next" onclick="nextVulnOldestPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- By Agent Tab -->
        <div class="tab-content" id="agent">
            <div class="endpoint-form">
                <div class="form-group">
                    <label for="agent-name-filter">Agent Name:</label>
                    <input type="text" id="agent-name-filter" placeholder="Enter agent name" required>
                </div>
                <button onclick="fetchByAgent()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="agent-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="agent-prev" onclick="prevAgentPage()" disabled>Previous</button>
                        <span class="page-info" id="agent-page-info">Page 1</span>
                        <button id="agent-next" onclick="nextAgentPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- OS Grouped Tab -->
        <div class="tab-content" id="os-grouped">
            <div class="endpoint-form">
                <button onclick="fetchOsGrouped()">Fetch Hosts</button>
                <div class="response-container">
                    <div id="os-grouped-response" class="json-viewer"></div>
                    <div class="pagination">
                        <button id="os-grouped-prev" onclick="prevOsGroupedPage()" disabled>Previous</button>
                        <span class="page-info" id="os-grouped-page-info">Page 1</span>
                        <button id="os-grouped-next" onclick="nextOsGroupedPage()" disabled>Next</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Global variables for pagination
        const limit = 4;
        const paginationState = {
            batch: { page: 1, hasMore: false },
            newest: { page: 1, hasMore: false },
            oldest: { page: 1, hasMore: false },
            vulnTop: { page: 1, hasMore: false },
            vulnBottom: { page: 1, hasMore: false },
            vulnNewest: { page: 1, hasMore: false },
            vulnOldest: { page: 1, hasMore: false },
            agent: { page: 1, hasMore: false },
            osGrouped: { page: 1, hasMore: false }
        };

        // Tab switching
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', () => {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                tab.classList.add('active');
                document.getElementById(tab.dataset.tab).classList.add('active');
            });
        });

        // Helper function to make API calls
        async function fetchData(url, responseElementId, paginationKey) {
            const responseElement = document.getElementById(responseElementId);
            responseElement.innerHTML = '<div class="loading"></div> Loading...';
            
            try {
                const response = await fetch(url);
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.detail || 'Failed to fetch data');
                }
                
                // Update pagination state
                if (Array.isArray(data)) {
                    paginationState[paginationKey].hasMore = data.length === limit;
                    updatePaginationButtons(paginationKey);
                }
                
                responseElement.innerHTML = '';
                responseElement.appendChild(jsonToHTML(data));
            } catch (error) {
                responseElement.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                console.error('Fetch error:', error);
            }
        }

        // Update pagination buttons state
        function updatePaginationButtons(key) {
            const state = paginationState[key];
            const prevBtn = document.getElementById(`${key}-prev`);
            const nextBtn = document.getElementById(`${key}-next`);
            const pageInfo = document.getElementById(`${key}-page-info`);
            
            prevBtn.disabled = state.page <= 1;
            nextBtn.disabled = !state.hasMore;
            pageInfo.textContent = `Page ${state.page}`;
        }

        function jsonToHTML(data) {
            data = Object.assign({}, data.identity, data)
            const container = document.createElement('div');
            
            if (data === null) {
                const span = document.createElement('span');
                span.className = 'json-null';
                span.textContent = 'null';
                container.appendChild(span);
                return container;
            }
            
            if (Array.isArray(data)) {
                if (data.length === 0) {
                    container.textContent = '[]';
                    return container;
                }
                
                const header = document.createElement('div');
                header.className = 'json-object-header';
                header.textContent = `Array (${data.length})`;
                container.appendChild(header);
                
                data.forEach((item, index) => {
                    const itemContainer = document.createElement('div');
                    itemContainer.className = 'json-array-item';
                    
                    const indexSpan = document.createElement('span');
                    indexSpan.className = 'json-array-index';
                    indexSpan.textContent = `${index}:`;
                    itemContainer.appendChild(indexSpan);
                    
                    itemContainer.appendChild(jsonToHTML(item));
                    container.appendChild(itemContainer);
                });
                
                return container;
            }
            
            if (typeof data === 'object') {
                const keys = Object.keys(data);
                if (keys.length === 0) {
                    container.textContent = '{}';
                    return container;
                }
                
                // Special handling for _id field
                if (data._id && data._id.$oid) {
                    const idHeader = document.createElement('div');
                    idHeader.className = 'json-object-id';
                    idHeader.textContent = `_id: ObjectId('${data._id.$oid}')`;
                    container.appendChild(idHeader);
                }
                
                keys.forEach(key => {
                    if (key === '_id' && data._id.$oid) return;
                    
                    const keyDiv = document.createElement('div');
                    keyDiv.className = 'json-item';
                    
                    const keySpan = document.createElement('span');
                    keySpan.className = 'json-key';
                    keySpan.textContent = `${key}: `;
                    keyDiv.appendChild(keySpan);
                    
                    if (typeof data[key] === 'object' && data[key] !== null) {
                        // Create collapsible container for objects and arrays
                        const collapsible = document.createElement('span');
                        collapsible.className = 'collapsible';
                        
                        const content = document.createElement('span');
                        content.className = 'hidden';
                        
                        if (Array.isArray(data[key])) {
                            collapsible.textContent = `Array (${data[key].length})`;
                            content.appendChild(jsonToHTML(data[key]));
                        } else {
                            collapsible.textContent = 'Object';
                            content.appendChild(jsonToHTML(data[key]));
                        }
                        
                        
                        collapsible.addEventListener('click', function() {
                            this.classList.toggle('collapsed');
                            content.classList.toggle('hidden');
                        });
                        
                        keyDiv.appendChild(collapsible);
                        keyDiv.appendChild(content);
                    } else {
                        // Primitive values
                        const valueSpan = document.createElement('span');
                        if (typeof data[key] === 'string') {
                            valueSpan.className = 'json-string';
                            valueSpan.textContent = `"${data[key]}"`;
                        } else if (typeof data[key] === 'number') {
                            valueSpan.className = 'json-number';
                            valueSpan.textContent = data[key];
                        } else if (typeof data[key] === 'boolean') {
                            valueSpan.className = 'json-boolean';
                            valueSpan.textContent = data[key] ? 'true' : 'false';
                        } else {
                            valueSpan.textContent = data[key];
                        }
                        keyDiv.appendChild(valueSpan);
                    }
                    
                    container.appendChild(keyDiv);
                });
                
                return container;
            }
            
            // Primitive types
            const span = document.createElement('span');
            if (typeof data === 'string') {
                span.className = 'json-string';
                span.textContent = `"${data}"`;
            } else if (typeof data === 'number') {
                span.className = 'json-number';
                span.textContent = data;
            } else if (typeof data === 'boolean') {
                span.className = 'json-boolean';
                span.textContent = data ? 'true' : 'false';
            } else {
                span.textContent = data;
            }
            
            container.appendChild(span);
            responseElement.appendChild(document.createElement('br'))
            responseElement.appendChild(document.createElement('br'))
            return container;
        }

        // Host Details
        function fetchHostDetails() {
            const hostname = document.getElementById('hostname').value.trim();
            if (!hostname) {
                alert('Please enter a hostname or external ID');
                return;
            }
            
            fetchData(
                `/hosts/read/details/${encodeURIComponent(hostname)}/`,
                'details-response',
                'details'
            );
        }

        // Batch Hosts
        function fetchBatchHosts(page = 1) {
            const agentName = document.getElementById('agent-name').value.trim();
            const skip = (page - 1) * limit;
            let url = `/hosts/read/batch/?skip=${skip}&limit=${limit}`;
            
            if (agentName) {
                url += `&agent_name=${encodeURIComponent(agentName)}`;
            }
            
            paginationState.batch.page = page;
            fetchData(url, 'batch-response', 'batch');
        }

        function prevBatchPage() {
            if (paginationState.batch.page > 1) {
                fetchBatchHosts(paginationState.batch.page - 1);
            }
        }

        function nextBatchPage() {
            if (paginationState.batch.hasMore) {
                fetchBatchHosts(paginationState.batch.page + 1);
            }
        }

        // Newest Audits
        function fetchNewestAudits(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/newest/?skip=${skip}&limit=${limit}`;
            
            paginationState.newest.page = page;
            fetchData(url, 'newest-response', 'newest');
        }

        function prevNewestPage() {
            if (paginationState.newest.page > 1) {
                fetchNewestAudits(paginationState.newest.page - 1);
            }
        }

        function nextNewestPage() {
            if (paginationState.newest.hasMore) {
                fetchNewestAudits(paginationState.newest.page + 1);
            }
        }

        // Oldest Audits
        function fetchOldestAudits(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/oldest/?skip=${skip}&limit=${limit}`;
            
            paginationState.oldest.page = page;
            fetchData(url, 'oldest-response', 'oldest');
        }

        function prevOldestPage() {
            if (paginationState.oldest.page > 1) {
                fetchOldestAudits(paginationState.oldest.page - 1);
            }
        }

        function nextOldestPage() {
            if (paginationState.oldest.hasMore) {
                fetchOldestAudits(paginationState.oldest.page + 1);
            }
        }

        // Most Vulnerable
        function fetchVulnTop(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/vuln-count/most/?skip=${skip}&limit=${limit}`;
            
            paginationState.vulnTop.page = page;
            fetchData(url, 'vuln-top-response', 'vulnTop');
        }

        function prevVulnTopPage() {
            if (paginationState.vulnTop.page > 1) {
                fetchVulnTop(paginationState.vulnTop.page - 1);
            }
        }

        function nextVulnTopPage() {
            if (paginationState.vulnTop.hasMore) {
                fetchVulnTop(paginationState.vulnTop.page + 1);
            }
        }

        // Least Vulnerable
        function fetchVulnBottom(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/vuln-count/least/?skip=${skip}&limit=${limit}`;
            
            paginationState.vulnBottom.page = page;
            fetchData(url, 'vuln-bottom-response', 'vulnBottom');
        }

        function prevVulnBottomPage() {
            if (paginationState.vulnBottom.page > 1) {
                fetchVulnBottom(paginationState.vulnBottom.page - 1);
            }
        }

        function nextVulnBottomPage() {
            if (paginationState.vulnBottom.hasMore) {
                fetchVulnBottom(paginationState.vulnBottom.page + 1);
            }
        }

        // Newest Vuln Scans
        function fetchVulnNewest(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/vuln-date/newest/?skip=${skip}&limit=${limit}`;
            
            paginationState.vulnNewest.page = page;
            fetchData(url, 'vuln-newest-response', 'vulnNewest');
        }

        function prevVulnNewestPage() {
            if (paginationState.vulnNewest.page > 1) {
                fetchVulnNewest(paginationState.vulnNewest.page - 1);
            }
        }

        function nextVulnNewestPage() {
            if (paginationState.vulnNewest.hasMore) {
                fetchVulnNewest(paginationState.vulnNewest.page + 1);
            }
        }

        // Oldest Vuln Scans
        function fetchVulnOldest(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/vuln-date/oldest/?skip=${skip}&limit=${limit}`;
            
            paginationState.vulnOldest.page = page;
            fetchData(url, 'vuln-oldest-response', 'vulnOldest');
        }

        function prevVulnOldestPage() {
            if (paginationState.vulnOldest.page > 1) {
                fetchVulnOldest(paginationState.vulnOldest.page - 1);
            }
        }

        function nextVulnOldestPage() {
            if (paginationState.vulnOldest.hasMore) {
                fetchVulnOldest(paginationState.vulnOldest.page + 1);
            }
        }

        // By Agent
        function fetchByAgent(page = 1) {
            const agentName = document.getElementById('agent-name-filter').value.trim();
            if (!agentName) {
                alert('Please enter an agent name');
                return;
            }
            
            const skip = (page - 1) * limit;
            const url = `/hosts/read/agent/?agent_name=${encodeURIComponent(agentName)}&skip=${skip}&limit=${limit}`;
            
            paginationState.agent.page = page;
            fetchData(url, 'agent-response', 'agent');
        }

        function prevAgentPage() {
            if (paginationState.agent.page > 1) {
                fetchByAgent(paginationState.agent.page - 1);
            }
        }

        function nextAgentPage() {
            if (paginationState.agent.hasMore) {
                fetchByAgent(paginationState.agent.page + 1);
            }
        }

        // OS Grouped
        function fetchOsGrouped(page = 1) {
            const skip = (page - 1) * limit;
            const url = `/hosts/read/os/grouped/?skip=${skip}&limit=${limit}`;
            
            paginationState.osGrouped.page = page;
            fetchData(url, 'os-grouped-response', 'osGrouped');
        }

        function prevOsGroupedPage() {
            if (paginationState.osGrouped.page > 1) {
                fetchOsGrouped(paginationState.osGrouped.page - 1);
            }
        }

        function nextOsGroupedPage() {
            if (paginationState.osGrouped.hasMore) {
                fetchOsGrouped(paginationState.osGrouped.page + 1);
            }
        }
    </script>
</body>
</html>
""",
    )
