# eta_module/eta.py
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

eta_bp = Blueprint('eta', __name__, template_folder='../templates')

# Train or Load model
MODEL_PATH = 'eta_model.pkl'
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    # Dummy training data
    df = pd.DataFrame({
        'distance_km': [2, 5, 10, 7],
        'traffic_level': [1, 2, 3, 1],
        'hour': [9, 14, 18, 11],
        'weekday': [0, 2, 4, 1],
        'duration_min': [10, 30, 45, 25]
    })
    X = df[['distance_km', 'traffic_level', 'hour', 'weekday']]
    y = df['duration_min']
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

# HTML Form View
@eta_bp.route('/form')
def eta_form():
    return render_template('eta_form.html')

# API Endpoint for Prediction
@eta_bp.route('/predict', methods=['POST'])
def predict_eta():
    data = request.get_json()
    try:
        input_features = [[
            data['distance_km'],
            data['traffic_level'],
            data['hour'],
            data['weekday']
        ]]
        prediction = model.predict(input_features)[0]
        return jsonify({'eta_minutes': round(prediction, 2)})
    except Exception as e:
        return jsonify({'error': str(e)})
