import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load and preprocess data
df = pd.read_csv("delivery_time_predictor/delivery_data.csv")
df['pickup_time'] = pd.to_datetime(df['pickup_time'])
df['delivery_time'] = pd.to_datetime(df['delivery_time'])
df['duration_min'] = (df['delivery_time'] - df['pickup_time']).dt.total_seconds() / 60
df['hour'] = df['pickup_time'].dt.hour
df['weekday'] = df['pickup_time'].dt.weekday

X = df[['distance_km', 'traffic_level', 'hour', 'weekday']]
y = df['duration_min']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# Hyperparameter tuning
param_grid = {
    'n_estimators': [100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5]
}
grid = GridSearchCV(RandomForestRegressor(), param_grid, cv=3, scoring='neg_mean_absolute_error')
grid.fit(X_train, y_train)
best_model = grid.best_estimator_

# Validation
y_pred = best_model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"Validation Mean Absolute Error: {mae:.2f} minutes")

# Save model
joblib.dump(best_model, 'delivery_time_predictor/eta_model.pkl')
print("Model trained and saved as eta_model.pkl")