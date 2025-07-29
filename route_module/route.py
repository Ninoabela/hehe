# route_module/views.py
from flask import render_template, request, jsonify
from . import route_bp
import requests

@route_bp.route('/map')
def index():
    return render_template('route_module/routing_dash.html')

@route_bp.route('/route', methods=['POST'])
def get_route():
    try:
        data = request.get_json()
        start = data['start']
        end = data['end']

        if not start or not end:
            return jsonify({'error': 'Missing coordinates'}), 400

        coords = f"{start[1]},{start[0]};{end[1]},{end[0]}"
        url = f"http://router.project-osrm.org/route/v1/driving/{coords}?overview=full&geometries=geojson"

        res = requests.get(url)
        res.raise_for_status()
        route_data = res.json()

        if 'routes' not in route_data or not route_data['routes']:
            return jsonify({'error': 'No route found'}), 404

        geometry = route_data['routes'][0]['geometry']['coordinates']
        distance_km = round(route_data['routes'][0]['distance'] / 1000, 2)

        # Convert [lon, lat] to [lat, lon] for Leaflet
        route_coords = [[lat, lon] for lon, lat in geometry]

        return jsonify({'route': route_coords, 'distance_km': distance_km})

    except Exception as e:
        return jsonify({'error': str(e)}), 500
