from fastapi import FastAPI
from fastapi.responses import JSONResponse
from model.predict import predict_output, MODEL_VERSION , model
from schema.user_input import UserInfo
from schema.prediction_response import PredictionResponse

app  = FastAPI()

@app.get('/')
def home():
    return JSONResponse(content={'message':'Welcome to the Insurance Premium Prediction API'})

@app.get('/health')
def health():
    return{
        'status':'ok',
        'version': MODEL_VERSION,
        'model' : model is not None
    }
    
@app.post('/predict' ,response_model = PredictionResponse)
def predict_premium(data: UserInfo):
    
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }
    
    try:
        premium = predict_output(user_input)
        return JSONResponse(content={'response': premium})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
    