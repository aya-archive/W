#!/usr/bin/env python3
"""
V2 API Routes - RESTful endpoints for V2 Main App
Provides API endpoints for external integrations and programmatic access
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import pandas as pd
import json
import logging
from V2_newai_service import get_newai_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create API router
router = APIRouter(prefix="/api/v2", tags=["V2 AURA API"])

# Pydantic models for request/response
class PredictionRequest(BaseModel):
    customer_data: List[Dict]
    
class PredictionResponse(BaseModel):
    success: bool
    total_customers: int
    high_risk: int
    medium_risk: int
    low_risk: int
    avg_probability: float
    predictions: List[Dict]
    model_used: str

class HealthResponse(BaseModel):
    status: str
    service: str
    model_available: bool
    models_loaded: bool
    version: str

class ModelInfoResponse(BaseModel):
    name: str
    type: str
    version: str
    features: List[str]
    performance: Dict
    available: bool
    model_path: str
    preprocess_path: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        newai_service = get_newai_service()
        health = newai_service.health_check()
        return HealthResponse(**health)
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/info", response_model=ModelInfoResponse)
async def get_model_info():
    """Get model information"""
    try:
        newai_service = get_newai_service()
        info = newai_service.get_model_info()
        return ModelInfoResponse(**info)
    except Exception as e:
        logger.error(f"❌ Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting model info: {str(e)}")

@router.post("/predict", response_model=PredictionResponse)
async def predict_churn(request: PredictionRequest):
    """Run churn prediction on provided data"""
    try:
        newai_service = get_newai_service()
        
        # Convert request data to DataFrame
        df = pd.DataFrame(request.customer_data)
        
        # Run prediction
        results = newai_service.predict_churn(df)
        
        if not results.get("success", False):
            raise HTTPException(status_code=400, detail=results.get("error", "Prediction failed"))
        
        return PredictionResponse(**results)
        
    except Exception as e:
        logger.error(f"❌ Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/upload")
async def upload_data(file: UploadFile = File(...)):
    """Upload CSV data for processing"""
    try:
        newai_service = get_newai_service()
        
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Validate data
        if 'customerID' not in df.columns:
            raise HTTPException(status_code=400, detail="Missing required column: customerID")
        
        # Upload and process data
        result = newai_service.upload_data(df)
        
        if not result.get("success", False):
            raise HTTPException(status_code=400, detail=result.get("error", "Upload failed"))
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"❌ Upload error: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/download-predictions")
async def download_predictions():
    """Download predictions CSV"""
    try:
        newai_service = get_newai_service()
        csv_content = newai_service.get_predictions_csv()
        
        if csv_content is None:
            raise HTTPException(status_code=404, detail="No predictions found. Please run predictions first.")
        
        # Return CSV file
        return JSONResponse(
            content={"csv_content": csv_content},
            headers={"Content-Type": "text/csv"}
        )
        
    except Exception as e:
        logger.error(f"❌ Download error: {e}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

@router.get("/sample-data")
async def get_sample_data():
    """Get sample data for testing"""
    try:
        # Generate sample data
        import numpy as np
        np.random.seed(42)
        n_customers = 100
        
        sample_data = {
            'customerID': [f'CUST_{i:04d}' for i in range(1, n_customers + 1)],
            'gender': np.random.choice(['Male', 'Female'], n_customers),
            'SeniorCitizen': np.random.choice([0, 1], n_customers),
            'Partner': np.random.choice(['Yes', 'No'], n_customers),
            'Dependents': np.random.choice(['Yes', 'No'], n_customers),
            'tenure': np.random.randint(1, 60, n_customers),
            'PhoneService': np.random.choice(['Yes', 'No'], n_customers),
            'MultipleLines': np.random.choice(['Yes', 'No', 'No phone service'], n_customers),
            'InternetService': np.random.choice(['DSL', 'Fiber optic', 'No'], n_customers),
            'OnlineSecurity': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'OnlineBackup': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'DeviceProtection': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'TechSupport': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'StreamingTV': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'StreamingMovies': np.random.choice(['Yes', 'No', 'No internet service'], n_customers),
            'Contract': np.random.choice(['Month-to-month', 'One year', 'Two year'], n_customers),
            'PaperlessBilling': np.random.choice(['Yes', 'No'], n_customers),
            'PaymentMethod': np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], n_customers),
            'MonthlyCharges': np.random.uniform(20, 100, n_customers),
            'TotalCharges': np.random.uniform(100, 5000, n_customers),
            'Churn': np.random.choice(['Yes', 'No'], n_customers)
        }
        
        return JSONResponse(content=sample_data)
        
    except Exception as e:
        logger.error(f"❌ Sample data error: {e}")
        raise HTTPException(status_code=500, detail=f"Sample data generation failed: {str(e)}")

@router.get("/stats")
async def get_statistics():
    """Get platform statistics"""
    try:
        newai_service = get_newai_service()
        health = newai_service.health_check()
        info = newai_service.get_model_info()
        
        stats = {
            "platform": "V2 AURA",
            "version": "2.0.0",
            "status": health["status"],
            "model_available": health["model_available"],
            "model_accuracy": info["performance"]["accuracy"],
            "features_count": len(info["features"]),
            "endpoints": [
                "/api/v2/health",
                "/api/v2/info", 
                "/api/v2/predict",
                "/api/v2/upload",
                "/api/v2/download-predictions",
                "/api/v2/sample-data",
                "/api/v2/stats"
            ]
        }
        
        return JSONResponse(content=stats)
        
    except Exception as e:
        logger.error(f"❌ Stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Statistics failed: {str(e)}")

# Import io for StringIO
import io
