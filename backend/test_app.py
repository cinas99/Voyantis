import unittest
from flask import json
from app import app 

class QueueAPITestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_post_message_to_queue(self):
        response = self.client.post('/api/test_queue', json={"message": "Hello, World!"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {"status": "Message added to queue"})

    def test_post_invalid_message(self):
        response = self.client.post('/api/test_queue', data="Not a JSON")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid JSON body"})

    def test_get_message_from_queue(self):
        # Add a message first
        self.client.post('/api/test_queue', json={"message": "Hello, World!"})
        
        # Retrieve the message
        response = self.client.get('/api/test_queue')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Hello, World!"})

    def test_get_message_from_empty_queue_with_timeout(self):
        response = self.client.get('/api/empty_queue?timeout=1000')  # 1 second timeout
        self.assertEqual(response.status_code, 204)  # No content

    def test_get_message_with_negative_timeout(self):
        response = self.client.get('/api/test_queue?timeout=-1000')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Timeout must be a positive integer"})

    def test_get_message_from_nonexistent_queue(self):
        response = self.client.get('/api/nonexistent_queue')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json(), {"error": "Queue 'nonexistent_queue' does not exist"})

    def test_list_all_queues(self):
        # Add messages to multiple queues
        self.client.post('/api/queue1', json={"message": "Message in Queue1"})
        self.client.post('/api/queue2', json={"message": "Message in Queue2"})
        
        response = self.client.get('/api/queues')
        self.assertEqual(response.status_code, 200)
        
        queues = response.get_json()
        self.assertIn('queue1', queues)
        self.assertIn('queue2', queues)
        self.assertEqual(queues['queue1'], 1)
        self.assertEqual(queues['queue2'], 1)

if __name__ == '__main__':
    unittest.main()
