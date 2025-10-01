import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def day_4_analysis_corrected():
    """
    Performs a deep dive analysis into pricing and geographic insights,
    including a correction for a data typo found during the initial run.
    """
    print("--- Starting Day 4: Deep Dive Analysis (Corrected Version) ---")

    # Define file paths
    cleaned_data_path = '../data/processed/cleaned_airbnb_data.csv'
    figures_dir = '../reports/figures/'

    # --- Load Data ---
    if not os.path.exists(cleaned_data_path):
        print(f"Error: Cleaned data file not found at '{cleaned_data_path}'")
        print("Please run the Day 2 data cleaning script first.")
        return

    try:
        df = pd.read_csv(cleaned_data_path)
        print(f"Successfully loaded cleaned data. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- Pre-Analysis Data Correction ---
    # Correcting the 'brookln' typo identified during the initial analysis.
    # This is a critical step to ensure data integrity for this script's operations.
    original_brooklyn_count = df[df['neighbourhood_group'] == 'Brooklyn'].shape[0]
    if 'brookln' in df['neighbourhood_group'].unique():
        df['neighbourhood_group'] = df['neighbourhood_group'].replace('brookln', 'Brooklyn')
        corrected_brooklyn_count = df[df['neighbourhood_group'] == 'Brooklyn'].shape[0]
        print(
            f"\nCorrected 'brookln' typo. Merged {corrected_brooklyn_count - original_brooklyn_count} row(s) into 'Brooklyn'.")
    else:
        print("\nNo 'brookln' typo found to correct.")

    # --- Task 1: Multifactorial Price Analysis ---
    print("\n[Task 1/3] Performing Multifactorial Price Analysis...")

    # Calculate statistics
    price_stats = df.groupby('neighbourhood_group')['price'].agg(['mean', 'median', 'std']).round(2)
    print("\nPrice Statistics by Borough (Corrected):")
    print(price_stats)

    # Create and save box plot
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='neighbourhood_group', y='price', data=df, palette='viridis',
                order=price_stats.sort_values('median', ascending=False).index)
    plt.title('Price Distribution by Neighbourhood Group', fontsize=16)
    plt.xlabel('Borough', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '5_price_boxplot_by_borough.png'))
    plt.close()
    print("Saved '5_price_boxplot_by_borough.png'")

    # Create and save violin plot
    plt.figure(figsize=(12, 8))
    sns.violinplot(x='neighbourhood_group', y='price', data=df, palette='viridis',
                   order=price_stats.sort_values('median', ascending=False).index)
    plt.title('Price Density and Distribution by Neighbourhood Group', fontsize=16)
    plt.xlabel('Borough', fontsize=12)
    plt.ylabel('Price ($)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '6_price_violinplot_by_borough.png'))
    plt.close()
    print("Saved '6_price_violinplot_by_borough.png'")

    # --- Task 2: Service Fee Correlation Analysis ---
    print("\n[Task 2/3] Analyzing Service Fee Correlation...")

    # Calculate Pearson correlation
    correlation = df['price'].corr(df['service_fee'])
    print(f"\nPearson Correlation between 'price' and 'service_fee': {correlation:.4f}")

    # Create and save scatter plot
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='price', y='service_fee', data=df, alpha=0.5)
    plt.title('Price vs. Service Fee Correlation', fontsize=16)
    plt.xlabel('Price ($)', fontsize=12)
    plt.ylabel('Service Fee ($)', fontsize=12)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '7_price_vs_service_fee_scatter.png'))
    plt.close()
    print("Saved '7_price_vs_service_fee_scatter.png'")

    # --- Task 3: Identify Premium Neighborhoods ---
    print("\n[Task 3/3] Identifying Top 10 Premium Neighborhoods...")

    # Calculate mean price and get top 10
    top_10_neighborhoods = df.groupby('neighbourhood')['price'].mean().sort_values(ascending=False).head(10).round(2)
    print("\nTop 10 Most Expensive Neighborhoods by Average Price:")
    print(top_10_neighborhoods)

    # Create and save bar chart
    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_10_neighborhoods.values, y=top_10_neighborhoods.index, palette='rocket')
    plt.title('Top 10 Most Expensive Neighborhoods in NYC', fontsize=16)
    plt.xlabel('Average Price ($)', fontsize=12)
    plt.ylabel('Neighborhood', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '8_top_10_premium_neighborhoods.png'))
    plt.close()
    print("Saved '8_top_10_premium_neighborhoods.png'")

    print("\n--- Day 4 Analysis Complete ---")


if __name__ == '__main__':
    day_4_analysis_corrected()

