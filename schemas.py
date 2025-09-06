"""
Pydantic schemas for request and response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator


class CropPredictionRequest(BaseModel):
    """Request schema for crop prediction"""
    
    N: float = Field(..., ge=0, le=200, description="Nitrogen content in soil (0-200)")
    P: float = Field(..., ge=0, le=200, description="Phosphorus content in soil (0-200)")
    K: float = Field(..., ge=0, le=250, description="Potassium content in soil (0-250)")
    temperature: float = Field(..., ge=0, le=50, description="Temperature in Celsius (0-50)")
    humidity: float = Field(..., ge=0, le=100, description="Relative humidity percentage (0-100)")
    ph: float = Field(..., ge=0, le=14, description="pH value of soil (0-14)")
    rainfall: float = Field(..., ge=0, le=400, description="Rainfall in mm (0-400)")
    
    class Config:
        schema_extra = {
            "example": {
                "N": 90,
                "P": 42,
                "K": 43,
                "temperature": 20.87,
                "humidity": 82.0,
                "ph": 6.5,
                "rainfall": 202.9
            }
        }


class CropPredictionResponse(BaseModel):
    """Response schema for crop prediction"""
    
    predicted_crop: str = Field(..., description="Recommended crop")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence (0-1)")
    all_probabilities: dict = Field(..., description="Probabilities for all crops")
    
    class Config:
        schema_extra = {
            "example": {
                "predicted_crop": "rice",
                "confidence": 0.95,
                "all_probabilities": {
                    "rice": 0.95,
                    "wheat": 0.03,
                    "maize": 0.02
                }
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request schema for batch predictions"""
    
    predictions: List[CropPredictionRequest] = Field(
        ..., 
        min_items=1, 
        max_items=100,
        description="List of crop prediction requests (max 100)"
    )


class BatchPredictionResponse(BaseModel):
    """Response schema for batch predictions"""
    
    predictions: List[CropPredictionResponse]
    total_predictions: int
    
    
class HealthResponse(BaseModel):
    """Health check response schema"""
    
    status: str
    message: str
    model_loaded: bool
    timestamp: str


class ModelInfoResponse(BaseModel):
    """Model information response schema"""
    
    model_name: str
    model_version: str
    features: List[str]
    supported_crops: List[str]
    accuracy: Optional[float] = None