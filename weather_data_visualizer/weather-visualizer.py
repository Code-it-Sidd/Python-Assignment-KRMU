import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Task 1: Generate realistic Delhi weather data (2023)
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
np.random.seed(42)

temperature = 20 + 10 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 3, len(dates))
humidity = 60 + 15 * np.sin(2 * np.pi * np.arange(len(dates)) / 365 + np.pi) + np.random.normal(0, 10, len(dates))
rainfall = np.random.exponential(2, len(dates))
rainfall = np.where(np.random.random(len(dates)) > 0.7, rainfall, 0)  # ~30% rainy days

df = pd.DataFrame({
    'date': dates,
    'temperature_c': np.clip(temperature, 5, 40),
    'humidity_percent': np.clip(humidity, 20, 95),
    'rainfall_mm': np.clip(rainfall, 0, 50)
})
df['date'] = pd.to_datetime(df['date'])

print("Task 1: Data loaded and inspected")
print(df.head())
print(df.info())
print(df.describe())

# Task 2: Data Cleaning
print("\nMissing values:", df.isnull().sum().sum())
df = df[['date', 'temperature_c', 'humidity_percent', 'rainfall_mm']]  # Keep relevant columns

# Task 3: Statistical Analysis with NumPy
print("\nTask 3: Daily statistics")
daily_stats = {
    'mean_temp': np.mean(df['temperature_c']),
    'min_temp': np.min(df['temperature_c']),
    'max_temp': np.max(df['temperature_c']),
    'std_temp': np.std(df['temperature_c'])
}
print(daily_stats)

# Monthly rainfall stats
monthly_rain = df.groupby(df['date'].dt.month)['rainfall_mm'].agg(['mean', 'sum', 'min', 'max', 'std'])
print("\nMonthly rainfall statistics:")
print(monthly_rain)

# Task 4: Visualization (Fixed)
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Weather Data Analysis (Delhi, 2023)', fontsize=16)

# 1. Line chart: Daily temperature trends
axes[0, 0].plot(df['date'], df['temperature_c'], linewidth=1.2, alpha=0.8)
axes[0, 0].set_title('Daily Temperature Trends')
axes[0, 0].set_ylabel('Temperature (°C)')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].tick_params(axis='x', rotation=45)

# 2. Bar chart: Monthly rainfall totals
monthly_rain_total = df.groupby(df['date'].dt.month)['rainfall_mm'].sum()
axes[0, 1].bar(monthly_rain_total.index, monthly_rain_total.values, alpha=0.8)
axes[0, 1].set_title('Monthly Rainfall Totals')
axes[0, 1].set_xlabel('Month')
axes[0, 1].set_ylabel('Rainfall (mm)')
axes[0, 1].grid(True, alpha=0.3)

# 3. Scatter plot: Humidity vs Temperature
axes[1, 0].scatter(df['temperature_c'], df['humidity_percent'], alpha=0.6, s=20,)
axes[1, 0].set_xlabel('Temperature (°C)')
axes[1, 0].set_ylabel('Humidity (%)')
axes[1, 0].set_title('Humidity vs Temperature')
axes[1, 0].grid(True, alpha=0.3)

# 4. Combined plot: Temperature & Rainfall trends
ax1 = axes[1, 1]
ax1.plot(df['date'], df['temperature_c'], alpha=0.8, label='Temperature (°C)')
ax1.set_ylabel('Temperature (°C)', color='tab:red')
ax1.tick_params(axis='y', labelcolor='tab:red')
ax1.set_title('Temperature & Rainfall Trends')
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.bar(df['date'], df['rainfall_mm'], alpha=0.3, label='Rainfall (mm)')
ax2.set_ylabel('Rainfall (mm)', color='tab:blue')
ax2.tick_params(axis='y', labelcolor='tab:blue')

# Adjust layout and save
plt.tight_layout()
plt.savefig('weather_analysis_plots_fixed.png', dpi=300, bbox_inches='tight')
print("\nPlots saved as 'weather_analysis_plots_fixed.png'")

# Task 5: Grouping and Aggregation
df['month'] = df['date'].dt.month
df['season'] = pd.cut(df['date'].dt.month, bins=[0, 3, 6, 9, 12], labels=['Winter', 'Pre-Monsoon', 'Monsoon', 'Post-Monsoon'])

seasonal_stats = df.groupby('season')[['temperature_c', 'rainfall_mm', 'humidity_percent']].agg(['mean', 'std'])
print("\nTask 5: Seasonal statistics")
print(seasonal_stats)

monthly_stats = df.groupby('month')[['temperature_c', 'rainfall_mm']].agg(['mean', 'sum'])
print("\nMonthly aggregated stats:")
print(monthly_stats)

# Resample to weekly
weekly_temp = df.resample('W', on='date')['temperature_c'].agg(['mean', 'max', 'min'])
print("\nWeekly temperature (first 5):")
print(weekly_temp.head())

# Task 6: Export cleaned data
df.to_csv('cleaned_weather_data.csv', index=False)
print("\nCleaned data exported to 'cleaned_weather_data.csv'")
print("\n=== ANALYSIS COMPLETE ===")
print("Files created: cleaned_weather_data.csv, weather_analysis_plots_fixed.png")

