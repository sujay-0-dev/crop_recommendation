"""
FastAPI application for Crop Recommendation System
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import traceback
from datetime import datetime
from typing import Dict, Any

from schemas import (
    CropPredictionRequest,
    CropPredictionResponse,
    BatchPredictionRequest,
    BatchPredictionResponse,
    HealthResponse,
    ModelInfoResponse
)
from model_training import ModelTrainer
from config import API_CONFIG, MODEL_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model instance
model_trainer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup for the FastAPI app"""
    global model_trainer
    
    # Startup
    logger.info("Starting Crop Recommendation API")
    try:
        model_trainer = ModelTrainer()
        model_trainer.load_model()
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        model_trainer = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down Crop Recommendation API")


# Initialize FastAPI app
app = FastAPI(
    title=API_CONFIG["title"],
    description=API_CONFIG["description"],
    version=API_CONFIG["version"],
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Crop Recommendation API",
        "version": API_CONFIG["version"],
        "status": "active"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_loaded = model_trainer is not None and model_trainer.model is not None
    
    return HealthResponse(
        status="healthy" if model_loaded else "unhealthy",
        message="Service is running" if model_loaded else "Model not loaded",
        model_loaded=model_loaded,
        timestamp=datetime.now().isoformat()
    )


@app.get("/model/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get information about the loaded model"""
    if model_trainer is None or model_trainer.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return ModelInfoResponse(
        model_name="XGBoost Classifier",
        model_version=API_CONFIG["version"],
        features=[
            "N", "P", "K", "temperature", "humidity", "ph", "rainfall"
        ],
        supported_crops=model_trainer.data_processor.get_all_crops(),
        accuracy=model_trainer.model_metrics.get('test_accuracy')
    )


@app.post("/predict", response_model=CropPredictionResponse)
async def predict_crop(request: CropPredictionRequest):
    """
    Predict the best crop based on soil and climate conditions
    
    - **N**: Nitrogen content in soil (0-200)
    - **P**: Phosphorus content in soil (0-200)
    - **K**: Potassium content in soil (0-250)
    - **temperature**: Temperature in Celsius (0-50)
    - **humidity**: Relative humidity percentage (0-100)
    - **ph**: pH value of soil (0-14)
    - **rainfall**: Rainfall in mm (0-400)
    """
    if model_trainer is None or model_trainer.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert request to dictionary
        input_data = request.dict()
        
        # Make prediction
        predicted_crop, confidence, all_probabilities = model_trainer.predict(input_data)
        
        return CropPredictionResponse(
            predicted_crop=predicted_crop,
            confidence=confidence,
            all_probabilities=all_probabilities
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse)
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict crops for multiple inputs
    
    Maximum 100 predictions per batch
    """
    if model_trainer is None or model_trainer.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(request.predictions) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 predictions per batch")
    
    try:
        # Convert requests to list of dictionaries
        input_batch = [req.dict() for req in request.predictions]
        
        # Make batch predictions
        results = model_trainer.batch_predict(input_batch)
        
        # Convert to response objects
        predictions = [CropPredictionResponse(**result) for result in results]
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_predictions=len(predictions)
        )
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/model/feature-importance")
async def get_feature_importance():
    """Get feature importance from the trained model"""
    if model_trainer is None or model_trainer.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        importance = model_trainer.get_feature_importance()
        # Sort by importance
        sorted_importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        return {"feature_importance": sorted_importance}
    except Exception as e:
        logger.error(f"Feature importance error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get feature importance: {str(e)}")


@app.post("/model/retrain")
async def retrain_model(background_tasks: BackgroundTasks, data_path: str = None):
    """
    Retrain the model (background task)
    
    This endpoint triggers model retraining in the background
    """
    if data_path is None:
        data_path = "data/Crop_recommendation.csv"  # Default path
    
    def retrain_task():
        try:
            global model_trainer
            logger.info("Starting model retraining")
            new_trainer = ModelTrainer()
            results = new_trainer.train_model(data_path)
            new_trainer.save_model()
            
            # Update global model
            model_trainer = new_trainer
            logger.info("Model retraining completed successfully")
            
        except Exception as e:
            logger.error(f"Model retraining failed: {e}")
    
    background_tasks.add_task(retrain_task)
    return {"message": "Model retraining started in background"}


# Error handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return HTTPException(status_code=500, detail="Internal server error")

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Cloud Run sets PORT
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,      
        log_level="info"
    )