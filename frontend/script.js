const API_BASE_URL = "http://localhost:5000/api";

async function fetchQueues() {
    try {
        const response = await fetch(`${API_BASE_URL}/queues`);
        const data = await response.json();

        const container = document.getElementById('queues');
        container.innerHTML = '';

        Object.keys(data).forEach(queueName => {
            const queueCard = document.createElement('div');
            queueCard.className = 'queue-card';
            queueCard.innerHTML = `
                <h2>${queueName}</h2>
                <p>Messages in queue: ${data[queueName]}</p>
                <button onclick="fetchMessage('${queueName}')">Go</button>
            `;
            container.appendChild(queueCard);
        });
    } catch (error) {
        console.error("Error fetching queues:", error);
        alert("Failed to load queues.");
    }
}

async function fetchMessage(queueName) {
    try {
        const response = await fetch(`${API_BASE_URL}/${queueName}?timeout=5000`);
        if (response.status === 204) {
            alert(`No messages available in ${queueName}.`);
        } else if (response.ok) {
            const message = await response.json();
            alert(`Message from ${queueName}: ${JSON.stringify(message)}`);
        } else {
            alert(`Failed to retrieve message from ${queueName}.`);
        }
    } catch (error) {
        console.error("Error fetching message:", error);
        alert("Failed to retrieve message.");
    }
}

fetchQueues();
