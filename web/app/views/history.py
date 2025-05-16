from flask import Blueprint, render_template, request

history_bp = Blueprint('history', __name__)

content = {'name':''}

@history_bp.route('/history')
def history():
    name = request.cookies.get("user_name")
    content['name'] = name
    return render_template('history.html',**content)