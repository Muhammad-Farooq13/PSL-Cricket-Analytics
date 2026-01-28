"""
Setup script for PSL Data Science Project
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

setup(
    name='psl-project',
    version='1.0.0',
    description='PSL Complete Dataset Analysis and Machine Learning Project',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Muhammad Farooq',
    author_email='mfarooqshafee333@gmail.com',
    url='https://github.com/Muhamma-Farooq-13/psl-project',
    packages=find_packages(exclude=['tests', 'notebooks', 'docs']),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.21.0',
        'scikit-learn>=1.0.0',
        'Flask>=2.0.0',
        'matplotlib>=3.4.0',
        'seaborn>=0.11.0',
        'joblib>=1.0.0',
        'pyyaml>=5.4.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'pylint>=2.12.0',
            'jupyter>=1.0.0',
        ],
    },
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    entry_points={
        'console_scripts': [
            'psl-train=mlops_pipeline:main',
            'psl-serve=flask_app:main',
        ],
    },
)
