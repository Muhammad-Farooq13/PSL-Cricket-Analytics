# 🏏 PSL Data Science Project

A comprehensive machine learning project for analyzing the Pakistan Super League (PSL) Complete Dataset (2016-2024). This project implements MLOps best practices and provides a production-ready Flask API for model deployment.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Dataset Description](#dataset-description)
- [Project Structure](#project-structure)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Data Exploration](#data-exploration)
  - [Model Training](#model-training)
  - [API Deployment](#api-deployment)
  - [Docker Deployment](#docker-deployment)
- [MLOps Pipeline](#mlops-pipeline)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Project Overview

This project provides a complete end-to-end machine learning solution for the PSL dataset, including:

- **Exploratory Data Analysis (EDA)**: Comprehensive data exploration and visualization
- **Data Preprocessing**: Automated data cleaning and transformation
- **Feature Engineering**: Advanced feature creation and selection
- **Model Development**: Multiple ML algorithms with hyperparameter tuning
- **Model Deployment**: Production-ready Flask API with Docker support
- **MLOps Integration**: Automated training pipeline with validation
- **Testing**: Comprehensive unit tests for all components

### 🎓 Methodology

The project follows industry best practices:
1. **Data-Centric Approach**: Focus on data quality and feature engineering
2. **Modular Design**: Reusable components for each stage of the pipeline
3. **Version Control**: Git-based workflow for reproducibility
4. **Automated Testing**: Comprehensive test coverage
5. **Containerization**: Docker-based deployment for consistency
6. **API-First**: RESTful API for easy integration

## 📊 Dataset Description

**Dataset**: PSL Complete Dataset (2016-2024)

**Source**: Located in `data/raw/Psl_Complete_Dataset(2016-2024).csv`

**Description**: The dataset contains comprehensive statistics from the Pakistan Super League spanning from 2016 to 2024, including match details, player performances, team statistics, and more.

### Preprocessing Steps

1. **Missing Value Handling**: Multiple strategies (drop, mean, median, mode)
2. **Duplicate Removal**: Automatic detection and removal
3. **Feature Scaling**: StandardScaler for numerical features
4. **Encoding**: Label encoding and one-hot encoding for categorical variables
5. **Feature Engineering**: Date-based features, aggregations, interactions

## 📁 Project Structure

```
psl/
├── data/
│   ├── raw/                        # Original dataset
│   │   └── Psl_Complete_Dataset(2016-2024).csv
│   └── processed/                  # Processed datasets
│
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   └── 02_model_development.ipynb
│
├── src/
│   ├── data/
│   │   ├── load_data.py           # Data loading utilities
│   │   └── preprocess.py          # Data preprocessing
│   ├── features/
│   │   └── build_features.py      # Feature engineering
│   ├── models/
│   │   ├── train_model.py         # Model training
│   │   └── predict_model.py       # Model prediction
│   ├── visualization/
│   │   └── visualize.py           # Visualization utilities
│   └── utils/
│       ├── logger.py              # Logging configuration
│       ├── config.py              # Configuration management
│       └── helpers.py             # Helper functions
│
├── tests/
│   ├── test_data_loading.py
│   ├── test_preprocessing.py
│   ├── test_models.py
│   └── test_flask_app.py
│
├── models/                         # Saved models
├── logs/                          # Application logs
├── config/                        # Configuration files
├── reports/                       # Generated reports and figures
│
├── flask_app.py                   # Flask API application
├── mlops_pipeline.py              # MLOps automation pipeline
├── Dockerfile                     # Docker configuration
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## ✨ Features

### Data Processing
- ✅ Automated data loading and validation
- ✅ Multiple missing value handling strategies
- ✅ Duplicate detection and removal
- ✅ Feature scaling and normalization
- ✅ Categorical encoding (Label, One-Hot)

### Feature Engineering
- ✅ DateTime feature extraction
- ✅ Aggregation features
- ✅ Interaction features
- ✅ Polynomial features
- ✅ Binning features

### Model Development
- ✅ Multiple algorithms (Random Forest, Gradient Boosting, Logistic Regression)
- ✅ Hyperparameter tuning with GridSearchCV
- ✅ Cross-validation
- ✅ Feature importance analysis
- ✅ Comprehensive model evaluation

### Deployment
- ✅ RESTful API with Flask
- ✅ Single and batch prediction endpoints
- ✅ Model versioning
- ✅ Docker containerization
- ✅ Health check endpoints

### MLOps
- ✅ Automated training pipeline
- ✅ Model validation and thresholds
- ✅ Experiment tracking
- ✅ Logging and monitoring
- ✅ CI/CD ready

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Docker and Docker Compose

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/psl-project.git
cd psl-project
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install the package in development mode**
```bash
pip install -e .
```

## ⚡ Quick Start

### 1. Explore the Data

Open the Jupyter notebook for exploratory data analysis:

```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

### 2. Train a Model

Run the MLOps pipeline to train a model:

```bash
python mlops_pipeline.py
```

Or use the Jupyter notebook:

```bash
jupyter notebook notebooks/02_model_development.ipynb
```

### 3. Start the API

Launch the Flask API server:

```bash
python flask_app.py
```

The API will be available at `http://localhost:5000`

## 📖 Usage

### Data Exploration

```python
from src.data.load_data import DataLoader
from src.visualization.visualize import DataVisualizer

# Load data
loader = DataLoader(data_path='data/raw')
df = loader.load_psl_dataset()

# Create visualizations
visualizer = DataVisualizer(output_dir='reports/figures')
visualizer.plot_distribution(df, numerical_columns)
visualizer.plot_correlation_matrix(df)
```

### Model Training

```python
from src.models.train_model import ModelTrainer

# Initialize trainer
trainer = ModelTrainer(model_type='random_forest', random_state=42)

# Split data
X_train, X_test, y_train, y_test = trainer.split_data(X, y, test_size=0.2)

# Train model
trainer.train(X_train, y_train)

# Evaluate
metrics = trainer.evaluate(X_test, y_test)
print(f"Accuracy: {metrics['accuracy']:.4f}")

# Save model
trainer.save_model('psl_model.pkl', model_path='models')
```

### Making Predictions

```python
from src.models.predict_model import ModelPredictor

# Load model
predictor = ModelPredictor(model_path='models')
predictor.load_model('psl_model.pkl')

# Make prediction
features = {'feature1': 1.0, 'feature2': 2.0, 'feature3': 3.0}
result = predictor.predict_single(features)
print(f"Prediction: {result}")
```

### API Deployment

#### Local Deployment

```bash
python flask_app.py
```

#### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 flask_app:app
```

### Docker Deployment

#### Build and Run with Docker

```bash
# Build the image
docker build -t psl-project .

# Run the container
docker run -p 5000:5000 -v $(pwd)/models:/app/models psl-project
```

#### Using Docker Compose

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔄 MLOps Pipeline

The automated MLOps pipeline handles the entire training workflow:

```bash
python mlops_pipeline.py
```

**Pipeline Steps:**
1. Data loading and validation
2. Data preprocessing and cleaning
3. Feature engineering
4. Train/test split
5. Model training
6. Model evaluation
7. Validation against thresholds
8. Model saving (if validation passes)
9. Metrics logging

**Configuration**: Edit `config/pipeline_config.json` to customize the pipeline.

## 🧪 Testing

### Run All Tests

```bash
# Using pytest
pytest tests/ -v

# Using unittest
python -m unittest discover tests/

# Run specific test file
pytest tests/test_models.py -v

# With coverage report
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

- Data loading and preprocessing
- Feature engineering
- Model training and evaluation
- Flask API endpoints
- Utility functions

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "psl_model.pkl"
}
```

#### 2. Single Prediction
```http
POST /predict
Content-Type: application/json

{
  "features": {
    "feature1": 1.0,
    "feature2": 2.0,
    "feature3": 3.0
  }
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "prediction": 1,
    "confidence": 0.85,
    "probabilities": [0.15, 0.85],
    "model": "psl_model.pkl"
  }
}
```

#### 3. Batch Prediction
```http
POST /predict/batch
Content-Type: application/json

{
  "data": [
    {"feature1": 1.0, "feature2": 2.0, "feature3": 3.0},
    {"feature1": 1.5, "feature2": 2.5, "feature3": 3.5}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "predictions": [...],
  "count": 2
}
```

#### 4. Model Information
```http
GET /model/info
```

**Response:**
```json
{
  "model_name": "psl_model.pkl",
  "model_type": "RandomForestClassifier",
  "has_feature_importance": true
}
```

### API Examples

**Using cURL:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"feature1": 1.0, "feature2": 2.0}}'
```

**Using Python:**
```python
import requests

url = "http://localhost:5000/predict"
data = {"features": {"feature1": 1.0, "feature2": 2.0}}
response = requests.post(url, json=data)
print(response.json())
```

**Using JavaScript:**
```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    features: {feature1: 1.0, feature2: 2.0}
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🛠️ Development

### Code Style

This project uses:
- **Black** for code formatting
- **Flake8** for linting
- **Pylint** for code analysis

```bash
# Format code
black src/ tests/

# Run linter
flake8 src/ tests/

# Run pylint
pylint src/
```

### Project Configuration

Configuration files can be placed in the `config/` directory:
- `pipeline_config.json`: MLOps pipeline configuration
- Custom configuration files as needed

### Logging

Logs are automatically generated in the `logs/` directory:
- Application logs
- Training logs
- API request logs

## 📈 Model Performance

Document your model performance metrics here after training:

| Model | Accuracy | Precision | Recall | F1 Score |
|-------|----------|-----------|--------|----------|
| Random Forest | - | - | - | - |
| Gradient Boosting | - | - | - | - |
| Logistic Regression | - | - | - | - |

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Muhammad Farooq - [@Muhamma-Farooq-13](https://github.com/Muhamma-Farooq-13)

## 🙏 Acknowledgments

- Pakistan Super League for the dataset
- Scikit-learn for machine learning tools
- Flask for the web framework
- All contributors and supporters

## 📞 Contact

For questions or support, please contact:
- Email: mfarooqshafee333@gmail.com
- GitHub: [@Muhamma-Farooq-13](https://github.com/Muhamma-Farooq-13)
- GitHub Issues: [https://github.com/Muhamma-Farooq-13/psl-project/issues](https://github.com/Muhamma-Farooq-13/psl-project/issues)

## 🗺️ Roadmap

- [ ] Add more advanced ML algorithms
- [ ] Implement model monitoring dashboard
- [ ] Add A/B testing capabilities
- [ ] Integrate with cloud platforms (AWS, Azure, GCP)
- [ ] Add real-time prediction streaming
- [ ] Implement model explainability (SHAP, LIME)

---

**⭐ If you find this project useful, please consider giving it a star!**
