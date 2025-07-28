# Lamina Route Finder

This is a lightweight Flask web application that calculates driving routes using the public [OSRM (Open Source Routing Machine)](http://project-osrm.org/) API. It takes two coordinates (start and end) and returns the optimized driving path, which can be displayed on a Leaflet map or similar frontend.

## Features

- Accepts coordinates for start and end points
- Calls the OSRM API for driving directions
- Returns route geometry and distance in kilometers
- Designed to integrate with a Leaflet.js frontend

## Requirements

- Python 3.7+
- Pip

## Installation

1. Copy the files into a local directory

2. Install the dependencies:

pip install -r requirements.txt

3. Run the App:

python app.py

4. Open your browser and go to:

http://127.0.0.1:5000/
