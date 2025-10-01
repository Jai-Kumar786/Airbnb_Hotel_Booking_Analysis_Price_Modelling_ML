import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import matplotlib.pyplot as plt
import seaborn as sns


def day_9_model_interpretation():
    """
    Interprets the trained stacked model using permutation importance and
    runs a "what-if" simulation to demonstrate its practical utility.
    """
    print("--- Starting Day 9: Model Interpretation & Simulation ---")

    # --- Define File Paths ---
    model_path = '../models/stacked_price_predictor.joblib'
    features_path = '../data/processed/model_features.csv'
    target_path = '../data/processed/model_target.csv'
    cleaned_data_path = '../data/processed/cleaned_airbnb_data.csv'
    figures_dir = '../reports/figures/'

    # --- Load Model and Data ---
    if not all([os.path.exists(f) for f in [model_path, features_path, target_path, cleaned_data_path]]):
        print("Error: Required model or data files not found. Please run prior day scripts.")
        return

    try:
        model = joblib.load(model_path)
        X = pd.read_csv(features_path)
        y = pd.read_csv(target_path).iloc[:, 0]
        # Load original cleaned data to get true median values for simulation
        df_cleaned = pd.read_csv(cleaned_data_path)
        print("Successfully loaded trained model and all required datasets.")
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    # Re-create a test set for permutation importance calculation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Task 1: Feature Importance Analysis (using Permutation Importance) ---
    print("\n[Task 1/2] Calculating feature importance using Permutation Importance...")
    print("This method is model-agnostic and ideal for interpreting stacked ensembles.")

    # Calculate permutation importance on the test set
    result = permutation_importance(
        model, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1
    )

    # Organize results into a DataFrame for plotting
    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance_mean': result.importances_mean,
        'importance_std': result.importances_std
    }).sort_values('importance_mean', ascending=False)

    # --- PLOT FIX: Replaced single barplot call with a two-step process for robustness ---
    print("Generating a clearer feature importance plot...")
    plt.figure(figsize=(12, 10))
    # Step 1: Create the main barplot using Seaborn
    ax = sns.barplot(x='importance_mean', y='feature', data=importance_df, palette='viridis')
    # Step 2: Overlay the error bars using Matplotlib's errorbar function
    ax.errorbar(x=importance_df['importance_mean'], y=np.arange(len(importance_df)),
                xerr=importance_df['importance_std'], fmt='none', c='black', capsize=3)

    plt.title('Permutation Importance of Features for Price Prediction', fontsize=18)
    plt.xlabel('Decrease in R² Score (Importance)', fontsize=14)
    plt.ylabel('Feature', fontsize=14)
    plt.axvline(x=0, color='k', linestyle='--')
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '14_feature_importance.png'))
    plt.close()
    print("Saved '14_feature_importance.png'")
    print("-" * 50)

    # --- Task 2: "What-If" Price Simulation ---
    print("\n[Task 2/2] Running 'What-If' Price Simulation...")

    # FIX: Re-engineer 'days_since_last_review' on df_cleaned before calculating medians
    print("Re-engineering 'days_since_last_review' for simulation medians...")
    reference_date = pd.to_datetime('2023-01-01')
    df_cleaned['last_review'] = pd.to_datetime(df_cleaned['last_review'])
    df_cleaned['days_since_last_review'] = (reference_date - df_cleaned['last_review']).dt.days
    df_cleaned['days_since_last_review'] = df_cleaned['days_since_last_review'].fillna(9999)
    print("Feature re-engineered successfully for simulation.")
    print("-" * 50)

    # Calculate median values for numeric features from the original cleaned dataset
    median_values = {
        'minimum_nights': df_cleaned['minimum_nights'].median(),
        'number_of_reviews': df_cleaned['number_of_reviews'].median(),
        'reviews_per_month': df_cleaned['reviews_per_month'].median(),
        'calculated_host_listings_count': df_cleaned['calculated_host_listings_count'].median(),
        'availability_365': df_cleaned['availability_365'].median(),
        'days_since_last_review': df_cleaned['days_since_last_review'].median()
    }

    # Create scenarios
    scenarios = {
        'Baseline': {
            'neighbourhood_group': 'Manhattan',
            'room_type': 'Entire home/apt',
            **median_values
        },
        'A (Downgrade)': {
            'neighbourhood_group': 'Manhattan',
            'room_type': 'Private room',  # Changed
            **median_values
        },
        'B (Improve Relevancy)': {
            'neighbourhood_group': 'Manhattan',
            'room_type': 'Entire home/apt',
            'days_since_last_review': 10,  # Changed to very recent
            **{k: v for k, v in median_values.items() if k != 'days_since_last_review'}  # Use other medians
        },
        'C (Location Change)': {
            'neighbourhood_group': 'Bronx',  # Changed
            'room_type': 'Entire home/apt',
            **median_values
        }
    }

    # Create a DataFrame from scenarios
    sim_df = pd.DataFrame.from_dict(scenarios, orient='index')

    # One-hot encode the simulation DataFrame
    sim_df_encoded = pd.get_dummies(sim_df)

    # IMPORTANT: Ensure the simulation DataFrame has the exact same columns as the training data
    sim_df_processed = sim_df_encoded.reindex(columns=X.columns, fill_value=0)

    # Make predictions
    log_predictions = model.predict(sim_df_processed)

    # Inverse transform predictions to get dollar amounts
    predicted_prices = np.expm1(log_predictions)

    # Add predictions to the original simulation DataFrame for a clear report
    sim_df['predicted_price'] = predicted_prices

    print("\n--- Price Simulation Results ---")
    print(sim_df[['predicted_price']].round(2))
    print("-" * 50)

    # Calculate and print the impact of each change
    baseline_price = sim_df.loc['Baseline', 'predicted_price']
    price_change_A = sim_df.loc['A (Downgrade)', 'predicted_price'] - baseline_price
    price_change_B = sim_df.loc['B (Improve Relevancy)', 'predicted_price'] - baseline_price
    price_change_C = sim_df.loc['C (Location Change)', 'predicted_price'] - baseline_price

    print("Impact of Strategic Changes vs. Baseline:")
    print(f"Scenario A (Downgrade to Private Room): ${price_change_A:+.2f}")
    print(f"Scenario B (Get a Recent Review):       ${price_change_B:+.2f}")
    print(f"Scenario C (Move to Bronx):             ${price_change_C:+.2f}")

    print("\n--- Day 9 Model Interpretation & Simulation Complete ---")


if __name__ == '__main__':
    day_9_model_interpretation()

