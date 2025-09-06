# Crop Recommendation API

A production-ready FastAPI application that provides ML-powered crop recommendations based on soil and climate conditions.

## 🌟 Features

- **High-Performance Model**: XGBoost classifier with 98.86% accuracy
- **RESTful API**: Clean, documented endpoints with automatic validation
- **Feature Engineering**: Advanced soil and climate feature processing
- **Batch Processing**: Support for multiple predictions in a single request
- **Health Monitoring**: Built-in health checks and monitoring endpoints
- **Docker Support**: Containerized deployment with Docker Compose
- **Auto Documentation**: Interactive API docs with Swagger UI
- **Production Ready**: Comprehensive error handling and logging

## 🚀 Quick Start

### Local Development

1. **Clone the repository**

```bash
git clone <https://github.com/Dhritikrishna123/crop_recommendation>
cd crop_recommendation
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Prepare your data**
   - Place your `Crop_recommendation.csv` file in the `data/` directory
   - The CSV should have columns: N, P, K, temperature, humidity, ph, rainfall, label

4. **Train the model**

```bash
python model_training.py
```

5. **Run the API**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker Deployment

1. **Build and run with Docker Compose**

```bash
docker-compose up --build
```

2. **Or build and run with Docker**

```bash
docker build -t crop-recommendation-api .
docker run -p 8000:8000 -v ./data:/app/data -v ./models:/app/models crop-recommendation-api
```

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 🛠 API Endpoints

### Core Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /model/info` - Model information

### Prediction Endpoints

- `POST /predict` - Single crop prediction
- `POST /predict/batch` - Batch predictions (max 100)

### Model Management

- `GET /model/feature-importance` - Get feature importance
- `POST /model/retrain` - Retrain model (background task)

## 📊 Supported Crops

The model can recommend from 22 different crops:

- **Cereals**: rice, maize
- **Legumes**: chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil
- **Fruits**: pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut
- **Cash Crops**: cotton, jute, coffee

## 🔧 Input Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| N | float | 0-200 | Nitrogen content in soil |
| P | float | 0-200 | Phosphorus content in soil |
| K | float | 0-250 | Potassium content in soil |
| temperature | float | 0-50 | Temperature in Celsius |
| humidity | float | 0-100 | Relative humidity percentage |
| ph | float | 0-14 | pH value of soil |
| rainfall | float | 0-400 | Rainfall in mm |

## 📝 Example Usage

### Single Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{
  "N": 90,
  "P": 42,
  "K": 43,
  "temperature": 20.87,
  "humidity": 82.0,
  "ph": 6.5,
  "rainfall": 202.9
}'
```

**Response:**

```json
{
  "predicted_crop": "rice",
  "confidence": 0.95,
  "all_probabilities": {
    "rice": 0.95,
    "maize": 0.03,
    "wheat": 0.02
  }
}
```

### Batch Prediction

```bash
curl -X POST "http://localhost:8000/predict/batch" \
-H "Content-Type: application/json" \
-d '{
  "predictions": [
    {
      "N": 90, "P": 42, "K": 43,
      "temperature": 20.87, "humidity": 82.0,
      "ph": 6.5, "rainfall": 202.9
    },
    {
      "N": 85, "P": 58, "K": 41,
      "temperature": 21.77, "humidity": 80.32,
      "ph": 7.04, "rainfall": 226.66
    }
  ]
}'
```

## 🏗 Project Structure

```
crop-recommendation-api/
├── main.py                 # FastAPI application
├── config.py              # Configuration settings
├── schemas.py             # Pydantic models for validation
├── data_processing.py     # Data preprocessing and feature engineering
├── model_training.py      # Model training and evaluation
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── README.md             # Project documentation
├── data/                 # Data directory
│   └── Crop_recommendation.csv
└── models/               # Model artifacts directory
    ├── crop_recommendation_model.joblib
    ├── data_processors.joblib
    └── model_metrics.joblib
```

## 🔬 Model Performance

- **Algorithm**: XGBoost Classifier
- **Test Accuracy**: 98.86%
- **Training Accuracy**: 99.94%
- **Features**: 13 (7 original + 6 engineered)
- **Classes**: 22 crop types

### Feature Engineering

The model uses several engineered features:

- **NPK**: Average of Nitrogen, Phosphorus, and Potassium
- **THI**: Temperature-Humidity Index
- **Rainfall Level**: Categorized rainfall (Low/Medium/High/Very High)
- **pH Category**: Soil acidity level (Acidic/Neutral/Alkaline)
- **Interaction Features**: Temperature×Rainfall, pH×Rainfall

## 🚀 Production Deployment

### Environment Variables

```bash
# Optional environment variables
PYTHONPATH=/app
LOG_LEVEL=info
MODEL_PATH=/app/models/crop_recommendation_model.joblib
```

### Health Monitoring

The API includes comprehensive health checks:

- Model loading status
- Service availability
- Response time monitoring

Monitor at: `GET /health`

### Scaling Considerations

- **Horizontal Scaling**: Deploy multiple instances behind a load balancer
- **Caching**: Implement Redis for frequently requested predictions
- **Database**: Add PostgreSQL for storing prediction history
- **Monitoring**: Use Prometheus + Grafana for metrics

## 🧪 Testing

### Manual Testing

Test the health endpoint:

```bash
curl http://localhost:8000/health
```

Test a prediction:

```bash
curl -X POST "http://localhost:8000/predict" \
-H "Content-Type: application/json" \
-d '{"N": 90, "P": 42, "K": 43, "temperature": 20.87, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9}'
```

### Load Testing

Use tools like Apache Bench or wrk for load testing:

```bash
# Install wrk and test
wrk -t12 -c400 -d30s --latency http://localhost:8000/health
```

## 🔧 Configuration

Edit `config.py` to modify:

- Model parameters
- API settings
- File paths
- Training configuration

## 📈 Monitoring & Logging

The application includes:

- Structured logging with Python's logging module
- Request/response logging
- Error tracking with stack traces
- Health check endpoints for monitoring systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **Model not loading**: Ensure the model files are in the `models/` directory
2. **Import errors**: Check that all dependencies are installed correctly
3. **Memory issues**: XGBoost models can be memory-intensive; ensure adequate RAM
4. **Port conflicts**: Change the port in `config.py` if 8000 is occupied

### Debug Mode

Run with debug logging:

```bash
LOG_LEVEL=debug uvicorn main:app --reload
```

### Docker Issues

Check container logs:

```bash
docker-compose logs -f crop-api
```

## 📞 Support

For issues and questions:

- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the logs for error messages
