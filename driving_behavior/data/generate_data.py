import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

drivers = ['D001', 'D002', 'D003']
records = []

start_date = datetime(2025, 6, 1)
end_date = datetime(2025, 7, 29)

# simulate data every 10 minutes from 08:00 to 18:00 (60 records/day)
time_intervals = [timedelta(minutes=10) * i for i in range(60)]

for driver in drivers:
    for day in pd.date_range(start=start_date, end=end_date):
        idle_counter = 0

        for t in time_intervals:
            timestamp = datetime.combine(day, datetime.min.time()) + timedelta(hours=8) + t

            if driver == 'D001':
                speed = np.random.choice([0]*2 + list(range(30, 85)))  
                accel = round(np.random.uniform(-2.5, 2.5), 2)         
                brake = round(np.random.uniform(0, 1.2), 2)         
                deviation = np.random.uniform(1, 6)                  
                fatigue_chance = 0.02                             
                on_time = random.choices([1, 0], weights=[85, 15])[0]
            elif driver == 'D002': 
                speed = np.random.choice([0]*4 + list(range(60, 120)))
                accel = round(np.random.uniform(-4, 4), 2)
                brake = round(np.random.uniform(0.6, 1.8), 2)
                deviation = np.random.uniform(6, 15)
                fatigue_chance = 0.15
                on_time = random.choices([1, 0], weights=[50, 50])[0]
            else: 
                speed = np.random.choice([0]*6 + list(range(90, 140)))
                accel = round(np.random.uniform(-6, 6), 2)
                brake = round(np.random.uniform(1.2, 2.5), 2)
                deviation = np.random.uniform(15, 25)
                fatigue_chance = 0.4
                on_time = random.choices([1, 0], weights=[20, 80])[0]

            gps_lat = round(random.uniform(14.5, 14.7), 6)
            gps_long = round(random.uniform(120.9, 121.1), 6)
            overspeed = 1 if speed > 100 else 0
            sudden_brake = 1 if brake > 1.0 else 0
            sharp_turn = 1 if abs(accel) > 2.5 else 0

            idle = 1 if speed == 0 else 0
            idle_counter = idle_counter + 1 if idle else 0
            long_idle = 1 if idle_counter >= 3 else 0
            fatigue = 1 if long_idle or random.random() < fatigue_chance else 0

            records.append([
                driver, timestamp, speed, accel, brake, gps_lat, gps_long,
                overspeed, sudden_brake, sharp_turn, deviation, on_time,
                idle, fatigue
            ])

df = pd.DataFrame(records, columns=[
    'driver_id', 'timestamp', 'speed', 'acceleration', 'brake_force',
    'gps_lat', 'gps_long', 'overspeed', 'sudden_brake', 'sharp_turn',
    'deviation_from_route', 'on_time_delivery', 'idle', 'fatigue_detected'
])

def calculate_score(row):
    score = 100

    if row['driver_id'] == 'D001':
        score -= row['overspeed'] * 5
        score -= row['sudden_brake'] * 3.5
        score -= row['sharp_turn'] * 2.5
        score -= row['deviation_from_route'] * 0.9
        score -= row['idle'] * 0.6
        score -= row['fatigue_detected'] * 4
        score += row['on_time_delivery'] * 0.5   
    elif row['driver_id'] == 'D002':
        score -= row['overspeed'] * 5
        score -= row['sudden_brake'] * 6
        score -= row['sharp_turn'] * 5
        score -= row['deviation_from_route'] * 1.2
        score -= row['idle'] * 1
        score -= row['fatigue_detected'] * 7
        score += row['on_time_delivery'] * 0.2
    else:
        score -= row['overspeed'] * 5
        score -= row['sudden_brake'] * 6
        score -= row['sharp_turn'] * 5
        score -= row['deviation_from_route'] * 1.5 
        score -= row['idle'] * 1.2                  
        score -= row['fatigue_detected'] * 8
        score += row['on_time_delivery'] * 0.2 

    return max(0, min(100, score))

df['score'] = df.apply(calculate_score, axis=1)

# save to csv
df.to_csv('driving_data.csv', index=False)
