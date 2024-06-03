from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import meteostat
import pandas as pd
from meteostat import Point, Hourly, Daily
now = datetime.now()

year = now.year

month = now.month
day = now.day
print(year, month, day)
# Set time period
try:
    start = datetime(year, month, day+1)
    end = datetime(year, month, day+1, 23, 59, 59)
except ValueError:
    start = datetime(year, month+1, 1)
    end = datetime(year, month+1, 1, 23, 59, 59)

#end = datetime(2024, 5, day+1)

# Create Point for Vancouver, BC
senimanmiekari = Point(-0.030952207938211476, 109.33624505209471, 70)

# Get daily data for 2018
data = Hourly(senimanmiekari, start, end)
data = data.fetch()

avg_temp = data['temp'].mean()
max_temp = data['temp'].max()
min_temp = data['temp'].min()
prcp = data['prcp'].sum()
summary = pd.DataFrame({
    'tavg': [avg_temp],
    'tmin': [min_temp],
    'tmax': [max_temp],
    'prcp': [prcp]
})
print(summary)
#extract = data.iloc[:, []]

# Plot line chart including average, minimum and maximum temperature
