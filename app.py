from flask import Flask, render_template, redirect, url_for
from route_module.route import route_bp
from damage_detection import damage_bp
from driving_behavior import behavior_bp
from delivery_time_predictor.eta_module import eta_bp   # Adjust this path if eta_module.py is in the same directory, or use the correct relative path


app = Flask(__name__)



# Register Blueprints
app.register_blueprint(route_bp, url_prefix='/route')
app.register_blueprint(damage_bp, url_prefix='/damage')
app.register_blueprint(behavior_bp, url_prefix='/behavior')
app.register_blueprint(eta_bp, url_prefix='/eta')


# Main Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/damage")
def damage():
    return "Damage Detection Module"

@app.route("/route")
def route():
    return "Route Optimizer Module"

# @app.route("/behavior")
# def behavior():
#    return "Driving Behavior Dashboard"

@app.route("/eta")
def eta():
    return "Delivery Time Predictor"

if __name__ == '__main__':
    app.run(debug=True)