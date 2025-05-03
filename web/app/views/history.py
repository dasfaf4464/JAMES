from flask import Blueprint, render_template

history_bp = Blueprint('history', __name__)

content = {}

@history_bp.route('/history')
def history():
    return render_template('history.html',**content)