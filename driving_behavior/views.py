from flask import Blueprint, render_template, request
from driving_behavior.behavior_dashboard import get_driver_dashboard

behavior_bp = Blueprint(
    'behavior_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@behavior_bp.route('/', methods=['GET', 'POST'])
def behavior_dashboard():
    if request.method == 'POST':
        driver_id = request.form.get('driver_id', default='D001')
        start_date = request.form.get('start_date', default=None)
        end_date = request.form.get('end_date', default=None)
    else:
        driver_id = request.args.get('driver_id', default='D001')
        start_date = request.args.get('start_date', default=None)
        end_date = request.args.get('end_date', default=None)

    dashboard_data = get_driver_dashboard(driver_id, start_date, end_date)
    return render_template("behavior_dashboard.html", **dashboard_data)
