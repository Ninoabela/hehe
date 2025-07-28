from flask import Flask, render_template
from route_module.views import route_bp

app = Flask(__name__)
app.register_blueprint(route_bp, url_prefix='/route')

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/damage")
def damage():
    return "Damage Detection Module"

@app.route("/behavior")
def behavior():
    return "Driving Behavior Dashboard"

@app.route("/eta")
def eta():
    return "Delivery Time Predictor"

if __name__ == "__main__":
    app.run(debug=True)
