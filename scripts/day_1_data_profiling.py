import pandas as pd
import numpy as np

# --- Day 1: Saturday, September 28 - Environment Setup & Data Profiling ---

# Objective: Prepare a professional, reproducible technical workspace and perform a
# thorough, high-level assessment of the dataset.

# --- Task 1: Environment Setup ---
# In PyCharm, a new Conda environment named 'airbnb_analysis' has been created.
# The following core libraries were installed using the terminal:
# conda install pandas
# conda install numpy
# conda install matplotlib
# conda install seaborn

print("--- Task 1: Environment Setup Complete ---")
print("Libraries (pandas, numpy, matplotlib, seaborn) are installed in the Conda environment.\n")


# --- Task 2: Load Data ---
# Loading the dataset into a pandas DataFrame.
# NOTE: Assuming the dataset is in the same directory and named 'NYC_Airbnb.csv'.
try:
    df = pd.read_excel(r'C:\Users\jaiku\PycharmProjects\Airbnb_Analysis\data\raw\1730285881-Airbnb_Open_Data.xlsx')
    print("--- Task 2: Load Data Complete ---")
    print("Dataset 'NYC_Airbnb.xlsx' loaded successfully.\n")

    print("--- Initial Memory Usage ---")
    # Checking the initial memory usage to understand the dataset's footprint.
    df.info(memory_usage='deep')
    print("\n")


    # --- Task 3: Initial Data Profiling ---
    print("--- Task 3: Initial Data Profiling ---")

    # Using df.info() to check column names, non-null counts, and data types.
    # This helps identify columns that might need data type conversion (e.g., last_review)
    # and gives a first look at missing data.
    print("\n[Profiling Step 1: DataFrame Info]")
    df.info()

    # Using df.shape to understand the scale of the data.
    print("\n\n[Profiling Step 2: Dataset Shape]")
    print(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns.")

    # Using df.head() and df.tail() to visually inspect the first and last few rows.
    # This is a quick check to ensure the data has loaded correctly and to see the format.
    print("\n\n[Profiling Step 3: First 5 Rows (head)]")
    print(df.head())

    print("\n\n[Profiling Step 4: Last 5 Rows (tail)]")
    print(df.tail())

    # Generating descriptive statistics for numerical columns with df.describe().
    # This is crucial for spotting potential outliers or illogical values (e.g., price=0).
    print("\n\n[Profiling Step 5: Descriptive Statistics for Numerical Columns]")
    print(df.describe())

    # Using df.isnull().sum() to get a precise count of missing values for each column.
    # This output directly informs the data cleaning strategy for Day 2.
    print("\n\n[Profiling Step 6: Count of Missing Values per Column]")
    print(df.isnull().sum())
    print("\n--- End of Day 1 Script ---")


except FileNotFoundError:
    print("--- ERROR ---")
    print("Dataset 'NYC_Airbnb.csv' not found. Please ensure the file is in the correct directory.")
