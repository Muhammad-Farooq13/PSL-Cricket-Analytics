# Contributing to PSL Data Science Project

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment details (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Example use cases

### Pull Requests

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation as needed
7. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/psl-project.git
cd psl-project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .[dev]
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting
- Run linters before submitting

```bash
# Format code
black src/ tests/

# Run linters
flake8 src/ tests/
pylint src/
```

### Testing

All new code should include tests:

```bash
# Run tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov-report=html
```

### Documentation

- Update README.md for significant changes
- Add docstrings to new functions/classes
- Update API documentation for endpoint changes

## Questions?

Feel free to open an issue for any questions or clarifications.

Thank you for contributing! Feel free to reach out to Muhammad Farooq at mfarooqshafee333@gmail.com with any questions.
