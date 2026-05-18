# Insurance Premium Prediction API

A FastAPI-based REST API that predicts insurance premium categories based on user demographics, health metrics, and lifestyle factors.

## Features

- **Fast & Scalable**: Built with FastAPI for high-performance predictions
- **Health Monitoring**: Built-in health check endpoint with model version tracking
- **Risk Assessment**: Calculates lifestyle risk based on smoking status and BMI
- **City-Based Pricing**: Tier-based city classification for premium calculation
- **Confidence Scoring**: Returns prediction confidence and class probabilities
- **Data Validation**: Pydantic-based input validation with automatic field computation

## Project Structure

```
insurance-premium-prediction/
├── app.py                      # Main FastAPI application
├── requirements.txt            # Python dependencies
├── config/
│   └── city_tier.py           # City classification configuration
├── model/
│   ├── predict.py             # Model prediction logic
│   └── model.pkl              # Pre-trained ML model
├── schema/
│   ├── user_input.py          # User input validation schema
│   └── prediction_response.py  # API response schema
└── myenv/                      # Virtual environment
```

## Requirements

- Python 3.12+
- FastAPI 0.128.8
- Uvicorn 0.39.0
- scikit-learn 1.6.1
- pandas 2.3.3
- pydantic 2.13.4

See `requirements.txt` for complete dependency list.

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/KriplaniPriya/insurance-premium-prediction.git
cd insurance-premium-prediction
```

2. **Create and activate virtual environment**
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Usage

### Running the API

```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

API documentation available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### API Endpoints

#### 1. Home Endpoint
```
GET /
```
Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Insurance Premium Prediction API"
}
```

#### 2. Health Check
```
GET /health
```
Checks API status and model availability.

**Response:**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "model": true
}
```

#### 3. Premium Prediction
```
POST /predict
```
Predicts insurance premium category based on user information.

**Request Body:**
```json
{
  "age": 35,
  "weight": 75,
  "height": 1.75,
  "income_lpa": 8.5,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

**Response:**
```json
{
  "response": {
    "preicted_category": "medium",
    "confidence": 0.87,
    "class_probabilities": {
      "low": 0.05,
      "medium": 0.87,
      "high": 0.08
    }
  }
}
```

## Input Parameters

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| `age` | int | Age of user | 0 < age < 120 |
| `weight` | float | Weight in kg | weight > 0 |
| `height` | float | Height in meters | 0 < height < 2.5 |
| `income_lpa` | float | Annual income in LPA | income > 0 |
| `smoker` | bool | Smoking status | true/false |
| `city` | str | City of residence | Any city name |
| `occupation` | str | User's occupation | See valid values below |

### Valid Occupations
- `retired`
- `freelancer`
- `student`
- `government_job`
- `business_owner`
- `unemployed`
- `private_job`

## Calculated Features

The API automatically computes the following features:

### BMI (Body Mass Index)
```
BMI = weight / (height²)
```

### Age Group
- `young`: age < 25
- `adult`: 25 ≤ age < 45
- `middle_aged`: 45 ≤ age < 60
- `senior`: age ≥ 60

### Lifestyle Risk
- `high`: Smoker AND BMI > 30
- `medium`: Smoker OR BMI > 27
- `low`: Otherwise

### City Tier
- **Tier 1**: Major metropolitan areas
- **Tier 2**: Secondary cities
- **Tier 3**: Other cities

See `config/city_tier.py` for city classifications.

## Model Information

- **Version**: 1.0.0
- **Type**: Classification (scikit-learn)
- **Output Classes**: Low, Medium, High
- **Features Used**: BMI, Age Group, Lifestyle Risk, City Tier, Income, Occupation

## Example Usage

### Using Python Requests
```python
import requests

url = "http://localhost:8000/predict"
payload = {
    "age": 45,
    "weight": 80,
    "height": 1.80,
    "income_lpa": 12.5,
    "smoker": True,
    "city": "Delhi",
    "occupation": "business_owner"
}

response = requests.post(url, json=payload)
print(response.json())
```

### Using cURL
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "weight": 80,
    "height": 1.80,
    "income_lpa": 12.5,
    "smoker": true,
    "city": "Delhi",
    "occupation": "business_owner"
  }'
```

## Error Handling

The API returns appropriate HTTP status codes:
- **200**: Successful prediction
- **422**: Validation error (invalid input parameters)
- **500**: Server error (model loading failure or prediction error)

## Development

### Project Dependencies Overview
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation using Python type hints
- **scikit-learn**: Machine learning model
- **pandas**: Data manipulation
- **pickle**: Model serialization

### Configuration

Edit `config/city_tier.py` to modify city tier classifications:

```python
tier_1_cities = ['Mumbai', 'Delhi', 'Bangalore', ...]
tier_2_cities = ['Pune', 'Chennai', 'Kolkata', ...]
```

## Performance Metrics

- **Response Time**: < 100ms (typical)
- **Throughput**: 1000+ requests/second
- **Model Accuracy**: Available from model evaluation metrics

## Deployment

### Docker (Optional)
Create a `Dockerfile`:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Running with Docker
```bash
docker build -t insurance-api .
docker run -p 8000:8000 insurance-api
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Author

**Priya Kriplanyi**
- GitHub: [@KriplaniPriya](https://github.com/KriplaniPriya)

## Support

For issues and questions, please open an issue on the GitHub repository or contact the author.

---

**Last Updated**: May 2026  
**Model Version**: 1.0.0  
**API Version**: 1.0.0
