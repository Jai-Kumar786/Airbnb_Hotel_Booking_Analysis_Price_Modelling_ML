import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.linear_model import Ridge
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, r2_score


def day_8_model_training():
    """
    Builds, trains, and evaluates a stacked generalization ensemble model
    to predict Airbnb listing prices.
    """
    print("--- Starting Day 8: Model Training & Evaluation ---")

    # --- Load Processed Data ---
    processed_dir = '../data/processed/'
    features_path = os.path.join(processed_dir, 'model_features.csv')
    target_path = os.path.join(processed_dir, 'model_target.csv')

    if not all([os.path.exists(features_path), os.path.exists(target_path)]):
        print("Error: Model-ready data files not found. Please run the Day 7 script first.")
        return

    try:
        X = pd.read_csv(features_path)
        y = pd.read_csv(target_path).iloc[:, 0]  # Ensure y is a Series
        print(f"Successfully loaded model-ready data. Features shape: {X.shape}, Target shape: {y.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- Task 1: Train-Test Split ---
    print("\n[Task 1/4] Splitting data into training (80%) and testing (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"Training set size: {X_train.shape[0]} samples")
    print(f"Testing set size: {X_test.shape[0]} samples")
    print("-" * 50)

    # --- Task 2: Model Selection (Base Models & Meta-Learner) ---
    print("\n[Task 2/4] Defining base models and meta-learner for the stacked ensemble...")

    # Define the base models
    base_models = [
        ('rf', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ('xgb', XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1)),
        ('lgbm', LGBMRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ]

    # Define the meta-learner
    meta_learner = Ridge(alpha=1.0)

    # Create the Stacking Ensemble
    stacked_model = StackingRegressor(
        estimators=base_models,
        final_estimator=meta_learner,
        cv=5,  # Use 5-fold cross-validation to generate predictions for the meta-learner
        n_jobs=-1
    )
    print("Stacked Generalization Ensemble configured successfully.")
    print("-" * 50)

    # --- Task 3: Model Training ---
    print("\n[Task 3/4] Training the stacked ensemble model... (This may take a few minutes)")
    stacked_model.fit(X_train, y_train)
    print("Model training complete.")
    print("-" * 50)

    # --- Task 4: Prediction & Rigorous Evaluation ---
    print("\n[Task 4/4] Making predictions and evaluating the model...")

    # Make predictions on the test set
    log_predictions = stacked_model.predict(X_test)

    # CRITICAL: Inverse transform the predictions and the true values to get actual dollar amounts
    # np.expm1 is the inverse of np.log1p
    actual_prices = np.expm1(y_test)
    predicted_prices = np.expm1(log_predictions)

    # Evaluate the model's performance
    mae = mean_absolute_error(actual_prices, predicted_prices)
    r2 = r2_score(actual_prices, predicted_prices)

    print("\n--- Model Performance Metrics ---")
    print(f"Mean Absolute Error (MAE): ${mae:.2f}")
    print("Interpretation: On average, the model's price predictions are off by approximately $" + f"{mae:.2f}.")

    print(f"\nR-squared (R²): {r2:.4f}")
    print(f"Interpretation: The model explains approximately {r2:.1%} of the variance in the Airbnb listing prices.")
    print("-" * 50)

    # Save the trained model for future use (optional, but good practice)
    import joblib
    model_path = os.path.join('../models', 'stacked_price_predictor.joblib')
    os.makedirs('models', exist_ok=True)
    joblib.dump(stacked_model, model_path)
    print(f"Trained model saved to '{model_path}'")

    print("\n--- Day 8 Model Training & Evaluation Complete ---")


if __name__ == '__main__':
    day_8_model_training()

