const API_BASE = 'http://127.0.0.1:8000/api/tasks';

document.getElementById('analyzeBtn').addEventListener('click', analyzeTasks);
document.getElementById('suggestBtn').addEventListener('click', getSuggestions);

async function analyzeTasks() {
    try {
        const input = document.getElementById('taskInput').value;
        console.log('Input:', input);
        
        const tasks = JSON.parse(input);
        console.log('Parsed tasks:', tasks);
        
        const requestBody = { tasks };
        console.log('Request body:', requestBody);
        
        console.log('Making POST request to:', `${API_BASE}/analyze/`);
        
        const response = await fetch(`${API_BASE}/analyze/`, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        console.log('Response status:', response.status);
        console.log('Response ok:', response.ok);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.error) {
            displayError('Server error: ' + data.error);
        } else {
            displayResults(data.tasks, 'Prioritized Tasks');
        }
    } catch (error) {
        console.error('Full error:', error);
        displayError('Error analyzing tasks: ' + error.message);
    }
}

async function getSuggestions() {
    try {
        const input = document.getElementById('taskInput').value;
        console.log('Input:', input);
        
        const tasks = JSON.parse(input);
        console.log('Parsed tasks:', tasks);
        
        console.log('Making POST request to:', `${API_BASE}/suggest/`);
        
        const response = await fetch(`${API_BASE}/suggest/`, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ tasks })
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.error) {
            displayError('Server error: ' + data.error);
        } else {
            displaySuggestions(data.suggestions);
        }
    } catch (error) {
        console.error('Full error:', error);
        displayError('Error getting suggestions: ' + error.message);
    }
}

function displayResults(tasks, title) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<h3>${title}</h3>`;
    
    tasks.forEach(task => {
        const card = createTaskCard(task);
        resultsDiv.appendChild(card);
    });
}

function displaySuggestions(suggestions) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '<h3>Top 3 Suggestions</h3>';
    
    suggestions.forEach((suggestion, index) => {
        const card = createTaskCard(suggestion.task, suggestion.explanation, index + 1);
        resultsDiv.appendChild(card);
    });
}

function createTaskCard(task, explanation = '', rank = null) {
    const card = document.createElement('div');
    card.className = 'task-card';
    
    // Priority styling
    if (task.score >= 100) card.classList.add('high-priority');
    else if (task.score >= 50) card.classList.add('medium-priority');
    else card.classList.add('low-priority');
    
    card.innerHTML = `
        <div class="task-title">${rank ? `#${rank} ` : ''}${task.title}</div>
        <div class="task-details">
            Due: ${task.due_date} | Importance: ${task.importance}/10 | 
            Hours: ${task.estimated_hours} | Score: ${task.score}
            ${explanation ? `<br><strong>${explanation}</strong>` : ''}
        </div>
    `;
    
    return card;
}

function displayError(message) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = `<div class="error">${message}</div>`;
}