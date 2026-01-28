"""
Flask Application for PSL Model Deployment
Provides REST API endpoints for model predictions
"""

from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.models.predict_model import ModelPredictor
from src.utils.helpers import NumpyEncoder
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.json_encoder = NumpyEncoder

# Initialize model predictor
predictor = ModelPredictor(model_path='models')

# Load model on startup
MODEL_FILE = 'psl_model.pkl'
try:
    predictor.load_model(MODEL_FILE)
    logger.info(f"Model loaded successfully: {MODEL_FILE}")
except Exception as e:
    logger.warning(f"Could not load model: {str(e)}")
    logger.warning("Model endpoints will not work until a model is trained and saved")


# HTML template for home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PSL Model API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        h2 {
            color: #555;
            margin-top: 30px;
        }
        .endpoint {
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 15px 0;
        }
        .method {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 10px;
        }
        .get { background-color: #61affe; color: white; }
        .post { background-color: #49cc90; color: white; }
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f4f4f4;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .status {
            padding: 5px 10px;
            border-radius: 4px;
            display: inline-block;
            margin-top: 10px;
        }
        .success { background-color: #d4edda; color: #155724; }
        .warning { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 PSL Model API</h1>
        <p>Welcome to the PSL Machine Learning Model API. This API provides endpoints for making predictions using the trained model.</p>
        
        <div class="status {{ status_class }}">
            <strong>Model Status:</strong> {{ model_status }}
        </div>
        
        <h2>📋 Available Endpoints</h2>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/</strong>
            <p>Home page with API documentation</p>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <strong>/health</strong>
            <p>Health check endpoint - returns API status</p>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span>
            <strong>/predict</strong>
            <p>Make a single prediction</p>
            <pre><code>{
  "features": {
    "feature1": value1,
    "feature2": value2,
    ...
  }
}</code></pre>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span>
            <strong>/predict/batch</strong>
            <p>Make batch predictions</p>
            <pre><code>{
  "data": [
    {"feature1": value1, "feature2": value2, ...},
    {"feature1": value1, "feature2": value2, ...}
  ]
}</code></pre>
        </div>
        
        <h2>📖 Example Usage</h2>
        <p>Using cURL:</p>
        <pre><code>curl -X POST http://localhost:5000/predict \\
  -H "Content-Type: application/json" \\
  -d '{"features": {"feature1": 1.0, "feature2": 2.0}}'</code></pre>
        
        <p>Using Python:</p>
        <pre><code>import requests

url = "http://localhost:5000/predict"
data = {"features": {"feature1": 1.0, "feature2": 2.0}}
response = requests.post(url, json=data)
print(response.json())</code></pre>
    </div>
</body>
</html>
"""


@app.route('/')
def home():
    """Home page with API documentation"""
    model_loaded = predictor.model is not None
    return render_template_string(
        HOME_TEMPLATE,
        model_status="Loaded and Ready" if model_loaded else "Not Loaded - Train a model first",
        status_class="success" if model_loaded else "warning"
    )


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_loaded = predictor.model is not None
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_loaded,
        'model_name': predictor.model_name if model_loaded else None
    }), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Single prediction endpoint
    Expected JSON format:
    {
        "features": {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    }
    """
    try:
        # Check if model is loaded
        if predictor.model is None:
            return jsonify({
                'error': 'Model not loaded. Please train and save a model first.'
            }), 503
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({
                'error': 'Invalid request format. Expected JSON with "features" key.'
            }), 400
        
        features = data['features']
        
        # Make prediction
        result = predictor.predict_single(features)
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Batch prediction endpoint
    Expected JSON format:
    {
        "data": [
            {"feature1": value1, "feature2": value2, ...},
            {"feature1": value1, "feature2": value2, ...}
        ]
    }
    """
    try:
        # Check if model is loaded
        if predictor.model is None:
            return jsonify({
                'error': 'Model not loaded. Please train and save a model first.'
            }), 503
        
        # Get JSON data from request
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({
                'error': 'Invalid request format. Expected JSON with "data" key.'
            }), 400
        
        # Convert to DataFrame
        df = pd.DataFrame(data['data'])
        
        # Make predictions
        result_df = predictor.batch_predict(df)
        
        # Convert to JSON-serializable format
        result = result_df.to_dict('records')
        
        return jsonify({
            'success': True,
            'predictions': result,
            'count': len(result)
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/model/info', methods=['GET'])
def model_info():
    """Get information about the loaded model"""
    try:
        if predictor.model is None:
            return jsonify({
                'error': 'Model not loaded'
            }), 503
        
        info = {
            'model_name': predictor.model_name,
            'model_type': type(predictor.model).__name__
        }
        
        # Add feature importance if available
        if hasattr(predictor.model, 'feature_importances_'):
            info['has_feature_importance'] = True
        
        return jsonify(info), 200
        
    except Exception as e:
        logger.error(f"Model info error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
