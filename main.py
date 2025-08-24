import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
regions = ['North', 'South', 'East', 'West']
num_months = 12
data = {
    'Region': np.random.choice(regions, size=num_months*len(regions), replace=True),
    'Month': np.tile(pd.date_range(start='2023-01-01', periods=num_months, freq='MS'), len(regions)),
    'Sales': np.random.randint(500, 2000, size=num_months*len(regions)) + np.random.normal(0, 200, size=num_months*len(regions))
}
df = pd.DataFrame(data)
#add some noise to simulate real-world data
df['Sales'] = df['Sales'] + np.random.normal(0,100,len(df))
df['Sales'] = df['Sales'].apply(lambda x: max(0,x)) #ensure no negative sales
# --- 2. Data Cleaning and Analysis ---
# Ensure data types are correct
df['Month'] = pd.to_datetime(df['Month'])
# Group data by region and month to calculate monthly sales
monthly_regional_sales = df.groupby(['Region', 'Month'])['Sales'].sum().reset_index()
# Calculate yearly sales for each region
yearly_regional_sales = monthly_regional_sales.groupby('Region')['Sales'].sum()
# Identify high-potential and underperforming regions (example logic)
avg_sales = yearly_regional_sales.mean()
high_potential = yearly_regional_sales[yearly_regional_sales > avg_sales * 1.2]
underperforming = yearly_regional_sales[yearly_regional_sales < avg_sales * 0.8]
# --- 3. Visualization ---
#Plot 1: Monthly Sales by Region
plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_regional_sales, x='Month', y='Sales', hue='Region')
plt.title('Monthly Sales Trend by Region')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_sales_by_region.png')
print("Plot saved to monthly_sales_by_region.png")
#Plot 2: Yearly Sales by Region (Bar Chart)
plt.figure(figsize=(8,6))
sns.barplot(x=yearly_regional_sales.index, y=yearly_regional_sales.values)
plt.title('Yearly Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Yearly Sales')
plt.tight_layout()
plt.savefig('yearly_sales_by_region.png')
print("Plot saved to yearly_sales_by_region.png")
# --- 4. Reporting (Optional) ---
print("\nYearly Sales Summary:")
print(yearly_regional_sales)
print("\nHigh-Potential Regions:")
print(high_potential)
print("\nUnderperforming Regions:")
print(underperforming)