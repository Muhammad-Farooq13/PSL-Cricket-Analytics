# PSL Project - Quick Start Guide

## Getting Started in 5 Minutes

This guide will help you get the PSL Data Science Project up and running quickly.

### Step 1: Install Dependencies (1 minute)

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install requirements
pip install -r requirements.txt
```

### Step 2: Explore the Data (2 minutes)

```bash
# Launch Jupyter notebook
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

Run the cells to see:
- Dataset overview
- Missing values analysis
- Data distributions
- Correlation analysis

### Step 3: Train a Model (1 minute)

Option A - Using Jupyter Notebook:
```bash
jupyter notebook notebooks/02_model_development.ipynb
```

Option B - Using MLOps Pipeline:
```bash
python mlops_pipeline.py
```

Note: You'll need to specify the target column in the code before training.

### Step 4: Start the API (1 minute)

```bash
python flask_app.py
```

Visit: http://localhost:5000

### Making Your First Prediction

Once a model is trained, make a prediction:

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d "{\"features\": {\"feature1\": 1.0, \"feature2\": 2.0}}"
```

## What's Next?

### Customize the Pipeline

1. Edit `config/pipeline_config.json` to adjust:
   - Data preprocessing parameters
   - Model selection
   - Validation thresholds

2. Modify feature engineering in `src/features/build_features.py`

3. Add custom models in `src/models/train_model.py`

### Deploy with Docker

```bash
# Build image
docker build -t psl-project .

# Run container
docker run -p 5000:5000 psl-project

# Or use Docker Compose
docker-compose up -d
```

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_models.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## Common Issues

### Issue: "Target column not found"
**Solution**: Update the `target_column` variable in the training scripts with your actual target column name from the dataset.

### Issue: "Model not loaded" when using API
**Solution**: Train a model first using the MLOps pipeline or notebook, then restart the Flask app.

### Issue: Import errors
**Solution**: Make sure you're in the project root directory and the virtual environment is activated.

## Project Structure Overview

```
psl/
├── data/               # Dataset storage
├── notebooks/          # Jupyter notebooks
├── src/               # Source code
│   ├── data/          # Data processing
│   ├── features/      # Feature engineering
│   ├── models/        # Model training/prediction
│   ├── visualization/ # Plotting utilities
│   └── utils/         # Helper functions
├── tests/             # Unit tests
├── models/            # Saved models
├── flask_app.py       # API server
└── mlops_pipeline.py  # Training pipeline
```

## Helpful Commands

```bash
# View dataset info
python -c "from src.data.load_data import DataLoader; loader = DataLoader(); df = loader.load_psl_dataset(); print(df.info())"

# Check model performance
python -c "import json; print(json.load(open('reports/metrics_*.json')))"

# Test API health
curl http://localhost:5000/health

# Format code
black src/ tests/

# Run linters
flake8 src/ tests/
```

## Need Help?

- 📖 Check the [README.md](README.md) for detailed documentation
- 🐛 Report issues on GitHub
- 💬 Contact: mfarooqshafee333@gmail.com
- 🔗 GitHub: [@Muhamma-Farooq-13](https://github.com/Muhamma-Farooq-13)

Happy coding! 🚀
