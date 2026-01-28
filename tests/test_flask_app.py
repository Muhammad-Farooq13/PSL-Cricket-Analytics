"""
Unit tests for Flask application
"""

import unittest
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from flask_app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask application"""
    
    def setUp(self):
        """Setup test fixtures"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
    
    def test_home_route(self):
        """Test home route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PSL Model API', response.data)
    
    def test_health_route(self):
        """Test health check route"""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_predict_route_no_data(self):
        """Test predict route with no data"""
        response = self.client.post('/predict')
        self.assertEqual(response.status_code, 400)
    
    def test_predict_route_invalid_format(self):
        """Test predict route with invalid format"""
        response = self.client.post(
            '/predict',
            data=json.dumps({'invalid': 'data'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
    
    def test_model_info_route(self):
        """Test model info route"""
        response = self.client.get('/model/info')
        # Will return 503 if no model is loaded, which is expected
        self.assertIn(response.status_code, [200, 503])
    
    def test_invalid_route(self):
        """Test invalid route (404)"""
        response = self.client.get('/invalid_route')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
