let map = L.map('map').setView([13.41, 122.56], 6); // Default to Philippines

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
}).addTo(map);

let startMarker = null;
let endMarker = null;
let routeLine = null;
let pinDropCount = 0;

// Colored pin icons
const greenIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

const orangeIcon = new L.Icon({
  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});

document.getElementById('dropPins').addEventListener('click', () => {
  pinDropCount = 0;
  alert('Pin Drop Mode Activated:\nFirst Click = Pickup\nSecond Click = Delivery');
});

map.on('click', (e) => {
  if (pinDropCount === 0) {
    if (startMarker) map.removeLayer(startMarker);
    startMarker = L.marker(e.latlng, { icon: greenIcon }).addTo(map).bindPopup("Pickup").openPopup();
    document.getElementById('start').value = `${e.latlng.lat},${e.latlng.lng}`;
    pinDropCount++;
  } else if (pinDropCount === 1) {
    if (endMarker) map.removeLayer(endMarker);
    endMarker = L.marker(e.latlng, { icon: orangeIcon }).addTo(map).bindPopup("Delivery").openPopup();
    document.getElementById('end').value = `${e.latlng.lat},${e.latlng.lng}`;
    pinDropCount = 0;
  }
});

document.getElementById('getRoute').addEventListener('click', () => {
  const startStr = document.getElementById('start').value.trim();
  const endStr = document.getElementById('end').value.trim();

  if (!startStr || !endStr) {
    alert('Please enter both start and end coordinates.');
    return;
  }

  const start = startStr.split(',').map(Number);
  const end = endStr.split(',').map(Number);

  if (start.length !== 2 || end.length !== 2 || start.includes(NaN) || end.includes(NaN)) {
    alert('Coordinates must be in format: lat,lon');
    return;
  }

  fetch('/route/route', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start, end })
  })
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert('Error: ' + data.error);
        return;
      }

      // Remove old route and markers
      if (routeLine) map.removeLayer(routeLine);
      if (startMarker) map.removeLayer(startMarker);
      if (endMarker) map.removeLayer(endMarker);

      // Draw route
      routeLine = L.polyline(data.route, { color: 'blue', weight: 5 }).addTo(map);
      map.fitBounds(routeLine.getBounds());

      // Place new markers
      const [startLat, startLng] = start;
      const [endLat, endLng] = end;
      startMarker = L.marker([startLat, startLng], { icon: greenIcon }).addTo(map).bindPopup("Pickup");
      endMarker = L.marker([endLat, endLng], { icon: orangeIcon }).addTo(map).bindPopup("Delivery");

      // Show distance
      document.getElementById('distance').textContent = `Distance: ${data.distance_km} km`;
    })
    .catch(err => {
      console.error(err);
      alert('There was a problem finding the route.');
      document.getElementById('distance').textContent = '';
    });
});

// Dropdown toggle
function toggleDropdown(id) {
  const dropdown = document.getElementById(id);
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';

  // Close other dropdowns
  document.querySelectorAll('.custom-dropdown').forEach(el => {
    if (el.id !== id) el.style.display = 'none';
  });
}

function selectCoord(inputId, coord) {
  document.getElementById(inputId).value = coord;
  document.getElementById(inputId + 'Dropdown').style.display = 'none';
}

// Close dropdowns on outside click
document.addEventListener('click', function (e) {
  if (!e.target.closest('.input-group')) {
    document.querySelectorAll('.custom-dropdown').forEach(el => {
      el.style.display = 'none';
    });
  }
});
