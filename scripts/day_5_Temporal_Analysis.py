import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def day_5_temporal_analysis():
    """
    Performs temporal analysis on the cleaned Airbnb dataset to uncover
    seasonality, long-term trends, and booking patterns.
    """
    print("--- Starting Day 5: Temporal Analysis & Booking Patterns ---")

    # Define file paths
    cleaned_data_path = '../data/processed/cleaned_airbnb_data.csv'
    figures_dir = '../reports/figures/'

    # --- Load Data ---
    if not os.path.exists(cleaned_data_path):
        print(f"Error: Cleaned data file not found at '{cleaned_data_path}'")
        return

    try:
        # Explicitly parse 'last_review' as a date column on load
        df = pd.read_csv(cleaned_data_path, parse_dates=['last_review'])
        print(f"Successfully loaded cleaned data. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- Task 1: Seasonality Analysis ---
    print("\n[Task 1/3] Analyzing seasonality based on review dates...")

    # Extract month from last_review
    df['review_month'] = df['last_review'].dt.month

    # Count reviews per month
    monthly_reviews = df['review_month'].value_counts().sort_index()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_reviews.index = month_names

    # Create and save bar chart for seasonality
    plt.figure(figsize=(12, 7))
    sns.barplot(x=monthly_reviews.index, y=monthly_reviews.values, palette='plasma')
    plt.title('Total Number of Reviews by Month (Seasonality)', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '9_seasonality_by_month.png'))
    plt.close()
    print("Saved '9_seasonality_by_month.png'")

    # --- Task 2: Long-Term Trend Analysis ---
    print("\n[Task 2/3] Analyzing long-term trends...")

    # Extract year from last_review
    df['review_year'] = df['last_review'].dt.year

    # Count reviews per year
    yearly_reviews = df['review_year'].value_counts().sort_index()

    # Filter out any years that might be anomalous if necessary (e.g., very old or future dates if not cleaned)
    yearly_reviews = yearly_reviews[yearly_reviews.index >= 2012]  # Assuming 2012 is a reasonable start

    # Create and save line chart for long-term trends
    plt.figure(figsize=(12, 7))
    sns.lineplot(x=yearly_reviews.index, y=yearly_reviews.values, marker='o', color='royalblue')
    plt.title('Long-Term Trend of Airbnb Activity (by Review Count)', fontsize=16)
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(yearly_reviews.index.astype(int))  # Ensure integer years on x-axis
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '10_long_term_trends_by_year.png'))
    plt.close()
    print("Saved '10_long_term_trends_by_year.png'")

    # --- Task 3: Stay Duration Analysis ---
    print("\n[Task 3/3] Analyzing stay duration via 'minimum_nights'...")

    # For a clearer histogram, filter to a reasonable range (e.g., up to 30 nights)
    df_filtered_nights = df[df['minimum_nights'] <= 30]

    # Create and save histogram for minimum nights
    plt.figure(figsize=(12, 7))
    sns.histplot(df_filtered_nights['minimum_nights'], bins=30, kde=False, color='darkorange')
    plt.title('Distribution of Minimum Nights Required (1-30 Nights)', fontsize=16)
    plt.xlabel('Minimum Nights', fontsize=12)
    plt.ylabel('Number of Listings', fontsize=12)
    plt.xticks(range(1, 31, 2))
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '11_minimum_nights_distribution.png'))
    plt.close()
    print("Saved '11_minimum_nights_distribution.png'")

    # **NEW PLOT ADDED**
    # Create and save box plot to compare minimum nights by room type
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='room_type', y='minimum_nights', data=df_filtered_nights, palette='coolwarm')
    plt.title('Minimum Nights Distribution by Room Type', fontsize=16)
    plt.xlabel('Room Type', fontsize=12)
    plt.ylabel('Minimum Nights Required', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '12_min_nights_by_room_type.png'))
    plt.close()
    print("Saved '12_min_nights_by_room_type.png'")

    print("\n--- Day 5 Analysis Complete ---")


if __name__ == '__main__':
    day_5_temporal_analysis()

