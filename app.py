from flask import Flask, render_template
from damage_detection import damage_bp

app = Flask(__name__)
app.register_blueprint(damage_bp, url_prefix='/damage')  # Register your blueprint

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/route')
def route():
    return "Route Optimizer Module"

@app.route('/behavior')
def behavior():
    return "Driving Behavior Dashboard"

@app.route('/eta')
def eta():
    return "Delivery Time Predictor"

if __name__ == '__main__':
    app.run(debug=True)
