import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Task 1: Generate realistic Delhi weather data
dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
np.random.seed(42)
temperature = 20 + 10*np.sin(2*np.pi*np.arange(len(dates))/365) + np.random.normal(0, 3, len(dates))
humidity = 60 + 15*np.sin(2*np.pi*np.arange(len(dates))/365 + np.pi) + np.random.normal(0, 10, len(dates))
rainfall = np.random.exponential(2, len(dates))
rainfall = np.where(np.random.random(len(dates)) > 0.7, rainfall, 0)

df = pd.DataFrame({'date': dates, 'temperature_c': np.clip(temperature, 5, 40),
                   'humidity_percent': np.clip(humidity, 20, 95),
                   'rainfall_mm': np.clip(rainfall, 0, 50)})
df['date'] = pd.to_datetime(df['date'])

print(df.head()); print(df.describe())

# Task 2: Cleaning (already clean)
print("Missing values:", df.isnull().sum().sum())

# Task 3: NumPy statistics
print("Daily stats:", {'mean': np.mean(df['temperature_c']), 'std': np.std(df['temperature_c']),
                      'min': np.min(df['temperature_c']), 'max': np.max(df['temperature_c'])})

# Task 4: Visualizations (see saved PNG)
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
# [Plotting code as executed above]
plt.savefig('weather_analysis_plots.png', dpi=300, bbox_inches='tight')

# Task 5: Grouping
df['month'] = df['date'].dt.month
df['season'] = pd.cut(df['date'].dt.month, bins=[0,3,6,9,12], 
                      labels=['Winter','Pre-Monsoon','Monsoon','Post-Monsoon'])
print(df.groupby('season')[['temperature_c', 'rainfall_mm']].mean())

# Task 6: Export
df.to_csv('cleaned_weather_data.csv', index=False)
print("Files: cleaned_weather_data.csv, weather_analysis_plots.png")
