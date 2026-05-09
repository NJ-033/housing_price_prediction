import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error
import joblib
import os

def train_and_save_model():
    if not os.path.exists('data/housing_data.csv'):
        print("Data not found. Generating mock data...")
        from src.mock_data import generate_mock_data
        generate_mock_data()
        
    df = pd.read_csv('data/housing_data.csv')
    
    X = df.drop('price', axis=1)
    y = df['price']
    
    categorical_features = ['subdivision']
    numeric_features = ['bedrooms', 'bathrooms', 'floor_area', 'land_size', 'build_year']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough'
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    y_pred = pipeline.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    
    print(f"Model Performance:")
    print(f"R2 Score: {r2:.4f}")
    print(f"RMSE: PHP {rmse:,.2f}")
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(pipeline, 'models/best_model.pkl')
    print("Model saved to models/best_model.pkl")

def predict_price(features):
    """
    Predict price based on features dictionary
    """
    model_path = 'models/best_model.pkl'
    if not os.path.exists(model_path):
        train_and_save_model()
        
    model = joblib.load(model_path)
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    return prediction

if __name__ == '__main__':
    train_and_save_model()
