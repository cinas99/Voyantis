document.addEventListener('DOMContentLoaded', () => {
    const queuesList = document.getElementById('queues-list');
    const queueSelector = document.getElementById('queue-selector');
    const fetchButton = document.getElementById('fetch-button');
    const responseOutput = document.getElementById('response-output');
  
    async function loadQueues() {
      try {
        console.log('Fetching queues...');
        const response = await fetch('http://127.0.0.1:5000/api/queues');
        if (!response.ok) throw new Error(`Error: ${response.status} ${response.statusText}`);
        const queues = await response.json();
        console.log('Queues fetched:', queues);
    
        // Populate the queues list
        queuesList.innerHTML = '';
        queueSelector.innerHTML = '<option value="" disabled selected>Queue dropdown</option>';
        
        for (const [queueName, messageCount] of Object.entries(queues)) {
          const listItem = document.createElement('li');
          listItem.textContent = `${queueName}: ${messageCount} message(s)`;
          queuesList.appendChild(listItem);
    
          const option = document.createElement('option');
          option.value = queueName;
          option.textContent = queueName;
          queueSelector.appendChild(option);
        }
      } catch (error) {
        console.error('Failed to load queues:', error);
      }
    }
  
    async function fetchMessages() {
      const selectedQueue = queueSelector.value;
      if (!selectedQueue) {
        alert('Please select a queue.');
        return;
      }
    
      try {
        const apiUrl = `http://127.0.0.1:5000/api/${selectedQueue}`;
        console.log(`Fetching messages from: ${apiUrl}`); // Debug log
    
        const response = await fetch(apiUrl);
        if (response.status === 204) {
          responseOutput.textContent = 'No messages available.';
        } else if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        } else {
          const message = await response.json();
          responseOutput.textContent = JSON.stringify(message, null, 2);
        }
      } catch (error) {
        console.error('Failed to fetch messages:', error);
        responseOutput.textContent = 'Error fetching messages.';
      }
    }
  
    fetchButton.addEventListener('click', fetchMessages);
  
    loadQueues();
  });
  