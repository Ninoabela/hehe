import pandas as pd
import plotly.express as px
from datetime import datetime

df = pd.read_csv("driving_behavior/data/driving_data.csv", parse_dates=["timestamp"])

def classify_risk(score):
    if score >= 80:
        return "Low"
    elif score >= 60:
        return "Medium"
    return "High"

def get_recommendation(score):
    if score >= 80:
        return "Maintain"
    elif score >= 60:
        return "Retraining"
    return "Disciplinary review"

def get_driver_dashboard(driver_id, start_date=None, end_date=None):
    filtered = df[df['driver_id'] == driver_id]

    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        filtered = filtered[(filtered['timestamp'] >= start) & (filtered['timestamp'] <= end)]

    avg_score = round(filtered['score'].mean(), 2)
    risk_level = classify_risk(avg_score)
    
    metrics = {
        'avg_score': avg_score,
        'risk_level': risk_level,
        'sudden_brake_total': int(filtered['sudden_brake'].sum()),
        'overspeed_total': int(filtered['overspeed'].sum()),
        'idle_minutes': int(filtered['idle'].sum()),
        'fatigue_flags': int(filtered['fatigue_detected'].sum()),
        'driver_id': driver_id,
        'start_date': start_date,
        'end_date': end_date,
        'recommendation': get_recommendation(avg_score),
        'drivers': df['driver_id'].unique()
    }

    # common layout
    base_layout = dict(
        template='plotly_dark',
        paper_bgcolor="#000000",
        plot_bgcolor="#000000",
        font=dict(color='white'),
        xaxis=dict(color='white', gridcolor='#444'),
        yaxis=dict(color='white', gridcolor='#444'),
        title_font=dict(size=16),
        margin=dict(t=40, b=40, l=20, r=20)
    )

    # speed over time
    speed_fig = px.line(filtered, x='timestamp', y='speed', title='Speed Trend', markers=True)
    speed_fig.update_layout(**base_layout)
    metrics['speed_plot'] = speed_fig.to_html(full_html=False)

    # acceleration plot with binary color
    filtered['sudden_brake_label'] = filtered['sudden_brake'].map({0: 'Normal', 1: 'Sudden Brake'})
    accel_fig = px.scatter(
        filtered, x='timestamp', y='acceleration',
        color='sudden_brake_label',
        title="Acceleration Pattern",
        color_discrete_map={'Normal': 'skyblue', 'Sudden Brake': 'red'}
    )
    accel_fig.update_layout(**base_layout)
    metrics['accel_plot'] = accel_fig.to_html(full_html=False)

    # brake force
    brake_fig = px.scatter(filtered, x='timestamp', y='brake_force', color='brake_force',
                           title="Brake Force Intensity", color_continuous_scale='blues')
    brake_fig.update_layout(**base_layout)
    metrics['brake_plot'] = brake_fig.to_html(full_html=False)

    # fatigue
    fatigue_fig = px.scatter(filtered, x='timestamp', y='fatigue_detected', title="Fatigue Events",
                             color='fatigue_detected', color_continuous_scale='reds')
    fatigue_fig.update_layout(**base_layout)
    metrics['fatigue_plot'] = fatigue_fig.to_html(full_html=False)

    # table
    metrics['table'] = filtered.to_html(classes='custom-dark-table', index=False, border=0)
    metrics['scorecard'] = get_top_driver_scorecards(start_date, end_date, top_n=5)
    return metrics

def get_top_driver_scorecards(start_date=None, end_date=None, top_n=3):
    driver_ids = df['driver_id'].unique()
    scorecards = []

    for driver_id in driver_ids:
        filtered = df[df['driver_id'] == driver_id]

        if start_date and end_date:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            filtered = filtered[(filtered['timestamp'] >= start) & (filtered['timestamp'] <= end)]

        avg_score = round(filtered['score'].mean(), 2)
        risk_level = classify_risk(avg_score)
        recommendation = get_recommendation(avg_score)

        scorecards.append({
            'driver_id': driver_id,
            'avg_score': avg_score,
            'risk_level': risk_level,
            'recommendation': recommendation
        })

    scorecards = sorted(scorecards, key=lambda x: x['driver_id'])[:top_n]
    return scorecards
