document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = chatInput.value.trim();
        if (!question) return;

        displayUserMessage(question);
        chatInput.value = '';
        displayLoadingMessage();

        try {
            const response = await fetch('http://127.0.0.1:5000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question }),
            });

            removeLoadingMessage();

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`HTTP error! status: ${response.status}, body: ${errorText}`);
            }

            const data = await response.json();
            displayBotMessage(data);
        } catch (error) {
            console.error('Error fetching data:', error);
            removeLoadingMessage();
            displayErrorMessage(`Sorry, something went wrong. Please try again. Error: ${error.message}`);
        }
    });

    function displayUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function displayBotMessage(data) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';

        const answer = marked.parse(data.answer);
        const sources = data.sources.map((source, index) => {
            const sourceId = `source-${Date.now()}-${index}`;
            return `
                <a href="#" class="source-link" data-target="${sourceId}">Source ${index + 1}: ${source.metadata.source} (Page ${source.metadata.page})</a>
                <div id="${sourceId}" class="source-content">${source.content}</div>
            `;
        }).join('');

        messageElement.innerHTML = `<div>${answer}</div><div class="sources"><h4>Sources:</h4>${sources}</div>`;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        // Add click listeners to source links
        messageElement.querySelectorAll('.source-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = e.target.getAttribute('data-target');
                const content = document.getElementById(targetId);
                if (content) {
                    content.style.display = content.style.display === 'block' ? 'none' : 'block';
                }
            });
        });
    }

    function displayErrorMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function displayLoadingMessage() {
        const loadingElement = document.createElement('div');
        loadingElement.className = 'message bot-message loading';
        loadingElement.innerHTML = `<p>Loading...</p>`;
        chatWindow.appendChild(loadingElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    function removeLoadingMessage() {
        const loadingElement = chatWindow.querySelector('.loading');
        if (loadingElement) {
            loadingElement.remove();
        }
    }
});
