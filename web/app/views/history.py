from flask import Blueprint, render_template, request
from app.manager.db_manager import mariadb_user_manager
from datetime import datetime, timezone

history_bp = Blueprint('history', __name__)

content = {'name':'', 'day':''}

@history_bp.route('/history')
def history():
    name = request.cookies.get("user_name")
    user_key = request.cookies.get("user_key")

    content['name'] = name
    sql_query = "SELECT create_at FROM userinfo WHERE user_key = %s"
    params = (user_key,)
    create_at = mariadb_user_manager.put_sql_result(sql_query, params)
    user_date = create_at[0].get('create_at')
    now_date =  datetime.now(tz=timezone.utc)
    day = (now_date.year - user_date.year)*365 + (now_date.day - user_date.day)
    content['day'] = day

    return render_template('history.html',**content)