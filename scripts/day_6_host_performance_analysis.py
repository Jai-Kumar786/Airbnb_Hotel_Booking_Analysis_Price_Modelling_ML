import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import os


def day_6_host_analysis():
    """
    Analyzes host performance, identifies top hosts, and uses a t-test
    to determine the statistical significance of host verification.
    """
    print("--- Starting Day 6: Host Performance & Verification Impact ---")

    # Define file paths
    cleaned_data_path = '../data/processed/cleaned_airbnb_data.csv'
    figures_dir = '../reports/figures/'

    # --- Load Data ---
    if not os.path.exists(cleaned_data_path):
        print(f"Error: Cleaned data file not found at '{cleaned_data_path}'")
        return

    try:
        df = pd.read_csv(cleaned_data_path)
        print(f"Successfully loaded cleaned data. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- Task 1: Identify Top Hosts ---
    print("\n[Task 1/3] Identifying Top 10 Hosts by Listing Count...")
    top_10_hosts = df['host_name'].value_counts().head(10)
    print("Top 10 Hosts:")
    print(top_10_hosts)
    print("-" * 50)

    # --- Task 2: Analyze "Power Host" Characteristics ---
    print("\n[Task 2/3] Analyzing 'Power Host' Characteristics...")

    # Create a DataFrame for top hosts' listings
    top_hosts_df = df[df['host_name'].isin(top_10_hosts.index)]

    # Compare descriptive statistics
    print("Comparing Average Stats: Power Hosts vs. General Population")

    # Define columns for comparison
    comparison_cols = ['price', 'service_fee', 'number_of_reviews', 'review_rate_number', 'availability_365']

    # Calculate stats
    power_host_stats = top_hosts_df[comparison_cols].mean().to_frame(name='Power Hosts')
    general_stats = df[comparison_cols].mean().to_frame(name='General Population')

    # Combine and print comparison table
    comparison_df = pd.concat([power_host_stats, general_stats], axis=1)
    print(comparison_df.round(2))
    print("-" * 50)

    # Analyze geographic and room type distribution for top hosts
    print("\nPower Host Portfolio Distribution:")
    print("\nBorough Distribution:")
    print(top_hosts_df['neighbourhood_group'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

    print("\nRoom Type Distribution:")
    print(top_hosts_df['room_type'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')
    print("-" * 50)

    # --- Task 3: Statistical Test for Verification Impact ---
    print("\n[Task 3/3] Statistical Test for Host Verification Impact...")

    # Hypothesis Formulation
    print("Hypothesis Test: Does verification impact the number of reviews?")
    print(
        "H₀ (Null Hypothesis): There is NO significant difference in the mean number of reviews between verified and unverified hosts.")
    print(
        "H₁ (Alternative Hypothesis): There IS a significant difference in the mean number of reviews between verified and unverified hosts.")
    print("-" * 50)

    # Visualization: Box plot
    print("Generating box plot for visual comparison...")
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='host_identity_verified', y='number_of_reviews', data=df, palette='viridis')
    plt.title('Number of Reviews: Verified vs. Unverified Hosts', fontsize=16)
    plt.xlabel('Host Identity Verified', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    # Set a y-limit to zoom in on the distribution, as outliers can skew the view
    plt.ylim(0, df['number_of_reviews'].quantile(0.95))
    plt.tight_layout()
    plt.savefig(os.path.join(figures_dir, '13_reviews_by_verification.png'))
    plt.close()
    print("Saved '13_reviews_by_verification.png'")

    # T-test Validation
    print("\nPerforming Independent Two-Sample T-test...")

    # Create two groups for the test
    verified_reviews = df[df['host_identity_verified'] == 'verified']['number_of_reviews']
    unverified_reviews = df[df['host_identity_verified'] == 'unconfirmed']['number_of_reviews']

    # Perform the t-test, ignoring NaNs
    t_statistic, p_value = stats.ttest_ind(verified_reviews, unverified_reviews, nan_policy='omit')

    print(f"T-statistic: {t_statistic:.4f}")
    print(f"P-value: {p_value:.4f}")

    # Interpretation of the P-value
    alpha = 0.05
    print(f"\nSignificance level (alpha): {alpha}")
    if p_value < alpha:
        print("Result: The p-value is less than alpha. We REJECT the null hypothesis.")
        print(
            "Conclusion: There is a statistically significant difference in the number of reviews between verified and unverified hosts.")
    else:
        print("Result: The p-value is greater than alpha. We FAIL TO REJECT the null hypothesis.")
        print(
            "Conclusion: There is no statistically significant difference in the number of reviews between verified and unverified hosts.")

    print("\n--- Day 6 Analysis Complete ---")


if __name__ == '__main__':
    day_6_host_analysis()
