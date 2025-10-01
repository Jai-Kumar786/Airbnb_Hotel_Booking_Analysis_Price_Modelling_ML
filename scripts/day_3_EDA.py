import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def run_eda():
    """
    Main function to run the Exploratory Data Analysis for Day 3.
    """
    print("--- Starting Day 3: Initial Exploratory Data Analysis ---")

    # Define file paths
    cleaned_data_path = r'C:\Users\jaiku\PycharmProjects\Airbnb_Analysis\data\processed\cleaned_airbnb_data.csv'
    output_dir = '../reports/figures'

    # --- Load Data ---
    try:
        df = pd.read_csv(cleaned_data_path)
        print(f"Successfully loaded cleaned data from '{cleaned_data_path}'.")
    except FileNotFoundError:
        print(f"Error: The cleaned data file was not found at '{cleaned_data_path}'.")
        print("Please ensure the Day 2 data cleaning script has been run successfully.")
        return

    # --- Create output directory ---
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created directory for saving plots: '{output_dir}'")

    # --- Set plot style ---
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12

    # --- [Plot 1] Geographic Distribution of Listings ---
    print("\n[Step 1/4] Generating Geographic Distribution Plot...")
    plt.figure()
    ax = sns.countplot(y=df['neighbourhood_group'], order=df['neighbourhood_group'].value_counts().index,
                       palette='viridis')
    ax.set_title('Geographic Distribution of Airbnb Listings by Borough', fontsize=16, fontweight='bold')
    ax.set_xlabel('Number of Listings', fontsize=12)
    ax.set_ylabel('Borough (Neighbourhood Group)', fontsize=12)

    # Add data labels
    for container in ax.containers:
        ax.bar_label(container, fmt='{:,.0f}')

    plot1_path = os.path.join(output_dir, '1_geographic_distribution.png')
    plt.tight_layout()
    plt.savefig(plot1_path)
    plt.close()
    print(f"Saved plot to '{plot1_path}'")

    # --- [Plot 2] Property Type Market Share ---
    print("\n[Step 2/4] Generating Property Type Market Share Plot...")
    plt.figure()
    room_type_counts = df['room_type'].value_counts()
    colors = sns.color_palette('viridis', len(room_type_counts))
    plt.pie(room_type_counts, labels=room_type_counts.index, autopct='%1.1f%%', startangle=140, colors=colors,
            wedgeprops=dict(width=0.4))  # This creates the donut effect

    # Draw a circle at the center to make it a donut chart
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.title('Market Share of Property Types in NYC', fontsize=16, fontweight='bold')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plot2_path = os.path.join(output_dir, '2_property_type_share.png')
    plt.tight_layout()
    plt.savefig(plot2_path)
    plt.close()
    print(f"Saved plot to '{plot2_path}'")

    # --- [Plot 3] Price Distribution Analysis ---
    print("\n[Step 3/4] Generating Price Distribution Plots...")
    # Plotting the full distribution
    plt.figure()
    sns.histplot(df['price'], bins=50, kde=True, color='purple')
    plt.title('Distribution of All Airbnb Listing Prices', fontsize=16, fontweight='bold')
    plt.xlabel('Price (in $)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plot3a_path = os.path.join(output_dir, '3a_price_distribution_full.png')
    plt.tight_layout()
    plt.savefig(plot3a_path)
    plt.close()
    print(f"Saved full price distribution plot to '{plot3a_path}'")

    # Plotting a filtered distribution for better visibility of the "typical" market
    plt.figure()
    price_cap = df['price'].quantile(0.95)  # Cap at the 95th percentile to remove extreme outliers
    sns.histplot(df[df['price'] < price_cap]['price'], bins=50, kde=True, color='purple')
    plt.title(f'Distribution of Listing Prices (Capped at 95th Percentile: ${price_cap:,.2f})', fontsize=16,
              fontweight='bold')
    plt.xlabel('Price (in $)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plot3b_path = os.path.join(output_dir, '3b_price_distribution_filtered.png')
    plt.tight_layout()
    plt.savefig(plot3b_path)
    plt.close()
    print(f"Saved filtered price distribution plot to '{plot3b_path}'")

    # --- [Plot 4] Geospatial Visualization of Listings ---
    print("\n[Step 4/4] Generating Geospatial Scatter Plot...")
    plt.figure(figsize=(14, 10))
    sns.scatterplot(data=df, x='long', y='lat', hue='neighbourhood_group', palette='viridis', s=10, alpha=0.5)
    plt.title('Geospatial Distribution of NYC Airbnb Listings', fontsize=16, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.legend(title='Borough', markerscale=2)
    plot4_path = os.path.join(output_dir, '4_geospatial_distribution.png')
    plt.tight_layout()
    plt.savefig(plot4_path)
    plt.close()
    print(f"Saved plot to '{plot4_path}'")

    print("\n--- Exploratory Data Analysis Complete ---")
    print(f"All plots have been saved in the '{output_dir}' directory.")


if __name__ == '__main__':
    run_eda()
