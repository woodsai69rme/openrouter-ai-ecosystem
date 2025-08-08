"""
Basic application tests
"""
import unittest
from app import create_app
from app.core.config import Config

class TestApp(unittest.TestCase):
    """Test Flask application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = create_app(Config)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up"""
        self.app_context.pop()
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')
    
    def test_landing_page(self):
        """Test landing page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'OpenRouter AI Agents', response.data)
    
    def test_api_status(self):
        """Test API status endpoint"""
        response = self.client.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('agents', data)
        self.assertEqual(data['cost'], 0.00)

if __name__ == '__main__':
    unittest.main()