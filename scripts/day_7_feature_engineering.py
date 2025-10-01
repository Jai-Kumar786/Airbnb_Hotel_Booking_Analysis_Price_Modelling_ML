import pandas as pd
import numpy as np
import os


def day_7_feature_engineering():
    """
    Prepares and transforms the dataset for machine learning by creating
    new features, selecting variables, and encoding categorical data.
    """
    print("--- Starting Day 7: Feature Engineering for Machine Learning ---")

    # Define file paths
    cleaned_data_path = '../data/processed/cleaned_airbnb_data.csv'
    processed_dir = '../data/processed/'
    features_path = os.path.join(processed_dir, 'model_features.csv')
    target_path = os.path.join(processed_dir, 'model_target.csv')

    # --- Load Data ---
    if not os.path.exists(cleaned_data_path):
        print(f"Error: Cleaned data file not found at '{cleaned_data_path}'")
        return

    try:
        df = pd.read_csv(cleaned_data_path, parse_dates=['last_review'])
        print(f"Successfully loaded cleaned data. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # **CRITICAL CORRECTION ADDED**
    # Correct the 'brookln' typo before any feature engineering
    df['neighbourhood_group'] = df['neighbourhood_group'].replace('brookln', 'Brooklyn')
    print("\nCorrected 'brookln' typo in neighbourhood_group.")
    print(f"Unique values in neighbourhood_group now: {df['neighbourhood_group'].unique()}")
    print("-" * 50)

    # --- Task 1: Create New, Insightful Features ---
    print("\n[Task 1/3] Engineering 'days_since_last_review' feature...")

    # Define a fixed recent date for reproducibility
    reference_date = pd.to_datetime('2023-01-01')

    # Calculate the difference in days
    df['days_since_last_review'] = (reference_date - df['last_review']).dt.days

    # Impute NaT values for listings with no reviews with a large number
    df['days_since_last_review'] = df['days_since_last_review'].fillna(9999)

    print("Feature 'days_since_last_review' created successfully.")
    print(df[['last_review', 'days_since_last_review']].head())
    print("-" * 50)

    # --- Task 2: Strategic Feature & Target Selection ---
    print("\n[Task 2/3] Selecting features (X) and target (y)...")

    # Define the list of features for the model
    feature_columns = [
        'neighbourhood_group',
        'room_type',
        'minimum_nights',
        'number_of_reviews',
        'reviews_per_month',
        'calculated_host_listings_count',
        'availability_355',  # Assuming this was a typo in the plan and should be availability_365
        'days_since_last_review'
    ]
    # Correcting potential typo in column name if it exists in your dataframe
    if 'availability_355' in df.columns and 'availability_365' not in feature_columns:
        pass  # keep as is
    elif 'availability_365' in df.columns:
        feature_columns[6] = 'availability_365'

    X = df[feature_columns]

    # Select the target variable and apply log transformation to handle skewness
    y_log = np.log1p(df['price'])

    print(f"Selected {len(X.columns)} features.")
    print("Target variable 'price' has been log-transformed.")
    print("-" * 50)

    # --- Task 3: Encode Categorical Variables ---
    print("\n[Task 3/3] Applying one-hot encoding to categorical features...")

    # Use pandas get_dummies to perform one-hot encoding
    X_processed = pd.get_dummies(X, columns=['neighbourhood_group', 'room_type'], drop_first=True)

    print("Categorical variables successfully encoded.")
    print(f"Shape of the final feature matrix: {X_processed.shape}")
    print("Sample of new columns created:")
    print(X_processed.columns)
    print("-" * 50)

    # --- Save Processed Data ---
    print("Saving the final processed feature matrix and target vector...")
    try:
        X_processed.to_csv(features_path, index=False)
        y_log.to_csv(target_path, index=False)
        print(f"Features saved to '{features_path}'")
        print(f"Target saved to '{target_path}'")
    except Exception as e:
        print(f"Error saving files: {e}")
        return

    print("\n--- Day 7 Feature Engineering Complete ---")


if __name__ == '__main__':
    day_7_feature_engineering()

