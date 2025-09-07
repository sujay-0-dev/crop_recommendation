"""
Configuration setting for Crop Recommendation API
"""
import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Model Setting
MODEL_CONFIG = {
    "model_name":"xgboost",
    "test_size":0.2,
    "random_state":42,
    "xgboost_params": {
        "random_state":42,
        "n_estimators":100,
        "learning_rate":0.1,
        "max_depth":6
    }
}

# API setting
API_CONFIG = {
    "title": "Crop Recommendation API",
    "description": "ML-powered API for crop recommendation based on soil and climate conditions",
    "version": "1.0.0",
    "host": "0.0.0.0",
    "port": 8000
}