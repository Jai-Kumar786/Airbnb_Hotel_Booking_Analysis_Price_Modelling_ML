import pandas as pd
import os

# --- Configuration ---
RAW_DATA_PATH = os.path.join('data', 'raw', r'C:\Users\jaiku\PycharmProjects\Airbnb_Analysis\data\raw\1730285881-Airbnb_Open_Data.xlsx')
PROCESSED_DATA_PATH = os.path.join('data', 'processed')
CLEANED_FILE_NAME = 'cleaned_airbnb_data.csv'


# --- Main Cleaning Function ---
def clean_airbnb_data():
    """
    Loads the raw Airbnb dataset, performs a comprehensive cleaning process,
    and saves the cleaned data to a new file.
    """
    print("--- Starting Day 2: Data Cleaning Process ---")

    # Load the raw data
    try:
        df = pd.read_excel(RAW_DATA_PATH)
        print(f"Successfully loaded raw data from '{RAW_DATA_PATH}'.")
        print(f"Initial shape of the dataset: {df.shape}")
    except FileNotFoundError:
        print(f"Error: The file was not found at '{RAW_DATA_PATH}'.")
        print("Please ensure the raw data is in the 'data/raw' directory.")
        return

    # --- Step 1: Standardize Column Names ---
    print("\n[Step 1/5] Standardizing column names...")
    original_columns = df.columns.tolist()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
    print("Column names standardized to lowercase with underscores.")
    # print(f"New columns: {df.columns.tolist()}")

    # --- Step 2: Remove Unnecessary Columns ---
    print("\n[Step 2/5] Removing unnecessary columns...")
    columns_to_drop = ['license', 'house_rules', 'country', 'country_code']
    # Check which columns actually exist in the dataframe before trying to drop
    existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
    df.drop(columns=existing_columns_to_drop, inplace=True)
    print(f"Dropped columns: {existing_columns_to_drop}")

    # --- Step 3: Handle Missing Values ---
    print("\n[Step 3/5] Handling missing values...")
    # Impute 'reviews_per_month' with 0 where 'number_of_reviews' is 0
    initial_nan_reviews = df['reviews_per_month'].isnull().sum()
    df.loc[df['number_of_reviews'] == 0, 'reviews_per_month'] = df.loc[
        df['number_of_reviews'] == 0, 'reviews_per_month'].fillna(0)
    imputed_count = initial_nan_reviews - df['reviews_per_month'].isnull().sum()
    print(f"Imputed {imputed_count} missing 'reviews_per_month' with 0 for listings with no reviews.")

    # Drop rows with any remaining missing values in any column
    rows_before_dropna = df.shape[0]
    df.dropna(inplace=True)
    rows_after_dropna = df.shape[0]
    print(f"Dropped {rows_before_dropna - rows_after_dropna} rows with other missing values.")

    # --- Step 4: Filter Invalid and Illogical Data ---
    print("\n[Step 4/5] Filtering illogical and invalid data...")
    rows_before_filter = df.shape[0]

    # Filter 'minimum_nights'
    df = df[df['minimum_nights'] >= 1]

    # Filter 'availability_365'
    df = df[(df['availability_365'] >= 0) & (df['availability_365'] <= 365)]

    # Filter 'last_review' for future dates
    df = df[df['last_review'] <= pd.to_datetime('today')]

    rows_after_filter = df.shape[0]
    print(f"Removed {rows_before_filter - rows_after_filter} rows with illogical values.")
    print(
        "Ensured 'minimum_nights' >= 1, 'availability_365' is between 0-365, and no future 'last_review' dates exist.")

    # --- Step 5: Final Verification and Save ---
    print("\n[Step 5/5] Final verification and saving cleaned data...")

    # Verify no missing values remain
    print(f"\nFinal check for missing values:\n{df.isnull().sum()}")

    # Display statistics of the cleaned data
    print(
        f"\nDescriptive statistics of key cleaned columns:\n{df[['price', 'minimum_nights', 'availability_365']].describe()}")

    # Create the processed data directory if it doesn't exist
    if not os.path.exists(PROCESSED_DATA_PATH):
        os.makedirs(PROCESSED_DATA_PATH)
        print(f"Created directory: '{PROCESSED_DATA_PATH}'")

    # Save the cleaned dataframe
    final_path = os.path.join(PROCESSED_DATA_PATH, CLEANED_FILE_NAME)
    df.to_csv(final_path, index=False)

    print(f"\n--- Data Cleaning Process Complete ---")
    print(f"Final shape of the cleaned dataset: {df.shape}")
    print(f"Cleaned data has been successfully saved to '{final_path}'")


# --- Execute the script ---
if __name__ == '__main__':
    clean_airbnb_data()
